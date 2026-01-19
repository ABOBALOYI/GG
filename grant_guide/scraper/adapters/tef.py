"""
TEF (Tony Elumelu Foundation) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.tef')


class TEFAdapter(BaseSourceAdapter):
    """Adapter for Tony Elumelu Foundation Entrepreneurship Programme."""
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URL for TEF programme."""
        yield "static://tef/entrepreneurship-programme"
    
    def scrape(self) -> Iterator[RawOpportunity]:
        """
        Override scrape to use static data.
        TEF website structure changes frequently.
        """
        yield RawOpportunity(
            title="Tony Elumelu Foundation Entrepreneurship Programme",
            funder_name="Tony Elumelu Foundation",
            funder_type="international",
            funding_type="grant",
            description="The TEF Entrepreneurship Programme is a 10-year, $100 million commitment to identify, train, mentor and fund 10,000 African entrepreneurs. Selected entrepreneurs receive seed capital, mentorship, and access to the TEFConnect digital platform.",
            industries=[],
            provinces=["National"],
            business_stage="startup",
            eligibility=[
                "Must be an African citizen",
                "Must have a business idea or early-stage business",
                "Must be 18 years or older",
                "Business must be registered or willing to register in Africa",
            ],
            funding_amount_min=None,
            funding_amount_max="$5,000",
            deadline=None,
            is_rolling=False,
            required_documents=[],
            application_steps=[],
            apply_url="https://www.tefconnect.com/",
            source_url="static://tef/entrepreneurship-programme",
            raw_html=""
        )
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Not used - scrape() is overridden."""
        pass
