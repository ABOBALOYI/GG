"""
Property-based tests for the Status Manager.

**Validates: Requirements 7.1, 7.2, 7.4**
"""
import pytest
from datetime import date, timedelta
from hypothesis import given, strategies as st, settings, HealthCheck

from scraper.status import StatusManager
from scraper.models import (
    NormalisedOpportunity, RecordType, FundingType, FunderType,
    BusinessStage, OpportunityStatus
)


def create_record(**overrides) -> NormalisedOpportunity:
    """Create a normalised record with optional overrides."""
    defaults = {
        'record_type': RecordType.FUNDING_OPPORTUNITY,
        'title': 'Test Funding Opportunity',
        'funder_name': 'Test Funder',
        'funder_type': FunderType.GOV,
        'funding_type': FundingType.GRANT,
        'description_short': 'A test funding opportunity.',
        'industry_tags': ['ICT'],
        'province_tags': ['Gauteng'],
        'business_stage': BusinessStage.SME,
        'eligibility_bullets': [],
        'funding_amount_min': None,
        'funding_amount_max': None,
        'deadline_date': None,
        'is_rolling': True,
        'required_documents_bullets': [],
        'application_steps': [],
        'official_apply_url': 'https://example.gov.za/apply',
        'source_url': 'https://example.gov.za/funding',
        'source_name': 'Test Source',
        'last_verified_date': date.today(),
        'status': OpportunityStatus.ACTIVE,
        'raw_content_hash': 'abc123',
        'validation_issues': []
    }
    defaults.update(overrides)
    return NormalisedOpportunity(**defaults)


class TestExpiryStatusManagement:
    """
    Feature: grant-guide-scraper-engine, Property 19: Expiry Status Management
    
    *For any* record with deadline_date in the past (< today),
    the status SHALL be set to "Expired".
    """
    
    @given(days_ago=st.integers(min_value=1, max_value=365))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_past_deadline_expired(self, days_ago):
        """Records with past deadlines are marked Expired."""
        status_manager = StatusManager()
        past_date = date.today() - timedelta(days=days_ago)
        record = create_record(deadline_date=past_date, is_rolling=False)
        
        status = status_manager.determine_status(record)
        assert status == OpportunityStatus.EXPIRED
    
    @given(days_ahead=st.integers(min_value=1, max_value=365))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_future_deadline_not_expired(self, days_ahead):
        """Records with future deadlines are not marked Expired."""
        status_manager = StatusManager()
        future_date = date.today() + timedelta(days=days_ahead)
        record = create_record(deadline_date=future_date, is_rolling=False)
        
        status = status_manager.determine_status(record)
        assert status != OpportunityStatus.EXPIRED
    
    def test_today_deadline_not_expired(self):
        """Records with today's deadline are not expired yet."""
        status_manager = StatusManager()
        record = create_record(deadline_date=date.today(), is_rolling=False)
        
        status = status_manager.determine_status(record)
        assert status != OpportunityStatus.EXPIRED
    
    def test_no_deadline_not_expired(self):
        """Records without deadline are not expired."""
        status_manager = StatusManager()
        record = create_record(deadline_date=None, is_rolling=True)
        
        status = status_manager.determine_status(record)
        assert status != OpportunityStatus.EXPIRED


