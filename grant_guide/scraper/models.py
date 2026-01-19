"""
Core data classes and enums for the Grant Guide Scraper Engine.
"""
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class SourceType(Enum):
    """Type of funding source organisation."""
    GOVERNMENT = "government"
    PROVINCIAL = "provincial"
    SETA = "seta"
    CORPORATE = "corporate"
    INTERNATIONAL = "international"


class RecordType(Enum):
    """Type of funding record."""
    FUNDING_OPPORTUNITY = "FundingOpportunity"  # Type A: time-bound with deadline
    FUNDING_PRODUCT = "FundingProduct"          # Type B: rolling/always open


class FundingType(Enum):
    """Type of funding offered."""
    GRANT = "Grant"
    LOAN = "Loan"
    EQUITY = "Equity"
    MIXED = "Mixed"
    COMPETITION_PRIZE = "CompetitionPrize"


class FunderType(Enum):
    """Type of funder organisation."""
    GOV = "Gov"
    DFI = "DFI"
    PRIVATE = "Private"
    NGO_DONOR = "NGO-Donor"
    MIXED = "Mixed"


class BusinessStage(Enum):
    """Business development stage."""
    STARTUP = "Startup"
    SME = "SME"
    ESTABLISHED = "Established"
    ANY = "Any"


class OpportunityStatus(Enum):
    """Status of a funding opportunity."""
    ACTIVE = "Active"
    EXPIRED = "Expired"
    DRAFT_NEEDS_REVIEW = "DraftNeedsReview"


@dataclass
class SourceConfig:
    """Configuration for an approved scraping source."""
    source_id: str
    source_name: str
    base_url: str
    scrape_urls: list[str]
    source_type: SourceType
    adapter_class: str
    is_active: bool = True
    rate_limit_seconds: float = 2.0
    last_scraped: Optional[datetime] = None
    needs_attention: bool = False
    consecutive_failures: int = 0


@dataclass
class RawOpportunity:
    """Raw extracted data before normalisation."""
    title: Optional[str] = None
    funder_name: Optional[str] = None
    funder_type: Optional[str] = None
    funding_type: Optional[str] = None
    description: Optional[str] = None
    industries: list[str] = field(default_factory=list)
    provinces: list[str] = field(default_factory=list)
    business_stage: Optional[str] = None
    eligibility: list[str] = field(default_factory=list)
    funding_amount_min: Optional[str] = None
    funding_amount_max: Optional[str] = None
    deadline: Optional[str] = None
    is_rolling: bool = False
    required_documents: list[str] = field(default_factory=list)
    application_steps: list[str] = field(default_factory=list)
    apply_url: Optional[str] = None
    source_url: str = ""
    raw_html: str = ""


@dataclass
class NormalisedOpportunity:
    """Fully normalised opportunity record."""
    record_type: RecordType
    title: str
    funder_name: str
    funder_type: FunderType
    funding_type: FundingType
    description_short: str
    industry_tags: list[str]
    province_tags: list[str]
    business_stage: BusinessStage
    eligibility_bullets: list[str]
    funding_amount_min: Optional[Decimal]
    funding_amount_max: Optional[Decimal]
    deadline_date: Optional[date]
    is_rolling: bool
    required_documents_bullets: list[str]
    application_steps: list[str]
    official_apply_url: str
    source_url: str
    source_name: str
    last_verified_date: date
    status: OpportunityStatus
    raw_content_hash: str
    validation_issues: list[str] = field(default_factory=list)


@dataclass
class FeedItem:
    """Represents an item from an RSS feed or news page."""
    guid: str
    title: str
    url: str
    published_date: Optional[datetime] = None


@dataclass
class DeduplicationResult:
    """Result of deduplication check."""
    is_duplicate: bool
    existing_record_id: Optional[int] = None
    match_type: Optional[str] = None  # "apply_url", "source_url", "fuzzy_title"
    similarity_score: Optional[float] = None


@dataclass
class ComplianceResult:
    """Result of compliance validation."""
    is_compliant: bool
    issues: list[str] = field(default_factory=list)
    rejection_reason: Optional[str] = None


@dataclass
class ImportResult:
    """Result of importing a record."""
    success: bool
    action: str  # "created", "updated", "skipped"
    record_id: Optional[int] = None
    error: Optional[str] = None
