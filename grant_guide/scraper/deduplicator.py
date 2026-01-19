"""
Deduplicator for identifying and handling duplicate records.
"""
from typing import Optional

from rapidfuzz import fuzz

from .models import NormalisedOpportunity, DeduplicationResult


class Deduplicator:
    """Identifies and handles duplicate records."""
    
    FUZZY_THRESHOLD = 0.92  # 92% similarity threshold (stricter to avoid false matches)
    
    def __init__(self, get_existing_records_func=None):
        """
        Initialize deduplicator.
        
        Args:
            get_existing_records_func: Function to get existing records from database.
                Should return list of dicts with keys: id, apply_link, source_link, funding_name, funder
        """
        self._get_existing_records = get_existing_records_func
    
    def check_duplicate(self, record: NormalisedOpportunity) -> DeduplicationResult:
        """
        Check if record already exists using priority order:
        1. Exact match on source_url (most reliable - unique per page)
        2. Exact match on official_apply_url (only if URL is specific, not generic)
        3. Fuzzy match on title+funder_name (>= 92% similarity)
        
        Args:
            record: Normalised opportunity to check.
            
        Returns:
            DeduplicationResult with match information.
        """
        if self._get_existing_records is None:
            return DeduplicationResult(is_duplicate=False)
        
        existing_records = self._get_existing_records()
        
        # Priority 1: Check by source URL (most reliable - unique per scraped page)
        result = self._check_by_source_url(record.source_url, existing_records)
        if result.is_duplicate:
            return result
        
        # Priority 2: Check by apply URL (skip generic application pages)
        # Skip if apply URL looks like a generic application portal
        apply_url = record.official_apply_url or ""
        is_generic_apply = any(term in apply_url.lower() for term in [
            'application-procedures', 'application-forms', 'apply-online',
            'login', 'register', 'portal'
        ])
        if not is_generic_apply:
            result = self._check_by_apply_url(record.official_apply_url, existing_records)
            if result.is_duplicate:
                return result
        
        # Priority 3: Fuzzy match on title + funder
        result = self.fuzzy_match_title_funder(
            record.title, record.funder_name, existing_records
        )
        if result.is_duplicate:
            return result
        
        return DeduplicationResult(is_duplicate=False)
    
    def _check_by_apply_url(
        self, apply_url: str, existing_records: list[dict]
    ) -> DeduplicationResult:
        """Check for exact match on apply URL."""
        if not apply_url:
            return DeduplicationResult(is_duplicate=False)
        
        for record in existing_records:
            if record.get('apply_link') == apply_url:
                return DeduplicationResult(
                    is_duplicate=True,
                    existing_record_id=record.get('id'),
                    match_type="apply_url",
                    similarity_score=1.0
                )
        
        return DeduplicationResult(is_duplicate=False)
    
    def _check_by_source_url(
        self, source_url: str, existing_records: list[dict]
    ) -> DeduplicationResult:
        """Check for exact match on source URL."""
        if not source_url:
            return DeduplicationResult(is_duplicate=False)
        
        for record in existing_records:
            if record.get('source_link') == source_url:
                return DeduplicationResult(
                    is_duplicate=True,
                    existing_record_id=record.get('id'),
                    match_type="source_url",
                    similarity_score=1.0
                )
        
        return DeduplicationResult(is_duplicate=False)
    
    def fuzzy_match_title_funder(
        self, title: str, funder: str, existing_records: list[dict]
    ) -> DeduplicationResult:
        """
        Perform fuzzy matching on title+funder combination.
        
        Uses rapidfuzz for efficient string matching with 85% threshold.
        """
        if not title or not funder:
            return DeduplicationResult(is_duplicate=False)
        
        # Combine title and funder for matching
        search_text = f"{title} {funder}".lower().strip()
        
        best_match = None
        best_score = 0.0
        
        for record in existing_records:
            existing_title = record.get('funding_name', '')
            existing_funder = record.get('funder', '')
            existing_text = f"{existing_title} {existing_funder}".lower().strip()
            
            # Calculate similarity using token_sort_ratio for better matching
            score = fuzz.token_sort_ratio(search_text, existing_text) / 100.0
            
            if score > best_score:
                best_score = score
                best_match = record
        
        if best_score >= self.FUZZY_THRESHOLD:
            return DeduplicationResult(
                is_duplicate=True,
                existing_record_id=best_match.get('id'),
                match_type="fuzzy_title",
                similarity_score=best_score
            )
        
        return DeduplicationResult(is_duplicate=False)


def create_django_deduplicator():
    """
    Create a deduplicator configured to use Django ORM.
    
    Returns:
        Deduplicator instance connected to Django database.
    """
    def get_existing_records():
        from opportunities.models import FundingOpportunity
        return list(
            FundingOpportunity.objects.values(
                'id', 'apply_link', 'source_link', 'funding_name', 'funder'
            )
        )
    
    return Deduplicator(get_existing_records_func=get_existing_records)
