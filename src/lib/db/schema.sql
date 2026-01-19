-- GrantGuide SA SQLite Schema (Turso)
-- Simplified schema for content-focused site

-- Grants table
CREATE TABLE IF NOT EXISTS grants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    eligibility_criteria TEXT NOT NULL, -- JSON string
    disqualifiers TEXT, -- JSON string
    income_thresholds TEXT, -- JSON string
    application_steps TEXT, -- JSON string
    processing_timeline TEXT,
    common_mistakes TEXT, -- JSON string
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Payment cycles
CREATE TABLE IF NOT EXISTS payment_cycles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL,
    grant_id INTEGER REFERENCES grants(id),
    payment_dates TEXT NOT NULL, -- JSON: [{method, start_date, end_date}]
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    UNIQUE(month, year, grant_id)
);

-- Status codes
CREATE TABLE IF NOT EXISTS status_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    official_meaning TEXT NOT NULL,
    simplified_meaning TEXT NOT NULL,
    real_world_patterns TEXT,
    recommended_actions TEXT, -- JSON string
    related_status_codes TEXT, -- JSON array
    created_at TEXT DEFAULT (datetime('now'))
);

-- Appeal guides
CREATE TABLE IF NOT EXISTS appeal_guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grant_id INTEGER REFERENCES grants(id),
    appeal_steps TEXT NOT NULL, -- JSON string
    required_documents TEXT, -- JSON string
    timeline TEXT,
    common_pitfalls TEXT, -- JSON string
    created_at TEXT DEFAULT (datetime('now'))
);

-- Document requirements
CREATE TABLE IF NOT EXISTS document_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grant_id INTEGER REFERENCES grants(id),
    scenario TEXT, -- e.g., "first_time", "renewal"
    documents TEXT NOT NULL, -- JSON: [{name, description, alternatives}]
    created_at TEXT DEFAULT (datetime('now'))
);

-- FAQs (for SEO)
CREATE TABLE IF NOT EXISTS faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grant_id INTEGER REFERENCES grants(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    display_order INTEGER DEFAULT 0
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_grants_slug ON grants(slug);
CREATE INDEX IF NOT EXISTS idx_grants_active ON grants(is_active);
CREATE INDEX IF NOT EXISTS idx_payment_cycles_date ON payment_cycles(year, month);
CREATE INDEX IF NOT EXISTS idx_status_codes_code ON status_codes(code);
CREATE INDEX IF NOT EXISTS idx_faqs_grant ON faqs(grant_id);
