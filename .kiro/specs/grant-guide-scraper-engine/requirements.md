# Requirements Document

## Introduction

The Grant Guide Scraper Engine is a web scraping system designed to automatically collect, verify, normalise, and import South African business funding opportunities into the Grant Guide Django application. The engine scrapes approved government, provincial, SETA, corporate, and international donor sources to maintain an up-to-date database of grants, loans, equity funding, competitions, and development finance opportunities.

The scraper operates within strict compliance boundaries: it never bypasses access controls, respects robots.txt, implements polite crawling with rate limiting, and avoids collecting personal data. When data is unclear or incomplete, records are flagged for manual review rather than published with incorrect information.

## Glossary

- **Scraper_Engine**: The main orchestration system that coordinates scraping jobs across all approved sources
- **Source_Adapter**: A source-specific module that knows how to extract data from a particular website
- **Feed_Monitor**: Component that monitors RSS feeds or news pages for new opportunities
- **Record_Normaliser**: Component that transforms raw scraped data into the standardised FundingOpportunity format
- **Deduplicator**: Component that identifies and merges duplicate records
- **Compliance_Checker**: Component that validates scraped data against trust and safety rules
- **Django_Importer**: Component that imports normalised records into the Grant Guide Django database
- **FundingOpportunity**: A time-bound funding opportunity with a specific deadline (Type A record)
- **FundingProduct**: A rolling/always-open funding programme (Type B record)
- **Raw_Content_Hash**: SHA-256 hash of the scraped content used for change detection

## Requirements

### Requirement 1: Compliance and Ethical Scraping

**User Story:** As a platform operator, I want the scraper to operate ethically and legally, so that we maintain trust and avoid legal issues.

#### Acceptance Criteria

1. WHEN the Scraper_Engine encounters a robots.txt file, THE Scraper_Engine SHALL parse and respect all directives including Crawl-delay
2. WHEN the Scraper_Engine encounters a login page, paywall, CAPTCHA, or access control, THE Scraper_Engine SHALL skip that resource and log the blocked access
3. WHEN the Scraper_Engine makes requests to a domain, THE Scraper_Engine SHALL enforce a minimum delay of 2 seconds between requests to the same domain
4. WHEN the Scraper_Engine extracts contact information, THE Scraper_Engine SHALL only collect official public contact details (published email/phone on official pages)
5. WHEN the Scraper_Engine encounters personal data (names, personal emails, personal phone numbers), THE Scraper_Engine SHALL exclude that data from the record
6. WHEN the Scraper_Engine encounters an opportunity requiring payment to apply, THE Scraper_Engine SHALL reject the record and log the rejection reason
7. WHEN the Scraper_Engine encounters a WhatsApp-only or social-media-only funding source, THE Scraper_Engine SHALL reject the record
8. WHEN the Scraper_Engine encounters an unverifiable organisation, THE Scraper_Engine SHALL reject the record

### Requirement 2: Approved Source Management

**User Story:** As a platform operator, I want to manage a list of approved sources, so that only trusted websites are scraped.

#### Acceptance Criteria

1. THE Scraper_Engine SHALL maintain a configuration of approved sources with the following attributes: source_id, source_name, source_url, source_type (government/provincial/seta/corporate/international), adapter_type, is_active, last_scraped_date
2. WHEN a source is not in the approved list, THE Scraper_Engine SHALL refuse to scrape it
3. THE Scraper_Engine SHALL support the following primary government sources: the dtic, DSBD, TIA, NYDA, SEFA, IDC, NEF
4. THE Scraper_Engine SHALL support the following provincial sources: GEP Gauteng, ECDC Eastern Cape, Western Cape DEDAT
5. THE Scraper_Engine SHALL support the following SETA sources: Services SETA, HWSETA, CETA
6. THE Scraper_Engine SHALL support the following private/corporate sources: SAB Foundation
7. THE Scraper_Engine SHALL support the following international donor sources: AECF, Tony Elumelu Foundation
8. WHEN a new source needs to be added, THE Scraper_Engine SHALL require manual configuration with a source-specific adapter

### Requirement 3: RSS and Feed Discovery

**User Story:** As a platform operator, I want the scraper to automatically discover and use RSS feeds, so that new opportunities are detected efficiently.

#### Acceptance Criteria

