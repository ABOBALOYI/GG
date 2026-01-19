# Grant Guide South Africa - Django Application Dockerfile
# Python 3.12 base image for Django application

FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=grant_guide.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy project files
COPY . .

# Collect static files (for production)
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Create non-root user for security
RUN addgroup --system --gid 1001 django \
    && adduser --system --uid 1001 --gid 1001 django \
    && chown -R django:django /app

USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/admin/ || exit 1

# Default command - use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "grant_guide.wsgi:application"]
