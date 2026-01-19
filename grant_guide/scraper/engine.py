"""
Scraper Engine - orchestrates the scraping pipeline.
"""
import importlib
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterator, Optional

from .models import (
    SourceConfig, RawOpportunity, NormalisedOpportunity,
    ComplianceResult, DeduplicationResult, ImportResult
)
from .config import load_sources
from .http_client import HttpClient
from .normaliser import RecordNormaliser
from .deduplicator import Deduplicator
from .compliance import ComplianceChecker
from .status import StatusManager
from .importer import DjangoImporter
from .exporter import JsonExporter
from .feed_monitor import FeedMonitor, FeedCache

logger = logging.getLogger('scraper.engine')


@dataclass
class SourceResult:
    """Result of processing a single source."""
    source_id: str
    source_name: str
    records_found: int = 0
    records_created: int = 0
    records_updated: int = 0
    records_skipped: int = 0
    records_rejected: int = 0
    errors: list[str] = field(default_factory=list)
    success: bool = True


@dataclass
class ScrapeResult:
    """Result of a complete scraping run."""
    started_at: datetime
    completed_at: Optional[datetime] = None
    sources_processed: int = 0
    sources_failed: int = 0
    total_records_found: int = 0
    total_records_created: int = 0
    total_records_updated: int = 0
    total_records_skipped: int = 0
    total_records_rejected: int = 0
    source_results: list[SourceResult] = field(default_factory=list)