1. WHEN the Feed_Monitor visits a source page, THE Feed_Monitor SHALL search for RSS feed links via `<link rel="alternate" type="application/rss+xml">` tags
2. WHEN the Feed_Monitor does not find an RSS link tag, THE Feed_Monitor SHALL test common RSS URL patterns: /feed/, /rss/, /category/news/feed/, /category/open-calls/feed/
3. WHEN a valid RSS feed is discovered, THE Feed_Monitor SHALL use the feed as the primary monitoring mechanism for that source
4. WHEN no RSS feed exists, THE Feed_Monitor SHALL use the designated "Open Calls" or "News" page as the monitoring target
5. WHEN an RSS feed item is new (not previously seen), THE Feed_Monitor SHALL trigger a full page scrape of the linked opportunity
6. THE Feed_Monitor SHALL store the last-seen RSS item GUIDs to avoid re-processing

### Requirement 4: Data Extraction and Record Types

**User Story:** As a platform operator, I want the scraper to extract structured data from web pages, so that opportunities are captured accurately.

#### Acceptance Criteria

1. WHEN the Source_Adapter extracts an opportunity, THE Source_Adapter SHALL classify it as either FundingOpportunity (Type A: time-bound with deadline) or FundingProduct (Type B: rolling/always open)
2. WHEN extracting a FundingOpportunity, THE Source_Adapter SHALL extract: title, funder_name, funder_type, funding_type, description_short, deadline_date
3. WHEN extracting a FundingProduct, THE Source_Adapter SHALL extract: title, funder_name, funder_type, funding_type, description_short, and set is_rolling=true
4. THE Source_Adapter SHALL extract the following required fields for all records: industry_tags, province_tags, business_stage, eligibility_bullets, funding_amount_min, funding_amount_max, required_documents_bullets, application_steps, official_apply_url, source_url
5. WHEN a required field cannot be extracted, THE Source_Adapter SHALL set the field to null and set status="DraftNeedsReview"
6. THE Source_Adapter SHALL compute and store a raw_content_hash (SHA-256) of the source page content for change detection
7. WHEN the description exceeds 300 characters, THE Source_Adapter SHALL truncate to 300 characters with ellipsis

### Requirement 5: Data Normalisation

**User Story:** As a platform operator, I want scraped data to be normalised to a consistent format, so that all records are uniform and searchable.

#### Acceptance Criteria

1. WHEN the Record_Normaliser encounters a monetary amount, THE Record_Normaliser SHALL convert it to ZAR (South African Rand)
2. WHEN the Record_Normaliser encounters a date, THE Record_Normaliser SHALL convert it to ISO format (YYYY-MM-DD)
3. WHEN the Record_Normaliser encounters a province name, THE Record_Normaliser SHALL map it to one of the canonical values: Eastern Cape, Free State, Gauteng, KwaZulu-Natal, Limpopo, Mpumalanga, Northern Cape, North West, Western Cape, National
4. WHEN the Record_Normaliser encounters an industry reference, THE Record_Normaliser SHALL map it to one or more canonical tags: Agriculture, Construction, Manufacturing, Retail, ICT, Tourism, Transport, Energy, Healthcare, Education, Creative, Finance, Mining, Services, Green Economy
5. WHEN the Record_Normaliser encounters a funding type, THE Record_Normaliser SHALL map it to: Grant, Loan, Equity, Mixed, or CompetitionPrize
6. WHEN the Record_Normaliser cannot map a value to a canonical form, THE Record_Normaliser SHALL preserve the original value and set status="DraftNeedsReview"
7. WHEN the Record_Normaliser processes eligibility requirements, THE Record_Normaliser SHALL format them as a JSON array of bullet strings

### Requirement 6: Deduplication

**User Story:** As a platform operator, I want duplicate records to be detected and merged, so that the database remains clean.

#### Acceptance Criteria

1. WHEN the Deduplicator processes a new record, THE Deduplicator SHALL check for existing records with matching official_apply_url
2. WHEN the Deduplicator does not find a URL match, THE Deduplicator SHALL check for existing records with matching source_url
3. WHEN the Deduplicator does not find a URL match, THE Deduplicator SHALL perform fuzzy matching on title+funder_name combination (similarity threshold >= 0.85)
4. WHEN a duplicate is found, THE Deduplicator SHALL update the existing record with new data and refresh last_verified_date
5. WHEN a duplicate is found, THE Deduplicator SHALL preserve the original record ID and creation date
6. WHEN no duplicate is found, THE Deduplicator SHALL create a new record

### Requirement 7: Expiry and Status Management

