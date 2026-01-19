"""
TIA (Technology Innovation Agency) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.tia')


class TIAAdapter(BaseSourceAdapter):
    """Adapter for scraping TIA open calls and funding opportunities."""
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """Yield URLs of open call pages from TIA."""
        for scrape_url in self.config.scrape_urls:
            try:
                html = self.http.get(scrape_url)
                soup = self.parse_html(html)
                
                # Find call links - TIA uses h2.title > a pattern
                for h2 in soup.find_all('h2', class_='title'):
                    link = h2.find('a', href=True)
                    if link:
                        href = link['href']
                        if 'call' in href.lower() or 'proposal' in href.lower():
                            yield self.make_absolute_url(href)
                            
            except Exception as e:
                logger.error(f"Error getting URLs from {scrape_url}: {e}")
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """Extract opportunity data from a TIA call page."""
        soup = self.parse_html(html)
        
        title = None
        h1 = soup.find('h1', class_='entry-title') or soup.find('h1')
        if h1:
            title = self.extract_text(h1)
        
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
        
        apply_url = None
        for link in soup.find_all('a', href=True):
            link_text = self.extract_text(link).lower()
            if any(word in link_text for word in ['apply', 'submit', 'application']):
                apply_url = self.make_absolute_url(link['href'])
                break
        
        return RawOpportunity(
            title=title,
            funder_name="TIA",
            funder_type="government",
            funding_type="grant",
            description=description,
            industries=["Technology", "Innovation"],
            provinces=["National"],
            business_stage=None,
            eligibility=eligibility,
            funding_amount_min=None,
            funding_amount_max=None,
            deadline=None,
            is_rolling=False,
            required_documents=[],
            application_steps=[],
            apply_url=apply_url,
            source_url=url,
            raw_html=html
        )
