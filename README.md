# 🤖 Otogram - Telegram Automation System

> **Personal Telegram mass messaging automation with intelligent blacklist management**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-D7FF64.svg)](https://github.com/astral-sh/ruff)

## ⚡ Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/dygje/Otogram.git
cd Otogram
make setup

# 2. Setup MongoDB
docker run -d -p 27017:27017 --name otogram-mongo mongo:7.0

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
- **🔒 Production Ready** - Built with clean architecture and modern Python

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

- **Python**: 3.11+ 
- **MongoDB**: 4.4+ (local or Docker)
- **Telegram API**: Get from [my.telegram.org](https://my.telegram.org)
- **Bot Token**: Create via [@BotFather](https://t.me/BotFather)

## 🎮 Usage

### Bot Commands
| Command | Description |
|---------|-------------|
| `/start` | Initialize bot dashboard |
| `/menu` | Main control panel |
| `/messages` | Manage broadcast messages |
| `/groups` | Manage target groups |
| `/status` | System status & statistics |

### Development Commands
```bash
make help          # Show all commands
make health        # System health check
make test          # Run test suite
make format        # Format code
make clean         # Clean temporary files
```

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

# Safety settings (recommended for beginners)
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

# Start full stack
docker-compose up -d

# Check status
docker-compose ps
```

## 🚨 Troubleshooting

**Database Error:**
```bash
# Check MongoDB
sudo systemctl status mongod
# Or Docker: docker ps | grep mongo
```

**Authentication Failed:**
```bash
make clean-sessions
make run
```

**Bot Not Responding:**
1. Verify bot token with @BotFather
2. Check logs: `tail -f logs/app.log`
3. Run health check: `make health`

## 📚 Documentation

- **[🚀 Getting Started](docs/GETTING_STARTED.md)** - Complete setup guide
- **[🏗️ Architecture](docs/ARCHITECTURE.md)** - System design overview
- **[🔒 Security](docs/SECURITY.md)** - Security guidelines
- **[📝 Contributing](docs/CONTRIBUTING.md)** - Development guide

## 📊 System Features

### 🎯 Broadcasting System
- MTProto integration via Pyrofork for maximum reliability
- Random delays (5-10s messages, 1.1-1.3h cycles) for natural behavior
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

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤖 About

**Otogram** is a personal project built with modern Python practices and clean architecture principles. 

**Status**: Active Development | **Version**: 2.0.2

---

**⚠️ Disclaimer**: Use responsibly and in compliance with Telegram's Terms of Service.