**User Story:** As a platform operator, I want records to be automatically expired and flagged for review, so that the database stays current.

#### Acceptance Criteria

1. WHEN a record has deadline_date < today, THE Scraper_Engine SHALL set status="Expired"
2. WHEN a record has is_rolling=true AND last_verified_date is more than 60 days ago, THE Scraper_Engine SHALL set status="DraftNeedsReview"
3. WHEN a record is missing any required field (title, funder_name, funding_type, official_apply_url, source_url), THE Scraper_Engine SHALL set status="DraftNeedsReview"
4. WHEN a record passes all validation checks and has all required fields, THE Scraper_Engine SHALL set status="Active"
5. WHEN the Scraper_Engine updates a record status, THE Scraper_Engine SHALL log the status change with timestamp and reason

### Requirement 8: Django Integration

**User Story:** As a platform operator, I want scraped records to be imported into the Django database, so that they appear on the website.

#### Acceptance Criteria

1. WHEN the Django_Importer receives a normalised record, THE Django_Importer SHALL map it to the FundingOpportunity model fields
2. WHEN the Django_Importer creates a new record, THE Django_Importer SHALL create an AuditLog entry with action="created_by_scraper"
3. WHEN the Django_Importer updates an existing record, THE Django_Importer SHALL create an AuditLog entry with action="updated_by_scraper" and record the changed fields
4. WHEN the Django_Importer encounters a validation error, THE Django_Importer SHALL log the error and skip the record without crashing
5. THE Django_Importer SHALL support both batch import (multiple records) and single record import
6. WHEN importing industry_tags, THE Django_Importer SHALL create Industry records if they don't exist and link via ManyToMany
7. WHEN importing province_tags, THE Django_Importer SHALL link to existing Province records via ManyToMany

### Requirement 9: Output Format

**User Story:** As a platform operator, I want scraped data to be available in JSON format, so that it can be reviewed before import.

#### Acceptance Criteria

1. THE Scraper_Engine SHALL output scraped records as a JSON array
2. WHEN outputting a record, THE Scraper_Engine SHALL include all required fields: record_type, title, funder_name, funder_type, funding_type, description_short, industry_tags, province_tags, business_stage, eligibility_bullets, funding_amount_min, funding_amount_max, deadline_date, is_rolling, required_documents_bullets, application_steps, official_apply_url, source_url, source_name, last_verified_date, status, raw_content_hash
3. WHEN a field value is unknown or not extracted, THE Scraper_Engine SHALL output null for that field
4. THE Scraper_Engine SHALL support outputting to a file path or stdout
5. THE Scraper_Engine SHALL validate JSON output against a schema before writing

### Requirement 10: Scraper Orchestration and Scheduling

**User Story:** As a platform operator, I want to run the scraper on a schedule and monitor its progress, so that data stays fresh.

#### Acceptance Criteria

1. THE Scraper_Engine SHALL support running as a Django management command
2. WHEN the Scraper_Engine runs, THE Scraper_Engine SHALL process all active sources in the approved list
3. THE Scraper_Engine SHALL support running for a single source via command-line argument
4. THE Scraper_Engine SHALL log progress including: source being processed, records found, records created, records updated, records skipped, errors encountered
5. WHEN the Scraper_Engine completes, THE Scraper_Engine SHALL output a summary report with totals
6. IF an error occurs while processing one source, THEN THE Scraper_Engine SHALL log the error and continue with the next source
7. THE Scraper_Engine SHALL support a --dry-run flag that outputs JSON without importing to Django

### Requirement 11: Error Handling and Logging

**User Story:** As a platform operator, I want comprehensive error handling and logging, so that I can diagnose issues.

#### Acceptance Criteria

1. WHEN the Scraper_Engine encounters a network error, THE Scraper_Engine SHALL retry up to 3 times with exponential backoff
2. WHEN the Scraper_Engine encounters a parsing error, THE Scraper_Engine SHALL log the error with source URL and continue processing
3. WHEN the Scraper_Engine encounters an unexpected page structure, THE Scraper_Engine SHALL log a warning and mark the source for manual review
4. THE Scraper_Engine SHALL log all operations at appropriate levels: DEBUG for detailed extraction, INFO for progress, WARNING for recoverable issues, ERROR for failures
5. THE Scraper_Engine SHALL include timestamps in all log entries
6. WHEN a source consistently fails (3+ consecutive runs), THE Scraper_Engine SHALL flag the source as needs_attention in the configuration
