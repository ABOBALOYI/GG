"""
DEDAT (Western Cape Department of Economic Development and Tourism) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.dedat')


class DEDATAdapter(BaseSourceAdapter):
    """Adapter for scraping Western Cape DEDAT funding opportunities."""
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URLs of DEDAT funding pages."""
        for scrape_url in self.config.scrape_urls:
            try:
                html = self.http.get(scrape_url)
                soup = self.parse_html(html)
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if any(word in href.lower() for word in ['fund', 'grant', 'programme', 'support']):
                        yield self.make_absolute_url(href)
                        
            except Exception as e:
                logger.error(f"Error getting URLs from {scrape_url}: {e}")
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Extract opportunity data from a DEDAT page."""
        soup = self.parse_html(html)
        
        title = None
        h1 = soup.find('h1')
        if h1:
            title = self.extract_text(h1)
        
        description = None
        content = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
        if content:
            parts = []
            for p in content.find_all('p', limit=5):
                text = self.extract_text(p)
                if text and len(text) > 20:
                    parts.append(text)
            if parts:
                description = ' '.join(parts[:3])
        
        eligibility = ["Must be a Western Cape-based business"]
        
        return RawOpportunity(
            title=title,
            funder_name="Western Cape DEDAT",
            funder_type="provincial",
            funding_type="grant",
            description=description,
            industries=[],
            provinces=["Western Cape"],
            business_stage=None,
            eligibility=eligibility,
            funding_amount_min=None,
            funding_amount_max=None,
            deadline=None,
            is_rolling=True,
            required_documents=[],
            application_steps=[],
            apply_url=url,
            source_url=url,
            raw_html=html
        )
