"""
Property-based tests for status transition correctness (P2).

**Validates: Requirements 3.3**
"""
import pytest
from datetime import date, timedelta
from io import StringIO
from django.core.management import call_command
from opportunities.models import FundingOpportunity, Industry, Province


@pytest.fixture
def setup_data(db):
    """Create test data for property tests."""
    industry = Industry.objects.create(name="Test Industry", slug="test-industry")
    province = Province.objects.create(name="Test Province", slug="test-province")
    return industry, province


@pytest.fixture
def create_opportunity(db, setup_data):
    """Factory to create a single opportunity."""
    industry, province = setup_data
    
    def _create(**kwargs):
        defaults = {
            'funding_name': "Test Opportunity",
            'funder': "Test Funder",
            'funding_type': 'grant',
            'description': "Test description",
            'business_stage': 'startup',
            'eligibility_requirements': ["Req 1"],
            'required_documents': ["Doc 1"],
            'application_steps': ["Step 1"],
            'apply_link': "https://example.com/apply",
            'source_link': "https://example.com/source",
            'last_verified': date.today(),
            'status': 'active',
        }
        defaults.update(kwargs)
        opp = FundingOpportunity.objects.create(**defaults)
        opp.industries.add(industry)
        opp.provinces.add(province)
        return opp
    return _create


class TestStatusTransitionCorrectness:
    """
    P2: Status Transition Correctness
    
    Property: Opportunities with passed deadlines must have status "Expired" 
    after status update runs.
    
    **Validates: Requirements 3.3**
    """

    @pytest.mark.django_db
    def test_passed_deadline_becomes_expired(self, create_opportunity):
        """Opportunities with passed deadlines should be marked as expired."""
        # Create opportunity with deadline in the past
        past_deadline = date.today() - timedelta(days=5)
        opp = create_opportunity(
            funding_name="Past Deadline Opp",
            deadline=past_deadline,
            is_rolling=False,
            status='active'
        )
        
        # Run the update command
        out = StringIO()
        call_command('update_statuses', stdout=out)
        
        # Refresh from database
        opp.refresh_from_db()
        
        # Property: Status must be expired
        assert opp.status == 'expired', f"Expected expired, got {opp.status}"

    @pytest.mark.django_db
    def test_future_deadline_stays_active(self, create_opportunity):
        """Opportunities with future deadlines should remain active."""
        future_deadline = date.today() + timedelta(days=30)
        opp = create_opportunity(
            funding_name="Future Deadline Opp",
            deadline=future_deadline,
            is_rolling=False,
            status='active'
        )
        
        out = StringIO()
        call_command('update_statuses', stdout=out)
        
        opp.refresh_from_db()
        
        assert opp.status == 'active', f"Expected active, got {opp.status}"

    @pytest.mark.django_db
    def test_rolling_not_affected_by_deadline_check(self, create_opportunity):
        """Rolling opportunities should not be marked expired based on deadline."""
        opp = create_opportunity(
            funding_name="Rolling Opp",
            deadline=None,
            is_rolling=True,
            status='active',
            last_verified=date.today()  # Recently verified
        )
        
        out = StringIO()
        call_command('update_statuses', stdout=out)
        
        opp.refresh_from_db()
        
        assert opp.status == 'active', f"Rolling opportunity should stay active, got {opp.status}"

    @pytest.mark.django_db
    def test_stale_rolling_becomes_needs_review(self, create_opportunity):
        """Rolling opportunities not updated for 60 days should need review."""
        stale_date = date.today() - timedelta(days=65)
        opp = create_opportunity(
            funding_name="Stale Rolling Opp",
            deadline=None,
            is_rolling=True,
            status='active',
            last_verified=stale_date
        )
        
        out = StringIO()
        call_command('update_statuses', stdout=out)
        
        opp.refresh_from_db()
        
        assert opp.status == 'needs_review', f"Expected needs_review, got {opp.status}"

    @pytest.mark.django_db
    def test_recently_verified_rolling_stays_active(self, create_opportunity):
        """Rolling opportunities verified within 60 days should stay active."""
        recent_date = date.today() - timedelta(days=30)
        opp = create_opportunity(
            funding_name="Recent Rolling Opp",
            deadline=None,
            is_rolling=True,
            status='active',
            last_verified=recent_date
        )
        
        out = StringIO()
        call_command('update_statuses', stdout=out)
        
        opp.refresh_from_db()
        
        assert opp.status == 'active', f"Expected active, got {opp.status}"

    @pytest.mark.django_db
    def test_draft_with_passed_deadline_becomes_expired(self, create_opportunity):
        """Draft opportunities with passed deadlines should also be marked expired."""
        past_deadline = date.today() - timedelta(days=10)
        opp = create_opportunity(
            funding_name="Draft Past Deadline",
            deadline=past_deadline,
            is_rolling=False,
            status='draft'
        )
        
        out = StringIO()
        call_command('update_statuses', stdout=out)
        
        opp.refresh_from_db()
        
        assert opp.status == 'expired', f"Expected expired, got {opp.status}"

    @pytest.mark.django_db
    def test_already_expired_not_changed(self, create_opportunity):
        """Already expired opportunities should not be changed."""
        past_deadline = date.today() - timedelta(days=10)
        opp = create_opportunity(
            funding_name="Already Expired",
            deadline=past_deadline,
            is_rolling=False,
            status='expired'
        )
        
        out = StringIO()
        call_command('update_statuses', stdout=out)
        
        opp.refresh_from_db()
        
        # Should still be expired (not changed to something else)
        assert opp.status == 'expired'
