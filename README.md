# 🤖 Otogram - Personal Telegram Automation

> **Modern, intelligent Telegram mass messaging automation with smart blacklist management**

[![Python](https://img.shields.io/badge/python-3.11%7C3.12-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)

---

## ⚡ Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/dygje/Otogram.git
cd Otogram
make setup

# 2. Setup MongoDB
make db-start

# 3. Configure credentials  
cp .env.example .env
nano .env  # Add your Telegram API credentials

# 4. Verify and run
make health
make run
```

## ✨ Key Features

- **📤 Mass Broadcasting** - Send messages to multiple Telegram groups automatically
- **🛡️ Smart Blacklist Management** - Auto-handles FloodWait, SlowMode, and permanent errors
- **🤖 Telegram Bot Interface** - Complete control through modern dashboard
- **⚙️ Intelligent Scheduling** - Random delays for natural behavior
- **🔒 Personal Project Ready** - Optimized for solo development and usage

## 🏗️ Architecture

```
src/
├── core/           # Configuration & database
├── models/         # Data models with Pydantic validation  
├── services/       # Business logic layer
└── telegram/       # Bot interface & userbot engine
    ├── bot_manager.py     # Orchestrates both bots
    ├── management_bot.py  # Dashboard interface
    ├── userbot.py         # Broadcasting engine
    └── handlers/          # Command handlers
```

## 📋 Requirements

- **Python**: 3.11+ or 3.12 (recommended)
- **MongoDB**: 4.4+ (local or Docker)
- **Telegram API**: Get from [my.telegram.org](https://my.telegram.org)
- **Bot Token**: Create via [@BotFather](https://t.me/BotFather)

## 🎮 Personal Development Commands

```bash
# Essential workflow
make setup         # Complete development setup
make health        # System health check
make dev           # Development session (format + health)
make run           # Start Otogram system

# Development tools
make quality       # Quick format + test (fast)
make format        # Format code automatically
make test-fast     # Quick tests without coverage
make clean-all     # Complete cleanup

# Database management
make db-setup      # MongoDB setup options
make db-start      # Start MongoDB container
make db-status     # Check MongoDB status
```

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot dashboard |
| `/menu` | Main control panel |
| `/messages` | Manage broadcast messages |
| `/groups` | Manage target groups |
| `/status` | System status & statistics |

## 🔧 Configuration

Configure via `.env` file:

```env
# Required Telegram credentials
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_PHONE_NUMBER=+628123456789

# Database
MONGO_URL=mongodb://localhost:27017

# Safety settings (recommended for personal use)
MIN_MESSAGE_DELAY=8
MAX_MESSAGE_DELAY=15
MIN_CYCLE_DELAY_HOURS=2.0
MAX_CYCLE_DELAY_HOURS=3.0
MAX_GROUPS_PER_CYCLE=20
```

## 🐳 Docker Deployment

```bash
# Copy and edit environment
cp .env.example .env
nano .env

# Start full stack
make docker-run

# Check status
make docker-logs
```

## 🚨 Troubleshooting

**Database Error:**
```bash
make db-status      # Check MongoDB status
make db-start       # Start MongoDB container
```

**Authentication Failed:**
```bash
make clean-sessions # Clear Telegram sessions
make run
```

**Bot Not Responding:**
1. Verify bot token with @BotFather
2. Check logs: `tail -f logs/app.log`
3. Run health check: `make health`

## 🔒 Security & Safety

### Essential Practices
- **Never commit** `.env` files to git
- **Enable 2FA** on your Telegram account
- **Start with conservative settings** (included in .env.example)
- **Monitor logs** regularly: `tail -f logs/app.log`

### Safe Default Settings
```env
MIN_MESSAGE_DELAY=8          # 8-15 seconds between messages
MAX_MESSAGE_DELAY=15         # Conservative timing
MIN_CYCLE_DELAY_HOURS=2.0    # 2-3 hours between cycles
MAX_CYCLE_DELAY_HOURS=3.0    # Prevents rate limiting
MAX_GROUPS_PER_CYCLE=20      # Start small, increase gradually
```

## 📊 Personal Project Features

### 🎯 Broadcasting System
- MTProto integration via Pyrofork for maximum reliability
- Random delays (8-15s messages, 2-3h cycles) for natural behavior
- Real-time dashboard with complete system control

### 🛡️ Intelligent Error Handling
- Automatic cleanup of expired temporary blacklists
- Smart classification of permanent vs temporary errors
- FloodWait duration respect and automatic retry
- Comprehensive Telegram API error mapping

### 🎛️ Management Interface
- Modern Telegram bot with keyboard navigation
- Message CRUD operations (add, edit, delete, manage)
- Group management (ID/username/link support)
- Real-time configuration without restart
- Analytics dashboard with success rates

### 🔧 Personal Development
- Simplified testing suite (5 essential tests vs 29 extensive)
- Personal-focused documentation and workflows
- Optimized Makefile with 25+ development commands
- Essential dependencies only (optional security tools)

## 📚 Advanced Documentation

For detailed information, see the [`docs/`](docs/) folder:

- **[🚀 Getting Started](docs/GETTING_STARTED.md)** - Complete setup guide
- **[🛠️ Development Guide](docs/CONTRIBUTING.md)** - Personal development workflow
- **[🔒 Security Guidelines](docs/SECURITY.md)** - Essential safety practices
- **[🏗️ Architecture](docs/ARCHITECTURE.md)** - System design overview
- **[📝 Changelog](docs/CHANGELOG.md)** - Version history

## 🎯 Personal Use Quick Tips

### First Time Setup
1. **Get Credentials**: Visit [my.telegram.org](https://my.telegram.org) and [@BotFather](https://t.me/BotFather)
2. **Start Small**: Add 5-10 groups first, test thoroughly
3. **Monitor**: Check `logs/app.log` regularly
4. **Conservative Settings**: Use default timing, increase gradually if needed

### Daily Workflow
```bash
make dev           # Start development session
# Make your changes...
make quality       # Quick validation
make run          # Test changes
```

### Maintenance
```bash
make health        # Regular health checks
make clean-all     # Periodic cleanup
make db-status     # Monitor database
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤖 About

**Otogram** is a personal project built with modern Python practices and clean architecture principles, optimized for solo developers and personal use.

**Status**: Personal Project Ready | **Version**: 2.0.4

---

**⚠️ Disclaimer**: Use responsibly and in compliance with Telegram's Terms of Service. This is for personal automation only.