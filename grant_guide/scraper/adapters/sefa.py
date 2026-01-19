"""
SEFA (Small Enterprise Finance Agency) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.sefa')


class SEFAAdapter(BaseSourceAdapter):
    """Adapter for scraping SEFA funding products."""
    
    # SEFA website has SSL issues, using known product pages
    FUNDING_PRODUCTS = [
        {
            "title": "SEFA Direct Lending",
            "description": "Direct loans to small businesses from R50,000 to R5 million for working capital, asset finance, and business expansion.",
            "funding_type": "loan",
            "min_amount": "R50,000",
            "max_amount": "R5,000,000",
        },
        {
            "title": "SEFA Wholesale Lending",
            "description": "Funding through financial intermediaries including microfinance institutions, retail financial institutions, and joint ventures.",
            "funding_type": "loan",
            "min_amount": None,
            "max_amount": None,
        },
        {
            "title": "Khula Credit Guarantee",
            "description": "Credit guarantees to banks and financial institutions to encourage lending to SMMEs that lack collateral.",
            "funding_type": "mixed",
            "min_amount": None,
            "max_amount": None,
        },
    ]
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield placeholder URLs for SEFA products."""
        # SEFA website has SSL issues, so we use static data
        for i, _ in enumerate(self.FUNDING_PRODUCTS):
            yield f"static://sefa/product/{i}"
    
    def scrape(self) -> Iterator[RawOpportunity]:
        """
        Override scrape to use static data instead of HTTP requests.
        SEFA website has SSL certificate issues.
        """
        for i, product in enumerate(self.FUNDING_PRODUCTS):
            yield RawOpportunity(
                title=product["title"],
                funder_name="SEFA",
                funder_type="government",
                funding_type=product["funding_type"],
                description=product["description"],
                industries=[],
                provinces=["National"],
                business_stage="sme",
                eligibility=[
                    "Must be a South African registered business",
                    "Must be an SMME (Small, Medium, or Micro Enterprise)",
                    "Must have a viable business plan",
                ],
                funding_amount_min=product["min_amount"],
                funding_amount_max=product["max_amount"],
                deadline=None,
                is_rolling=True,
                required_documents=[],
                application_steps=[],
                apply_url="https://www.sefa.org.za/",
                source_url=f"static://sefa/product/{i}",
                raw_html=""
            )
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Not used - scrape() is overridden."""
        pass
