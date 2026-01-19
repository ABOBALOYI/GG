"""
IDC (Industrial Development Corporation) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.idc')


class IDCAdapter(BaseSourceAdapter):
    """Adapter for scraping IDC funding products."""
    
    FUNDING_PAGES = [
        "/what-we-offer-2/",
        "/crisis-funding/",
        "/energy-funding/",
    ]
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URLs of IDC funding product pages."""
        base = self.config.base_url.rstrip('/')
        for path in self.FUNDING_PAGES:
            yield f"{base}{path}"
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Extract opportunity data from an IDC funding page."""
        soup = self.parse_html(html)
        
        title = None
        h1 = soup.find('h1')
        if h1:
            title = self.extract_text(h1)
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = self.extract_text(title_tag).replace(' - IDC', '').strip()
        
        description = None
        content = soup.find('div', class_='entry-content') or soup.find('article') or soup.find('main')
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
                if any(word in prev_text for word in ['eligib', 'criteria', 'require']):
                    for li in ul.find_all('li'):
                        text = self.extract_text(li)
                        if text and len(text) > 5:
                            eligibility.append(text)
        
        apply_url = "https://www.idc.co.za/apply-for-funding/"
        
        return RawOpportunity(
            title=title,
            funder_name="IDC",
            funder_type="government",
            funding_type="loan",
            description=description,
            industries=[],
            provinces=["National"],
            business_stage=None,
            eligibility=eligibility,
            funding_amount_min="R1,000,000",
            funding_amount_max=None,
            deadline=None,
            is_rolling=True,
            required_documents=[],
            application_steps=[],
            apply_url=apply_url,
            source_url=url,
            raw_html=html
        )
