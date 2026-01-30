# Deployment Guide - AWS Lightsail

This guide covers deploying Grant Guide South Africa to AWS Lightsail with CI/CD from GitHub.

## Prerequisites

- AWS Account with Lightsail access
- GitHub repository with code
- Domain name (grantsguide.co.za)
- GitHub Personal Access Token

## Step 1: Create Lightsail Instance

1. **Log in to AWS Lightsail Console**
   - Go to https://lightsail.aws.amazon.com/

2. **Create Instance**
   - Click "Create instance"
   - Choose Region: Select closest to South Africa (e.g., `eu-west-1` or `af-south-1` if available)
   - Select Platform: **Linux/Unix**
   - Select Blueprint: **OS Only** → **Ubuntu 22.04 LTS**
   - Choose Instance Plan: **$10/month** (2 GB RAM, 1 vCPU) minimum
   - Name your instance: `grant-guide-prod`
   - Click "Create instance"

3. **Configure Networking**
   - Go to instance → Networking tab
   - Create static IP and attach to instance
   - Open ports:
     - HTTP (80)
     - HTTPS (443)
     - Custom TCP (8000) - for testing only, remove later

4. **Note your Static IP**: `YOUR_LIGHTSAIL_IP`

## Step 2: Setup Lightsail Instance

1. **Connect via SSH**
   ```bash
   # Download SSH key from Lightsail console
   chmod 400 LightsailDefaultKey-*.pem
   ssh -i LightsailDefaultKey-*.pem ubuntu@YOUR_LIGHTSAIL_IP
   ```

2. **Run Setup Script**
   ```bash
   # Download and run setup script
   curl -o setup.sh https://raw.githubusercontent.com/ABOBALOYI/GG/main/grant_guide/scripts/lightsail-setup.sh
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure Environment Variables**
   ```bash
   cd /opt/grant-guide/grant_guide
   nano .env
   ```
   
   Update these values:
   ```env
   DJANGO_SECRET_KEY=<generate-with-command-below>
   POSTGRES_PASSWORD=<strong-password>
   DJANGO_ALLOWED_HOSTS=grantsguide.co.za,www.grantsguide.co.za,YOUR_LIGHTSAIL_IP
   ```
   
   Generate secret key:
   ```bash
   python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

## Step 3: Configure DNS

1. **Update DNS Records** (at your domain registrar)
   ```
   Type    Name    Value
   A       @       YOUR_LIGHTSAIL_IP
   A       www     YOUR_LIGHTSAIL_IP
   ```

2. **Wait for DNS propagation** (5-30 minutes)
   ```bash
   # Check DNS
   nslookup grantsguide.co.za
   ```

## Step 4: Deploy Application

1. **Start Services**
   ```bash
   cd /opt/grant-guide/grant_guide
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Setup SSL Certificate** (Let's Encrypt)
   ```bash
   # First, start nginx without SSL
   docker-compose -f docker-compose.prod.yml up -d nginx
   
   # Get SSL certificate
   docker-compose -f docker-compose.prod.yml run --rm certbot certonly \
     --webroot \
     --webroot-path /var/www/certbot \
     --email your-email@example.com \
     --agree-tos \
     --no-eff-email \
     -d grantsguide.co.za \
     -d www.grantsguide.co.za
   
   # Restart nginx with SSL
   docker-compose -f docker-compose.prod.yml restart nginx
   ```

3. **Run Migrations**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   ```

5. **Load Initial Data**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py create_sample_data
   ```

6. **Test the Application**
   - Visit: https://grantsguide.co.za
   - Admin: https://grantsguide.co.za/admin

## Step 5: Setup CI/CD with GitHub Actions

1. **Generate SSH Key for GitHub Actions**
   ```bash
   ssh-keygen -t ed25519 -C "github-actions" -f ~/.ssh/github_actions
   cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
   cat ~/.ssh/github_actions  # Copy this private key
   ```

2. **Add GitHub Secrets**
   
   Go to GitHub repository → Settings → Secrets and variables → Actions
   
   Add these secrets:
   
   | Secret Name | Value |
   |-------------|-------|
   | `AWS_ACCESS_KEY_ID` | Your AWS access key |
   | `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
   | `AWS_REGION` | Your AWS region (e.g., `us-east-1`) |
   | `LIGHTSAIL_HOST` | Your Lightsail static IP |
   | `LIGHTSAIL_USER` | `ubuntu` |
   | `LIGHTSAIL_SSH_KEY` | Private key from step 1 |

3. **Test CI/CD**
   ```bash
   # Make a change and push
   git add .
   git commit -m "test: CI/CD deployment"
   git push origin main
   ```
   
   Check GitHub Actions tab for deployment status.

## Step 6: Monitoring & Maintenance

### View Logs
```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Check Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

### Restart Services
```bash
# All services
docker-compose -f docker-compose.prod.yml restart

# Specific service
docker-compose -f docker-compose.prod.yml restart web
```

### Database Backup
```bash
# Backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U grant_guide grant_guide > backup_$(date +%Y%m%d).sql

# Restore
docker-compose -f docker-compose.prod.yml exec -T db psql -U grant_guide grant_guide < backup_20240119.sql
```

### Update Application
```bash
cd /opt/grant-guide
./grant_guide/scripts/deploy.sh
```

### Run Scraper Manually
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py scrape_opportunities
```

### Update Statuses
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py update_statuses
```

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs web

# Check environment variables
docker-compose -f docker-compose.prod.yml exec web env
```

### Database connection issues
```bash
# Check database is running
docker-compose -f docker-compose.prod.yml ps db

# Test connection
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

### SSL certificate issues
```bash
# Renew certificate manually
docker-compose -f docker-compose.prod.yml run --rm certbot renew

# Check certificate expiry
docker-compose -f docker-compose.prod.yml exec nginx openssl x509 -in /etc/letsencrypt/live/grantsguide.co.za/fullchain.pem -noout -dates
```

### High memory usage
```bash
# Check resource usage
docker stats

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

## Security Checklist

- [ ] Changed default `DJANGO_SECRET_KEY`
- [ ] Changed default `POSTGRES_PASSWORD`
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configured `DJANGO_ALLOWED_HOSTS`
- [ ] SSL certificate installed and working
- [ ] Firewall configured (only ports 80, 443 open)
- [ ] Regular backups scheduled
- [ ] Monitoring setup
- [ ] Strong admin password set
- [ ] SSH key-based authentication only

## Cost Estimate

- **Lightsail Instance**: $10-20/month (2-4 GB RAM)
- **Static IP**: Free (included)
- **Data Transfer**: 2 TB included
- **Domain**: ~$10-15/year
- **SSL Certificate**: Free (Let's Encrypt)

**Total**: ~$10-20/month + domain

## Support

For issues or questions:
- Check logs: `docker-compose -f docker-compose.prod.yml logs -f`
- GitHub Issues: https://github.com/ABOBALOYI/GG/issues
- Documentation: See README.md and PROJECT_STATUS.md
