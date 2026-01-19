"""
Django management command for running the high-performance scheduled scraper.
"""
import logging
import signal
import sys
from datetime import datetime

from django.core.management.base import BaseCommand

from scraper.scheduler import ScraperScheduler, ScheduleConfig


class Command(BaseCommand):
    help = 'Run the high-performance scheduled scraper with timeout handling'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = None
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--once',
            action='store_true',
            help='Run scraper once and exit (no scheduling).'
        )
        parser.add_argument(
            '--source',
            type=str,
            help='Specific source ID to scrape.'
        )
        parser.add_argument(
            '--interval-days',
            type=int,
            default=7,
            help='Days between scrape runs (default: 7 for weekly).'
        )
        parser.add_argument(
            '--run-hour',
            type=int,
            default=2,
            help='Hour of day to run (0-23, default: 2 for 2 AM).'
        )
        parser.add_argument(
            '--source-timeout',
            type=int,
            default=300,
            help='Timeout per source in seconds (default: 300 = 5 minutes).'
        )
        parser.add_argument(
            '--total-timeout',
            type=int,
            default=3600,
            help='Total timeout for all sources in seconds (default: 3600 = 1 hour).'
        )
        parser.add_argument(
            '--request-timeout',
            type=int,
            default=60,
            help='Timeout per HTTP request in seconds (default: 60).'
        )
        parser.add_argument(
            '--max-workers',
            type=int,
            default=2,
            help='Max parallel source scrapers (default: 2).'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose logging.'
        )
        parser.add_argument(
            '--health-check',
            action='store_true',
            help='Show health status of all sources and exit.'
        )
    
    def handle(self, *args, **options):
        # Configure logging
        log_level = logging.DEBUG if options['verbose'] else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
            ]
        )
        
        # Create scheduler config
        config = ScheduleConfig(
            interval_days=options['interval_days'],
            run_hour=options['run_hour'],
            source_timeout=options['source_timeout'],
            total_timeout=options['total_timeout'],
            request_timeout=options['request_timeout'],
            max_workers=options['max_workers'],
        )
        
        self.scheduler = ScraperScheduler(config)
        
        # Handle health check
        if options['health_check']:
            self._show_health_status()
            return
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        if options['once']:
            # Run once and exit
            self._run_once(options.get('source'))
        else:
            # Run scheduled
            self._run_scheduled()
    
    def _run_once(self, source_id=None):
        """Run scraper once with full output."""
        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(self.style.NOTICE('HIGH-PERFORMANCE SCRAPER - SINGLE RUN'))
        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(f'Started at: {datetime.now().isoformat()}')
        self.stdout.write(f'Source timeout: {self.scheduler.config.source_timeout}s')
        self.stdout.write(f'Total timeout: {self.scheduler.config.total_timeout}s')
        self.stdout.write(f'Request timeout: {self.scheduler.config.request_timeout}s')
        self.stdout.write(f'Max workers: {self.scheduler.config.max_workers}')
        self.stdout.write('')
        
        results = self.scheduler.run_once(source_id=source_id)
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('SCRAPE COMPLETED'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'Duration: {results.get("duration_seconds", 0):.1f} seconds')
        self.stdout.write(f'Sources processed: {len(results.get("sources", []))}')
        self.stdout.write(self.style.SUCCESS(f'Records created: {results.get("total_created", 0)}'))
        self.stdout.write(self.style.SUCCESS(f'Records updated: {results.get("total_updated", 0)}'))
        
        if results.get('total_errors', 0) > 0:
            self.stdout.write(self.style.ERROR(f'Errors: {results.get("total_errors", 0)}'))
        
        # Show per-source results
        self.stdout.write('')
        self.stdout.write('Source Results:')
        for source in results.get('sources', []):
            if source.get('success'):
                self.stdout.write(
                    f'  ✓ {source.get("source_id")}: '
                    f'found={source.get("found", 0)}, '
                    f'created={source.get("created", 0)}, '
                    f'updated={source.get("updated", 0)}'
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'  ✗ {source.get("source_id")}: {source.get("error", "Unknown error")}'
                    )
                )
        
        # Show health status
        self.stdout.write('')
        self._show_health_status()
    
    def _run_scheduled(self):
        """Run scheduler in continuous mode."""
        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(self.style.NOTICE('HIGH-PERFORMANCE SCRAPER - SCHEDULED MODE'))
        self.stdout.write(self.style.NOTICE('=' * 60))
        self.stdout.write(f'Interval: Every {self.scheduler.config.interval_days} days')
        self.stdout.write(f'Run time: {self.scheduler.config.run_hour:02d}:{self.scheduler.config.run_minute:02d}')
        self.stdout.write(f'Next run: {self.scheduler.get_next_run_time().isoformat()}')
        self.stdout.write('')
        self.stdout.write('Press Ctrl+C to stop...')
        self.stdout.write('')
        
        def on_complete(results):
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS(
                f'Scheduled run completed: '
                f'created={results.get("total_created", 0)}, '
                f'updated={results.get("total_updated", 0)}, '
                f'errors={results.get("total_errors", 0)}'
            ))
            self.stdout.write(f'Next run: {self.scheduler.get_next_run_time().isoformat()}')
        
        self.scheduler.run_scheduled(callback=on_complete)
    
    def _show_health_status(self):
        """Display health status of all sources."""
        health = self.scheduler.get_health_status()
        
        if not health:
            self.stdout.write('No source health data available yet.')
            return
        
        self.stdout.write('Source Health Status:')
        for source_id, status in health.items():
            if status['is_healthy']:
                icon = self.style.SUCCESS('✓')
            else:
                icon = self.style.ERROR('✗')
            
            last_success = status.get('last_success', 'Never')
            failures = status.get('consecutive_failures', 0)
            records = status.get('total_records', 0)
            
            self.stdout.write(
                f'  {icon} {source_id}: '
                f'last_success={last_success}, '
                f'failures={failures}, '
                f'total_records={records}'
            )
            
            if status.get('error'):
                self.stdout.write(
                    self.style.WARNING(f'      Error: {status["error"]}')
                )
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Received shutdown signal, stopping...'))
        if self.scheduler:
            self.scheduler.stop()
