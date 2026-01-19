# Grant Guide South Africa - Requirements

## Overview
Grant Guide South Africa is a funding opportunity aggregator platform for businesses in South Africa. The platform collects, verifies, summarises, and publishes legitimate business funding opportunities in a clear and searchable format.

**Important**: This is an information platform only. It does not provide funding and does not guarantee approval.

---

## User Stories

### 1. Funding Opportunity Discovery

#### 1.1 Browse Funding Opportunities
**As a** business owner in South Africa  
**I want to** browse available funding opportunities  
**So that** I can find relevant funding for my business

**Acceptance Criteria:**
- [ ] 1.1.1 User can view a list of all active funding opportunities
- [ ] 1.1.2 Each listing displays: Title, Funder, Funding Type, Industries, Provinces, Business Stage, Funding Amount, Deadline
- [ ] 1.1.3 Listings are sorted by deadline (closing soon first) by default
- [ ] 1.1.4 User can click on a listing to view full details
- [ ] 1.1.5 Platform disclaimer is visible on all pages

#### 1.2 Search and Filter Opportunities
**As a** business owner  
**I want to** search and filter funding opportunities  
**So that** I can find opportunities relevant to my specific situation

**Acceptance Criteria:**
- [ ] 1.2.1 User can search by keyword (funding name, funder, description)
- [ ] 1.2.2 User can filter by Industry (multiple selection)
- [ ] 1.2.3 User can filter by Province (including "National" option)
- [ ] 1.2.4 User can filter by Funding Type (Grant/Loan/Equity/Mixed/Competition Prize)
- [ ] 1.2.5 User can filter by Business Stage (Startup/SME/Established/Any)
- [ ] 1.2.6 User can filter by Target Group (Women/Youth/Township/Rural/Exporters/Innovators)
- [ ] 1.2.7 User can filter by Deadline Urgency ("Closing Soon" = within 30 days)
- [ ] 1.2.8 Filters can be combined
- [ ] 1.2.9 Search results update in real-time or on submit

#### 1.3 View Opportunity Details
**As a** business owner  
**I want to** view complete details of a funding opportunity  
**So that** I can determine if I'm eligible and how to apply

**Acceptance Criteria:**
- [ ] 1.3.1 Detail page shows all required fields in standardised format
- [ ] 1.3.2 Summary follows format: What it is, Who it's for, What it funds, How to apply, Deadline
- [ ] 1.3.3 Eligibility requirements displayed as bullet list
- [ ] 1.3.4 Required documents displayed as bullet list
- [ ] 1.3.5 Application steps displayed as numbered list
- [ ] 1.3.6 Official Apply Link is prominently displayed and clickable
- [ ] 1.3.7 Source Link is visible for verification
- [ ] 1.3.8 Last Verified Date is displayed
- [ ] 1.3.9 Disclaimer is visible on detail page

---

### 2. Funding Opportunity Data Model

#### 2.1 Required Data Fields
**As a** platform  
**I need to** store structured funding opportunity data  
**So that** information is consistent and searchable

**Acceptance Criteria:**
- [ ] 2.1.1 Each opportunity has: Funding Name (required, string)
- [ ] 2.1.2 Each opportunity has: Funder/Organisation (required, string)
- [ ] 2.1.3 Each opportunity has: Funding Type (required, enum: Grant/Loan/Equity/Mixed/Competition Prize)
- [ ] 2.1.4 Each opportunity has: Description (required, 1-3 lines plain text)
- [ ] 2.1.5 Each opportunity has: Industries Supported (required, array of tags)
- [ ] 2.1.6 Each opportunity has: Provinces Covered (required, array of tags or "National")
- [ ] 2.1.7 Each opportunity has: Business Stage (required, enum: Startup/SME/Established/Any)
- [ ] 2.1.8 Each opportunity has: Eligibility Requirements (required, array of strings)
- [ ] 2.1.9 Each opportunity has: Funding Amount/Range (optional, string)
- [ ] 2.1.10 Each opportunity has: Deadline Date (required, date or "Rolling/Always Open")
- [ ] 2.1.11 Each opportunity has: Required Documents (required, array of strings)
- [ ] 2.1.12 Each opportunity has: Application Steps (required, array of numbered steps)
- [ ] 2.1.13 Each opportunity has: Official Apply Link (required, valid URL)
- [ ] 2.1.14 Each opportunity has: Source Link (required, valid URL)
- [ ] 2.1.15 Each opportunity has: Last Verified Date (required, date)
- [ ] 2.1.16 Each opportunity has: Status (required, enum: Active/Expired/Draft)

#### 2.2 Optional Data Fields
**As a** platform  
**I need to** support additional optional fields  
**So that** more detailed information can be captured when available

