# Grant Guide South Africa

A funding opportunity aggregator platform for South African businesses. Find grants, loans, equity funding, competitions, and development finance opportunities.

## Quick Start

### Using Docker (Recommended)

```bash
# Clone and navigate to project
cd grant_guide

# Copy environment file
cp .env.example .env

# Start services
docker compose up

# Access at http://localhost:8000
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL database (update .env with your credentials)
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | (generate one) |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1,grantsguide.co.za` |
| `POSTGRES_DB` | Database name | `grant_guide` |
| `POSTGRES_USER` | Database user | `grant_guide` |
| `POSTGRES_PASSWORD` | Database password | `grant_guide` |
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run property-based tests only
pytest tests/properties/

# Run with coverage
pytest --cov=opportunities
```

## Management Commands

```bash
# Update opportunity statuses (run daily)
python manage.py update_statuses

# Dry run (see what would change)
python manage.py update_statuses --dry-run

# Run scraper for all active sources
python manage.py scrape_opportunities

# Run scraper for specific source
python manage.py scrape_opportunities --source dtic

# Run scraper in dry-run mode (no database changes)
python manage.py scrape_opportunities --dry-run --output output.json

# List all configured sources
python manage.py scrape_opportunities --list-sources
```

## High-Performance Weekly Scraper

The scraper includes a high-performance scheduler with timeout handling for production use.

### Running the Scheduled Scraper

```bash
# Run once with timeout handling
python manage.py run_scheduled_scraper --once

# Run with custom timeouts
python manage.py run_scheduled_scraper --once \
    --source-timeout 300 \
    --total-timeout 3600 \
    --request-timeout 60 \
    --max-workers 2

# Run specific source
python manage.py run_scheduled_scraper --once --source dtic

# Check health status of all sources
python manage.py run_scheduled_scraper --health-check

# Run in continuous scheduled mode (weekly at 2 AM)
python manage.py run_scheduled_scraper --interval-days 7 --run-hour 2
```

### Scheduler Options

| Option | Description | Default |
|--------|-------------|---------|
| `--once` | Run once and exit | False |
| `--source` | Specific source ID | All active |
| `--interval-days` | Days between runs | 7 |
| `--run-hour` | Hour to run (0-23) | 2 |
| `--source-timeout` | Timeout per source (seconds) | 300 |
| `--total-timeout` | Total timeout (seconds) | 3600 |
| `--request-timeout` | HTTP request timeout (seconds) | 60 |
| `--max-workers` | Parallel workers | 2 |

### Production Deployment with Cron

```bash
# Add to crontab (run every Sunday at 2 AM)
0 2 * * 0 /path/to/grant_guide/scripts/weekly_scrape.sh >> /var/log/grant_guide/scraper.log 2>&1
```

### Production Deployment with Systemd

```bash
# Copy service files
sudo cp scripts/systemd/grant-guide-scraper.service /etc/systemd/system/
sudo cp scripts/systemd/grant-guide-scraper.timer /etc/systemd/system/

# Enable and start timer
sudo systemctl daemon-reload
sudo systemctl enable grant-guide-scraper.timer
sudo systemctl start grant-guide-scraper.timer

# Check timer status
sudo systemctl list-timers grant-guide-scraper.timer
```

## Scraper Sources

The scraper collects funding opportunities from 12 active sources:

| Source | Type | Status |
|--------|------|--------|
| DTIC | Government | ✅ Active |
| TIA | Government | ✅ Active |
| NYDA | Government | ✅ Active |
| SEFA | Government | ✅ Active (static) |
| IDC | Government | ✅ Active |
| NEF | Government | ✅ Active |
| ECDC | Provincial | ✅ Active |
| Services SETA | SETA | ✅ Active |
| HWSETA | SETA | ✅ Active |
| SAB Foundation | Corporate | ✅ Active |
| AECF | International | ✅ Active |
| TEF | International | ✅ Active (static) |
| DSBD | Government | ❌ SSL issues |
| GEP | Provincial | ❌ Timeout issues |
| DEDAT | Provincial | ❌ Blocked by robots.txt |
| CETA | SETA | ❌ Blocked by robots.txt |

## Admin Access

1. Create a superuser: `python manage.py createsuperuser`
2. Access admin at: `http://localhost:8000/admin/`

## Project Structure

```
grant_guide/
├── grant_guide/          # Django project settings
├── opportunities/        # Main app
│   ├── models.py        # Data models
│   ├── views.py         # Views
│   ├── filters.py       # Search/filter logic
│   ├── admin.py         # Admin configuration
│   └── templates/       # HTML templates
├── templates/           # Base templates
├── tests/               # Test suite
│   └── properties/      # Property-based tests
└── static/              # Static files
```

## Disclaimer

Grant Guide South Africa is an independent funding information platform. We do not provide funding, do not influence approvals, and cannot guarantee success. Funding decisions are made by the official funders, and eligibility criteria may change without notice.
