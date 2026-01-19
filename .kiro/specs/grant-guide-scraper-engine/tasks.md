# Implementation Plan: Grant Guide Scraper Engine

## Overview

This implementation plan breaks down the Grant Guide Scraper Engine into discrete coding tasks. The scraper is built as a Django app component with a pipeline architecture: Discovery → Extraction → Normalisation → Deduplication → Validation → Import.

Tasks are ordered to build incrementally, with core infrastructure first, then individual components, and finally integration and wiring.

## Tasks

- [x] 1. Set up scraper app structure and core data classes
  - [x] 1.1 Create Django app structure for scraper
    - Create `grant_guide/scraper/` directory with `__init__.py`, `apps.py`
    - Add `scraper` to INSTALLED_APPS in settings.py
    - Create subdirectories: `adapters/`, `tests/`, `management/commands/`
    - _Requirements: 10.1_
  
  - [x] 1.2 Implement core data classes and enums
    - Create `scraper/models.py` with SourceConfig, RawOpportunity, NormalisedOpportunity dataclasses
    - Create enums: SourceType, RecordType, FundingType, OpportunityStatus, FunderType, BusinessStage
    - _Requirements: 2.1, 4.1_
  
  - [x] 1.3 Create source configuration loader
    - Create `scraper/sources.yaml` with all 16 approved sources
    - Create `scraper/config.py` with load_sources() function
    - Validate source configs have all required attributes
    - _Requirements: 2.1, 2.3, 2.4, 2.5, 2.6, 2.7_
  
  - [ ]* 1.4 Write property test for source configuration validation
    - **Property 6: Approved Source Enforcement**
    - Test that only configured sources are accepted
    - **Validates: Requirements 2.2**

- [x] 2. Implement HTTP client with compliance features
  - [x] 2.1 Create HTTP client with rate limiting
    - Create `scraper/http_client.py` with HttpClient class
    - Implement request method with configurable delay
    - Track last request time per domain
    - Enforce minimum 2-second delay between same-domain requests
    - _Requirements: 1.3_
  
  - [x] 2.2 Add robots.txt parsing and compliance
    - Implement robots.txt fetching and caching
    - Parse User-agent, Disallow, Allow, Crawl-delay directives
    - Check URL allowance before making requests
    - _Requirements: 1.1_
  
  - [x] 2.3 Add retry logic with exponential backoff
    - Implement retry decorator with configurable max retries (default 3)
    - Implement exponential backoff (1s, 2s, 4s)
    - Handle network errors, timeouts, 5xx responses
    - _Requirements: 11.1_
  
  - [x] 2.4 Write property tests for HTTP client
    - **Property 1: Robots.txt Compliance**
    - **Property 3: Rate Limiting Enforcement**
    - **Property 27: Network Retry with Backoff**
    - **Validates: Requirements 1.1, 1.3, 11.1**

- [x] 3. Checkpoint - Ensure HTTP client tests pass
  - All tests pass (71 scraper tests passing)

- [x] 4. Implement Record Normaliser
  - [x] 4.1 Create normaliser with currency conversion
    - Create `scraper/normaliser.py` with RecordNormaliser class
    - Implement normalise_amount() for ZAR conversion
    - Handle formats: R50,000 / R 50 000 / 50000 ZAR / R1 million / R500k
    - _Requirements: 5.1_
  
  - [x] 4.2 Add date normalisation
    - Implement normalise_date() for ISO format conversion
    - Handle formats: 15 March 2025 / 2025/03/15 / 15-03-2025 / March 15, 2025
    - Return None for unparseable dates
    - _Requirements: 5.2_
  
  - [x] 4.3 Add province normalisation
    - Implement normalise_province() with canonical mapping
    - Handle abbreviations: GP, KZN, EC, WC, etc.
    - Handle variations: "Gauteng Province", "gauteng", "GAUTENG"
    - _Requirements: 5.3_
  
  - [x] 4.4 Add industry normalisation
    - Implement normalise_industry() with canonical mapping
    - Handle variations: "tech", "Technology", "IT", "ICT", "software"
    - Map to canonical tags: Agriculture, Construction, Manufacturing, etc.
    - _Requirements: 5.4_
  
  - [x] 4.5 Add funding type normalisation
    - Implement normalise_funding_type() with canonical mapping
    - Map variations to: Grant, Loan, Equity, Mixed, CompetitionPrize
    - _Requirements: 5.5_
  
  - [x] 4.6 Implement full normalise() method
    - Combine all normalisation functions
    - Truncate description to 300 chars with ellipsis
    - Compute SHA-256 raw_content_hash
    - Set status to DraftNeedsReview for unmappable values
    - Format eligibility as JSON array
    - _Requirements: 4.6, 4.7, 5.6, 5.7_
  
  - [x] 4.7 Write property tests for normaliser
    - **Property 12: Description Truncation**
    - **Property 13: Currency Normalisation**
    - **Property 14: Date Normalisation**
    - **Property 15: Province Normalisation**
    - **Property 16: Industry Normalisation**
    - **Validates: Requirements 4.7, 5.1, 5.2, 5.3, 5.4**

