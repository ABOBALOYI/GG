"""
Base adapter class for source-specific scrapers.
"""
from abc import ABC, abstractmethod
from typing import Iterator, Optional

from bs4 import BeautifulSoup

from ..models import SourceConfig, RawOpportunity, RecordType
from ..http_client import HttpClient


class BaseSourceAdapter(ABC):
    """Abstract base class for source-specific adapters."""
    
    def __init__(self, config: SourceConfig, http_client: HttpClient):
        """
        Initialize adapter.
        
        Args:
            config: Source configuration.
            http_client: HTTP client for making requests.
        """
        self.config = config
        self.http = http_client
    
    @abstractmethod
    def get_opportunity_urls(self) -> Iterator[str]:
        """
        Yield URLs of individual opportunity pages to scrape.
        
        Returns:
            Iterator of opportunity page URLs.
        """
        pass
    
    @abstractmethod
    def extract_opportunity(self, url: str, html: str) -> RawOpportunity:
        """
        Extract opportunity data from a page.
        
        Args:
            url: URL of the page.
            html: HTML content of the page.
            
        Returns:
            RawOpportunity with extracted data.
        """
        pass
    
    def scrape(self) -> Iterator[RawOpportunity]:
        """
        Main scraping method - iterates through opportunities.
        
        Yields:
            RawOpportunity for each scraped page.
        """
        for url in self.get_opportunity_urls():
            try:
                html = self.http.get(url)
                yield self.extract_opportunity(url, html)
            except Exception as e:
                # Log error but continue with next URL
                import logging
                logging.getLogger('scraper.adapter').error(
                    f"Error scraping {url}: {e}"
                )
    
    def classify_record_type(
        self,
        deadline: Optional[str],
        is_rolling: bool
    ) -> RecordType:
        """
        Classify record as FundingOpportunity or FundingProduct.
        
        Args:
            deadline: Deadline string (if any).
            is_rolling: Whether opportunity is rolling/always open.
            
        Returns:
            RecordType.FUNDING_OPPORTUNITY if deadline exists,
            RecordType.FUNDING_PRODUCT if rolling/no deadline.
        """
        if deadline and not is_rolling:
            return RecordType.FUNDING_OPPORTUNITY
        return RecordType.FUNDING_PRODUCT
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content into BeautifulSoup object.
        
        Args:
            html: HTML content string.
            
        Returns:
            BeautifulSoup object for parsing.
        """
        return BeautifulSoup(html, 'lxml')
    
    def extract_text(self, element, default: str = "") -> str:
        """
        Safely extract text from a BeautifulSoup element.
        
        Args:
            element: BeautifulSoup element or None.
            default: Default value if element is None.
            
        Returns:
            Extracted text or default.
        """
        if element is None:
            return default
        return element.get_text(strip=True)
    
    def extract_href(self, element, default: str = "") -> str:
        """
        Safely extract href from a BeautifulSoup element.
        
        Args:
            element: BeautifulSoup element or None.
            default: Default value if element is None.
            
        Returns:
            Extracted href or default.
        """
        if element is None:
            return default
        return element.get('href', default)
    
    def make_absolute_url(self, url: str) -> str:
        """
        Convert relative URL to absolute using base URL.
        
        Args:
            url: URL (may be relative).
            
        Returns:
            Absolute URL.
        """
        if url.startswith('http'):
            return url
        if url.startswith('/'):
            return f"{self.config.base_url}{url}"
        return f"{self.config.base_url}/{url}"
