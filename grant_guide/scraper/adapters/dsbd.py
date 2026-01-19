"""
DSBD (Department of Small Business Development) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.dsbd')


class DSBDAdapter(BaseSourceAdapter):
    """Adapter for scraping DSBD programmes and funding opportunities."""
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """
        Yield URLs of individual opportunity pages from DSBD.
        """
        for scrape_url in self.config.scrape_urls:
            try:
                html = self.http.get(scrape_url)
                soup = self.parse_html(html)
                
                # Find programme cards/links
                content = soup.find('main') or soup.find('div', class_='content') or soup
                
                for link in content.find_all('a', href=True):
                    href = link['href']
                    
                    # Filter for programme pages
                    if any(keyword in href.lower() for keyword in 
                           ['programme', 'fund', 'support', 'grant', 'loan']):
                        yield self.make_absolute_url(href)
                        
            except Exception as e:
                logger.error(f"Error getting URLs from {scrape_url}: {e}")
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """
        Extract opportunity data from a DSBD programme page.
        """
        soup = self.parse_html(html)
        
        # Extract title
        title = None
        title_elem = soup.find('h1')
        if title_elem:
            title = self.extract_text(title_elem)
        
        # Extract description
        description = None
        content_area = soup.find('article') or soup.find('div', class_='content')
        if content_area:
            paragraphs = content_area.find_all('p', limit=3)
            description = ' '.join(self.extract_text(p) for p in paragraphs)
        
        # Extract eligibility
        eligibility = []
        for section in soup.find_all(['div', 'section']):
            heading = section.find(['h2', 'h3', 'h4'])
            if heading and 'eligib' in self.extract_text(heading).lower():
                for li in section.find_all('li'):
                    eligibility.append(self.extract_text(li))
        
        # Find apply link
        apply_url = None
        for link in soup.find_all('a', href=True):
            link_text = self.extract_text(link).lower()
            if 'apply' in link_text:
                apply_url = self.make_absolute_url(link['href'])
                break
        
        # DSBD focuses on SMEs
        business_stage = "sme"
        
        return RawOpportunity(
            title=title,
            funder_name="DSBD",
            funder_type="government",
            funding_type="grant",
            description=description,
            industries=[],
            provinces=["National"],
            business_stage=business_stage,
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