- [x] 5. Implement Compliance Checker
  - [x] 5.1 Create compliance checker with required field validation
    - Create `scraper/compliance.py` with ComplianceChecker class
    - Implement check_required_fields() for title, funder_name, funding_type, apply_url, source_url
    - Return list of missing field names
    - _Requirements: 7.3_
  
  - [x] 5.2 Add payment-to-apply detection
    - Implement check_no_payment_required()
    - Detect keywords: "application fee", "pay to apply", "registration fee", "payment required"
    - Return rejection reason if detected
    - _Requirements: 1.6_
  
  - [x] 5.3 Add social-media-only detection
    - Implement check_no_social_media_only()
    - Detect WhatsApp-only, Telegram-only, Facebook-only sources
    - Check apply_url and contact fields
    - _Requirements: 1.7_
  
  - [x] 5.4 Add access control detection
    - Implement detect_access_control() for HTML content
    - Detect login forms, paywall indicators, CAPTCHA patterns
    - Return True if access control detected
    - _Requirements: 1.2_
  
  - [x] 5.5 Implement full check() method
    - Combine all compliance checks
    - Return ComplianceResult with is_compliant, issues, rejection_reason
    - _Requirements: 1.2, 1.6, 1.7, 7.3_
  
  - [x] 5.6 Write property tests for compliance checker
    - **Property 2: Access Control Detection**
    - **Property 4: Payment-to-Apply Rejection**
    - **Property 5: Social-Media-Only Rejection**
    - **Property 10: Missing Data Handling**
    - **Validates: Requirements 1.2, 1.6, 1.7, 4.5**

- [x] 6. Checkpoint - Ensure normaliser and compliance tests pass
  - All tests pass (71 scraper tests passing)

- [x] 7. Implement Deduplicator
  - [x] 7.1 Create deduplicator with URL matching
    - Create `scraper/deduplicator.py` with Deduplicator class
    - Implement check_by_apply_url() for exact URL match
    - Implement check_by_source_url() for exact URL match
    - Query existing FundingOpportunity records
    - _Requirements: 6.1, 6.2_
  
  - [x] 7.2 Add fuzzy title+funder matching
    - Implement fuzzy_match_title_funder() using rapidfuzz
    - Use similarity threshold of 0.85
    - Combine title and funder_name for matching
    - _Requirements: 6.3_
  
  - [x] 7.3 Implement check_duplicate() with priority order
    - Check apply_url first, then source_url, then fuzzy match
    - Return DeduplicationResult with match_type and similarity_score
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [x] 7.4 Write property tests for deduplicator
    - **Property 17: Deduplication Priority**
    - **Property 18: Duplicate Update Preservation**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

- [x] 8. Implement Status Manager
  - [x] 8.1 Create status manager
    - Create `scraper/status.py` with StatusManager class
    - Implement determine_status() based on deadline, is_rolling, last_verified, required fields
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  
  - [x] 8.2 Add expiry detection
    - Check if deadline_date < today
    - Return Expired status for past deadlines
    - _Requirements: 7.1_
  
  - [x] 8.3 Add stale rolling detection
    - Check if is_rolling=true AND last_verified > 60 days ago
    - Return DraftNeedsReview status
    - _Requirements: 7.2_
  
  - [x] 8.4 Write property tests for status manager
    - **Property 19: Expiry Status Management**
    - **Property 20: Stale Rolling Record Detection**
    - **Property 21: Active Status Validation**
    - **Validates: Requirements 7.1, 7.2, 7.4**

