"""
Status manager for determining and updating opportunity statuses.
"""
from datetime import date, timedelta
from typing import Optional

from .models import NormalisedOpportunity, OpportunityStatus


class StatusManager:
    """Manages opportunity status based on deadlines, verification, and required fields."""
    
    STALE_ROLLING_DAYS = 60  # Days before rolling opportunity needs review
    
    def determine_status(
        self,
        record: NormalisedOpportunity,
        existing_last_verified: Optional[date] = None
    ) -> OpportunityStatus:
        """
        Determine the appropriate status for an opportunity.
        
        Priority order:
        1. Expired if deadline has passed
        2. DraftNeedsReview if rolling and stale (>60 days since verification)
        3. DraftNeedsReview if missing required fields
        4. Active if all checks pass
        
        Args:
            record: Normalised opportunity record.
            existing_last_verified: Last verified date from existing record (for updates).
            
        Returns:
            Appropriate OpportunityStatus.
        """
        # Check for expired deadline
        if self.is_expired(record.deadline_date):
            return OpportunityStatus.EXPIRED
        
        # Check for stale rolling opportunity
        last_verified = existing_last_verified or record.last_verified_date
        if self.is_stale_rolling(record.is_rolling, last_verified):
            return OpportunityStatus.DRAFT_NEEDS_REVIEW
        
        # Check for missing required fields
        if self.is_missing_required_fields(record):
            return OpportunityStatus.DRAFT_NEEDS_REVIEW
        
        # All checks passed
        return OpportunityStatus.ACTIVE
    
    def is_expired(self, deadline_date: Optional[date]) -> bool:
        """
        Check if deadline has passed.
        
        Args:
            deadline_date: Deadline date to check.
            
        Returns:
            True if deadline is in the past, False otherwise.
        """
        if deadline_date is None:
            return False
        return deadline_date < date.today()
    
    def is_stale_rolling(self, is_rolling: bool, last_verified: date) -> bool:
        """
        Check if rolling opportunity is stale (not verified in 60+ days).
        
        Args:
            is_rolling: Whether opportunity is rolling/always open.
            last_verified: Date of last verification.
            
        Returns:
            True if rolling and stale, False otherwise.
        """
        if not is_rolling:
            return False
        
        stale_threshold = date.today() - timedelta(days=self.STALE_ROLLING_DAYS)
        return last_verified < stale_threshold
    
    def is_missing_required_fields(self, record: NormalisedOpportunity) -> bool:
        """
        Check if any required fields are missing.
        
        Required fields: title, funder_name, funding_type, official_apply_url, source_url
        
        Args:
            record: Normalised opportunity record.
            
        Returns:
            True if any required field is missing, False otherwise.
        """
        if not record.title:
            return True
        if not record.funder_name:
            return True
        if not record.funding_type:
            return True
        if not record.official_apply_url:
            return True
        if not record.source_url:
            return True
        return False
    
    def get_status_reason(self, record: NormalisedOpportunity) -> str:
        """
        Get human-readable reason for the current status.
        
        Args:
            record: Normalised opportunity record.
            
        Returns:
            String explaining the status.
        """
        if self.is_expired(record.deadline_date):
            return f"Deadline passed: {record.deadline_date}"
        
        if self.is_stale_rolling(record.is_rolling, record.last_verified_date):
            return f"Rolling opportunity not verified since {record.last_verified_date}"
        
        missing = []
        if not record.title:
            missing.append("title")
        if not record.funder_name:
            missing.append("funder_name")
        if not record.funding_type:
            missing.append("funding_type")
        if not record.official_apply_url:
            missing.append("official_apply_url")
        if not record.source_url:
            missing.append("source_url")
        
        if missing:
            return f"Missing required fields: {', '.join(missing)}"
        
        return "All validation checks passed"
