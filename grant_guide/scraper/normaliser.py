"""
Record normaliser for transforming raw scraped data into canonical format.
"""
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Optional

from .models import (
    RawOpportunity, NormalisedOpportunity, RecordType, FundingType,
    FunderType, BusinessStage, OpportunityStatus
)
from .http_client import compute_content_hash


class RecordNormaliser:
    """Transforms raw extracted data into normalised format."""
    
    CANONICAL_PROVINCES = [
        "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal",
        "Limpopo", "Mpumalanga", "Northern Cape", "North West",
        "Western Cape", "National"
    ]
    
    PROVINCE_ALIASES = {
        # Abbreviations
        'ec': 'Eastern Cape', 'eastern cape': 'Eastern Cape',
        'fs': 'Free State', 'free state': 'Free State',
        'gp': 'Gauteng', 'gauteng': 'Gauteng', 'gauteng province': 'Gauteng',
        'kzn': 'KwaZulu-Natal', 'kwazulu-natal': 'KwaZulu-Natal', 
        'kwazulu natal': 'KwaZulu-Natal', 'kwa-zulu natal': 'KwaZulu-Natal',
        'lp': 'Limpopo', 'limpopo': 'Limpopo',
        'mp': 'Mpumalanga', 'mpumalanga': 'Mpumalanga',
        'nc': 'Northern Cape', 'northern cape': 'Northern Cape',
        'nw': 'North West', 'north west': 'North West', 'northwest': 'North West',
        'wc': 'Western Cape', 'western cape': 'Western Cape',
        'national': 'National', 'nationwide': 'National', 'all provinces': 'National',
        'south africa': 'National', 'sa': 'National',
    }
    
    CANONICAL_INDUSTRIES = [
        "Agriculture", "Construction", "Manufacturing", "Retail", "ICT",
        "Tourism", "Transport", "Energy", "Healthcare", "Education",
        "Creative", "Finance", "Mining", "Services", "Green Economy"
    ]
    
    INDUSTRY_ALIASES = {
        # ICT variations
        'ict': 'ICT', 'it': 'ICT', 'tech': 'ICT', 'technology': 'ICT',
        'software': 'ICT', 'digital': 'ICT', 'information technology': 'ICT',
        # Agriculture
        'agriculture': 'Agriculture', 'agri': 'Agriculture', 'farming': 'Agriculture',
        'agribusiness': 'Agriculture', 'agro': 'Agriculture',
        # Manufacturing
        'manufacturing': 'Manufacturing', 'production': 'Manufacturing',
        # Retail
        'retail': 'Retail', 'trade': 'Retail', 'wholesale': 'Retail',
        'retail & trade': 'Retail', 'commerce': 'Retail',
        # Tourism
        'tourism': 'Tourism', 'hospitality': 'Tourism', 'tourism & hospitality': 'Tourism',
        # Transport
        'transport': 'Transport', 'logistics': 'Transport', 'transport & logistics': 'Transport',
        # Energy
        'energy': 'Energy', 'renewables': 'Energy', 'energy & renewables': 'Energy',
        'renewable energy': 'Energy', 'green energy': 'Energy',
        # Healthcare
        'healthcare': 'Healthcare', 'health': 'Healthcare', 'medical': 'Healthcare',
        # Education
        'education': 'Education', 'training': 'Education', 'skills': 'Education',
        # Creative
        'creative': 'Creative', 'creative industries': 'Creative', 'arts': 'Creative',
        'media': 'Creative', 'entertainment': 'Creative',
        # Finance
        'finance': 'Finance', 'financial services': 'Finance', 'banking': 'Finance',
        'fintech': 'Finance',
        # Mining
        'mining': 'Mining', 'minerals': 'Mining',
        # Services
        'services': 'Services', 'professional services': 'Services',
        # Construction
        'construction': 'Construction', 'building': 'Construction',
        # Green Economy
        'green economy': 'Green Economy', 'green': 'Green Economy',
        'sustainability': 'Green Economy', 'environmental': 'Green Economy',
    }
    
    FUNDING_TYPE_ALIASES = {
        'grant': FundingType.GRANT, 'grants': FundingType.GRANT,
        'loan': FundingType.LOAN, 'loans': FundingType.LOAN, 'finance': FundingType.LOAN,
        'equity': FundingType.EQUITY, 'investment': FundingType.EQUITY,
        'mixed': FundingType.MIXED, 'blended': FundingType.MIXED,
        'competition': FundingType.COMPETITION_PRIZE, 'prize': FundingType.COMPETITION_PRIZE,
        'challenge': FundingType.COMPETITION_PRIZE, 'award': FundingType.COMPETITION_PRIZE,
    }
    
    BUSINESS_STAGE_ALIASES = {
        'startup': BusinessStage.STARTUP, 'start-up': BusinessStage.STARTUP,
        'early stage': BusinessStage.STARTUP, 'new business': BusinessStage.STARTUP,
        'sme': BusinessStage.SME, 'small business': BusinessStage.SME,
        'medium business': BusinessStage.SME, 'smme': BusinessStage.SME,
        'established': BusinessStage.ESTABLISHED, 'mature': BusinessStage.ESTABLISHED,
        'corporate': BusinessStage.ESTABLISHED,
        'any': BusinessStage.ANY, 'all': BusinessStage.ANY,
    }
    
    def normalise(self, raw: RawOpportunity, source_name: str) -> NormalisedOpportunity:
        """
        Transform raw data to normalised format.
        
        Args:
            raw: Raw opportunity data from scraper.
            source_name: Name of the source for attribution.
            
        Returns:
            Normalised opportunity record.
        """
        validation_issues = []
        
        # Determine record type
        deadline_date = self.normalise_date(raw.deadline)
        if deadline_date is not None or not raw.is_rolling:
            record_type = RecordType.FUNDING_OPPORTUNITY
        else:
            record_type = RecordType.FUNDING_PRODUCT
        
        # Normalise fields
        title = raw.title or ""
        funder_name = raw.funder_name or ""
        
        # Funder type
        funder_type = self._normalise_funder_type(raw.funder_type)
        if funder_type is None:
            funder_type = FunderType.GOV  # Default
            validation_issues.append("Could not determine funder type")
        
        # Funding type
        funding_type = self.normalise_funding_type(raw.funding_type)
        if funding_type is None:
            funding_type = FundingType.GRANT  # Default
            validation_issues.append("Could not determine funding type")
        
        # Description (truncate to 300 chars)
        description_short = self._truncate_description(raw.description or "")
        
        # Industries
        industry_tags = [
            self.normalise_industry(i) for i in raw.industries
            if self.normalise_industry(i) is not None
        ]
        if not industry_tags and raw.industries:
            validation_issues.append(f"Could not map industries: {raw.industries}")
        
        # Provinces
        province_tags = [
            self.normalise_province(p) for p in raw.provinces
            if self.normalise_province(p) is not None
        ]
        if not province_tags:
            province_tags = ["National"]  # Default
        
        # Business stage
        business_stage = self._normalise_business_stage(raw.business_stage)
        if business_stage is None:
            business_stage = BusinessStage.ANY
            if raw.business_stage:
                validation_issues.append(f"Could not map business stage: {raw.business_stage}")
        
        # Amounts
        funding_amount_min = self.normalise_amount(raw.funding_amount_min)
        funding_amount_max = self.normalise_amount(raw.funding_amount_max)
        
        # Compute content hash
        raw_content_hash = compute_content_hash(raw.raw_html)
        
        # Determine status
        status = self._determine_status(
            title, funder_name, funding_type, raw.apply_url, raw.source_url,
            deadline_date, raw.is_rolling, validation_issues
        )
        
        return NormalisedOpportunity(
            record_type=record_type,
            title=title,
            funder_name=funder_name,
            funder_type=funder_type,
            funding_type=funding_type,
            description_short=description_short,
            industry_tags=industry_tags,
            province_tags=province_tags,
            business_stage=business_stage,
            eligibility_bullets=raw.eligibility or [],
            funding_amount_min=funding_amount_min,
            funding_amount_max=funding_amount_max,
            deadline_date=deadline_date,
            is_rolling=raw.is_rolling,
            required_documents_bullets=raw.required_documents or [],
            application_steps=raw.application_steps or [],
            official_apply_url=raw.apply_url or "",
            source_url=raw.source_url,
            source_name=source_name,
            last_verified_date=date.today(),
            status=status,
            raw_content_hash=raw_content_hash,
            validation_issues=validation_issues
        )
    
    def normalise_amount(self, amount_str: Optional[str]) -> Optional[Decimal]:
        """
        Convert amount string to ZAR Decimal.
        
        Handles formats: R50,000 / R 50 000 / 50000 ZAR / R1 million / R500k
        Also handles integers/floats passed directly.
        """
        if amount_str is None:
            return None
        
        # Handle numeric types directly
        if isinstance(amount_str, (int, float)):
            return Decimal(str(amount_str))
        
        if not isinstance(amount_str, str):
            return None
        
        # Clean the string
        amount = amount_str.strip().upper()
        
        # Remove currency indicators
        amount = re.sub(r'^R\s*', '', amount)
        amount = re.sub(r'\s*ZAR$', '', amount)
        amount = re.sub(r'\s*RAND$', '', amount)
        
        # Handle multipliers
        multiplier = 1
        if 'MILLION' in amount or 'MIL' in amount:
            multiplier = 1_000_000
            amount = re.sub(r'\s*(MILLION|MIL).*', '', amount)
        elif 'K' in amount:
            multiplier = 1_000
            amount = re.sub(r'\s*K.*', '', amount)
        elif 'BILLION' in amount:
            multiplier = 1_000_000_000
            amount = re.sub(r'\s*BILLION.*', '', amount)
        
        # Remove spaces and commas
        amount = amount.replace(' ', '').replace(',', '')
        
        # Extract number
        match = re.search(r'[\d.]+', amount)
        if not match:
            return None
        
        try:
            value = Decimal(match.group()) * multiplier
            return value
        except InvalidOperation:
            return None
    
    def normalise_date(self, date_str: Optional[str]) -> Optional[date]:
        """
        Convert date string to ISO date.
        
        Handles formats: 15 March 2025 / 2025/03/15 / 15-03-2025 / March 15, 2025
        """
        if not date_str:
            return None
        
        import re
        from datetime import datetime
        
        date_str = date_str.strip()
        
        # Common date formats to try
        formats = [
            '%Y-%m-%d',           # 2025-03-15
            '%d-%m-%Y',           # 15-03-2025
            '%Y/%m/%d',           # 2025/03/15
            '%d/%m/%Y',           # 15/03/2025
            '%d %B %Y',           # 15 March 2025
            '%d %b %Y',           # 15 Mar 2025
            '%B %d, %Y',          # March 15, 2025
            '%b %d, %Y',          # Mar 15, 2025
            '%d %B, %Y',          # 15 March, 2025
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        return None
    
    def normalise_province(self, province: str) -> Optional[str]:
        """Map province to canonical name."""
        if not province:
            return None
        
        key = province.strip().lower()
        return self.PROVINCE_ALIASES.get(key)
    
    def normalise_industry(self, industry: str) -> Optional[str]:
        """Map industry to canonical tag."""
        if not industry:
            return None
        
        key = industry.strip().lower()
        return self.INDUSTRY_ALIASES.get(key)
    
    def normalise_funding_type(self, funding_type: Optional[str]) -> Optional[FundingType]:
        """Map funding type to canonical enum."""
        if not funding_type:
            return None
        
        key = funding_type.strip().lower()
        return self.FUNDING_TYPE_ALIASES.get(key)
    
    def _normalise_funder_type(self, funder_type: Optional[str]) -> Optional[FunderType]:
        """Map funder type to canonical enum."""
        if not funder_type:
            return None
        
        key = funder_type.strip().lower()
        mapping = {
            'gov': FunderType.GOV, 'government': FunderType.GOV,
            'dfi': FunderType.DFI, 'development finance': FunderType.DFI,
            'private': FunderType.PRIVATE, 'corporate': FunderType.PRIVATE,
            'ngo': FunderType.NGO_DONOR, 'donor': FunderType.NGO_DONOR,
            'ngo-donor': FunderType.NGO_DONOR, 'international': FunderType.NGO_DONOR,
            'mixed': FunderType.MIXED,
        }
        return mapping.get(key)
    
    def _normalise_business_stage(self, stage: Optional[str]) -> Optional[BusinessStage]:
        """Map business stage to canonical enum."""
        if not stage:
            return None
        
        key = stage.strip().lower()
        return self.BUSINESS_STAGE_ALIASES.get(key)
    
    def _truncate_description(self, description: str, max_length: int = 300) -> str:
        """Truncate description to max length with ellipsis."""
        if len(description) <= max_length:
            return description
        return description[:297] + "..."
    
    def _determine_status(
        self,
        title: str,
        funder_name: str,
        funding_type: Optional[FundingType],
        apply_url: Optional[str],
        source_url: str,
        deadline_date: Optional[date],
        is_rolling: bool,
        validation_issues: list[str]
    ) -> OpportunityStatus:
        """Determine the status of the opportunity."""
        # Check for expired deadline
        if deadline_date and deadline_date < date.today():
            return OpportunityStatus.EXPIRED
        
        # Check for missing required fields
        if not title or not funder_name or not funding_type or not apply_url or not source_url:
            return OpportunityStatus.DRAFT_NEEDS_REVIEW
        
        # Check for validation issues
        if validation_issues:
            return OpportunityStatus.DRAFT_NEEDS_REVIEW
        
        return OpportunityStatus.ACTIVE