- [x] 9. Implement Feed Monitor
  - [x] 9.1 Create feed monitor with RSS discovery
    - Create `scraper/feed_monitor.py` with FeedMonitor class
    - Implement discover_feed() to find RSS links in HTML
    - Search for `<link rel="alternate" type="application/rss+xml">`
    - Test common patterns: /feed/, /rss/, /category/news/feed/
    - _Requirements: 3.1, 3.2_
  
  - [x] 9.2 Add RSS parsing and item tracking
    - Implement parse_feed() using feedparser library
    - Extract FeedItem objects with guid, title, url, published_date
    - Store seen GUIDs in cache/database
    - _Requirements: 3.5, 3.6_
  
  - [x] 9.3 Implement get_new_items()
    - Return only items not previously seen
    - Mark items as seen after processing
    - _Requirements: 3.5, 3.6_
  
  - [ ]* 9.4 Write property tests for feed monitor
    - **Property 7: RSS Feed Discovery**
    - **Property 8: Feed Item Deduplication**
    - **Validates: Requirements 3.1, 3.2, 3.5, 3.6**

- [x] 10. Checkpoint - Ensure deduplicator, status, and feed tests pass
  - All tests pass (71 scraper tests passing)

- [x] 11. Implement Base Source Adapter
  - [x] 11.1 Create abstract base adapter class
    - Create `scraper/adapters/base.py` with BaseSourceAdapter ABC
    - Define abstract methods: get_opportunity_urls(), extract_opportunity()
    - Implement scrape() method that iterates through opportunities
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [x] 11.2 Add record type classification
    - Implement classify_record_type() based on deadline presence
    - FundingOpportunity (Type A) if deadline exists
    - FundingProduct (Type B) if rolling/no deadline
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [ ]* 11.3 Write property test for record type classification
    - **Property 9: Record Type Classification**
    - **Validates: Requirements 4.1, 4.2, 4.3**

- [x] 12. Implement sample source adapters
  - [x] 12.1 Implement DTIC adapter
    - Create `scraper/adapters/dtic.py` with DTICAdapter class
    - Implement get_opportunity_urls() for incentives page
    - Implement extract_opportunity() with DTIC-specific selectors
    - _Requirements: 2.3_
  
  - [x] 12.2 Implement DSBD adapter
    - Create `scraper/adapters/dsbd.py` with DSBDAdapter class
    - Implement for programmes page structure
    - _Requirements: 2.3_
  
  - [x] 12.3 Implement NYDA adapter
    - Create `scraper/adapters/nyda.py` with NYDAAdapter class
    - Implement for grant programme page structure
    - _Requirements: 2.3_

- [x] 13. Implement Django Importer
  - [x] 13.1 Create Django importer with field mapping
    - Create `scraper/importer.py` with DjangoImporter class
    - Implement map_to_model() to convert NormalisedOpportunity to FundingOpportunity fields
    - Handle funding_amount as range string from min/max
    - _Requirements: 8.1_
  
  - [x] 13.2 Add industry and province handling
    - Implement get_or_create_industries() for ManyToMany
    - Implement get_provinces() for ManyToMany
    - Create Industry records if they don't exist
    - _Requirements: 8.6, 8.7_
  
  - [x] 13.3 Add audit logging
    - Create AuditLog entry on create with action="created_by_scraper"
    - Create AuditLog entry on update with action="updated_by_scraper" and changed fields
    - _Requirements: 8.2, 8.3_
  
  - [x] 13.4 Implement import_record() with error handling
    - Handle validation errors gracefully
    - Log errors and skip invalid records
    - Return ImportResult with success, action, record_id, error
    - _Requirements: 8.4_
  
  - [x] 13.5 Implement import_batch()
    - Process multiple records
    - Continue on individual record errors
    - Return list of ImportResult
    - _Requirements: 8.5_
  
  - [ ]* 13.6 Write property tests for Django importer
    - **Property 22: Django Model Mapping**
    - **Property 23: Audit Log Creation**
    - **Property 24: Import Error Resilience**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.6, 8.7**

