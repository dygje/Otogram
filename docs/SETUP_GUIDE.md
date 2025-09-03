# 🚀 Otogram Setup Guide

> **Complete installation and configuration guide for Otogram - Advanced Telegram Automation System**

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+), macOS 12+, Windows 10+
- **Python**: 3.11+ (3.12 recommended)
- **Memory**: 1GB minimum, 2GB recommended
- **Storage**: 500MB free space
- **Network**: Stable internet connection

### Required Accounts
- **Telegram Account**: Active phone number for userbot authentication
- **Telegram API**: Developer account at [my.telegram.org](https://my.telegram.org)
- **Bot Account**: Bot created via [@BotFather](https://t.me/BotFather)

## 🛠️ Installation Methods

### Method 1: Standard Installation (Recommended)

#### Step 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/dygje/Otogram.git
cd Otogram

# Verify you're in the right directory
ls -la  # Should show main.py, pyproject.toml, etc.
```

#### Step 2: Python Environment Setup
```bash
# Check Python version (must be 3.11+)
python --version

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Install all dependencies
make install-dev
# OR manually:
pip install -e ".[dev]"
```

#### Step 3: Database Setup
Choose one of these MongoDB options:

**Option A: Local MongoDB (Recommended for development)**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mongodb

# macOS (with Homebrew)
brew install mongodb-community

# Start MongoDB
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS

# Create data directory
mkdir -p mongodb_data
mongod --dbpath mongodb_data --fork --logpath logs/mongodb.log
```

**Option B: Docker MongoDB (Easiest)**
```bash
# Run MongoDB in Docker
docker run -d \
  --name otogram-mongo \
  -p 27017:27017 \
  -v $(pwd)/mongodb_data:/data/db \
  mongo:7.0

# Verify it's running
docker ps | grep mongo
```

**Option C: MongoDB Atlas (Cloud)**
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create free cluster
3. Get connection string
4. Use in MONGO_URL environment variable

#### Step 4: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env  # or your preferred editor
```

Fill in your credentials:
```env
# =============================================================================
# OTOGRAM - TELEGRAM AUTOMATION SYSTEM CONFIGURATION
# =============================================================================

# 🔐 TELEGRAM CREDENTIALS (REQUIRED)
# Get from https://my.telegram.org
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_here

# Get from @BotFather
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Your phone number (international format)
TELEGRAM_PHONE_NUMBER=+628123456789

# 🗄️ DATABASE
MONGO_URL=mongodb://localhost:27017
DB_NAME=otogram

# ⚙️ SYSTEM SETTINGS
LOG_LEVEL=INFO
ENABLE_DEBUG=false

# 📨 MESSAGE TIMING (SAFETY SETTINGS)
MIN_MESSAGE_DELAY=5
MAX_MESSAGE_DELAY=10
MIN_CYCLE_DELAY_HOURS=1.1
MAX_CYCLE_DELAY_HOURS=1.3

# 🛡️ SAFETY LIMITS
MAX_GROUPS_PER_CYCLE=50
MAX_MESSAGES_PER_DAY=1000
AUTO_CLEANUP_BLACKLIST=true
```

#### Step 5: Verification
```bash
# Run health check
make health

# Expected output:
# 🎉 System is HEALTHY and ready to run!
```

### Method 2: Docker Installation (Production)

#### Quick Start with Docker Compose
```bash
# Clone repository
git clone https://github.com/dygje/Otogram.git
cd Otogram

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Start full stack
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f otogram
```

#### Manual Docker Setup
```bash
# Build image
docker build -t otogram .

# Run MongoDB
docker run -d --name otogram-mongo \
  -p 27017:27017 \
  mongo:7.0

# Run Otogram
docker run -d --name otogram \
  --env-file .env \
  --link otogram-mongo:mongo \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/sessions:/app/sessions \
  otogram
```

## 🔐 Credential Setup Guide

### 1. Telegram API Credentials

**Get API ID and Hash:**
1. Go to [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Go to **API Development Tools**
4. Create new application:
   - **App title**: Otogram
   - **Short name**: otogram
   - **Platform**: Desktop
   - **Description**: Telegram automation system
5. Copy **API ID** and **API Hash**

### 2. Bot Token

**Create Telegram Bot:**
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Choose bot name: `Otogram Bot` (or your preference)
4. Choose username: `your_otogram_bot` (must end with 'bot')
5. Copy the **token** provided

**Configure Bot (Optional):**
```
/setdescription - Advanced Telegram automation system
/setabouttext - Otogram - Production-ready Telegram automation
/setuserpic - Upload a logo image
/setcommands - 
start - Initialize bot interface
menu - Main dashboard  
status - System status
help - Help center
```

### 3. Phone Number

- Use your actual phone number in international format
- Example: `+628123456789` (Indonesia), `+14155552671` (US)
- This number will be used for userbot authentication

## ⚙️ Configuration Options

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_API_ID` | - | **Required** API ID from my.telegram.org |
| `TELEGRAM_API_HASH` | - | **Required** API Hash from my.telegram.org |
| `TELEGRAM_BOT_TOKEN` | - | **Required** Bot token from @BotFather |
| `TELEGRAM_PHONE_NUMBER` | - | **Required** Phone number for userbot |
| `MONGO_URL` | `mongodb://localhost:27017` | MongoDB connection string |
| `DB_NAME` | `otogram` | Database name |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `MIN_MESSAGE_DELAY` | `5` | Minimum seconds between messages |
| `MAX_MESSAGE_DELAY` | `10` | Maximum seconds between messages |
| `MIN_CYCLE_DELAY_HOURS` | `1.1` | Minimum hours between broadcast cycles |
| `MAX_CYCLE_DELAY_HOURS` | `1.3` | Maximum hours between broadcast cycles |
| `MAX_GROUPS_PER_CYCLE` | `50` | Maximum groups per broadcast cycle |
| `MAX_MESSAGES_PER_DAY` | `1000` | Daily message sending limit |

### Safety Configuration

**Message Timing (Recommended)**:
```env
# Conservative settings (safer)
MIN_MESSAGE_DELAY=8
MAX_MESSAGE_DELAY=15
MIN_CYCLE_DELAY_HOURS=2.0
MAX_CYCLE_DELAY_HOURS=3.0

# Aggressive settings (faster, higher risk)
MIN_MESSAGE_DELAY=3
MAX_MESSAGE_DELAY=7
MIN_CYCLE_DELAY_HOURS=0.5
MAX_CYCLE_DELAY_HOURS=1.0
```

**Group & Message Limits**:
```env
# Small scale operation
MAX_GROUPS_PER_CYCLE=20
MAX_MESSAGES_PER_DAY=500

# Large scale operation
MAX_GROUPS_PER_CYCLE=100
MAX_MESSAGES_PER_DAY=2000
```

## 🚀 First Run

### 1. Start the System
```bash
# Using make command (recommended)
make run

# Or directly
python main.py
```

### 2. Initial Authentication

**Userbot Authentication:**
1. System will prompt for phone number verification
2. Enter the code sent to your Telegram
3. If 2FA is enabled, enter your password
4. Sessions are saved for future runs

**Bot Verification:**
1. Find your bot on Telegram (username from @BotFather)
2. Send `/start` to initialize
3. You should see the main dashboard

### 3. Basic Setup via Bot

**Add Your First Message:**
1. Click **📝 Messages** on dashboard
2. Click **➕ Add Message**
3. Send your broadcast message
4. Message is now ready for broadcasting

**Add Target Groups:**
1. Click **👥 Groups** on dashboard
2. Click **➕ Add Group**
3. Send group ID, username, or invite link
4. Group is added to broadcast list

**Start Broadcasting:**
1. Go to **⚙️ System Control**
2. Click **🚀 Start Broadcasting**
3. System begins automated broadcast cycles

## 🎛️ Management Interface

### Telegram Bot Dashboard

The management bot provides a modern interface with:

- **📊 Dashboard**: System overview and quick actions
- **📝 Messages**: CRUD operations for broadcast messages
- **👥 Groups**: Group management (single and bulk operations)
- **🚫 Blacklist**: View and manage blacklisted groups
- **⚙️ Settings**: System configuration
- **📈 Analytics**: Broadcasting statistics
- **🆘 Help**: Interactive tutorials and FAQ

### Command Line Interface

```bash
# Development commands
make help          # Show all available commands
make health        # System health check
make status        # Service status
make logs          # View application logs

# Quality assurance
make test          # Run test suite
make lint          # Code linting
make security      # Security checks
make format        # Code formatting

# Maintenance
make clean         # Clean temporary files
make clean-logs    # Clean log files
make clean-sessions # Clean Telegram sessions
```

## 🔍 Troubleshooting

### Common Issues

**1. Authentication Failed**
```bash
# Solution: Clean sessions and restart
make clean-sessions
python main.py
```

**2. Database Connection Error**
```bash
# Check MongoDB status
sudo systemctl status mongod

# Or start MongoDB
sudo systemctl start mongod

# For Docker:
docker ps | grep mongo
docker start otogram-mongo
```

**3. Bot Not Responding**
1. Verify bot token with [@BotFather](https://t.me/BotFather)
2. Check network connectivity: `ping api.telegram.org`
3. Review logs: `tail -f logs/app.log`

**4. Import Errors**
```bash
# Reinstall dependencies
make clean
make install-dev

# Or manually:
pip uninstall -y otogram
pip install -e ".[dev]"
```

**5. Permission Errors (Linux)**
```bash
# Fix ownership
sudo chown -R $USER:$USER .

# Fix permissions
chmod +x scripts/*.py
```

### Health Check Debugging

```bash
# Run comprehensive health check
make health

# If health check fails:
python scripts/health_check.py --verbose

# Check specific components:
python -c "from src.core.config import settings; print(settings.is_configured())"
python -c "from src.core.database import database; import asyncio; asyncio.run(database.connect())"
```

### Log Analysis

```bash
# Application logs
tail -f logs/app.log

# MongoDB logs (if local)
tail -f logs/mongodb.log

# System logs (Linux)
journalctl -u mongod -f

# Docker logs
docker-compose logs -f otogram
docker-compose logs -f mongodb
```

## 🔒 Security Best Practices

### Credential Security
- Never commit `.env` file to version control
- Use environment variables in production
- Rotate API keys periodically
- Use separate credentials for development/production

### Network Security
- Run behind firewall in production
- Restrict MongoDB access to localhost only
- Use VPN for remote management
- Monitor network traffic for anomalies

### Operational Security
- Use dedicated Telegram account for automation
- Set appropriate rate limits for your use case
- Monitor blacklist for unusual patterns
- Regular backup of database and sessions

### Production Deployment
```bash
# Use production-ready configurations
LOG_LEVEL=WARNING
ENABLE_DEBUG=false

# Implement monitoring
# - System resource usage
# - Database performance
# - Message delivery rates
# - Error frequency

# Setup log rotation
# - Prevent disk space issues
# - Maintain audit trail
# - Archive old logs
```

## 📊 Performance Optimization

### Database Tuning
```bash
# MongoDB optimization
# - Enable oplog
# - Configure appropriate indexes
# - Set up replication for high availability
# - Regular maintenance and compaction
```

### Resource Management
```bash
# Monitor system resources
htop
df -h
free -h

# Optimize Python performance
# - Use production WSGI server
# - Enable concurrent processing
# - Optimize memory usage
```

### Scaling Considerations
- **Horizontal Scaling**: Multiple instances with load balancing
- **Vertical Scaling**: More CPU/RAM for single instance
- **Database Sharding**: For large datasets
- **Message Queuing**: For high-volume broadcasting

## 🆘 Getting Help

### Documentation
- **API Reference**: [docs/API.md](API.md)
- **Contributing Guide**: [docs/CONTRIBUTING.md](CONTRIBUTING.md)
- **Security Policy**: [docs/SECURITY.md](SECURITY.md)

### Community Support
- **GitHub Issues**: [Report bugs and request features](https://github.com/dygje/Otogram/issues)
- **Discussions**: [Community discussions](https://github.com/dygje/Otogram/discussions)

### Professional Support
For production deployments and custom modifications, consider:
- Professional installation and configuration
- Custom feature development
- Performance tuning and optimization
- 24/7 monitoring and maintenance

---

**Last Updated**: January 2025 | **Version**: 2.0.3  
**Status**: 🟢 Production Ready

**Next Steps**: After successful setup, check out the [API Documentation](API.md) for development or start using the Telegram bot interface for management.