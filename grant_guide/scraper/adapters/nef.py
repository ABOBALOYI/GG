"""
NEF (National Empowerment Fund) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.nef')


class NEFAdapter(BaseSourceAdapter):
    """Adapter for scraping NEF funding products."""
    
    FUNDING_PAGES = [
        "/products-services/women-empowerment-fund/",
        "/products-services/imbewu-fund/",
        "/products-services/umnotho-fund/",
        "/products-services/strategic-projects-fund/",
    ]
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URLs of NEF funding product pages."""
        base = self.config.base_url.rstrip('/')
        for path in self.FUNDING_PAGES:
            yield f"{base}{path}"
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Extract opportunity data from a NEF funding page."""
        soup = self.parse_html(html)
        
        title = None
        h1 = soup.find('h1', class_='page-header-title') or soup.find('h1')
        if h1:
            title = self.extract_text(h1)
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = self.extract_text(title_tag).split('|')[0].strip()
        
        description = None
        content = soup.find('div', class_='entry-content') or soup.find('article')
        if content:
            parts = []
            for p in content.find_all('p', limit=5):
                text = self.extract_text(p)
                if text and len(text) > 20:
                    parts.append(text)
            if parts:
                description = ' '.join(parts[:3])
        
        eligibility = []
        for ul in soup.find_all(['ul', 'ol']):
            prev = ul.find_previous(['h2', 'h3', 'h4', 'strong'])
            if prev:
                prev_text = self.extract_text(prev).lower()
                if any(word in prev_text for word in ['eligib', 'criteria', 'require', 'who can']):
                    for li in ul.find_all('li'):
                        text = self.extract_text(li)
                        if text and len(text) > 5:
                            eligibility.append(text)
        
        # NEF requires black ownership
        if not any('black' in e.lower() or 'bee' in e.lower() for e in eligibility):
            eligibility.insert(0, "Must be a black-owned business (minimum 50.1% black ownership)")
        
        funding_type = "loan"
        if 'grant' in url.lower() or 'grant' in (title or '').lower():
            funding_type = "grant"
        
        return RawOpportunity(
            title=title,
            funder_name="NEF",
            funder_type="government",
            funding_type=funding_type,
            description=description,
            industries=[],
            provinces=["National"],
            business_stage=None,
            eligibility=eligibility,
            funding_amount_min="R250,000",
            funding_amount_max="R75,000,000",
            deadline=None,
            is_rolling=True,
            required_documents=[],
            application_steps=[],
            apply_url="https://www.nefcorp.co.za/apply-for-funding/",
            source_url=url,
            raw_html=html
        )
