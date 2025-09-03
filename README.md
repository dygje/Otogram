# 🤖 Telegram Automation System

> **Professional Telegram mass messaging automation system with comprehensive management through Telegram Bot interface.**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](https://github.com/dygje/Otogram/actions)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://dygje.github.io/Otogram)

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -e ".[dev]"

# 2. Setup credentials (interactive wizard)
python scripts/setup.py

# 3. Run system
python main.py
```

## 🏗️ Architecture

- **Language**: Python 3.11+
- **Framework**: Pyrogram (MTProto) + python-telegram-bot
- **Database**: MongoDB 
- **Pattern**: Clean Architecture

```
src/
├── core/           # Infrastructure (config, database)
├── models/         # Domain entities  
├── services/       # Business logic
└── telegram/       # Interface layer
```

## ✨ Features

### 🎯 **Core Features**
- **Mass Broadcasting** - Kirim pesan ke multiple grup secara otomatis
- **Smart Blacklist** - Auto-blacklist grup bermasalah (temporary/permanent)
- **Telegram Bot Interface** - Kelola sistem melalui Telegram bot
- **Real-time Monitoring** - Dashboard dan analytics lengkap

### 🛡️ **Safety Features**
- **Flood Protection** - Anti-flood dengan delay dinamis
- **Error Recovery** - Auto-recovery dari error Telegram
- **Rate Limiting** - Kontrol rate sesuai limit Telegram
- **Smart Retry** - Retry dengan exponential backoff

### 🔧 **Management Features**
- **Message Management** - CRUD pesan broadcast
- **Group Management** - Kelola grup target (bulk import)
- **Configuration** - Setting sistem yang fleksibel
- **Logs & Analytics** - Tracking performance dan errors

## 📋 Requirements

### System Requirements
- **Python**: 3.11+ (recommended), minimum 3.8
- **MongoDB**: 4.4+
- **RAM**: 1GB minimum, 2GB recommended
- **OS**: Ubuntu 20.04+, macOS 12+, Windows 10+

### Telegram Requirements
- **API Credentials** dari [my.telegram.org](https://my.telegram.org)
- **Bot Token** dari [@BotFather](https://t.me/BotFather)
- **Phone Number** untuk userbot (same account as API)

## 🛠️ Installation

### 1. Clone & Dependencies

```bash
git clone <repository>
cd telegram-automation-system
pip install -r requirements.txt
```

### 2. Setup Environment

**Option A: Interactive Setup (Recommended)**
```bash
python scripts/setup.py
```

**Option B: Manual Setup**
```bash
cp .env.example .env
# Edit .env dengan credentials Anda
```

### 3. Verify Installation

```bash
python scripts/health_check.py
```

Expected output:
```
🎉 System is HEALTHY and ready to run!
```

## 🎮 Usage

### Start System
```bash
python main.py
```

### First Time Setup
1. System akan prompt untuk **OTP code** dari Telegram
2. Jika ada 2FA, masukkan **password**
3. Bot akan ready di Telegram

### Bot Commands
| Command | Description |
|---------|-------------|
| `/start` | Initialize bot interface |
| `/menu` | Main dashboard |
| `/messages` | Manage broadcast messages |
| `/groups` | Manage target groups |
| `/config` | System configuration |
| `/status` | System status & stats |
| `/blacklist` | View blacklist entries |

### Basic Workflow

1. **Add Messages**: `/messages` → Add broadcast content
2. **Add Groups**: `/groups` → Add target groups
3. **Configure**: `/config` → Adjust delays & settings
4. **Monitor**: `/status` → Check system performance

## 📊 Dashboard Features

### 🎛️ Main Dashboard
- **System Statistics** - Real-time metrics
- **Quick Actions** - Fast access to common tasks
- **Status Overview** - Health monitoring

### 📝 Message Management
- **Add/Edit Messages** - Rich text support
- **Bulk Operations** - Multiple message management
- **Usage Analytics** - Message performance tracking

### 👥 Group Management
- **Multiple Formats** - ID, username, links
- **Bulk Import** - Import many groups at once
- **Group Analytics** - Performance per group

### 🚫 Smart Blacklist
- **Auto-Detection** - Error-based blacklisting
- **Temporary Blocks** - Time-based recovery
- **Manual Control** - Override auto-decisions

## 🔧 Configuration

### Environment Variables
```bash
# Required Credentials
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_PHONE_NUMBER=+628123456789

# System Settings
LOG_LEVEL=INFO
MIN_MESSAGE_DELAY=5
MAX_MESSAGE_DELAY=10
MIN_CYCLE_DELAY_HOURS=1.1
MAX_CYCLE_DELAY_HOURS=1.3

# Safety Limits
MAX_GROUPS_PER_CYCLE=50
MAX_MESSAGES_PER_DAY=1000
```

### Advanced Configuration
Access via `/config` in bot or edit configurations in database.

## 🛡️ Safety & Best Practices

### Rate Limiting
- **Message Delays**: 5-10 seconds between messages
- **Cycle Delays**: 1-2 hours between broadcast cycles
- **Group Limits**: Max 50 groups per cycle (configurable)

### Error Handling
- **Permanent Errors** → Auto-blacklist forever
- **Temporary Errors** → Auto-blacklist with timer
- **Unknown Errors** → Log and continue

### Monitoring
- **Real-time Dashboard** via Telegram bot
- **File Logs** in `logs/` directory
- **Database Logs** untuk detailed tracking

## 📖 Development

### Health Check
```bash
python scripts/health_check.py
```

### Run Tests
```bash
python -m pytest tests/ -v
```

### Code Quality
```bash
# Format code
make format

# Run linting
make lint

# Full development setup
make dev
```

### Using Makefile
```bash
make help          # Show all available commands
make setup         # Complete development setup
make run           # Run the application
make health        # Run health check
make clean         # Clean up temporary files
```

## 🔍 Troubleshooting

### Common Issues

**Authentication Failed**
```bash
# Clear sessions and retry
rm -rf sessions/
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
1. Verify bot token dengan [@BotFather](https://t.me/BotFather)
2. Check network: `ping api.telegram.org`
3. Test token:
```bash
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Check Python version
python --version  # Should be 3.11+
```

### Getting Help

1. **Check Logs**: `tail -f logs/app.log`
2. **Run Health Check**: `python scripts/health_check.py`
3. **Bot Help**: Send `/help` to your bot
4. **Documentation**: Check `docs/` directory

## 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [Getting Started](docs/GETTING_STARTED.md) | Setup & basic usage | New users |
| [API Reference](docs/API.md) | Code interfaces | Developers |
| [Contributing](CONTRIBUTING.md) | Development guide | Contributors |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Run health check (`python scripts/health_check.py`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚡ Performance

- **Throughput**: ~100 messages per hour (safe rate)
- **Groups**: Supports 1000+ groups efficiently
- **Memory**: ~50MB RAM usage
- **Database**: Optimized MongoDB queries with indexes

## 🔄 Updates

Check [CHANGELOG.md](docs/CHANGELOG.md) for version history and updates.

---

**Built with modern Python best practices & clean architecture** 🚀