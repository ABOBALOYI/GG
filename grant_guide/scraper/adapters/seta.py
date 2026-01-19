"""
SETA (Sector Education and Training Authority) adapters.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.seta')


class BaseSETAAdapter(BaseSourceAdapter):
    """Base adapter for SETA funding opportunities."""
    
    SETA_NAME = "SETA"
    SECTOR = "General"
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URLs of SETA funding/grant pages."""
        for scrape_url in self.config.scrape_urls:
            try:
                html = self.http.get(scrape_url)
                soup = self.parse_html(html)
                
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if any(word in href.lower() for word in ['grant', 'fund', 'bursary', 'learnership', 'skills']):
                        yield self.make_absolute_url(href)
                        
            except Exception as e:
                logger.error(f"Error getting URLs from {scrape_url}: {e}")
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Extract opportunity data from a SETA page."""
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
        content = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
        if content:
            parts = []
            for p in content.find_all('p', limit=5):
                text = self.extract_text(p)
                if text and len(text) > 20:
                    parts.append(text)
            if parts:
                description = ' '.join(parts[:3])
        
        eligibility = [
            f"Must operate in the {self.SECTOR} sector",
            "Must be registered with the relevant SETA",
        ]
        
        return RawOpportunity(
            title=title,
            funder_name=self.SETA_NAME,
            funder_type="seta",
            funding_type="grant",
            description=description,
            industries=[self.SECTOR],
            provinces=["National"],
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


class ServicesSETAAdapter(BaseSETAAdapter):
    """Adapter for Services SETA."""
    SETA_NAME = "Services SETA"
    SECTOR = "Services"


class HWSETAAdapter(BaseSETAAdapter):
    """Adapter for Health and Welfare SETA."""
    SETA_NAME = "HWSETA"
    SECTOR = "Health and Welfare"


class CETAAdapter(BaseSETAAdapter):
    """Adapter for Construction Education and Training Authority."""
    SETA_NAME = "CETA"
    SECTOR = "Construction"
