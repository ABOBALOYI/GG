"""
Feed monitor for discovering and tracking RSS feeds and news pages.
"""
import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterator, Optional, Set
from urllib.parse import urljoin

import feedparser
from bs4 import BeautifulSoup

from .models import FeedItem
from .http_client import HttpClient

logger = logging.getLogger('scraper.feed')


@dataclass
class FeedCache:
    """Simple in-memory cache for tracking seen feed items."""
    seen_guids: dict[str, Set[str]] = field(default_factory=dict)
    
    def is_seen(self, source_id: str, guid: str) -> bool:
        """Check if a GUID has been seen for a source."""
        if source_id not in self.seen_guids:
            return False
        return guid in self.seen_guids[source_id]
    
    def mark_seen(self, source_id: str, guid: str) -> None:
        """Mark a GUID as seen for a source."""
        if source_id not in self.seen_guids:
            self.seen_guids[source_id] = set()
        self.seen_guids[source_id].add(guid)
    
    def clear(self, source_id: Optional[str] = None) -> None:
        """Clear cache for a source or all sources."""
        if source_id:
            self.seen_guids.pop(source_id, None)
        else:
            self.seen_guids.clear()


class FeedMonitor:
    """Monitors RSS feeds and news pages for new content."""
    
    # Common RSS feed URL patterns to try
    COMMON_FEED_PATTERNS = [
        '/feed/',
        '/feed',
        '/rss/',
        '/rss',
        '/rss.xml',
        '/feed.xml',
        '/atom.xml',
        '/news/feed/',
        '/blog/feed/',
        '/category/news/feed/',
    ]
    
    def __init__(self, http_client: HttpClient, cache: Optional[FeedCache] = None):
        """
        Initialize feed monitor.
        
        Args:
            http_client: HTTP client for making requests.
            cache: Feed cache for tracking seen items.
        """
        self.http = http_client
        self.cache = cache or FeedCache()
    
    def discover_feed(self, page_url: str) -> Optional[str]:
        """
        Attempt to discover RSS feed URL from a page.
        
        Searches for:
        1. <link rel="alternate" type="application/rss+xml"> tags
        2. <link rel="alternate" type="application/atom+xml"> tags
        3. Common RSS URL patterns
        
        Args:
            page_url: URL of the page to search.
            
        Returns:
            Feed URL if found, None otherwise.
        """
        try:
            html = self.http.get(page_url, check_robots=False)
            soup = BeautifulSoup(html, 'lxml')
            
            # Look for RSS link tags
            feed_link = soup.find('link', {
                'rel': 'alternate',
                'type': re.compile(r'application/(rss|atom)\+xml')
            })
            
            if feed_link and feed_link.get('href'):
                feed_url = feed_link['href']
                return urljoin(page_url, feed_url)
            
            # Try common patterns
            for pattern in self.COMMON_FEED_PATTERNS:
                feed_url = urljoin(page_url, pattern)
                if self._is_valid_feed(feed_url):
                    return feed_url
            
            return None
            
        except Exception as e:
            logger.warning(f"Error discovering feed for {page_url}: {e}")
            return None
    
    def _is_valid_feed(self, feed_url: str) -> bool:
        """Check if URL returns a valid RSS/Atom feed."""
        try:
            content = self.http.get(feed_url, check_robots=False)
            feed = feedparser.parse(content)
            return bool(feed.entries)
        except Exception:
            return False
    
    def parse_feed(self, feed_url: str) -> list[FeedItem]:
        """
        Parse RSS/Atom feed and extract items.
        
        Args:
            feed_url: URL of the feed to parse.
            
        Returns:
            List of FeedItem objects.
        """
        try:
            content = self.http.get(feed_url, check_robots=False)
            feed = feedparser.parse(content)
            
            items = []
            for entry in feed.entries:
                # Generate GUID from id or link
                guid = entry.get('id') or entry.get('link') or ''
                if not guid:
                    # Generate hash from title + link as fallback
                    guid = hashlib.md5(
                        f"{entry.get('title', '')}{entry.get('link', '')}".encode()
                    ).hexdigest()
                
                # Parse published date
                published_date = None
                if entry.get('published_parsed'):
                    try:
                        published_date = datetime(*entry.published_parsed[:6])
                    except (TypeError, ValueError):
                        pass
                
                items.append(FeedItem(
                    guid=guid,
                    title=entry.get('title', ''),
                    url=entry.get('link', ''),
                    published_date=published_date
                ))
            
            logger.info(f"Parsed {len(items)} items from {feed_url}")
            return items
            
        except Exception as e:
            logger.error(f"Error parsing feed {feed_url}: {e}")
            return []
    
    def get_new_items(self, source_id: str, feed_url: str) -> Iterator[FeedItem]:
        """
        Return only items not previously seen.
        
        Args:
            source_id: Unique identifier for the source.
            feed_url: URL of the feed to check.
            
        Yields:
            FeedItem objects that haven't been seen before.
        """
        items = self.parse_feed(feed_url)
        
        for item in items:
            if not self.cache.is_seen(source_id, item.guid):
                yield item
    
    def mark_seen(self, source_id: str, guid: str) -> None:
        """
        Mark an item as processed.
        
        Args:
            source_id: Unique identifier for the source.
            guid: GUID of the item to mark.
        """
        self.cache.mark_seen(source_id, guid)
    
    def get_all_items(self, source_id: str, feed_url: str) -> list[FeedItem]:
        """
        Get all items from feed (regardless of seen status).
        
        Args:
            source_id: Unique identifier for the source.
            feed_url: URL of the feed.
            
        Returns:
            List of all FeedItem objects.
        """
        return self.parse_feed(feed_url)