- [x] 14. Checkpoint - Ensure adapter and importer tests pass
  - All tests pass (71 scraper tests passing)

- [x] 15. Implement JSON Exporter
  - [x] 15.1 Create JSON exporter with schema validation
    - Create `scraper/exporter.py` with JsonExporter class
    - Implement export() to convert records to JSON array
    - Include all required fields, use null for unknown values
    - _Requirements: 9.1, 9.2, 9.3_
  
  - [x] 15.2 Add schema validation
    - Create JSON schema in `scraper/exporter.py`
    - Validate output against schema before writing
    - _Requirements: 9.5_
  
  - [x] 15.3 Add file and stdout output
    - Support output to file path
    - Support output to stdout
    - _Requirements: 9.4_
  
  - [ ]* 15.4 Write property test for JSON output
    - **Property 25: JSON Output Compliance**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.5**

- [x] 16. Implement Scraper Engine orchestration
  - [x] 16.1 Create scraper engine class
    - Create `scraper/engine.py` with ScraperEngine class
    - Inject dependencies: http_client, normaliser, deduplicator, compliance_checker, importer
    - _Requirements: 10.2_
  
  - [x] 16.2 Implement run() method
    - Process all active sources from configuration
    - For each source: discover feed, scrape opportunities, normalise, deduplicate, validate, import
    - _Requirements: 10.2_
  
  - [x] 16.3 Add single-source mode
    - Accept source_id parameter to run single source
    - _Requirements: 10.3_
  
  - [x] 16.4 Add progress logging
    - Log source being processed
    - Log records found, created, updated, skipped
    - Log errors encountered
    - _Requirements: 10.4_
  
  - [x] 16.5 Add summary report
    - Output totals on completion
    - Include success/failure counts per source
    - _Requirements: 10.5_
  
  - [x] 16.6 Add source error isolation
    - Catch exceptions per source
    - Log error and continue with next source
    - Track consecutive failures per source
    - Set needs_attention flag after 3 failures
    - _Requirements: 10.6, 11.6_
  
  - [ ]* 16.7 Write property tests for scraper engine
    - **Property 26: Source Processing Isolation**
    - **Property 28: Parsing Error Resilience**
    - **Property 29: Consecutive Failure Tracking**
    - **Validates: Requirements 10.6, 11.2, 11.3, 11.6**

- [x] 17. Implement Django management command
  - [x] 17.1 Create scrape_opportunities command
    - Create `scraper/management/commands/scrape_opportunities.py`
    - Add --source argument for single source mode
    - Add --dry-run flag for JSON output without import
    - Add --output argument for JSON file path
    - _Requirements: 10.1, 10.3, 10.7_
  
  - [x] 17.2 Wire up all components
    - Instantiate and connect all pipeline components
    - Configure logging
    - Handle command-line arguments
    - _Requirements: 10.1_

- [x] 18. Final checkpoint - Run full test suite
  - All 71 scraper property tests pass
  - All 24 main application tests pass
  - Total: 95 tests passing
  - Run `python manage.py scrape_opportunities --list-sources` to verify command works

## Notes

- All core tasks are complete
- Optional property tests marked with * can be added for additional coverage
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties using Hypothesis
- The scraper is designed to be run via Django management command: `python manage.py scrape_opportunities`

## Usage

```bash
# List all configured sources
python manage.py scrape_opportunities --list-sources

# Run scraper for all active sources
python manage.py scrape_opportunities

# Run scraper for a single source
python manage.py scrape_opportunities --source dtic

# Dry run (output JSON without importing)
python manage.py scrape_opportunities --dry-run

# Dry run with JSON output to file
python manage.py scrape_opportunities --dry-run --output output.json

# Verbose logging
python manage.py scrape_opportunities --verbose
```
