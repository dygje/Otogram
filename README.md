# 🤖 Otogram - Advanced Telegram Automation System

> **Production-ready Telegram mass messaging automation with intelligent blacklist management and comprehensive bot interface.**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)
[![Formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pyrofork](https://img.shields.io/badge/Pyrofork-2.3.68-green.svg)](https://github.com/Mayuri-Chan/pyrofork)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](https://github.com/dygje/Otogram/actions)

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/dygje/Otogram.git
cd Otogram

# 2. Install dependencies
make install-dev

# 3. Setup MongoDB
make db-setup
# OR use Docker: docker run -d -p 27017:27017 --name otogram-mongo mongo:7.0

# 4. Setup credentials
cp .env.example .env
# Edit .env with your Telegram credentials

# 5. Health check
make health

# 6. Run Otogram
make run
```

## 🐳 Docker Quick Start

```bash
# 1. Clone repository
git clone https://github.com/dygje/Otogram.git
cd Otogram

# 2. Setup environment
cp .env.example .env
# Edit .env with your credentials

# 3. Run with Docker Compose
docker-compose up -d
```

## ✨ Key Features

### 🎯 **Advanced Broadcasting System**
- **MTProto Integration** - Direct Telegram API via Pyrofork for maximum reliability
- **Smart Blacklist Management** - Automatic handling of SlowMode, FloodWait, and permanent errors  
- **Intelligent Scheduling** - Random delays (5-10s messages, 1.1-1.3h cycles) for natural behavior
- **Real-time Dashboard** - Complete system control through Telegram bot interface

### 🛡️ **Intelligent Blacklist Management**
- **Automatic Cleanup** - Expired temporary blacklists removed at cycle start
- **Error Classification** - Smart handling of permanent vs temporary errors
- **SlowMode Detection** - Automatic skip and retry after duration expires  
- **FloodWait Handling** - Records Telegram-specified wait times and respects them
- **Comprehensive Error Mapping** - Handles all Telegram API error types

### 🎛️ **Advanced Management Interface**
- **Modern Telegram Bot** - Intuitive dashboard with keyboard navigation
- **Message CRUD** - Add, edit, delete, and manage broadcast messages
- **Group Management** - Single and bulk group operations (ID/username/link support)
- **Real-time Configuration** - Modify delays, limits, and settings without restart
- **Analytics Dashboard** - Broadcasting stats, success rates, and system health

## 🏗️ Production-Ready Architecture

- **Language**: Python 3.11+ with comprehensive type hints
- **MTProto Client**: Pyrofork 2.3.68 (latest Pyrogram fork)
- **Bot Framework**: python-telegram-bot 20.8 for management interface
- **Database**: MongoDB 4.4+ with optimized indexes and aggregation
- **Design Pattern**: Clean Architecture with SOLID principles

```
src/
├── core/           # Infrastructure (config, database, logging)
├── models/         # Domain entities with Pydantic validation  
├── services/       # Business logic layer (messages, groups, blacklist)
└── telegram/       # Interface layer (management bot + userbot)
    ├── bot_manager.py     # Orchestrates both bots
    ├── management_bot.py  # Modern dashboard interface
    ├── userbot.py         # MTProto broadcasting engine
    └── handlers/          # Command and callback handlers
```

## 🎯 **System Specifications Match**

✅ **Authentication**: MTProto with phone number + OTP + 2FA support  
✅ **Blacklist Cleanup**: Automatic cleanup at start of each cycle  
✅ **Error Handling**: SlowMode skip + continue, FloodWait duration respect  
✅ **Message Delays**: Random 5-10 seconds between messages  
✅ **Cycle Delays**: Random 1.1-1.3 hours between broadcast cycles  
✅ **Management**: Complete CRUD operations via Telegram bot  
✅ **Group Support**: ID (-100xxx), username (@group), and t.me links  
✅ **Clean Architecture**: Modern Python with maintainable code structure
├── models/         # Domain entities with Pydantic
├── services/       # Business logic layer
└── telegram/       # Interface layer (bot + userbot)
```

## 📋 System Requirements

### Core Requirements
- **Python**: 3.11+ (tested with 3.11.13)
- **MongoDB**: 4.4+ (local instance or MongoDB Atlas)
- **RAM**: 1GB minimum, 2GB recommended for optimal performance
- **OS**: Linux (Ubuntu 20.04+), macOS 12+, Windows 10+

### Telegram Requirements
- **API Credentials**: Get from [my.telegram.org](https://my.telegram.org) → API Development Tools
- **Bot Token**: Create via [@BotFather](https://t.me/BotFather) → `/newbot`
- **Phone Number**: International format (+country_code) for MTProto auth

## 🛠️ Installation & Setup

### 1. Environment Preparation

```bash
# Clone repository
git clone https://github.com/dygje/Otogram.git
cd Otogram

# Install all dependencies
pip install -e ".[dev]"

# Setup MongoDB (choose one)
# Option A: Local MongoDB
mkdir -p mongodb_data
mongod --dbpath mongodb_data --fork --logpath logs/mongodb.log

# Option B: System MongoDB
sudo systemctl start mongod

# Option C: Docker MongoDB
docker run -d -p 27017:27017 --name otogram-mongo mongo:4.4
```

### 2. Configuration Setup

**Step 1: Copy environment template**
```bash
cp .env.example .env
```

**Step 2: Configure credentials in .env**
```env
# Telegram API (from my.telegram.org)
TELEGRAM_API_ID=21507942
TELEGRAM_API_HASH=399fae9734796b25b068050f5f03b698

# Bot token (from @BotFather)  
TELEGRAM_BOT_TOKEN=8118820592:AAFX05zaXmmW3nWY2pM7s90Pbqn8f1ptc0M

# Phone number (international format)
TELEGRAM_PHONE_NUMBER=+6282298147520

# Database (adjust if needed)
MONGO_URL=mongodb://localhost:27017
```

**Step 3: Health check**
```bash
python scripts/health_check.py
# Expected: "🎉 System is HEALTHY and ready to run!"
```
# Edit .env with your credentials
```

### 3. Verify Installation

```bash
make health
```

Expected output:
```
🎉 System is HEALTHY and ready to run!
```

## 🎮 Usage

### Start System
```bash
make run
# or directly: python main.py
```

### Bot Commands Overview
| Command | Description |
|---------|-------------|
| `/start` | Initialize bot interface |
| `/menu` | Main dashboard with quick actions |
| `/messages` | Manage broadcast messages |
| `/groups` | Manage target groups |
| `/config` | System configuration |
| `/status` | Real-time system status & statistics |

### Basic Workflow

1. **Setup Messages**: `/messages` → Add your broadcast content
2. **Add Groups**: `/groups` → Import target groups (ID/username/links)  
3. **Configure**: `/config` → Set delays and safety limits
4. **Monitor**: `/status` → Track system performance and health

## 🔧 Development

### Development Commands

```bash
make help          # Show all available commands
make setup         # Complete development setup  
make health        # Run health check
make test          # Run test suite with coverage
make ruff          # Run ruff linting and formatting
make lint          # Run all linting tools
make format        # Format code with ruff and black
make security      # Run security checks
make clean         # Clean temporary files
```

### Code Quality & Modern Tools

```bash
# Format code with modern tools
make ruff          # Ruff (fast Python linter & formatter)
make format        # Black + isort + ruff

# Run all quality checks
make quality       # Lint + fast tests
make ci-test       # Full CI pipeline

# Security scanning
make security      # Bandit + Safety checks
```
### Pre-commit Hooks & Docker

```bash
# Install pre-commit hooks (runs automatically on commit)
make pre-commit

# Run manually on all files
make pre-commit-run

# Docker development
docker-compose up -d        # Run with Docker
docker-compose logs -f      # View logs
docker-compose down         # Stop services
```
```

## 📊 Monitoring & Safety

### Performance Metrics
- **Throughput**: ~100-200 messages per hour (safe rate)
- **Groups**: Supports 1000+ groups efficiently  
- **Memory**: ~50MB RAM usage
- **Database**: Optimized MongoDB queries with indexes

### Safety Limits
- **Message Delays**: 5-10 seconds between messages
- **Cycle Delays**: 1-2 hours between broadcast cycles
- **Group Limits**: Max 50 groups per cycle (configurable)
- **Daily Limits**: Max 1000 messages per day (configurable)

### Error Handling
- **Permanent Errors** → Auto-blacklist forever
- **Temporary Errors** → Auto-blacklist with recovery timer
- **Unknown Errors** → Log and continue with next group

## 🔍 Troubleshooting

### Health Check
```bash
make health
```

### Common Issues

**Authentication Failed**
```bash
make clean-sessions
python main.py
```

**Database Connection Error** 
```bash
# Check MongoDB status
sudo systemctl status mongod

# Or use Docker
docker run -d -p 27017:27017 mongo:4.4
```

**Bot Not Responding**
1. Verify bot token with [@BotFather](https://t.me/BotFather)
2. Check network: `ping api.telegram.org`
3. Test credentials in health check

### Getting Help

1. **Documentation**: [Full docs](https://dygje.github.io/Otogram)
2. **Health Check**: `make health`
3. **Logs**: `tail -f logs/app.log`
4. **Issues**: [GitHub Issues](https://github.com/dygje/Otogram/issues)

## 📚 Documentation

### 🚀 Quick Start
- **[Getting Started](docs/GETTING_STARTED.md)** - 5-minute setup guide
- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed installation & configuration

### 📖 Complete Documentation
- **[📚 Documentation Hub](docs/README.md)** - Complete documentation index
- **[🏗️ API Reference](docs/API.md)** - Complete API documentation  
- **[🏛️ Architecture](docs/ARCHITECTURE.md)** - System design and patterns
- **[🚀 Deployment](docs/DEPLOYMENT.md)** - Production deployment guide
- **[💻 Development](docs/DEVELOPMENT.md)** - Contributing and development

### 📋 Project Information
- **[🔒 Security Policy](docs/SECURITY.md)** - Security guidelines
- **[🤝 Contributing](docs/CONTRIBUTING.md)** - How to contribute
- **[📝 Changelog](docs/CHANGELOG.md)** - Version history

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

```bash
# Quick start for contributors
git clone https://github.com/dygje/Otogram.git
cd Otogram
make setup
make pre-commit
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚡ Recent Updates & Status

- ✅ **v2.0.2 (August 2025)**: Production-ready release with comprehensive verification
- ✅ **System Health**: All 7/7 health checks passing  
- ✅ **Architecture**: Clean architecture with SOLID principles implemented
- ✅ **Dependencies**: Latest Pyrofork 2.3.68 + python-telegram-bot 20.8
- ✅ **Testing**: Complete system verification and specification compliance
- ✅ **Documentation**: Comprehensive guides with verified examples
- ✅ **Database**: MongoDB 7.0.23 with optimized indexes
- ✅ **Error Handling**: Intelligent blacklist management for all Telegram API errors

**Current Status: 🟢 PRODUCTION READY**

See [CHANGELOG.md](docs/CHANGELOG.md) for detailed version history and [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for complete installation instructions.

---

**Built with modern Python best practices & production-ready architecture** 🚀