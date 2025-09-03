# 🤖 Otogram - Advanced Telegram Automation System

> **Production-ready Telegram mass messaging automation with intelligent blacklist management and comprehensive bot interface.**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pyrofork](https://img.shields.io/badge/Pyrofork-2.3.68-green.svg)](https://github.com/Mayuri-Chan/pyrofork)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -e ".[dev]"

# 2. Setup MongoDB
mkdir -p mongodb_data && mongod --dbpath mongodb_data --fork --logpath logs/mongodb.log

# 3. Setup credentials
cp .env.example .env
# Edit .env with your Telegram credentials

# 4. Health check
python scripts/health_check.py

# 5. Run system
python main.py
```

## ✨ Key Features

### 🎯 **Advanced Broadcasting System**
- **MTProto Integration** - Direct Telegram API via Pyrofork for maximum reliability
- **Smart Blacklist Management** - Automatic handling of SlowMode, FloodWait, and permanent errors  
- **Intelligent Scheduling** - Random delays (5-10s messages, 1.1-1.3h cycles) for natural behavior
- **Real-time Dashboard** - Complete system control through Telegram bot interface

### 🛡️ **Safety & Reliability**
- **Smart Blacklist** - Auto-blacklist problematic groups (temporary/permanent)
- **Flood Protection** - Anti-flood with dynamic delays
- **Error Recovery** - Auto-recovery from Telegram errors
- **Rate Limiting** - Smart retry with exponential backoff

### 🎛️ **Management Interface**
- **Telegram Bot** - Complete system control through Telegram
- **Message Management** - CRUD operations for broadcast messages
- **Group Management** - Bulk import and organize target groups
- **Configuration** - Flexible system settings and monitoring

## 🏗️ Modern Architecture

- **Language**: Python 3.11+ with type hints
- **Framework**: Pyrofork (MTProto) + python-telegram-bot
- **Database**: MongoDB with optimized indexes
- **Pattern**: Clean Architecture with separation of concerns

```
src/
├── core/           # Infrastructure (config, database)
├── models/         # Domain entities with Pydantic
├── services/       # Business logic layer
└── telegram/       # Interface layer (bot + userbot)
```

## 📋 Requirements

### System Requirements
- **Python**: 3.11+ (with type checking)
- **MongoDB**: 4.4+ (local or cloud)
- **RAM**: 1GB minimum, 2GB recommended
- **OS**: Ubuntu 20.04+, macOS 12+, Windows 10+

### Telegram Requirements
- **API Credentials** from [my.telegram.org](https://my.telegram.org)
- **Bot Token** from [@BotFather](https://t.me/BotFather)
- **Phone Number** for userbot authentication

## 🛠️ Installation & Setup

### 1. Clone & Install

```bash
git clone https://github.com/dygje/Otogram.git
cd Otogram
pip install -e ".[dev]"
```

### 2. Environment Setup

**Interactive Setup (Recommended)**
```bash
make setup-wizard
```

**Manual Setup**
```bash
cp .env.example .env
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
make test          # Run test suite
make lint          # Run code linting
make format        # Format code with black
make clean         # Clean temporary files
```

### Code Quality

```bash
# Format code
make format

# Run all quality checks
make lint

# Run tests with coverage
make test
```

### Pre-commit Hooks

```bash
# Install hooks (runs automatically on commit)
make pre-commit

# Run manually on all files
pre-commit run --all-files
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

| Resource | Description |
|----------|-------------|
| [**Full Documentation**](https://dygje.github.io/Otogram) | Complete user and API docs |
| [Getting Started](docs/GETTING_STARTED.md) | Setup and basic usage |
| [API Reference](docs/API.md) | Code interfaces |
| [Contributing](docs/CONTRIBUTING.md) | Development guide |

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

## ⚡ Recent Updates

- ✅ **v2.0.1**: Migrated from pyrogram to pyrofork for continued support
- ✅ **v2.0.0**: Complete rewrite with clean architecture
- ✅ **Professional Setup**: Modern Python tooling (black, mypy, pytest)
- ✅ **CI/CD Pipeline**: Automated testing and quality checks
- ✅ **Type Safety**: Full type hints and validation
- ✅ **Documentation**: Comprehensive docs with MkDocs

See [CHANGELOG.md](docs/CHANGELOG.md) for detailed version history.

---

**Built with modern Python best practices & production-ready architecture** 🚀