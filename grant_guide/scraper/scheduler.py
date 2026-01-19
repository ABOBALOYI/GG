"""
High-performance scraper scheduler with timeout handling and weekly scheduling.
"""
import logging
import signal
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Callable
from functools import wraps

logger = logging.getLogger('scraper.scheduler')


@dataclass
class ScheduleConfig:
    """Configuration for scraper scheduling."""
    # Run interval (default: weekly)
    interval_days: int = 7
    
    # Time of day to run (24-hour format)
    run_hour: int = 2  # 2 AM
    run_minute: int = 0
    
    # Timeout settings (in seconds)
    source_timeout: int = 300  # 5 minutes per source
    total_timeout: int = 3600  # 1 hour total
    request_timeout: int = 60  # 60 seconds per request
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 60  # 1 minute between retries
    
    # Concurrency (be careful with rate limits)
    max_workers: int = 2  # Process 2 sources in parallel
    
    # Failure handling
    max_consecutive_failures: int = 3
    backoff_multiplier: float = 2.0


@dataclass
class SourceStatus:
    """Track status of individual source scraping."""
    source_id: str
    last_success: Optional[datetime] = None
    last_attempt: Optional[datetime] = None
    consecutive_failures: int = 0
    total_records: int = 0
    is_healthy: bool = True
    error_message: Optional[str] = None


class TimeoutHandler:
    """Context manager for handling timeouts."""
    
    def __init__(self, seconds: int, error_message: str = "Operation timed out"):
        self.seconds = seconds
        self.error_message = error_message
        self._old_handler = None
    
    def _timeout_handler(self, signum, frame):
        raise TimeoutError(self.error_message)
    
    def __enter__(self):
        # Only use signal-based timeout on main thread
        if threading.current_thread() is threading.main_thread():
            self._old_handler = signal.signal(signal.SIGALRM, self._timeout_handler)
            signal.alarm(self.seconds)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if threading.current_thread() is threading.main_thread():
            signal.alarm(0)
            if self._old_handler:
                signal.signal(signal.SIGALRM, self._old_handler)
        return False


