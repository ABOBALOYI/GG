# Grant Guide South Africa - Technical Design

## Overview
A Django-based web application for aggregating and displaying South African business funding opportunities. The platform provides a public-facing search interface and an admin panel for managing listings.

## Tech Stack
- **Backend**: Django 5.x (Python)
- **Database**: PostgreSQL
- **Frontend**: Django Templates + HTMX for interactivity
- **CSS**: Tailwind CSS
- **Search**: Django ORM with PostgreSQL full-text search
- **Testing**: pytest + Hypothesis (property-based testing)
- **Deployment**: Docker-ready

## Architecture

### High-Level Components
```
┌─────────────────────────────────────────────────────────┐
│                    Public Frontend                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Home/List  │  │   Search    │  │  Detail Page    │  │
│  │    Page     │  │   Filters   │  │                 │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    Django Backend                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   Views     │  │   Models    │  │   Admin Panel   │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    PostgreSQL                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ Opportunity │  │  Industry   │  │    Province     │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Data Models

### FundingOpportunity (Main Model)
```python
class FundingOpportunity(models.Model):
    # Required fields
    funding_name = models.CharField(max_length=255)
    funder = models.CharField(max_length=255)
    funding_type = models.CharField(max_length=20, choices=FUNDING_TYPE_CHOICES)
    description = models.TextField(max_length=500)  # 1-3 lines
    business_stage = models.CharField(max_length=20, choices=BUSINESS_STAGE_CHOICES)
    eligibility_requirements = models.JSONField()  # Array of strings
    funding_amount = models.CharField(max_length=100, blank=True)
    deadline = models.DateField(null=True, blank=True)  # null = Rolling
    is_rolling = models.BooleanField(default=False)
    required_documents = models.JSONField()  # Array of strings
    application_steps = models.JSONField()  # Array of numbered steps
    apply_link = models.URLField()
    source_link = models.URLField()
    last_verified = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    # Optional fields
    bbbee_requirement = models.CharField(max_length=10, choices=BBBEE_CHOICES, blank=True)
    target_groups = models.JSONField(default=list, blank=True)
    processing_time = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Relationships
    industries = models.ManyToManyField('Industry')
    provinces = models.ManyToManyField('Province')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)  # Admin notes, e.g., "Needs verification"
    
    # Audit
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_opportunities')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_opportunities')
```

### Supporting Models
```python
class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

