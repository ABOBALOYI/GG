#!/bin/bash
# Weekly Scraper Script for Grant Guide SA
# 
# This script runs the high-performance scraper with timeout handling.
# Designed to be run via cron or systemd timer.
#
# Cron example (run every Sunday at 2 AM):
#   0 2 * * 0 /path/to/grant_guide/scripts/weekly_scrape.sh >> /var/log/grant_guide/scraper.log 2>&1
#
# Systemd timer example: see weekly-scraper.timer and weekly-scraper.service

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="${PROJECT_DIR}/venv"
LOG_DIR="${PROJECT_DIR}/logs"
LOCK_FILE="/tmp/grant_guide_scraper.lock"

# Timeout settings (in seconds)
SOURCE_TIMEOUT=300      # 5 minutes per source
TOTAL_TIMEOUT=3600      # 1 hour total
REQUEST_TIMEOUT=60      # 60 seconds per request
MAX_WORKERS=2           # Parallel workers

# Create log directory if needed
mkdir -p "$LOG_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Check for existing lock (prevent concurrent runs)
if [ -f "$LOCK_FILE" ]; then
    PID=$(cat "$LOCK_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        log "ERROR: Scraper already running (PID: $PID)"
        exit 1
    else
        log "WARNING: Stale lock file found, removing..."
        rm -f "$LOCK_FILE"
    fi
fi

# Create lock file
echo $$ > "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

log "=========================================="
log "Grant Guide Weekly Scraper Starting"
log "=========================================="
log "Project directory: $PROJECT_DIR"
log "Source timeout: ${SOURCE_TIMEOUT}s"
log "Total timeout: ${TOTAL_TIMEOUT}s"

# Activate virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
    log "Virtual environment activated"
else
    log "ERROR: Virtual environment not found at $VENV_DIR"
    exit 1
fi

# Change to project directory
cd "$PROJECT_DIR"

# Run the scraper with timeout
log "Starting scraper..."
timeout "${TOTAL_TIMEOUT}s" python manage.py run_scheduled_scraper \
    --once \
    --source-timeout "$SOURCE_TIMEOUT" \
    --total-timeout "$TOTAL_TIMEOUT" \
    --request-timeout "$REQUEST_TIMEOUT" \
    --max-workers "$MAX_WORKERS" \
    --verbose

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    log "Scraper completed successfully"
elif [ $EXIT_CODE -eq 124 ]; then
    log "ERROR: Scraper timed out after ${TOTAL_TIMEOUT}s"
else
    log "ERROR: Scraper failed with exit code $EXIT_CODE"
fi

# Update status timestamps
log "Updating opportunity statuses..."
python manage.py update_statuses

log "=========================================="
log "Grant Guide Weekly Scraper Finished"
log "=========================================="

exit $EXIT_CODE