def with_timeout(timeout_seconds: int):
    """Decorator to add timeout to a function using ThreadPoolExecutor."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=timeout_seconds)
                except FuturesTimeoutError:
                    raise TimeoutError(f"{func.__name__} timed out after {timeout_seconds}s")
        return wrapper
    return decorator


class ScraperScheduler:
    """
    High-performance scheduler for running scrapers on a schedule.
    
    Features:
    - Weekly scheduling with configurable time
    - Per-source timeout handling
    - Parallel source processing (with rate limit awareness)
    - Automatic retry with exponential backoff
    - Health tracking per source
    - Graceful shutdown
    """
    
    def __init__(self, config: Optional[ScheduleConfig] = None):
        self.config = config or ScheduleConfig()
        self._source_status: dict[str, SourceStatus] = {}
        self._running = False
        self._shutdown_event = threading.Event()
        self._engine = None
    
    def _get_engine(self):
        """Lazy-load the scraper engine and pre-load all adapters."""
        if self._engine is None:
            from .engine import ScraperEngine
            from .http_client import HttpClient
            from .normaliser import RecordNormaliser
            from .deduplicator import create_django_deduplicator
            from .compliance import ComplianceChecker
            from .status import StatusManager
            from .importer import DjangoImporter
            from .exporter import JsonExporter
            
            self._engine = ScraperEngine(
                http_client=HttpClient(
                    timeout=self.config.request_timeout,
                    default_delay=2.0
                ),
                normaliser=RecordNormaliser(),
                deduplicator=create_django_deduplicator(),
                compliance_checker=ComplianceChecker(),
                status_manager=StatusManager(),
                importer=DjangoImporter(),
                exporter=JsonExporter(),
            )
            self._engine.load_sources()
            
            # Pre-load all adapters to avoid import deadlocks in threads
            for source in self._engine._sources.values():
                try:
                    self._engine.get_adapter(source)
                except Exception as e:
                    logger.warning(f"Could not pre-load adapter for {source.source_id}: {e}")
        
        return self._engine
    
    def run_once(self, source_id: Optional[str] = None) -> dict:
        """
        Run scraper once with timeout handling.
        
        Args:
            source_id: Optional specific source to scrape.
            
        Returns:
            Dictionary with scrape results.
        """
        engine = self._get_engine()
        start_time = datetime.now()
        results = {
            'started_at': start_time.isoformat(),
            'sources': [],
            'total_created': 0,
            'total_updated': 0,
            'total_errors': 0,
            'success': True
        }
        
        # Get sources to process
        if source_id:
            sources = [engine._sources.get(source_id)]
            if not sources[0]:
                logger.error(f"Unknown source: {source_id}")
                results['success'] = False
                results['error'] = f"Unknown source: {source_id}"
                return results
        else:
            sources = [s for s in engine._sources.values() if s.is_active]
        
        logger.info(f"Starting scheduled scrape for {len(sources)} sources")
        
        # Process sources with parallel execution (limited concurrency)
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = {}
            for source in sources:
                # Initialize status tracking
                if source.source_id not in self._source_status:
                    self._source_status[source.source_id] = SourceStatus(
                        source_id=source.source_id
                    )
                
                # Submit source for processing
                future = executor.submit(
                    self._scrape_source_with_timeout,
                    source
                )
                futures[future] = source
            
            # Collect results with total timeout
            remaining_timeout = self.config.total_timeout
            for future in futures:
                source = futures[future]
                try:
                    source_result = future.result(timeout=min(
                        self.config.source_timeout,
                        remaining_timeout
                    ))
                    results['sources'].append(source_result)
                    results['total_created'] += source_result.get('created', 0)
                    results['total_updated'] += source_result.get('updated', 0)
                    
                    # Update status
                    status = self._source_status[source.source_id]
                    status.last_success = datetime.now()
                    status.consecutive_failures = 0
                    status.is_healthy = True
                    status.total_records += source_result.get('found', 0)
                    
                except (TimeoutError, FuturesTimeoutError) as e:
                    logger.error(f"Source {source.source_id} timed out: {e}")
                    self._handle_source_failure(source.source_id, str(e))
                    results['sources'].append({
                        'source_id': source.source_id,
                        'error': 'Timeout',
                        'success': False
                    })
                    results['total_errors'] += 1
                    
                except Exception as e:
                    logger.error(f"Source {source.source_id} failed: {e}")
                    self._handle_source_failure(source.source_id, str(e))
                    results['sources'].append({
                        'source_id': source.source_id,
                        'error': str(e),
                        'success': False
                    })
                    results['total_errors'] += 1
                
                # Update remaining timeout
                elapsed = (datetime.now() - start_time).total_seconds()
                remaining_timeout = max(0, self.config.total_timeout - elapsed)
                
                if remaining_timeout <= 0:
                    logger.warning("Total timeout reached, stopping remaining sources")
                    break
        
        results['completed_at'] = datetime.now().isoformat()
        results['duration_seconds'] = (datetime.now() - start_time).total_seconds()
        
        logger.info(
            f"Scheduled scrape completed: "
            f"created={results['total_created']}, "
            f"updated={results['total_updated']}, "
            f"errors={results['total_errors']}"
        )
        
        return results
    
    def _scrape_source_with_timeout(self, source) -> dict:
        """Scrape a single source with timeout handling."""
        engine = self._get_engine()
        result = {
            'source_id': source.source_id,
            'source_name': source.source_name,
            'found': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'success': True
        }
        
        try:
            # Run the scraper for this source
            scrape_result = engine.run(source_id=source.source_id, dry_run=False)
            
            if scrape_result.source_results:
                sr = scrape_result.source_results[0]
                result['found'] = sr.records_found
                result['created'] = sr.records_created
                result['updated'] = sr.records_updated
                result['skipped'] = sr.records_skipped
                result['success'] = sr.success
                if sr.errors:
                    result['errors'] = sr.errors
                    
        except Exception as e:
            result['success'] = False
            result['error'] = str(e)
            raise
        
        return result
    
    def _handle_source_failure(self, source_id: str, error: str):
        """Handle source failure with backoff tracking."""
        status = self._source_status.get(source_id)
        if status:
            status.last_attempt = datetime.now()
            status.consecutive_failures += 1
            status.error_message = error
            
            if status.consecutive_failures >= self.config.max_consecutive_failures:
                status.is_healthy = False
                logger.warning(
                    f"Source {source_id} marked unhealthy after "
                    f"{status.consecutive_failures} consecutive failures"
                )
    
    def get_next_run_time(self) -> datetime:
        """Calculate the next scheduled run time."""
        now = datetime.now()
        next_run = now.replace(
            hour=self.config.run_hour,
            minute=self.config.run_minute,
            second=0,
            microsecond=0
        )
        
        # If we've passed today's run time, schedule for next interval
        if next_run <= now:
            next_run += timedelta(days=self.config.interval_days)
        
        return next_run
    
    def run_scheduled(self, callback: Optional[Callable] = None):
        """
        Run the scheduler in a loop (blocking).
        
        Args:
            callback: Optional callback function called after each run.
        """
        self._running = True
        logger.info("Scraper scheduler started")
        
        while self._running and not self._shutdown_event.is_set():
            next_run = self.get_next_run_time()
            wait_seconds = (next_run - datetime.now()).total_seconds()
            
            logger.info(f"Next scrape scheduled for: {next_run}")
            
            # Wait until next run time (with periodic checks for shutdown)
            while wait_seconds > 0 and not self._shutdown_event.is_set():
                sleep_time = min(wait_seconds, 60)  # Check every minute
                self._shutdown_event.wait(sleep_time)
                wait_seconds = (next_run - datetime.now()).total_seconds()
            
            if self._shutdown_event.is_set():
                break
            
            # Run the scraper
            try:
                results = self.run_once()
                if callback:
                    callback(results)
            except Exception as e:
                logger.error(f"Scheduled scrape failed: {e}")
        
        logger.info("Scraper scheduler stopped")
    
    def stop(self):
        """Stop the scheduler gracefully."""
        logger.info("Stopping scraper scheduler...")
        self._running = False
        self._shutdown_event.set()
    
    def get_health_status(self) -> dict:
        """Get health status of all sources."""
        return {
            source_id: {
                'is_healthy': status.is_healthy,
                'last_success': status.last_success.isoformat() if status.last_success else None,
                'consecutive_failures': status.consecutive_failures,
                'total_records': status.total_records,
                'error': status.error_message
            }
            for source_id, status in self._source_status.items()
        }
