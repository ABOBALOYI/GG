"""
NYDA (National Youth Development Agency) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.nyda')


class NYDAAdapter(BaseSourceAdapter):
    """Adapter for scraping NYDA grant programmes."""
    
    PROGRAMME_PAGES = [
        "/Products-Services/NYDA-Grant-Programme.html",
        "/Products-Services/NYDA-Voucher-Programme.html",
        "/Products-Services/Solomon-Kalushi-Mahlangu-Scholarship-Fund.html",
        "/Products-Services/Sponsorships-Thusano-Fund.html",
        "/Products-Services/Education-and-Skills.html",
        "/Products-Services/Business-Management-Training.html",
        "/Products-Services/Market-Linkages.html",
    ]
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URLs of individual opportunity pages from NYDA."""
        base = self.config.base_url.rstrip('/')
        for path in self.PROGRAMME_PAGES:
            yield f"{base}{path}"
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Extract opportunity data from an NYDA programme page."""
        soup = self.parse_html(html)
        
        title = None
        title_tag = soup.find('title')
        if title_tag:
            title = self.extract_text(title_tag).strip()
        
        if not title or title.lower() in ['welcome', 'nyda', '']:
            h1 = soup.find('h1')
            if h1:
                title = self.extract_text(h1)
        
        description = None
        for tag, attrs in [('div', {'class': 'description'}), ('div', {'class': 'Normal'})]:
            content = soup.find(tag, attrs)
            if content:
                parts = []
                for p in content.find_all('p', limit=3):
                    text = self.extract_text(p)
                    if text and len(text) > 20:
                        parts.append(text)
                if parts:
                    description = ' '.join(parts)
                    break

        eligibility = []
        for ul in soup.find_all(['ul', 'ol']):
            prev = ul.find_previous(['h2', 'h3', 'h4', 'strong', 'b'])
            if prev:
                prev_text = self.extract_text(prev).lower()
                if any(word in prev_text for word in ['eligib', 'criteria', 'require']):
                    for li in ul.find_all('li'):
                        text = self.extract_text(li)
                        if text and len(text) > 5:
                            eligibility.append(text)
        
        if not any('18' in e or '35' in e for e in eligibility):
            eligibility.insert(0, "Must be a South African citizen between 18-35 years old")
        
        apply_url = None
        for link in soup.find_all('a', href=True):
            href = link['href'].lower()
            if any(skip in href for skip in ['login', 'register', 'returnurl']):
                continue
            link_text = self.extract_text(link).lower()
            if any(word in link_text for word in ['apply', 'application']):
                apply_url = self.make_absolute_url(link['href'])
                break
        
        return RawOpportunity(
            title=title,
            funder_name="NYDA",
            funder_type="government",
            funding_type="grant",
            description=description,
            industries=[],
            provinces=["National"],
            business_stage="startup",
            eligibility=eligibility,
            funding_amount_min=None,
            funding_amount_max=None,
            deadline=None,
            is_rolling=True,
            required_documents=[],
            application_steps=[],
            apply_url=apply_url,
            source_url=url,
            raw_html=html
        )
