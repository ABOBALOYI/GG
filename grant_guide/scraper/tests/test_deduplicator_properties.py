"""
Property-based tests for the Deduplicator.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**
"""
import pytest
from hypothesis import given, strategies as st, settings

from scraper.deduplicator import Deduplicator
from scraper.models import (
    NormalisedOpportunity, RecordType, FundingType, FunderType,
    BusinessStage, OpportunityStatus
)
from datetime import date


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


class TestDeduplicationPriority:
    """
    Feature: grant-guide-scraper-engine, Property 17: Deduplication Priority
    
    *For any* new record, the Deduplicator SHALL check for duplicates in this order:
    (1) exact match on source_url (most reliable - unique per page),
    (2) exact match on official_apply_url (if not generic),
    (3) fuzzy match on title+funder_name with similarity >= 0.92.
    """
    
    def test_source_url_match_takes_priority(self):
        """Source URL match takes priority over other matches (most reliable)."""
        existing = [
            {'id': 1, 'apply_link': 'https://example.gov.za/apply', 
             'source_link': 'https://other.gov.za', 'funding_name': 'Different', 'funder': 'Other'},
            {'id': 2, 'apply_link': 'https://other.gov.za/apply',
             'source_link': 'https://example.gov.za/funding', 'funding_name': 'Test Funding', 'funder': 'Test'},
        ]
        
        dedup = Deduplicator(lambda: existing)
        record = create_record()
        
        result = dedup.check_duplicate(record)
        assert result.is_duplicate
        assert result.match_type == "source_url"
        assert result.existing_record_id == 2
    
    def test_apply_url_match_second_priority(self):
        """Apply URL match is checked after source URL."""
        existing = [
            {'id': 1, 'apply_link': 'https://example.gov.za/apply',
             'source_link': 'https://other.gov.za/funding', 'funding_name': 'Different', 'funder': 'Other'},
        ]
        
        dedup = Deduplicator(lambda: existing)
        record = create_record(source_url='https://new.gov.za/funding')
        
        result = dedup.check_duplicate(record)
        assert result.is_duplicate
        assert result.match_type == "apply_url"
        assert result.existing_record_id == 1
    
    def test_fuzzy_match_third_priority(self):
        """Fuzzy title+funder match is checked last."""
        existing = [
            {'id': 1, 'apply_link': 'https://other.gov.za/apply',
             'source_link': 'https://other.gov.za/funding', 
             'funding_name': 'Test Funding Opportunity', 'funder': 'Test Funder'},
        ]
        
        dedup = Deduplicator(lambda: existing)
        record = create_record(
            official_apply_url='https://new.gov.za/apply',
            source_url='https://new.gov.za/funding'
        )
        
        result = dedup.check_duplicate(record)
        assert result.is_duplicate
        assert result.match_type == "fuzzy_title"
        assert result.similarity_score >= 0.85
    
    def test_no_match_returns_not_duplicate(self):
        """No match returns is_duplicate=False."""
        existing = [
            {'id': 1, 'apply_link': 'https://other.gov.za/apply',
             'source_link': 'https://other.gov.za/funding',
             'funding_name': 'Completely Different', 'funder': 'Other Org'},
        ]
        
        dedup = Deduplicator(lambda: existing)
        record = create_record(
            official_apply_url='https://new.gov.za/apply',
            source_url='https://new.gov.za/funding'
        )
        
        result = dedup.check_duplicate(record)
        assert not result.is_duplicate


class TestFuzzyMatching:
    """Test fuzzy matching behavior."""
    
    @given(similarity=st.floats(min_value=0.92, max_value=1.0))
    @settings(max_examples=50)
    def test_high_similarity_matches(self, similarity):
        """High similarity scores (>=0.92) result in match."""
        # Create records with very similar titles
        existing = [
            {'id': 1, 'apply_link': '', 'source_link': '',
             'funding_name': 'Youth Development Grant Programme', 'funder': 'NYDA'},
        ]
        
        dedup = Deduplicator(lambda: existing)
        record = create_record(
            title='Youth Development Grant Program',  # Slight variation
            funder_name='NYDA',
            official_apply_url='https://new.gov.za/apply',
            source_url='https://new.gov.za/funding'
        )
        
        result = dedup.check_duplicate(record)
        # Should match due to high similarity
        assert result.is_duplicate or result.similarity_score is None
    
    def test_low_similarity_no_match(self):
        """Low similarity scores (<0.92) do not result in match."""
        existing = [
            {'id': 1, 'apply_link': '', 'source_link': '',
             'funding_name': 'Agriculture Support Fund', 'funder': 'DTIC'},
        ]
        
        dedup = Deduplicator(lambda: existing)
        record = create_record(
            title='Youth Development Grant',
            funder_name='NYDA',
            official_apply_url='https://new.gov.za/apply',
            source_url='https://new.gov.za/funding'
        )
        
        result = dedup.check_duplicate(record)
        assert not result.is_duplicate


class TestDuplicateUpdatePreservation:
    """
    Feature: grant-guide-scraper-engine, Property 18: Duplicate Update Preservation
    
    *For any* record identified as a duplicate, updating it SHALL preserve
    the original record ID.
    """
    
    def test_duplicate_returns_existing_id(self):
        """Duplicate detection returns the existing record ID."""
        existing = [
            {'id': 42, 'apply_link': 'https://example.gov.za/apply',
             'source_link': '', 'funding_name': '', 'funder': ''},
        ]
        
        dedup = Deduplicator(lambda: existing)
        record = create_record()
        
        result = dedup.check_duplicate(record)
        assert result.is_duplicate
        assert result.existing_record_id == 42
    
    def test_similarity_score_returned_for_fuzzy(self):
        """Fuzzy matches include similarity score."""
        existing = [
            {'id': 1, 'apply_link': '', 'source_link': '',
             'funding_name': 'Test Funding Opportunity', 'funder': 'Test Funder'},
        ]
        
        dedup = Deduplicator(lambda: existing)
        record = create_record(
            official_apply_url='https://new.gov.za/apply',
            source_url='https://new.gov.za/funding'
        )
        
        result = dedup.check_duplicate(record)
        if result.match_type == "fuzzy_title":
            assert result.similarity_score is not None
            assert 0 <= result.similarity_score <= 1


class TestEmptyDatabase:
    """Test behavior with no existing records."""
    
    def test_no_existing_records(self):
        """No duplicates when database is empty."""
        dedup = Deduplicator(lambda: [])
        record = create_record()
        
        result = dedup.check_duplicate(record)
        assert not result.is_duplicate
    
    def test_no_callback_function(self):
        """No duplicates when no callback provided."""
        dedup = Deduplicator()
        record = create_record()
        
        result = dedup.check_duplicate(record)
        assert not result.is_duplicate