class TestStaleRollingRecordDetection:
    """
    Feature: grant-guide-scraper-engine, Property 20: Stale Rolling Record Detection
    
    *For any* record with is_rolling=true and last_verified_date more than 60 days ago,
    the status SHALL be set to "DraftNeedsReview".
    """
    
    @given(days_ago=st.integers(min_value=61, max_value=365))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_stale_rolling_needs_review(self, days_ago):
        """Rolling records not verified in 60+ days need review."""
        status_manager = StatusManager()
        stale_date = date.today() - timedelta(days=days_ago)
        record = create_record(
            is_rolling=True,
            deadline_date=None,
            last_verified_date=stale_date
        )
        
        status = status_manager.determine_status(record)
        assert status == OpportunityStatus.DRAFT_NEEDS_REVIEW
    
    @given(days_ago=st.integers(min_value=0, max_value=59))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_recent_rolling_not_stale(self, days_ago):
        """Rolling records verified within 60 days are not stale."""
        status_manager = StatusManager()
        recent_date = date.today() - timedelta(days=days_ago)
        record = create_record(
            is_rolling=True,
            deadline_date=None,
            last_verified_date=recent_date
        )
        
        status = status_manager.determine_status(record)
        assert status != OpportunityStatus.DRAFT_NEEDS_REVIEW or \
               status_manager.is_missing_required_fields(record)
    
    def test_exactly_60_days_not_stale(self):
        """Rolling record verified exactly 60 days ago is not stale."""
        status_manager = StatusManager()
        boundary_date = date.today() - timedelta(days=60)
        record = create_record(
            is_rolling=True,
            deadline_date=None,
            last_verified_date=boundary_date
        )
        
        # 60 days is the boundary, should not be stale yet
        assert not status_manager.is_stale_rolling(True, boundary_date)
    
    def test_non_rolling_not_affected(self):
        """Non-rolling records are not affected by stale check."""
        status_manager = StatusManager()
        stale_date = date.today() - timedelta(days=100)
        record = create_record(
            is_rolling=False,
            deadline_date=date.today() + timedelta(days=30),
            last_verified_date=stale_date
        )
        
        # Should be Active because it has a future deadline and is not rolling
        status = status_manager.determine_status(record)
        assert status == OpportunityStatus.ACTIVE


class TestActiveStatusValidation:
    """
    Feature: grant-guide-scraper-engine, Property 21: Active Status Validation
    
    *For any* record that has all required fields, valid URLs, a future or null deadline,
    and passes all compliance checks, the status SHALL be set to "Active".
    """
    
    def test_complete_record_active(self):
        """Complete record with all fields is Active."""
        status_manager = StatusManager()
        record = create_record(
            deadline_date=date.today() + timedelta(days=30),
            is_rolling=False,
            last_verified_date=date.today()
        )
        
        status = status_manager.determine_status(record)
        assert status == OpportunityStatus.ACTIVE
    
    def test_rolling_record_active(self):
        """Rolling record with recent verification is Active."""
        status_manager = StatusManager()
        record = create_record(
            deadline_date=None,
            is_rolling=True,
            last_verified_date=date.today()
        )
        
        status = status_manager.determine_status(record)
        assert status == OpportunityStatus.ACTIVE
    
    @given(field=st.sampled_from([
        'title', 'funder_name', 'official_apply_url', 'source_url'
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_missing_required_field_not_active(self, field):
        """Records missing required fields are not Active."""
        status_manager = StatusManager()
        record = create_record(**{field: ''})
        
        status = status_manager.determine_status(record)
        assert status == OpportunityStatus.DRAFT_NEEDS_REVIEW


class TestStatusReason:
    """Test status reason explanations."""
    
    def test_expired_reason(self):
        """Expired status has correct reason."""
        status_manager = StatusManager()
        past_date = date.today() - timedelta(days=10)
        record = create_record(deadline_date=past_date, is_rolling=False)
        
        reason = status_manager.get_status_reason(record)
        assert "Deadline passed" in reason
    
    def test_stale_reason(self):
        """Stale rolling status has correct reason."""
        status_manager = StatusManager()
        stale_date = date.today() - timedelta(days=100)
        record = create_record(
            is_rolling=True,
            deadline_date=None,
            last_verified_date=stale_date
        )
        
        reason = status_manager.get_status_reason(record)
        assert "not verified" in reason.lower()
    
    def test_missing_fields_reason(self):
        """Missing fields status has correct reason."""
        status_manager = StatusManager()
        record = create_record(title='')
        
        reason = status_manager.get_status_reason(record)
        assert "Missing required fields" in reason
        assert "title" in reason
    
    def test_valid_reason(self):
        """Valid record has correct reason."""
        status_manager = StatusManager()
        record = create_record(
            deadline_date=date.today() + timedelta(days=30),
            is_rolling=False
        )
        
        reason = status_manager.get_status_reason(record)
        assert "passed" in reason.lower()