class ScraperEngine:
    """Orchestrates the scraping pipeline across all sources."""
    
    MAX_CONSECUTIVE_FAILURES = 3
    
    def __init__(
        self,
        http_client: Optional[HttpClient] = None,
        normaliser: Optional[RecordNormaliser] = None,
        deduplicator: Optional[Deduplicator] = None,
        compliance_checker: Optional[ComplianceChecker] = None,
        status_manager: Optional[StatusManager] = None,
        importer: Optional[DjangoImporter] = None,
        exporter: Optional[JsonExporter] = None,
        feed_monitor: Optional[FeedMonitor] = None,
    ):
        """
        Initialize scraper engine with dependencies.
        
        All dependencies are optional and will be created with defaults if not provided.
        """
        self.http_client = http_client or HttpClient()
        self.normaliser = normaliser or RecordNormaliser()
        self.deduplicator = deduplicator or Deduplicator()
        self.compliance_checker = compliance_checker or ComplianceChecker()
        self.status_manager = status_manager or StatusManager()
        self.importer = importer or DjangoImporter()
        self.exporter = exporter or JsonExporter()
        self.feed_monitor = feed_monitor or FeedMonitor(self.http_client, FeedCache())
        
        self._sources: dict[str, SourceConfig] = {}
        self._adapters: dict[str, type] = {}

    def load_sources(self, sources_file: Optional[str] = None) -> None:
        """Load source configurations from YAML file."""
        sources = load_sources(sources_file)
        self._sources = {s.source_id: s for s in sources}
        logger.info(f"Loaded {len(self._sources)} source configurations")
    
    def get_adapter(self, source: SourceConfig):
        """
        Get or create adapter instance for a source.
        
        Args:
            source: Source configuration.
            
        Returns:
            Adapter instance.
        """
        if source.adapter_class not in self._adapters:
            # Dynamically import adapter class
            module_path, class_name = source.adapter_class.rsplit('.', 1)
            module = importlib.import_module(module_path)
            self._adapters[source.adapter_class] = getattr(module, class_name)
        
        adapter_class = self._adapters[source.adapter_class]
        return adapter_class(source, self.http_client)
    
    def run(
        self,
        source_id: Optional[str] = None,
        dry_run: bool = False
    ) -> ScrapeResult:
        """
        Run the scraping pipeline.
        
        Args:
            source_id: Optional source ID to run single source.
            dry_run: If True, don't import to database.
            
        Returns:
            ScrapeResult with summary of the run.
        """
        result = ScrapeResult(started_at=datetime.now())
        
        # Load sources if not already loaded
        if not self._sources:
            self.load_sources()
        
        # Determine which sources to process
        if source_id:
            if source_id not in self._sources:
                logger.error(f"Unknown source: {source_id}")
                result.sources_failed = 1
                return result
            sources = [self._sources[source_id]]
        else:
            sources = [s for s in self._sources.values() if s.is_active]
        
        logger.info(f"Starting scrape run for {len(sources)} sources")
        
        # Process each source
        for source in sources:
            source_result = self._process_source(source, dry_run)
            result.source_results.append(source_result)
            
            if source_result.success:
                result.sources_processed += 1
            else:
                result.sources_failed += 1
            
            # Aggregate totals
            result.total_records_found += source_result.records_found
            result.total_records_created += source_result.records_created
            result.total_records_updated += source_result.records_updated
            result.total_records_skipped += source_result.records_skipped
            result.total_records_rejected += source_result.records_rejected
        
        result.completed_at = datetime.now()
        self._log_summary(result)
        
        return result
    
    def _process_source(self, source: SourceConfig, dry_run: bool) -> SourceResult:
        """Process a single source with error isolation."""
        result = SourceResult(
            source_id=source.source_id,
            source_name=source.source_name
        )
        
        logger.info(f"Processing source: {source.source_name} ({source.source_id})")
        
        try:
            # Get adapter for this source
            adapter = self.get_adapter(source)
            
            # Scrape opportunities
            for raw in adapter.scrape():
                result.records_found += 1
                
                try:
                    # Process through pipeline
                    import_result = self._process_record(raw, source, dry_run)
                    
                    if import_result:
                        if import_result.action == 'created':
                            result.records_created += 1
                        elif import_result.action == 'updated':
                            result.records_updated += 1
                        elif import_result.action == 'skipped':
                            result.records_skipped += 1
                    else:
                        result.records_rejected += 1
                        
                except Exception as e:
                    logger.error(f"Error processing record from {source.source_id}: {e}")
                    result.errors.append(str(e))
                    result.records_skipped += 1
            
            # Update source metadata
            source.last_scraped = datetime.now()
            source.consecutive_failures = 0
            
        except Exception as e:
            logger.error(f"Error processing source {source.source_id}: {e}")
            result.success = False
            result.errors.append(str(e))
            
            # Track consecutive failures
            source.consecutive_failures += 1
            if source.consecutive_failures >= self.MAX_CONSECUTIVE_FAILURES:
                source.needs_attention = True
                logger.warning(
                    f"Source {source.source_id} marked for attention "
                    f"after {source.consecutive_failures} consecutive failures"
                )
        
        logger.info(
            f"Completed {source.source_name}: "
            f"found={result.records_found}, created={result.records_created}, "
            f"updated={result.records_updated}, skipped={result.records_skipped}"
        )
        
        return result
    
    def _process_record(
        self,
        raw: RawOpportunity,
        source: SourceConfig,
        dry_run: bool
    ) -> Optional[ImportResult]:
        """
        Process a single record through the pipeline.
        
        Pipeline: Normalise → Deduplicate → Validate → Import
        """
        # 1. Normalise
        normalised = self.normaliser.normalise(raw, source.source_name)
        
        # 2. Check compliance
        compliance = self.compliance_checker.check(normalised)
        if not compliance.is_compliant and compliance.rejection_reason:
            logger.info(f"Rejected: {normalised.title} - {compliance.rejection_reason}")
            return None
        
        # 3. Check for duplicates
        dedup = self.deduplicator.check_duplicate(normalised)
        existing_id = dedup.existing_record_id if dedup.is_duplicate else None
        
        if dedup.is_duplicate:
            logger.debug(
                f"Duplicate found: {normalised.title} "
                f"(match_type={dedup.match_type}, score={dedup.similarity_score})"
            )
        
        # 4. Determine final status
        normalised.status = self.status_manager.determine_status(normalised)
        
        # 5. Import (unless dry run)
        if dry_run:
            return ImportResult(
                success=True,
                action='created' if not existing_id else 'updated',
                record_id=existing_id
            )
        
        return self.importer.import_record(normalised, existing_id)
    
    def scrape_to_json(
        self,
        source_id: Optional[str] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Scrape and export to JSON without importing to database.
        
        Args:
            source_id: Optional source ID to scrape.
            output_path: Optional file path for JSON output.
            
        Returns:
            JSON string of scraped records.
        """
        records = []
        
        if not self._sources:
            self.load_sources()
        
        sources = ([self._sources[source_id]] if source_id 
                   else [s for s in self._sources.values() if s.is_active])
        
        for source in sources:
            try:
                adapter = self.get_adapter(source)
                for raw in adapter.scrape():
                    normalised = self.normaliser.normalise(raw, source.source_name)
                    compliance = self.compliance_checker.check(normalised)
                    
                    if compliance.is_compliant or not compliance.rejection_reason:
                        normalised.status = self.status_manager.determine_status(normalised)
                        records.append(normalised)
                        
            except Exception as e:
                logger.error(f"Error scraping {source.source_id}: {e}")
        
        return self.exporter.export(records, output_path)
    
    def _log_summary(self, result: ScrapeResult) -> None:
        """Log summary of scrape run."""
        duration = (result.completed_at - result.started_at).total_seconds()
        
        logger.info("=" * 60)
        logger.info("SCRAPE RUN SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Sources processed: {result.sources_processed}")
        logger.info(f"Sources failed: {result.sources_failed}")
        logger.info(f"Total records found: {result.total_records_found}")
        logger.info(f"Records created: {result.total_records_created}")
        logger.info(f"Records updated: {result.total_records_updated}")
        logger.info(f"Records skipped: {result.total_records_skipped}")
        logger.info(f"Records rejected: {result.total_records_rejected}")
        logger.info("=" * 60)
