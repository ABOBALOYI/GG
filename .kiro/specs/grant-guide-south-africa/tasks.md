# Grant Guide South Africa - Implementation Tasks

## Task List

### 1. Project Setup
- [x] 1.1 Initialize Django project with PostgreSQL configuration
  - Create Django project `grant_guide`
  - Create `opportunities` app
  - Configure PostgreSQL database settings
  - Add requirements.txt with dependencies (Django, psycopg2, django-filter, hypothesis, pytest-django)
- [x] 1.2 Create Docker configuration
  - Create Dockerfile for Django app
  - Create docker-compose.yml with Django + PostgreSQL services
  - Add .env.example for environment variables

### 2. Data Models
- [x] 2.1 Create Industry and Province models
  - Industry model with name and slug
  - Province model with name, slug, and is_national flag
  - Add initial data migration for SA provinces and common industries
- [x] 2.2 Create FundingOpportunity model
  - All required fields (funding_name, funder, funding_type, description, etc.)
  - All optional fields (bbbee_requirement, target_groups, etc.)
  - ManyToMany relationships to Industry and Province
  - Audit fields (created_at, updated_at, created_by, updated_by)
- [x] 2.3 Create AuditLog model
  - Link to FundingOpportunity
  - Track action, changes, user, timestamp
- [x] 2.4 [PBT] Property test: Required fields validation (P3)
  - Test that active opportunities must have all required fields populated
  - Use Hypothesis to generate opportunity data

### 3. Admin Panel
- [x] 3.1 Configure Django admin for FundingOpportunity
  - List display with key fields
  - List filters by status, funding_type, deadline
  - Search fields (funding_name, funder, description)
  - Auto-populate last_verified on save
- [x] 3.2 Add bulk admin actions
  - Mark selected as Expired
  - Mark selected as Needs Review
  - Mark selected as Active
- [x] 3.3 Create admin for Industry and Province
  - Simple list/edit interface
  - Prepopulated slug from name

### 4. Status Management
- [x] 4.1 Create management command `update_statuses`
  - Mark opportunities with passed deadlines as Expired
  - Mark rolling opportunities not updated for 60 days as Needs Review
  - Log changes made
- [x] 4.2 [PBT] Property test: Status transition correctness (P2)
  - Test that passed deadlines result in Expired status
  - Test rolling + 60 days results in Needs Review

### 5. Public Views - List & Search
- [x] 5.1 Create opportunity list view
  - Display paginated list of active opportunities
  - Default sort by deadline (closing soon first)
  - Show key fields in card format
- [x] 5.2 Create filter functionality
  - Multi-select filters for Industry, Province, Funding Type, Business Stage, Target Group
  - "Closing Soon" filter (within 30 days)
  - HTMX partial for instant filter results
- [x] 5.3 Create search functionality
  - Full-text search on funding_name, funder, description
  - Combine with filters
- [x] 5.4 [PBT] Property test: Filter correctness (P1)
  - Test that filtered results match ALL applied filters
- [x] 5.5 [PBT] Property test: Search result relevance (P4)
  - Test that search results contain query in searchable fields
- [x] 5.6 [PBT] Property test: Deadline urgency correctness (P5)
  - Test "Closing Soon" returns only opportunities within 30 days

### 6. Public Views - Detail Page
- [x] 6.1 Create opportunity detail view
  - Display all fields in standardised format
  - Summary section: What it is, Who it's for, What it funds, How to apply, Deadline
  - Prominent Apply Now button
  - Source link and Last Verified date
- [x] 6.2 Add "Closing Soon" badge logic
  - Show badge if deadline within 30 days

### 7. Templates & Styling
- [x] 7.1 Create base template with Tailwind CSS
  - Header with site name
  - Footer with disclaimer
  - Responsive layout
- [x] 7.2 Create opportunity list template
  - Card layout for opportunities
  - Filter sidebar
  - Pagination
- [x] 7.3 Create opportunity detail template
  - Structured layout following design spec
  - Mobile-friendly
- [x] 7.4 Create disclaimer include template
  - Reusable disclaimer component
  - Include on all pages

### 8. URL Configuration
- [x] 8.1 Configure URL routes
  - `/` - Home/list page
  - `/opportunities/` - Full list with filters
  - `/opportunities/<slug>/` - Detail page
  - `/search/` - HTMX search endpoint

### 9. Validation & Business Rules
- [x] 9.1 Implement model validation
  - URL validation for apply_link and source_link
  - Required fields check before Active status
  - Description max length enforcement
- [x] 9.2 Implement form validation
  - Admin form validation
  - Non-empty arrays for eligibility, documents, steps

### 10. Testing Setup
- [x] 10.1 Configure pytest and Hypothesis
  - pytest-django configuration
  - Hypothesis profiles for property tests
  - Test database setup
- [x] 10.2 Create test fixtures
  - Sample industries and provinces
  - Sample opportunities in various states

### 11. Final Integration
- [ ] 11.1 Add Google AdSense integration
  - Add script to base template
  - Configure ad placements
- [x] 11.2 Create README with setup instructions
  - Local development setup
  - Docker setup
  - Environment variables
- [ ] 11.3 Final testing and verification
  - Run all tests
  - Manual verification of all pages
  - Check disclaimer visibility
