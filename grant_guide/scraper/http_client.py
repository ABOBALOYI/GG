"""
HTTP client with rate limiting, robots.txt compliance, and retry logic.
"""
import hashlib
import logging
import time
from datetime import datetime
from functools import wraps
from typing import Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

logger = logging.getLogger('scraper.http')

# Default user agent
DEFAULT_USER_AGENT = "GrantGuideSA-Scraper/1.0 (+https://grantsguide.co.za/about)"


class HttpClientError(Exception):
    """Base exception for HTTP client errors."""
    pass


class AccessDeniedError(HttpClientError):
    """Raised when access is denied (login, paywall, CAPTCHA)."""
    pass


class RobotsDisallowedError(HttpClientError):
    """Raised when robots.txt disallows access."""
    pass


def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
    """
    Decorator for retrying requests with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts.
        base_delay: Base delay in seconds (doubles each retry).
        max_delay: Maximum delay between retries.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (Timeout, ConnectionError, RequestException) as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        logger.warning(
                            f"Request failed (attempt {attempt + 1}/{max_retries + 1}), "
                            f"retrying in {delay}s: {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"Request failed after {max_retries + 1} attempts: {e}")
            raise last_exception
        return wrapper
    return decorator


class HttpClient:
    """HTTP client with rate limiting and robots.txt compliance."""
    
    def __init__(
        self,
        user_agent: str = DEFAULT_USER_AGENT,
        default_delay: float = 2.0,
        timeout: int = 30
    ):
        """
        Initialize HTTP client.
        
        Args:
            user_agent: User agent string for requests.
            default_delay: Default delay between requests to same domain (seconds).
            timeout: Request timeout in seconds.
        """
        self.user_agent = user_agent
        self.default_delay = default_delay
        self.timeout = timeout
        self._robots_cache: dict[str, RobotFileParser] = {}
        self._last_request: dict[str, datetime] = {}
        self._session = requests.Session()
        self._session.headers.update({'User-Agent': user_agent})
    
    def get(self, url: str, check_robots: bool = True) -> str:
        """
        Fetch URL with rate limiting and robots.txt compliance.
        
        Args:
            url: URL to fetch.
            check_robots: Whether to check robots.txt (default True).
            
        Returns:
            HTML content as string.
            
        Raises:
            RobotsDisallowedError: If robots.txt disallows access.
            HttpClientError: For other HTTP errors.
        """
        # Check robots.txt
        if check_robots and not self.is_allowed(url):
            raise RobotsDisallowedError(f"Access disallowed by robots.txt: {url}")
        
        # Enforce rate limiting
        domain = self._get_domain(url)
        self._enforce_rate_limit(domain, url)
        
        # Make request with retry
        return self._make_request(url)
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def _make_request(self, url: str) -> str:
        """Make HTTP request with retry logic."""
        logger.debug(f"Fetching: {url}")
        
        response = self._session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        # Update last request time
        domain = self._get_domain(url)
        self._last_request[domain] = datetime.now()
        
        logger.info(f"Fetched {url} ({len(response.text)} bytes)")
        return response.text
    
    def is_allowed(self, url: str) -> bool:
        """
        Check if URL is allowed by robots.txt.
        
        Args:
            url: URL to check.
            
        Returns:
            True if allowed, False if disallowed.
        """
        domain = self._get_domain(url)
        robots = self._get_robots_parser(domain)
        
        if robots is None:
            # No robots.txt found, assume allowed
            return True
        
        return robots.can_fetch(self.user_agent, url)
    
    def get_crawl_delay(self, url: str) -> float:
        """
        Get crawl delay from robots.txt or use default.
        
        Args:
            url: URL to get delay for.
            
        Returns:
            Crawl delay in seconds.
        """
        domain = self._get_domain(url)
        robots = self._get_robots_parser(domain)
        
        if robots is not None:
            delay = robots.crawl_delay(self.user_agent)
            if delay is not None:
                return max(delay, self.default_delay)
        
        return self.default_delay
    
    def _get_robots_parser(self, domain: str) -> Optional[RobotFileParser]:
        """Get or fetch robots.txt parser for domain."""
        if domain in self._robots_cache:
            return self._robots_cache[domain]
        
        robots_url = f"https://{domain}/robots.txt"
        parser = RobotFileParser()
        parser.set_url(robots_url)
        
        try:
            parser.read()
            self._robots_cache[domain] = parser
            logger.debug(f"Loaded robots.txt for {domain}")
            return parser
        except Exception as e:
            logger.debug(f"Could not load robots.txt for {domain}: {e}")
            self._robots_cache[domain] = None
            return None
    
    def _enforce_rate_limit(self, domain: str, url: str) -> None:
        """Wait if necessary to respect rate limits."""
        if domain not in self._last_request:
            return
        
        delay = self.get_crawl_delay(url)
        elapsed = (datetime.now() - self._last_request[domain]).total_seconds()
        
        if elapsed < delay:
            wait_time = delay - elapsed
            logger.debug(f"Rate limiting: waiting {wait_time:.2f}s for {domain}")
            time.sleep(wait_time)
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        parsed = urlparse(url)
        return parsed.netloc
    
    def close(self):
        """Close the HTTP session."""
        self._session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def compute_content_hash(content: str) -> str:
    """
    Compute SHA-256 hash of content for change detection.
    
    Args:
        content: Content to hash.
        
    Returns:
        Hex-encoded SHA-256 hash.
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
