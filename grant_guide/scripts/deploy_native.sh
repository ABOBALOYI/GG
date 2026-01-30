#!/bin/bash
# Grant Guide Native Deployment Script (No Docker)
# Run this on your Ubuntu server

set -e  # Exit on error

echo "==================================="
echo "Grant Guide Deployment Script"
echo "==================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get current directory
PROJECT_DIR=$(pwd)
echo "Project directory: $PROJECT_DIR"
echo ""

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: manage.py not found. Please run this script from the grant_guide directory.${NC}"
    exit 1
fi

# Step 1: Pull latest code
echo -e "${GREEN}Step 1: Pulling latest code from GitHub...${NC}"
git pull origin main || {
    echo -e "${YELLOW}Warning: Git pull failed. Continuing anyway...${NC}"
}
echo ""

# Step 2: Activate virtual environment
echo -e "${GREEN}Step 2: Activating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo ""

# Step 3: Install/update dependencies
echo -e "${GREEN}Step 3: Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
echo ""

# Step 4: Run migrations
echo -e "${GREEN}Step 4: Running database migrations...${NC}"
python manage.py migrate
echo ""

# Step 5: Collect static files
echo -e "${GREEN}Step 5: Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo ""

# Step 6: Check for errors
echo -e "${GREEN}Step 6: Running Django checks...${NC}"
python manage.py check
echo ""

# Step 7: Restart services (if systemd service exists)
if systemctl is-active --quiet grant-guide; then
    echo -e "${GREEN}Step 7: Restarting Grant Guide service...${NC}"
    sudo systemctl restart grant-guide
    echo "Service restarted successfully!"
else
    echo -e "${YELLOW}Step 7: Grant Guide service not found. Skipping restart.${NC}"
    echo "You can start the development server with: python manage.py runserver 0.0.0.0:8000"
fi
echo ""

# Step 8: Show status
echo -e "${GREEN}==================================="
echo "Deployment Complete!"
echo "===================================${NC}"
echo ""
echo "Next steps:"
echo "1. Check application status: sudo systemctl status grant-guide"
echo "2. View logs: sudo journalctl -u grant-guide -f"
echo "3. Access admin: https://your-domain.com/admin"
echo ""
echo "Management commands:"
echo "- Run scraper: python manage.py scrape_opportunities"
echo "- Update statuses: python manage.py update_statuses"
echo "- Create superuser: python manage.py createsuperuser"
echo ""
