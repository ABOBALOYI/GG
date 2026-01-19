"""
SAB Foundation adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.sab')


class SABFoundationAdapter(BaseSourceAdapter):
    """Adapter for scraping SAB Foundation programmes."""
    
    PROGRAMMES = [
        "/tholoana-enterprise-programme/",
        "/social-innovation-awards/",
    ]
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URLs of SAB Foundation programme pages."""
        base = self.config.base_url.rstrip('/')
        for path in self.PROGRAMMES:
            yield f"{base}{path}"
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Extract opportunity data from a SAB Foundation page."""
        soup = self.parse_html(html)
        
        title = None
        h1 = soup.find('h1')
        if h1:
            title = self.extract_text(h1)
        if not title:
            title_tag = soup.find('title')
            if title_tag:
                title = self.extract_text(title_tag).split('|')[0].strip()
        
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
        
        return RawOpportunity(
            title=title,
            funder_name="SAB Foundation",
            funder_type="corporate",
            funding_type="grant",
            description=description,
            industries=[],
            provinces=["National"],
            business_stage="startup",
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
