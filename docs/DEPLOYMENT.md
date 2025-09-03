# 🚀 Otogram Deployment Guide

> **Production deployment guide for Otogram - Advanced Telegram Automation System**

## 📋 Deployment Options

### 1. Docker Deployment (Recommended) 🐳

#### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  otogram:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: otogram-prod
    restart: unless-stopped
    env_file:
      - .env.prod
    volumes:
      - ./logs:/app/logs
      - ./sessions:/app/sessions
      - ./backups:/app/backups
    depends_on:
      - mongodb
      - redis
    networks:
      - otogram-network
    healthcheck:
      test: ["CMD", "python", "scripts/health_check.py"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  mongodb:
    image: mongo:7.0
    container_name: otogram-mongo-prod
    restart: unless-stopped
    ports:
      - "127.0.0.1:27017:27017"
    volumes:
      - mongodb_data:/data/db
      - ./mongodb_backups:/backups
    environment:
      MONGO_INITDB_DATABASE: otogram
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
    networks:
      - otogram-network
    command: --auth --bind_ip_all

  redis:
    image: redis:7-alpine
    container_name: otogram-redis-prod
    restart: unless-stopped
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - otogram-network
    command: redis-server --requirepass ${REDIS_PASSWORD}

  nginx:
    image: nginx:alpine
    container_name: otogram-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - otogram
    networks:
      - otogram-network

volumes:
  mongodb_data:
  redis_data:

networks:
  otogram-network:
    driver: bridge
```

#### Production Environment Configuration

Create `.env.prod`:

```env
# =============================================================================
# OTOGRAM PRODUCTION CONFIGURATION
# =============================================================================

# 🔐 TELEGRAM CREDENTIALS
TELEGRAM_API_ID=your_production_api_id
TELEGRAM_API_HASH=your_production_api_hash
TELEGRAM_BOT_TOKEN=your_production_bot_token
TELEGRAM_PHONE_NUMBER=your_production_phone

# 🗄️ DATABASE (Production MongoDB with Auth)
MONGO_URL=mongodb://otogram_user:${MONGO_PASSWORD}@mongodb:27017/otogram?authSource=otogram
MONGO_ROOT_PASSWORD=secure_root_password_here
MONGO_PASSWORD=secure_user_password_here
DB_NAME=otogram

# 🔴 REDIS (Optional - for caching)
REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
REDIS_PASSWORD=secure_redis_password_here

# ⚙️ PRODUCTION SETTINGS
LOG_LEVEL=WARNING
ENABLE_DEBUG=false
DEV_MODE=false

# 📨 CONSERVATIVE MESSAGE TIMING (PRODUCTION SAFE)
MIN_MESSAGE_DELAY=8
MAX_MESSAGE_DELAY=15
MIN_CYCLE_DELAY_HOURS=2.0
MAX_CYCLE_DELAY_HOURS=3.0

# 🛡️ PRODUCTION SAFETY LIMITS
MAX_GROUPS_PER_CYCLE=30
MAX_MESSAGES_PER_DAY=800
AUTO_CLEANUP_BLACKLIST=true
BLACKLIST_CLEANUP_INTERVAL=12

# 🔒 SECURITY
SESSION_DIR=sessions
LOG_DIR=logs
```

#### Deploy with Docker Compose

```bash
# 1. Prepare production environment
cp .env.example .env.prod
# Edit .env.prod with production credentials

# 2. Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# 3. Verify deployment
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f otogram

# 4. Run health check
docker-compose -f docker-compose.prod.yml exec otogram python scripts/health_check.py
```

### 2. VPS/Cloud Server Deployment 🌐

#### Ubuntu 22.04 LTS Setup

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.11+
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# 3. Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install mongodb-org -y

# 4. Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# 5. Install additional dependencies
sudo apt install git curl build-essential nginx redis-server -y

# 6. Create application user
sudo useradd -m -s /bin/bash otogram
sudo usermod -aG sudo otogram
```

#### Application Setup

```bash
# 1. Switch to otogram user
sudo su - otogram

# 2. Clone repository
git clone https://github.com/dygje/Otogram.git
cd Otogram

# 3. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip
pip install -e ".[dev]"

# 5. Setup configuration
cp .env.example .env
# Edit .env with production credentials

# 6. Run health check
python scripts/health_check.py
```

#### Systemd Service Setup

Create `/etc/systemd/system/otogram.service`:

```ini
[Unit]
Description=Otogram Telegram Automation System
After=network.target mongod.service
Wants=mongod.service

[Service]
Type=simple
User=otogram
Group=otogram
WorkingDirectory=/home/otogram/Otogram
Environment=PATH=/home/otogram/Otogram/venv/bin
ExecStart=/home/otogram/Otogram/venv/bin/python main.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=otogram

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ReadWritePaths=/home/otogram/Otogram/logs /home/otogram/Otogram/sessions
ProtectHome=yes

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Enable service
sudo systemctl daemon-reload
sudo systemctl enable otogram
sudo systemctl start otogram

# Check status
sudo systemctl status otogram

# View logs
sudo journalctl -u otogram -f
```

### 3. Cloud Platform Deployment ☁️

#### AWS EC2 Deployment

**1. Launch EC2 Instance:**
- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.medium (minimum)
- Storage: 20GB GP3
- Security Group: Allow SSH (22), HTTP (80), HTTPS (443)

**2. Setup Application:**
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker ubuntu

# Deploy Otogram
git clone https://github.com/dygje/Otogram.git
cd Otogram
cp .env.example .env
# Edit .env with credentials

# Deploy with Docker
docker-compose -f docker-compose.prod.yml up -d
```

#### Google Cloud Platform (GCP)

**1. Create Compute Engine Instance:**
```bash
# Using gcloud CLI
gcloud compute instances create otogram-prod \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB \
    --tags=http-server,https-server
```

**2. Deploy Application:**
```bash
# SSH to instance
gcloud compute ssh otogram-prod --zone=us-central1-a

# Follow standard deployment steps
```

#### DigitalOcean Droplet

**1. Create Droplet:**
- Image: Ubuntu 22.04 LTS
- Size: Basic $12/month (2GB RAM, 50GB SSD)
- Datacenter: Choose closest to your target audience

**2. Deploy with One-Click:**
```bash
# SSH to droplet
ssh root@your-droplet-ip

# Run deployment script
curl -fsSL https://raw.githubusercontent.com/dygje/Otogram/main/scripts/deploy.sh | bash
```

## 🔧 Production Configuration

### Environment Optimization

#### Production .env Configuration

```env
# Performance settings
LOG_LEVEL=WARNING
ENABLE_DEBUG=false
DEV_MODE=false

# Conservative timing (production safe)
MIN_MESSAGE_DELAY=10
MAX_MESSAGE_DELAY=20
MIN_CYCLE_DELAY_HOURS=3.0
MAX_CYCLE_DELAY_HOURS=4.0

# Reduced limits for stability
MAX_GROUPS_PER_CYCLE=20
MAX_MESSAGES_PER_DAY=500

# Enhanced security
AUTO_CLEANUP_BLACKLIST=true
BLACKLIST_CLEANUP_INTERVAL=6
```

#### MongoDB Production Configuration

Create `/etc/mongod.conf`:

```yaml
# Network interfaces
net:
  port: 27017
  bindIp: 127.0.0.1

# Security
security:
  authorization: enabled

# Storage
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true

# Operation Profiling
operationProfiling:
  slowOpThresholdMs: 100
  mode: slowOp

# Logging
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
```

#### Nginx Reverse Proxy (Optional)

Create `/etc/nginx/sites-available/otogram`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/otogram.crt;
    ssl_certificate_key /etc/ssl/private/otogram.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # Monitoring endpoint
    location /health {
        proxy_pass http://localhost:8000;
        access_log off;
    }
    
    # Admin interface (if needed)
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoring & Logging

### Log Management

#### Logrotate Configuration

Create `/etc/logrotate.d/otogram`:

```
/home/otogram/Otogram/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 otogram otogram
    postrotate
        systemctl reload otogram
    endscript
}
```

#### Centralized Logging (Optional)

**ELK Stack Integration:**

```yaml
# docker-compose.logging.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.11.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

