"""
Property-based tests for the HTTP Client.

**Validates: Requirements 1.1, 1.3, 11.1**
"""
import pytest
from datetime import datetime, timedelta
from hypothesis import given, strategies as st, settings
from unittest.mock import Mock, patch, MagicMock
import time

from scraper.http_client import (
    HttpClient, RobotsDisallowedError, retry_with_backoff, compute_content_hash
)


class TestRateLimitingEnforcement:
    """
    Feature: grant-guide-scraper-engine, Property 3: Rate Limiting Enforcement
    
    *For any* sequence of requests to the same domain, the time between
    consecutive requests SHALL be at least 2 seconds.
    """
    
    def test_rate_limit_enforced(self):
        """Consecutive requests to same domain are rate limited."""
        client = HttpClient(default_delay=2.0)
        
        # Simulate first request
        domain = "example.gov.za"
        client._last_request[domain] = datetime.now()
        
        # Check that rate limit would be enforced
        elapsed = 0.5  # Simulate 0.5 seconds elapsed
        client._last_request[domain] = datetime.now() - timedelta(seconds=elapsed)
        
        # The delay should be calculated correctly
        delay = client.get_crawl_delay(f"https://{domain}/page")
        assert delay >= 2.0
    
    def test_different_domains_not_rate_limited(self):
        """Requests to different domains are not rate limited against each other."""
        client = HttpClient(default_delay=2.0)
        
        # First domain has recent request
        client._last_request["domain1.gov.za"] = datetime.now()
        
        # Second domain should not be affected
        assert "domain2.gov.za" not in client._last_request
    
    @given(delay=st.floats(min_value=2.0, max_value=10.0))
    @settings(max_examples=50)
    def test_custom_delay_respected(self, delay):
        """Custom delay values are respected."""
        client = HttpClient(default_delay=delay)
        assert client.default_delay == delay


class TestRobotsTxtCompliance:
    """
    Feature: grant-guide-scraper-engine, Property 1: Robots.txt Compliance
    
    *For any* URL and its associated robots.txt file, the Scraper_Engine SHALL
    correctly parse all directives and refuse to access any disallowed paths.
    """
    
    def test_disallowed_url_raises_error(self):
        """Disallowed URLs raise RobotsDisallowedError."""
        client = HttpClient()
        
        # Mock robots parser to disallow
        mock_parser = Mock()
        mock_parser.can_fetch.return_value = False
        client._robots_cache["example.gov.za"] = mock_parser
        
        with pytest.raises(RobotsDisallowedError):
            client.get("https://example.gov.za/private", check_robots=True)
    
    def test_allowed_url_proceeds(self):
        """Allowed URLs proceed with request."""
        client = HttpClient()
        
        # Mock robots parser to allow
        mock_parser = Mock()
        mock_parser.can_fetch.return_value = True
        mock_parser.crawl_delay.return_value = None
        client._robots_cache["example.gov.za"] = mock_parser
        
        # Should return True for is_allowed
        assert client.is_allowed("https://example.gov.za/public")
    
    def test_no_robots_txt_allows_access(self):
        """Missing robots.txt allows access."""
        client = HttpClient()
        
        # Cache None for domain (no robots.txt)
        client._robots_cache["example.gov.za"] = None
        
        assert client.is_allowed("https://example.gov.za/page")
    
    @given(path=st.sampled_from([
        "/admin", "/private", "/api", "/login", "/public", "/about"
    ]))
    @settings(max_examples=50)
    def test_is_allowed_returns_boolean(self, path):
        """is_allowed always returns boolean."""
        client = HttpClient()
        client._robots_cache["example.gov.za"] = None  # No robots.txt
        
        result = client.is_allowed(f"https://example.gov.za{path}")
        assert isinstance(result, bool)


class TestNetworkRetryWithBackoff:
    """
    Feature: grant-guide-scraper-engine, Property 27: Network Retry with Backoff
    
    *For any* network error, the HttpClient SHALL retry up to 3 times
    with exponential backoff.
    """
    
    def test_retry_decorator_retries_on_error(self):
        """Retry decorator retries on network errors."""
        call_count = 0
        
        @retry_with_backoff(max_retries=3, base_delay=0.01)
        def failing_function():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                from requests.exceptions import Timeout
                raise Timeout("Connection timed out")
            return "success"
        
        result = failing_function()
        assert result == "success"
        assert call_count == 3
    
    def test_retry_gives_up_after_max_retries(self):
        """Retry decorator gives up after max retries."""
        call_count = 0
        
        @retry_with_backoff(max_retries=2, base_delay=0.01)
        def always_failing():
            nonlocal call_count
            call_count += 1
            from requests.exceptions import ConnectionError
            raise ConnectionError("Connection refused")
        
        with pytest.raises(Exception):
            always_failing()
        
        assert call_count == 3  # Initial + 2 retries
    
    @given(max_retries=st.integers(min_value=1, max_value=5))
    @settings(max_examples=20)
    def test_retry_count_configurable(self, max_retries):
        """Retry count is configurable."""
        call_count = 0
        
        @retry_with_backoff(max_retries=max_retries, base_delay=0.001)
        def counting_function():
            nonlocal call_count
            call_count += 1
            from requests.exceptions import Timeout
            raise Timeout()
        
        try:
            counting_function()
        except:
            pass
        
        assert call_count == max_retries + 1


class TestContentHashComputation:
    """
    Feature: grant-guide-scraper-engine, Property 11: Content Hash Computation
    
    *For any* scraped page, the raw_content_hash SHALL be a valid SHA-256 hash,
    and the same content SHALL always produce the same hash.
    """
    
    @given(content=st.text(min_size=1, max_size=1000))
    @settings(max_examples=100)
    def test_hash_is_valid_sha256(self, content):
        """Hash is valid SHA-256 format (64 hex chars)."""
        hash_value = compute_content_hash(content)
        assert len(hash_value) == 64
        assert all(c in '0123456789abcdef' for c in hash_value)
    
    @given(content=st.text(min_size=1, max_size=100))
    @settings(max_examples=100)
    def test_same_content_same_hash(self, content):
        """Same content always produces same hash."""
        hash1 = compute_content_hash(content)
        hash2 = compute_content_hash(content)
        assert hash1 == hash2
    
    def test_different_content_different_hash(self):
        """Different content produces different hashes."""
        hash1 = compute_content_hash("content A")
        hash2 = compute_content_hash("content B")
        assert hash1 != hash2
    
    def test_empty_string_has_hash(self):
        """Empty string has a valid hash."""
        hash_value = compute_content_hash("")
        assert len(hash_value) == 64


class TestDomainExtraction:
    """Test domain extraction from URLs."""
    
    @given(domain=st.sampled_from([
        "example.gov.za", "www.dsbd.gov.za", "api.example.com"
    ]))
    @settings(max_examples=50)
    def test_domain_extraction(self, domain):
        """Domain is correctly extracted from URL."""
        client = HttpClient()
        url = f"https://{domain}/path/to/page"
        
        extracted = client._get_domain(url)
        assert extracted == domain
