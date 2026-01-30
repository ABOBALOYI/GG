# Native Ubuntu Deployment Guide (No Docker)

This guide covers deploying Grant Guide South Africa directly on Ubuntu without Docker.

## Prerequisites

- Ubuntu 22.04 LTS server
- SSH access
- Sudo privileges
- Domain name (optional)

## Quick Deployment Commands

Run these commands in your SSH terminal:

```bash
# 1. Navigate to project directory (or clone if needed)
cd /path/to/your/project/grant_guide

# 2. Update system packages
sudo apt update && sudo apt upgrade -y

# 3. Install system dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx git

# 4. Setup PostgreSQL database
sudo -u postgres psql << EOF
CREATE DATABASE grant_guide;
CREATE USER grant_guide WITH PASSWORD 'your_secure_password';
ALTER ROLE grant_guide SET client_encoding TO 'utf8';
ALTER ROLE grant_guide SET default_transaction_isolation TO 'read committed';
ALTER ROLE grant_guide SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE grant_guide TO grant_guide;
\q
EOF

# 5. Create Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 6. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# 7. Create .env file
cp .env.example .env
nano .env  # Edit with your settings

# 8. Run migrations
python manage.py migrate

# 9. Create superuser
python manage.py createsuperuser

# 10. Collect static files
python manage.py collectstatic --noinput

# 11. Load initial data (optional)
python manage.py create_sample_data

# 12. Test the application
python manage.py runserver 0.0.0.0:8000
```

## Environment Variables (.env)

Edit your `.env` file with these values:

```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# PostgreSQL Database
POSTGRES_DB=grant_guide
POSTGRES_USER=grant_guide
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Google AdSense (optional)
GOOGLE_ADSENSE_CLIENT_ID=
```

Generate secret key:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## Setup Gunicorn Service

Create systemd service file:

```bash
sudo nano /etc/systemd/system/grant-guide.service
```

Add this content (adjust paths):

```ini
[Unit]
Description=Grant Guide Django Application
After=network.target postgresql.service

[Service]
Type=notify
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/grant_guide
Environment="PATH=/home/ubuntu/grant_guide/venv/bin"
ExecStart=/home/ubuntu/grant_guide/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/ubuntu/grant_guide/grant_guide.sock \
    --timeout 120 \
    --access-logfile /var/log/grant-guide/access.log \
    --error-logfile /var/log/grant-guide/error.log \
    grant_guide.wsgi:application

[Install]
WantedBy=multi-user.target
```

Create log directory:
```bash
sudo mkdir -p /var/log/grant-guide
sudo chown ubuntu:www-data /var/log/grant-guide
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable grant-guide
sudo systemctl start grant-guide
sudo systemctl status grant-guide
```

## Setup Nginx

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/grant-guide
```

Add this content:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/ubuntu/grant_guide/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/grant_guide/grant_guide.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/grant-guide /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Setup SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## Setup Scraper Cron Job

Edit crontab:
```bash
crontab -e
```

Add weekly scraper job (runs every Sunday at 2 AM):
```cron
0 2 * * 0 /home/ubuntu/grant_guide/venv/bin/python /home/ubuntu/grant_guide/manage.py scrape_opportunities >> /var/log/grant-guide/scraper.log 2>&1
```

Add daily status update (runs every day at 3 AM):
```cron
0 3 * * * /home/ubuntu/grant_guide/venv/bin/python /home/ubuntu/grant_guide/manage.py update_statuses >> /var/log/grant-guide/status-update.log 2>&1
```

## Useful Commands

### Application Management

```bash
# Restart application
sudo systemctl restart grant-guide

# View logs
sudo journalctl -u grant-guide -f

# Check status
sudo systemctl status grant-guide
```

### Database Management

```bash
# Backup database
pg_dump -U grant_guide grant_guide > backup_$(date +%Y%m%d).sql

# Restore database
psql -U grant_guide grant_guide < backup_20240119.sql

# Access database
sudo -u postgres psql grant_guide
```

### Django Management

```bash
# Activate virtual environment first
cd /home/ubuntu/grant_guide
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run scraper
python manage.py scrape_opportunities

# Update statuses
python manage.py update_statuses

# Django shell
python manage.py shell
```

### Update Application

```bash
cd /home/ubuntu/grant_guide
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart grant-guide
```

## Troubleshooting

### Application won't start
```bash
# Check logs
sudo journalctl -u grant-guide -n 50

# Check socket file
ls -la /home/ubuntu/grant_guide/grant_guide.sock

# Test manually
cd /home/ubuntu/grant_guide
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### Database connection issues
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U grant_guide -h localhost -d grant_guide

# Check pg_hba.conf
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

### Nginx issues
```bash
# Check nginx config
sudo nginx -t

# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Restart nginx
sudo systemctl restart nginx
```

### Permission issues
```bash
# Fix ownership
sudo chown -R ubuntu:www-data /home/ubuntu/grant_guide
sudo chmod -R 755 /home/ubuntu/grant_guide

# Fix socket permissions
sudo chmod 660 /home/ubuntu/grant_guide/grant_guide.sock
```

## Security Checklist

- [ ] Changed default `DJANGO_SECRET_KEY`
- [ ] Changed default `POSTGRES_PASSWORD`
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configured `DJANGO_ALLOWED_HOSTS`
- [ ] SSL certificate installed
- [ ] Firewall configured (UFW)
- [ ] Regular backups scheduled
- [ ] Strong admin password
- [ ] SSH key-based authentication only
- [ ] Fail2ban installed

## Firewall Setup

```bash
# Install UFW
sudo apt install -y ufw

# Configure firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

## Monitoring

### Setup basic monitoring

```bash
# Install htop
sudo apt install -y htop

# Check system resources
htop

# Check disk usage
df -h

# Check memory
free -h
```

## Performance Tuning

### PostgreSQL

Edit `/etc/postgresql/14/main/postgresql.conf`:

```ini
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 2621kB
min_wal_size = 1GB
max_wal_size = 4GB
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### Gunicorn Workers

Adjust workers based on CPU cores:
```
workers = (2 x CPU cores) + 1
```

For 2 CPU cores: `--workers 5`

## Cost Estimate

- **Server**: $10-20/month (2-4 GB RAM)
- **Domain**: ~$10-15/year
- **SSL**: Free (Let's Encrypt)

**Total**: ~$10-20/month + domain
