# Deployment Guide

This guide covers deploying the E-commerce FastAPI backend to production.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Production Setup](#production-setup)
3. [Database Setup](#database-setup)
4. [Environment Configuration](#environment-configuration)
5. [Deployment Options](#deployment-options)
6. [Health Checks](#health-checks)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Python 3.8+
- PostgreSQL or MySQL (recommended for production)
- Gunicorn or similar ASGI server
- Nginx or Apache for reverse proxy
- SSL certificate (for HTTPS)
- Domain name (optional but recommended)

---

## Production Setup

### 1. System Requirements

**Minimum:**
- 1GB RAM
- 1 CPU
- 10GB Storage

**Recommended:**
- 2GB RAM
- 2 CPUs
- 20GB Storage

### 2. Create Production User (Linux)

```bash
# Create dedicated user for the app
sudo useradd -m -s /bin/bash ecomapp

# Switch to that user
sudo su - ecomapp
```

### 3. Clone and Setup

```bash
cd /home/ecomapp

# Clone repository
git clone https://github.com/your-repo/ecommerce-backend.git
cd ecommerce-backend/Backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn  # ASGI server
```

---

## Database Setup

### PostgreSQL (Recommended)

#### Option 1: Local Installation

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'your_secure_password';

ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce_user SET default_transaction_deferrable TO on;
ALTER ROLE ecommerce_user SET default_transaction_read_only TO off;

GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

#### Option 2: Cloud Database (AWS RDS, Azure, DigitalOcean)

```bash
# No installation needed, just use the connection string
```

### MySQL

```bash
# Install MySQL
sudo apt-get install mysql-server

# Create database
mysql -u root -p
```

```sql
CREATE DATABASE ecommerce_db;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## Environment Configuration

### 1. Create Production .env

```bash
cp .env.example .env
nano .env  # or vim .env
```

```env
# PostgreSQL
DATABASE_URL=postgresql://ecommerce_user:your_secure_password@localhost:5432/ecommerce_db

# MySQL
# DATABASE_URL=mysql+pymysql://ecommerce_user:your_secure_password@localhost:3306/ecommerce_db

# Generate a new secret key
SECRET_KEY=generate-a-long-random-string-here-use-openssl-rand-hex-32

# Security
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30

# CORS (restrict to your frontend domain)
# Update in main.py: allow_origins=["https://your-frontend-domain.com"]
```

### 2. Generate Secret Key

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Secure .env File

```bash
chmod 600 .env  # Only owner can read/write
```

---

## Deployment Options

### Option 1: Traditional VPS with Gunicorn + Nginx

#### 1. Configure Gunicorn

Create `gunicorn_config.py`:

```python
import multiprocessing

# Gunicorn configuration
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 10000
max_requests_jitter = 1000
timeout = 60
keepalive = 2
access_log = "/home/ecomapp/logs/access.log"
error_log = "/home/ecomapp/logs/error.log"
loglevel = "info"
```

#### 2. Create Systemd Service

Create `/etc/systemd/system/ecommerce-api.service`:

```ini
[Unit]
Description=E-commerce API
After=network.target

[Service]
Type=notify
User=ecomapp
WorkingDirectory=/home/ecomapp/ecommerce-backend/Backend
Environment="PATH=/home/ecomapp/ecommerce-backend/Backend/venv/bin"
ExecStart=/home/ecomapp/ecommerce-backend/Backend/venv/bin/gunicorn -c gunicorn_config.py main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 3. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable ecommerce-api
sudo systemctl start ecommerce-api
sudo systemctl status ecommerce-api
```

#### 4. Configure Nginx

Create `/etc/nginx/sites-available/ecommerce-api`:

```nginx
upstream ecommerce_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    # Proxy settings
    location / {
        proxy_pass http://ecommerce_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files (if applicable)
    location /static/ {
        alias /home/ecomapp/ecommerce-backend/Backend/static/;
        expires 30d;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/ecommerce-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. SSL Certificate (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

---

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Run migrations and start server
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ecommerce_db
      POSTGRES_USER: ecommerce_user
      POSTGRES_PASSWORD: your_secure_password
    ports:
      - "5432:5432"

  api:
    build: ./Backend
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://ecommerce_user:your_secure_password@db:5432/ecommerce_db
      SECRET_KEY: your-secret-key
    volumes:
      - ./Backend:/app

volumes:
  postgres_data:
```

Deploy:

```bash
docker-compose up -d
docker-compose logs -f api
```

---

### Option 3: Cloud Platform (Heroku, Railway, Render)

#### Heroku Deployment

1. Install Heroku CLI
2. Create `Procfile`:

```
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT main:app
```

3. Deploy:

```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

---

## Health Checks

### Application Health

```bash
curl -X GET "https://your-domain.com/health"
```

### Database Health

```bash
curl -X GET "https://your-domain.com/docs"  # If docs work, DB is connected
```

### Monitor Logs

```bash
# Systemd
sudo journalctl -u ecommerce-api -f

# Docker
docker-compose logs -f api

# Files
tail -f /home/ecomapp/logs/access.log
tail -f /home/ecomapp/logs/error.log
```

---

## Monitoring

### Tools

- **PM2 Plus**: Monitor and manage Node.js/Python apps
- **New Relic**: Application performance monitoring
- **Datadog**: Infrastructure and application monitoring
- **Sentry**: Error tracking and performance monitoring

### Sentry Setup

```bash
pip install sentry-sdk
```

In `main.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1
)
```

---

## Troubleshooting

### Database Connection Failed

```bash
# Check connection
psql -h localhost -U ecommerce_user -d ecommerce_db

# Test from app
python -c "from database import engine; print(engine.connect())"
```

### Port Already in Use

```bash
lsof -i :8000
kill -9 <PID>
```

### Permission Denied

```bash
# Check ownership
ls -la /home/ecomapp/
# Fix permissions
sudo chown -R ecomapp:ecomapp /home/ecomapp/ecommerce-backend
```

### Nginx Not Routing

```bash
# Test configuration
sudo nginx -t

# Check upstream
curl 127.0.0.1:8000/health

# Check DNS
nslookup your-domain.com
```

### Out of Memory

```bash
# Check memory
free -h

# Reduce workers in gunicorn_config.py
workers = 2  # Instead of CPU count
```

---

## Performance Optimization

### 1. Database Indexing

```sql
CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_order_user_id ON Orders(user_id);
CREATE INDEX idx_orderitem_order_id ON order_items(order_id);
```

### 2. Caching

```python
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

@app.get("/api/products/")
@cached(expire=300)
async def get_products():
    ...
```

### 3. Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40
)
```

---

## Backup Strategy

### Automated Backups

```bash
# Create backup script
#!/bin/bash
pg_dump -h localhost -U ecommerce_user ecommerce_db > /backups/ecommerce_$(date +%Y%m%d_%H%M%S).sql

# Schedule with cron
0 2 * * * /home/ecomapp/backup.sh
```

### Restore from Backup

```bash
psql -h localhost -U ecommerce_user ecommerce_db < backup.sql
```

---

## Security Checklist

- [ ] Change SECRET_KEY to a secure random string
- [ ] Set up HTTPS with valid SSL certificate
- [ ] Restrict CORS to frontend domain
- [ ] Enable database user permissions properly
- [ ] Use environment variables for all secrets
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Database backups enabled
- [ ] Log monitoring active
- [ ] Rate limiting configured

---

## Useful Commands

```bash
# View app status
systemctl status ecommerce-api

# Restart app
systemctl restart ecommerce-api

# View database info
psql -l  # list databases

# Clear database (WARNING - destructive!)
python -c "from database import Base, engine; Base.metadata.drop_all(engine)"

# Reinitialize database
python -c "from database import Base, engine; Base.metadata.create_all(engine)"
```

---

## Support

For deployment issues:
1. Check logs
2. Verify environment variables
3. Test database connection
4. Review firewall settings
5. Consult Nginx/Gunicorn documentation