### Health Monitoring

#### Monitoring Script

Create `scripts/monitor.py`:

```python
#!/usr/bin/env python3
"""
Production monitoring script for Otogram
"""
import asyncio
import json
import time
from datetime import datetime, timedelta
import psutil
import subprocess
from src.core.database import database
from src.core.config import settings

async def check_system_health():
    """Comprehensive system health check"""
    health_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
        },
        "database": await check_database_health(),
        "application": await check_application_health(),
    }
    
    # Send to monitoring service (e.g., Prometheus, DataDog)
    await send_metrics(health_data)
    
    return health_data

async def check_database_health():
    """Check MongoDB health"""
    try:
        await database.connect()
        # Check if we can perform basic operations
        test_collection = database.get_collection("health_check")
        await test_collection.insert_one({"test": True, "timestamp": datetime.utcnow()})
        await test_collection.delete_many({"test": True})
        return {"status": "healthy", "connection": True}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

async def check_application_health():
    """Check application components"""
    try:
        # Check if main process is running
        result = subprocess.run(
            ["systemctl", "is-active", "otogram"],
            capture_output=True,
            text=True
        )
        
        service_status = result.stdout.strip()
        
        return {
            "service_status": service_status,
            "is_healthy": service_status == "active"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    asyncio.run(check_system_health())
```