class Province(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    is_national = models.BooleanField(default=False)  # For "National" option

class AuditLog(models.Model):
    opportunity = models.ForeignKey(FundingOpportunity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20)  # created, updated, status_changed
    changes = models.JSONField()  # What changed
    timestamp = models.DateTimeField(auto_now_add=True)
```

### Enums/Choices
```python
FUNDING_TYPE_CHOICES = [
    ('grant', 'Grant'),
    ('loan', 'Loan'),
    ('equity', 'Equity'),
    ('mixed', 'Mixed'),
    ('competition', 'Competition Prize'),
]

BUSINESS_STAGE_CHOICES = [
    ('startup', 'Startup'),
    ('sme', 'SME'),
    ('established', 'Established'),
    ('any', 'Any'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('expired', 'Expired'),
    ('draft', 'Draft'),
    ('needs_review', 'Needs Review'),
]

BBBEE_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
    ('unknown', 'Unknown'),
]

TARGET_GROUP_CHOICES = [
    ('women', 'Women'),
    ('youth', 'Youth'),
    ('township', 'Township'),
    ('rural', 'Rural'),
    ('exporters', 'Exporters'),
    ('innovators', 'Innovators'),
]
```

## URL Structure

```
/                           # Home - list of active opportunities
/opportunities/             # Full list with filters
/opportunities/<slug>/      # Detail page
/search/                    # Search results (HTMX partial)

# Admin (Django Admin)
/admin/                     # Django admin panel
```

## Key Components

### 1. Opportunity List View
- Displays paginated list of active opportunities
- Default sort: deadline ascending (closing soon first)
- Shows key fields: Title, Funder, Type, Industries, Provinces, Stage, Amount, Deadline
- "Closing Soon" badge for deadlines within 30 days

### 2. Search & Filter Component
- Full-text search on: funding_name, funder, description
- Multi-select filters for: Industry, Province, Funding Type, Business Stage, Target Group
- Deadline urgency filter: "Closing Soon" (within 30 days)
- HTMX-powered for instant results without page reload

### 3. Detail Page
- Standardised layout following the summary format:
  - What it is (description)
  - Who it's for (business stage, target groups, eligibility)
  - What it funds (funding amount, type)
  - How to apply (numbered steps)
  - Deadline
- Prominent "Apply Now" button linking to official apply link
- Source link for verification
- Last verified date displayed
- Disclaimer at bottom

### 4. Admin Panel (Django Admin)
- Custom admin for FundingOpportunity with:
  - List filters by status, funding type, deadline
  - Bulk actions: Mark as Expired, Mark as Needs Review
  - Inline editing for quick updates
  - Auto-populate last_verified on save
  - Validation for required fields and URLs

### 5. Automated Status Management
- Management command to run daily:
  - Mark opportunities with passed deadlines as "Expired"
  - Mark rolling opportunities not updated for 60 days as "Needs Review"

## Validation Rules

### Source Validation (Implemented in Model/Form)
1. `apply_link` must be a valid URL
2. `source_link` must be a valid URL
3. Both URLs must use HTTPS (recommended)
4. Status cannot be "Active" if required fields are missing

### Content Validation
1. `description` max 500 characters (enforced)
2. `eligibility_requirements` must be non-empty array
3. `required_documents` must be non-empty array
4. `application_steps` must be non-empty array

## Correctness Properties

### P1: Filter Correctness
**Property**: When filtering by any criteria, all returned opportunities must match ALL applied filters.
```
∀ opportunity in filtered_results:
  if industry_filter: opportunity.industries ∩ industry_filter ≠ ∅
  if province_filter: opportunity.provinces ∩ province_filter ≠ ∅
  if funding_type_filter: opportunity.funding_type ∈ funding_type_filter
  if business_stage_filter: opportunity.business_stage ∈ business_stage_filter
  if target_group_filter: opportunity.target_groups ∩ target_group_filter ≠ ∅
```
**Validates: Requirements 1.2**

### P2: Status Transition Correctness
**Property**: Opportunities with passed deadlines must have status "Expired" after status update runs.
```
∀ opportunity where deadline < today AND NOT is_rolling:
  after_status_update(opportunity).status == "expired"
```
**Validates: Requirements 3.3**

### P3: Required Fields Validation
**Property**: Active opportunities must have all required fields populated.
```
∀ opportunity where status == "active":
  opportunity.funding_name IS NOT NULL AND
  opportunity.funder IS NOT NULL AND
  opportunity.funding_type IS NOT NULL AND
  opportunity.description IS NOT NULL AND
  opportunity.apply_link IS NOT NULL AND
  opportunity.source_link IS NOT NULL AND
  opportunity.industries.count() > 0 AND
  opportunity.provinces.count() > 0
```
**Validates: Requirements 2.1, 4.1**

### P4: Search Result Relevance
**Property**: Search results must contain the search term in at least one searchable field.
```
∀ opportunity in search_results(query):
  query.lower() IN opportunity.funding_name.lower() OR
  query.lower() IN opportunity.funder.lower() OR
  query.lower() IN opportunity.description.lower()
```
**Validates: Requirements 1.2**

### P5: Deadline Urgency Correctness
**Property**: "Closing Soon" filter returns only opportunities with deadlines within 30 days.
```
∀ opportunity in closing_soon_results:
  opportunity.deadline IS NOT NULL AND
  opportunity.deadline <= today + 30 days AND
  opportunity.deadline >= today
```
**Validates: Requirements 1.2**

## File Structure
```
grant_guide/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── grant_guide/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── opportunities/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   ├── filters.py
│   ├── management/
│   │   └── commands/
│   │       └── update_statuses.py
│   └── templates/
│       └── opportunities/
│           ├── list.html
│           ├── detail.html
│           ├── _opportunity_card.html
│           └── _filter_form.html
├── templates/
│   ├── base.html
│   └── includes/
│       └── disclaimer.html
├── static/
│   └── css/
│       └── styles.css
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    ├── test_filters.py
    └── properties/
        ├── test_filter_properties.py
        ├── test_status_properties.py
        └── test_validation_properties.py
```

## Testing Strategy

### Unit Tests (pytest)
- Model validation tests
- View response tests
- Admin action tests

### Property-Based Tests (Hypothesis)
- Filter correctness (P1)
- Status transitions (P2)
- Required field validation (P3)
- Search relevance (P4)
- Deadline urgency (P5)

### Integration Tests
- Full search flow
- Admin create/edit flow
- Status update management command

## Disclaimer Implementation
The disclaimer text will be stored in a template include and rendered on:
- Homepage (above footer)
- List page (above footer)
- Detail page (below opportunity details)
- Footer (all pages)

```html
<!-- templates/includes/disclaimer.html -->
<div class="disclaimer">
  <p>Grant Guide South Africa is an independent funding information platform. 
  We do not provide funding, do not influence approvals, and cannot guarantee success. 
  Funding decisions are made by the official funders, and eligibility criteria may change without notice.</p>
</div>
```
