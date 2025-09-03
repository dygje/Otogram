# 🤖 Otogram - Telegram Automation System

> **Telegram mass messaging automation with intelligent blacklist management and bot interface.**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)
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
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890

# Bot token (from @BotFather)  
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Phone number (international format)
TELEGRAM_PHONE_NUMBER=+1234567890

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

## 📊 Features

### 🎯 **Core Features**
- **MTProto Integration** - Direct Telegram API via Pyrofork for reliability
- **Smart Blacklist Management** - Automatic handling of SlowMode, FloodWait, and errors  
- **Intelligent Scheduling** - Random delays for natural behavior
- **Management Dashboard** - Complete control through Telegram bot interface

### 🛡️ **Safety Features**
- **Error Classification** - Smart handling of permanent vs temporary errors
- **Automatic Cleanup** - Expired blacklists removed automatically
- **Rate Limiting** - Configurable delays and limits
- **Recovery System** - Auto-retry after wait periods expire

## 🔍 Troubleshooting

### Quick Fixes
```bash
# Health check
make health

# Clean sessions and restart
make clean-sessions
python main.py

# Check MongoDB
sudo systemctl status mongod
# Or use Docker: docker run -d -p 27017:27017 mongo:7.0
```

### Common Issues
- **Authentication Failed**: Clean sessions with `make clean-sessions`
- **Database Error**: Ensure MongoDB is running
- **Bot Not Responding**: Verify bot token with @BotFather

## 📚 Documentation

For detailed information, see the `docs/` folder:
- **[Setup Guide](docs/SETUP_GUIDE.md)** - Complete installation guide
- **[Architecture](docs/ARCHITECTURE.md)** - System design overview
- **[Contributing](docs/CONTRIBUTING.md)** - Development guidelines

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤖 About

Otogram is developed as a personal project using modern Python practices and clean architecture principles. Built with AI assistance from emergent.sh.

**Status**: Active Development | **Version**: 2.0.2

---

**⚠️ Disclaimer**: Use responsibly and in compliance with Telegram's Terms of Service.