#### Cron Job for Monitoring

```bash
# Add to crontab (crontab -e)
# Check health every 5 minutes
*/5 * * * * /home/otogram/Otogram/venv/bin/python /home/otogram/Otogram/scripts/monitor.py >> /var/log/otogram/monitor.log 2>&1

# Daily backup
0 2 * * * /home/otogram/Otogram/scripts/backup.sh

# Weekly cleanup
0 3 * * 0 /home/otogram/Otogram/scripts/cleanup.sh
```

## 🔒 Security Hardening

### System Security

#### Firewall Configuration (UFW)

```bash
# Basic firewall setup
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (change port if needed)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS (if using web interface)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow MongoDB (only from localhost)
sudo ufw allow from 127.0.0.1 to any port 27017

# Enable firewall
sudo ufw enable
```

#### SSH Hardening

Edit `/etc/ssh/sshd_config`:

```
# Disable root login
PermitRootLogin no

# Use key-based authentication only
PasswordAuthentication no
PubkeyAuthentication yes

# Change default port (optional)
Port 2222

# Limit login attempts
MaxAuthTries 3
MaxStartups 2

# Disable unused features
X11Forwarding no
AllowTcpForwarding no
```

### Application Security

#### File Permissions

```bash
# Set proper ownership
sudo chown -R otogram:otogram /home/otogram/Otogram

# Secure configuration files
chmod 600 /home/otogram/Otogram/.env
chmod 600 /home/otogram/Otogram/.env.prod

# Secure session files
chmod 700 /home/otogram/Otogram/sessions
chmod 600 /home/otogram/Otogram/sessions/*

# Secure log files
chmod 640 /home/otogram/Otogram/logs/*.log
```

#### Database Security

```bash
# Create MongoDB admin user
mongosh admin --eval '
  db.createUser({
    user: "admin",
    pwd: "secure_admin_password",
    roles: ["root"]
  })
'

# Create application user
mongosh otogram --eval '
  db.createUser({
    user: "otogram_user",
    pwd: "secure_app_password",
    roles: [
      { role: "readWrite", db: "otogram" }
    ]
  })
'
```

## 🔄 Backup & Recovery

### Database Backup

#### Automated Backup Script

Create `scripts/backup.sh`:

```bash
#!/bin/bash
# Otogram Database Backup Script

BACKUP_DIR="/home/otogram/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="otogram"

# Create backup directory
mkdir -p $BACKUP_DIR

# MongoDB backup
mongodump --db $DB_NAME --out $BACKUP_DIR/mongodb_$DATE

# Compress backup
tar -czf $BACKUP_DIR/otogram_backup_$DATE.tar.gz -C $BACKUP_DIR mongodb_$DATE
rm -rf $BACKUP_DIR/mongodb_$DATE

# Keep only last 7 days of backups
find $BACKUP_DIR -name "otogram_backup_*.tar.gz" -mtime +7 -delete

# Session files backup
tar -czf $BACKUP_DIR/sessions_$DATE.tar.gz -C /home/otogram/Otogram sessions/

echo "Backup completed: otogram_backup_$DATE.tar.gz"
```

#### Restore Process

```bash
# Stop application
sudo systemctl stop otogram

# Restore database
cd /home/otogram/backups
tar -xzf otogram_backup_YYYYMMDD_HHMMSS.tar.gz
mongorestore --db otogram --drop mongodb_YYYYMMDD_HHMMSS/otogram/

# Restore sessions (if needed)
tar -xzf sessions_YYYYMMDD_HHMMSS.tar.gz -C /home/otogram/Otogram/

# Start application
sudo systemctl start otogram
```

