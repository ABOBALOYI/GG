#!/bin/bash
# Deployment script for Grant Guide South Africa

set -e

echo "🚀 Starting deployment..."

# Pull latest code
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Build and start containers
echo "🏗️  Building and starting containers..."
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

# Create superuser if needed (optional)
# docker-compose -f docker-compose.prod.yml exec -T web python manage.py createsuperuser --noinput || true

# Check container status
echo "✅ Checking container status..."
docker-compose -f docker-compose.prod.yml ps

echo "🎉 Deployment complete!"
echo "📊 View logs: docker-compose -f docker-compose.prod.yml logs -f"
