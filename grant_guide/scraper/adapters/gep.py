"""
GEP (Gauteng Enterprise Propeller) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.gep')


class GEPAdapter(BaseSourceAdapter):
    """Adapter for scraping GEP funding opportunities."""
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URLs of GEP call for proposals pages."""
        for scrape_url in self.config.scrape_urls:
            try:
                html = self.http.get(scrape_url)
                soup = self.parse_html(html)
                
                # Find proposal/call links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if any(word in href.lower() for word in ['call', 'proposal', 'fund', 'grant']):
                        yield self.make_absolute_url(href)
                        
            except Exception as e:
                logger.error(f"Error getting URLs from {scrape_url}: {e}")
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Extract opportunity data from a GEP page."""
        soup = self.parse_html(html)
        
        title = None
        h1 = soup.find('h1')
        if h1:
            title = self.extract_text(h1)
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = self.extract_text(title_tag)
        
        description = None
        content = soup.find('article') or soup.find('div', class_='content')
        if content:
            parts = []
            for p in content.find_all('p', limit=5):
                text = self.extract_text(p)
                if text and len(text) > 20:
                    parts.append(text)
            if parts:
                description = ' '.join(parts[:3])
        
        eligibility = ["Must be a Gauteng-based business"]
        
        return RawOpportunity(
            title=title,
            funder_name="GEP",
            funder_type="provincial",
            funding_type="grant",
            description=description,
            industries=[],
            provinces=["Gauteng"],
            business_stage=None,
            eligibility=eligibility,
            funding_amount_min=None,
            funding_amount_max=None,
            deadline=None,
            is_rolling=False,
            required_documents=[],
            application_steps=[],
            apply_url=url,
            source_url=url,
            raw_html=html
        )
