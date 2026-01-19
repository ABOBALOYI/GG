"""
DTIC (Department of Trade, Industry and Competition) adapter.
"""
import logging
from typing import Iterator

from .base import BaseSourceAdapter
from ..models import RawOpportunity

logger = logging.getLogger('scraper.adapter.dtic')


class DTICAdapter(BaseSourceAdapter):
    """Adapter for scraping DTIC incentives and programmes."""
    
    def get_opportunity_urls(self) -> Iterator[str]:
        """
        Yield URLs of individual opportunity pages from DTIC.
        
        Scrapes the incentives listing page and extracts links to
        individual programme pages.
        """
        for scrape_url in self.config.scrape_urls:
            try:
                html = self.http.get(scrape_url)
                soup = self.parse_html(html)
                
                # Find programme links - DTIC uses various structures
                # Look for links in content area
                content_area = soup.find('div', class_='content') or soup.find('main') or soup
                
                # Find all links that look like programme pages
                for link in content_area.find_all('a', href=True):
                    href = link['href']
                    
                    # Filter for programme/incentive pages
                    if any(keyword in href.lower() for keyword in 
                           ['incentive', 'programme', 'scheme', 'fund', 'grant']):
                        yield self.make_absolute_url(href)
                        
            except Exception as e:
                logger.error(f"Error getting URLs from {scrape_url}: {e}")
    
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """
        Extract opportunity data from a DTIC programme page.
        
        Args:
            url: URL of the page.
            html: HTML content of the page.
            
        Returns:
            RawOpportunity with extracted data.
        """
        soup = self.parse_html(html)
        
        # Extract title
        title = None
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            title = self.extract_text(title_elem)
            # Clean up title
            title = title.replace(' | the dtic', '').replace(' - the dtic', '').strip()
        
        # Extract description
        description = None
        desc_elem = (
            soup.find('div', class_='field-body') or
            soup.find('div', class_='content') or
            soup.find('article')
        )
        if desc_elem:
            # Get first few paragraphs
            paragraphs = desc_elem.find_all('p', limit=3)
            description = ' '.join(self.extract_text(p) for p in paragraphs)
        
        # Extract eligibility from lists
        eligibility = []
        for ul in soup.find_all('ul'):
            # Check if this looks like eligibility criteria
            prev_elem = ul.find_previous(['h2', 'h3', 'h4', 'strong'])
            if prev_elem and any(word in self.extract_text(prev_elem).lower() 
                                 for word in ['eligib', 'criteria', 'require', 'who can']):
                for li in ul.find_all('li'):
                    eligibility.append(self.extract_text(li))
        
        # Extract application steps
        application_steps = []
        for ol in soup.find_all('ol'):
            prev_elem = ol.find_previous(['h2', 'h3', 'h4', 'strong'])
            if prev_elem and any(word in self.extract_text(prev_elem).lower()
                                 for word in ['apply', 'process', 'step', 'how to']):
                for li in ol.find_all('li'):
                    application_steps.append(self.extract_text(li))
        
        # Find apply link
        apply_url = None
        for link in soup.find_all('a', href=True):
            link_text = self.extract_text(link).lower()
            if any(word in link_text for word in ['apply', 'application', 'register']):
                apply_url = self.make_absolute_url(link['href'])
                break
        
        # Determine record type
        deadline = None  # DTIC programmes are typically rolling
        is_rolling = True
        
        return RawOpportunity(
            title=title,
            funder_name="the dtic",
            funder_type="government",
            funding_type="grant",  # Most DTIC programmes are grants/incentives
            description=description,
            industries=[],  # Would need more specific parsing
            provinces=["National"],  # DTIC is national
            business_stage=None,
            eligibility=eligibility,
            funding_amount_min=None,
            funding_amount_max=None,
            deadline=deadline,
            is_rolling=is_rolling,
            required_documents=[],
            application_steps=application_steps,
            apply_url=apply_url,
            source_url=url,
            raw_html=html
        )
