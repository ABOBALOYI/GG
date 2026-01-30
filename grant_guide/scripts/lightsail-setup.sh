#!/bin/bash
# AWS Lightsail initial setup script
# Run this script on your Lightsail instance after creation

set -e

echo "🔧 Setting up AWS Lightsail instance for Grant Guide..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Git
echo "📚 Installing Git..."
sudo apt-get install -y git

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/grant-guide
sudo chown $USER:$USER /opt/grant-guide

# Clone repository
echo "📥 Cloning repository..."
cd /opt/grant-guide
git clone https://github.com/ABOBALOYI/GG.git .

# Create .env file
echo "📝 Creating .env file..."
cd grant_guide
cat > .env << 'EOF'
# Django Settings
DJANGO_SECRET_KEY=CHANGE_THIS_TO_A_SECURE_RANDOM_STRING
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=grantsguide.co.za,www.grantsguide.co.za,YOUR_LIGHTSAIL_IP

# PostgreSQL Database
POSTGRES_DB=grant_guide
POSTGRES_USER=grant_guide
POSTGRES_PASSWORD=CHANGE_THIS_TO_A_SECURE_PASSWORD

# Google AdSense (optional)
GOOGLE_ADSENSE_CLIENT_ID=

# AWS Region
AWS_REGION=us-east-1
EOF

echo "⚠️  IMPORTANT: Edit /opt/grant-guide/grant_guide/.env and update:"
echo "   - DJANGO_SECRET_KEY"
echo "   - POSTGRES_PASSWORD"
echo "   - DJANGO_ALLOWED_HOSTS"
echo ""

# Setup SSL certificate (Let's Encrypt)
echo "🔐 Setting up SSL certificate..."
echo "Run these commands after updating .env:"
echo "  cd /opt/grant-guide/grant_guide"
echo "  docker-compose -f docker-compose.prod.yml up -d nginx"
echo "  docker-compose -f docker-compose.prod.yml run --rm certbot certonly --webroot --webroot-path /var/www/certbot -d grantsguide.co.za -d www.grantsguide.co.za"
echo ""

# Setup systemd service for auto-restart
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/grant-guide.service > /dev/null << 'EOF'
[Unit]
Description=Grant Guide Docker Compose Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/grant-guide/grant_guide
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable grant-guide.service

# Setup weekly scraper cron job
echo "⏰ Setting up weekly scraper cron job..."
(crontab -l 2>/dev/null; echo "0 2 * * 0 cd /opt/grant-guide/grant_guide && docker-compose -f docker-compose.prod.yml exec -T web python manage.py scrape_opportunities") | crontab -

# Setup daily status update cron job
(crontab -l 2>/dev/null; echo "0 3 * * * cd /opt/grant-guide/grant_guide && docker-compose -f docker-compose.prod.yml exec -T web python manage.py update_statuses") | crontab -

echo "✅ Lightsail setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit /opt/grant-guide/grant_guide/.env with your settings"
echo "2. Generate Django secret key: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
echo "3. Update DNS records to point to this Lightsail instance"
echo "4. Run: cd /opt/grant-guide/grant_guide && docker-compose -f docker-compose.prod.yml up -d"
echo "5. Setup SSL certificate (see commands above)"
echo "6. Create Django superuser: docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo ""
echo "🔍 Useful commands:"
echo "  - View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  - Restart: sudo systemctl restart grant-guide"
echo "  - Status: docker-compose -f docker-compose.prod.yml ps"
