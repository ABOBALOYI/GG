"""
Django management command for running the scraper.
"""
import logging
import sys

from django.core.management.base import BaseCommand, CommandError

from scraper.engine import ScraperEngine
from scraper.http_client import HttpClient
from scraper.normaliser import RecordNormaliser
from scraper.deduplicator import create_django_deduplicator
from scraper.compliance import ComplianceChecker
from scraper.status import StatusManager
from scraper.importer import DjangoImporter
from scraper.exporter import JsonExporter


class Command(BaseCommand):
    help = 'Scrape funding opportunities from approved sources'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            help='Source ID to scrape (e.g., "dtic", "dsbd"). If not specified, scrapes all active sources.'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run scraper without importing to database. Outputs JSON to stdout or file.'
        )
        parser.add_argument(
            '--output',
            type=str,
            help='Output file path for JSON (used with --dry-run). If not specified, outputs to stdout.'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose logging output.'
        )
        parser.add_argument(
            '--list-sources',
            action='store_true',
            help='List all configured sources and exit.'
        )
    
    def handle(self, *args, **options):
        # Configure logging
        log_level = logging.DEBUG if options['verbose'] else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
        )
        
        # Create engine with all components
        engine = ScraperEngine(
            http_client=HttpClient(),
            normaliser=RecordNormaliser(),
            deduplicator=create_django_deduplicator(),
            compliance_checker=ComplianceChecker(),
            status_manager=StatusManager(),
            importer=DjangoImporter(),
            exporter=JsonExporter(),
        )
        
        # Load sources
        engine.load_sources()
        
        # Handle --list-sources
        if options['list_sources']:
            self._list_sources(engine)
            return
        
        source_id = options.get('source')
        dry_run = options.get('dry_run', False)
        output_path = options.get('output')
        
        if dry_run:
            # Dry run - output JSON
            self.stdout.write(self.style.NOTICE('Running in dry-run mode (no database import)'))
            
            json_output = engine.scrape_to_json(
                source_id=source_id,
                output_path=output_path
            )
            
            if not output_path:
                # Output to stdout
                self.stdout.write(json_output)
            else:
                self.stdout.write(self.style.SUCCESS(f'JSON output written to: {output_path}'))
        else:
            # Normal run - import to database
            result = engine.run(source_id=source_id, dry_run=False)
            
            # Output summary
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(self.style.SUCCESS('SCRAPE COMPLETED'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(f'Sources processed: {result.sources_processed}')
            self.stdout.write(f'Sources failed: {result.sources_failed}')
            self.stdout.write(f'Records found: {result.total_records_found}')
            self.stdout.write(self.style.SUCCESS(f'Records created: {result.total_records_created}'))
            self.stdout.write(self.style.SUCCESS(f'Records updated: {result.total_records_updated}'))
            self.stdout.write(f'Records skipped: {result.total_records_skipped}')
            self.stdout.write(f'Records rejected: {result.total_records_rejected}')
            
            if result.sources_failed > 0:
                self.stdout.write('')
                self.stdout.write(self.style.WARNING('Failed sources:'))
                for sr in result.source_results:
                    if not sr.success:
                        self.stdout.write(f'  - {sr.source_name}: {", ".join(sr.errors)}')
    
    def _list_sources(self, engine):
        """List all configured sources."""
        self.stdout.write(self.style.SUCCESS('Configured Sources:'))
        self.stdout.write('')
        
        for source_id, source in engine._sources.items():
            status = self.style.SUCCESS('ACTIVE') if source.is_active else self.style.WARNING('INACTIVE')
            attention = self.style.ERROR(' [NEEDS ATTENTION]') if source.needs_attention else ''
            
            self.stdout.write(f'  {source_id}:')
            self.stdout.write(f'    Name: {source.source_name}')
            self.stdout.write(f'    Type: {source.source_type.value}')
            self.stdout.write(f'    Status: {status}{attention}')
            self.stdout.write(f'    URLs: {", ".join(source.scrape_urls)}')
            self.stdout.write('')