### Cloud Backup Integration

#### AWS S3 Backup

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Upload backup to S3
aws s3 cp otogram_backup_$DATE.tar.gz s3://your-backup-bucket/otogram/
```

## 🚀 Performance Optimization

### Database Performance

#### MongoDB Indexing

```javascript
// Connect to MongoDB
mongosh otogram

// Create performance indexes
db.messages.createIndex({ "is_active": 1 })
db.messages.createIndex({ "created_at": -1 })
db.messages.createIndex({ "usage_count": -1 })

db.groups.createIndex({ "group_id": 1 }, { unique: true })
db.groups.createIndex({ "is_active": 1 })
db.groups.createIndex({ "last_message_at": -1 })

db.blacklists.createIndex({ "group_id": 1 })
db.blacklists.createIndex({ "blacklist_type": 1 })
db.blacklists.createIndex({ "expires_at": 1 })

db.logs.createIndex({ "timestamp": -1 })
db.logs.createIndex({ "log_type": 1, "timestamp": -1 })
```

### Application Performance

#### Python Optimization

```bash
# Use production WSGI server (if web interface added)
pip install gunicorn

# Configure for production
gunicorn --workers 4 --bind 0.0.0.0:8000 main:app
```

#### Memory Management

```python
# Add to main.py for memory monitoring
import psutil
import gc

def monitor_memory():
    """Monitor and optimize memory usage"""
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    
    if memory_mb > 500:  # 500MB threshold
        gc.collect()  # Force garbage collection
        
    return memory_mb
```

## 📈 Scaling Strategies

### Horizontal Scaling

#### Load Balancer Configuration

```nginx
upstream otogram_backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://otogram_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Multi-Instance Setup

```bash
# Run multiple instances on different ports
# Instance 1
PORT=8001 python main.py &

# Instance 2  
PORT=8002 python main.py &

# Instance 3
PORT=8003 python main.py &
```

### Database Scaling

#### MongoDB Replica Set

```javascript
// Initialize replica set
rs.initiate({
  _id: "otogram-rs",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
```

## 🔍 Troubleshooting Production Issues

### Common Production Issues

#### High Memory Usage

```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head

# Optimize MongoDB
# Add to /etc/mongod.conf
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1  # Limit cache size
```

#### Database Connection Issues

```bash
# Check MongoDB status
sudo systemctl status mongod

# Check connections
mongosh --eval "db.serverStatus().connections"

# Optimize connection pool
# In .env:
MONGO_URL=mongodb://localhost:27017/otogram?maxPoolSize=10&maxIdleTimeMS=30000
```

#### High CPU Usage

```bash
# Monitor processes
htop

# Check slow queries
mongosh otogram --eval "db.setProfilingLevel(2, { slowms: 100 })"

# Optimize query performance
# Add appropriate indexes
# Optimize application logic
```

### Emergency Procedures

#### Service Recovery Script

Create `scripts/emergency_restart.sh`:

```bash
#!/bin/bash
# Emergency service recovery

echo "Starting emergency recovery..."

# Stop services
sudo systemctl stop otogram
sudo systemctl stop mongod

# Check disk space
df -h

# Clean logs if needed
if [ $(df / | awk 'NR==2 {print $5}' | sed 's/%//') -gt 90 ]; then
    echo "Disk space critical, cleaning logs..."
    find /home/otogram/Otogram/logs -name "*.log" -mtime +3 -delete
fi

# Start database
sudo systemctl start mongod
sleep 10

# Verify database
mongosh --eval "db.stats()" > /dev/null
if [ $? -eq 0 ]; then
    echo "Database is healthy"
else
    echo "Database issues detected!"
    exit 1
fi

# Start application
sudo systemctl start otogram
sleep 5

# Verify application
if sudo systemctl is-active --quiet otogram; then
    echo "Recovery successful!"
else
    echo "Recovery failed!"
    exit 1
fi
```

---

**Last Updated**: January 2025 | **Version**: 2.0.3  
**Status**: 🟢 Production Ready

**Support**: For production deployment assistance, contact the maintainers or create an issue on GitHub.