**Acceptance Criteria:**
- [ ] 2.2.1 BBBEE Requirement field (enum: Yes/No/Unknown)
- [ ] 2.2.2 Target Group field (array: Women/Youth/Township/Rural/Exporters/Innovators)
- [ ] 2.2.3 Processing Time field (string, only if stated by funder)
- [ ] 2.2.4 Contact Email field (string, only if publicly listed)
- [ ] 2.2.5 Contact Phone field (string, only if publicly listed)

---

### 3. Admin Management

#### 3.1 Create Funding Opportunity
**As an** admin  
**I want to** create new funding opportunity listings  
**So that** users can discover new funding sources

**Acceptance Criteria:**
- [ ] 3.1.1 Admin can enter all required fields via form
- [ ] 3.1.2 Admin can enter optional fields
- [ ] 3.1.3 Form validates required fields before submission
- [ ] 3.1.4 Form validates URL fields are valid URLs
- [ ] 3.1.5 Last Verified Date auto-populates to current date
- [ ] 3.1.6 Status defaults to "Draft" if any key info is missing
- [ ] 3.1.7 Admin can save as Draft or publish as Active

#### 3.2 Edit Funding Opportunity
**As an** admin  
**I want to** edit existing funding opportunity listings  
**So that** information stays accurate and current

**Acceptance Criteria:**
- [ ] 3.2.1 Admin can edit all fields of existing listings
- [ ] 3.2.2 Last Verified Date updates when admin verifies and saves
- [ ] 3.2.3 Admin can change status (Active/Expired/Draft)
- [ ] 3.2.4 Edit history is preserved (audit trail)

#### 3.3 Verification Workflow
**As an** admin  
**I want to** verify funding opportunities  
**So that** only trustworthy information is published

**Acceptance Criteria:**
- [ ] 3.3.1 Admin can mark opportunity as "Verified" which updates Last Verified Date
- [ ] 3.3.2 System flags opportunities where deadline has passed → auto-mark as Expired
- [ ] 3.3.3 System flags rolling opportunities not updated for 60 days → "Needs Review"
- [ ] 3.3.4 Admin dashboard shows listings needing review
- [ ] 3.3.5 Admin can bulk-update status for multiple listings

---

### 4. Trust & Safety Rules

#### 4.1 Source Validation
**As a** platform  
**I need to** enforce source validation rules  
**So that** only legitimate opportunities are published

**Acceptance Criteria:**
- [ ] 4.1.1 Only opportunities from verifiable organisations are accepted (government, corporate, DFI, NGO, international donor)
- [ ] 4.1.2 Every listing must have an official source link
- [ ] 4.1.3 Every listing must have an official apply link or verified application page
- [ ] 4.1.4 Opportunities requiring payment to apply are rejected
- [ ] 4.1.5 Unverified social media posts (WhatsApp/Telegram/Facebook only) are rejected
- [ ] 4.1.6 "Guaranteed funding" or "instant approval" claims are rejected
- [ ] 4.1.7 Unclear owners or unverifiable organisations are rejected

#### 4.2 Content Standards
**As a** platform  
**I need to** enforce content standards  
**So that** listings are neutral and factual

**Acceptance Criteria:**
- [ ] 4.2.1 Descriptions are summarised, not copy/pasted from source
- [ ] 4.2.2 Language is neutral, simple, and factual
- [ ] 4.2.3 No sales language or marketing speak
- [ ] 4.2.4 No promises of success or approval guarantees
- [ ] 4.2.5 If information is unclear, listing is saved as Draft with "Needs verification" note

---

### 5. Platform Compliance

#### 5.1 Disclaimer Display
**As a** platform  
**I must** display appropriate disclaimers  
**So that** users understand the platform's role

**Acceptance Criteria:**
- [ ] 5.1.1 Disclaimer text displayed on homepage: "Grant Guide South Africa is an independent funding information platform. We do not provide funding, do not influence approvals, and cannot guarantee success. Funding decisions are made by the official funders, and eligibility criteria may change without notice."
- [ ] 5.1.2 Disclaimer visible on all listing pages
- [ ] 5.1.3 Disclaimer visible on detail pages
- [ ] 5.1.4 Disclaimer in footer of all pages

---

## South African Provinces Reference
- Eastern Cape
- Free State
- Gauteng
- KwaZulu-Natal
- Limpopo
- Mpumalanga
- Northern Cape
- North West
- Western Cape
- National (all provinces)

## Industry Tags Reference (Initial Set)
- Agriculture
- Manufacturing
- Technology/ICT
- Tourism & Hospitality
- Retail & Trade
- Construction
- Mining
- Healthcare
- Education
- Creative Industries
- Transport & Logistics
- Financial Services
- Energy & Renewables
- Food & Beverage
- Professional Services

## Priority Order (Non-Functional)
1. Accuracy - Information must be correct
2. Trust - Sources must be verifiable
3. Clarity - Content must be easy to understand
4. Freshness - Information must be current
5. Coverage - Comprehensive listing of opportunities
6. Speed - Performance is important but not at expense of above
