# 🚀 Quick Start Guide

> **Get Otogram running in 5 minutes - Personal project optimized**

## ⚡ Quick Setup

### 1. Install & Setup
```bash
# Clone and install
git clone https://github.com/dygje/Otogram.git
cd Otogram
make setup

# Setup MongoDB (Docker - recommended)
make db-start
# OR: make db-setup  # for local MongoDB installation info
```

### 2. Configure Credentials
```bash
# Copy template and edit
cp .env.example .env
nano .env    # or your preferred editor
```

Fill in these **required** credentials:
```env
# Get from https://my.telegram.org
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_here

# Get from @BotFather
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Your phone number (international format)
TELEGRAM_PHONE_NUMBER=+628123456789
```

### 3. Run & Verify
```bash
# Health check
make health
# Expected: 4/5 or 5/5 checks passed

# Start Otogram
make run
```

### 4. Bot Setup
1. Find your bot on Telegram (username from @BotFather)
2. Send `/start` → See dashboard
3. Add messages: "📝 Messages" → "➕ Add Message"
4. Add groups: "👥 Groups" → "➕ Add Group"

## 🎯 Key Features

- **📤 Mass Broadcasting**: Automated message sending to multiple groups
- **🛡️ Smart Blacklist**: Auto-handles Telegram restrictions (FloodWait, SlowMode)
- **🤖 Bot Interface**: Complete control via Telegram dashboard
- **⚙️ Safe Defaults**: Conservative settings for reliable operation
- **🔧 Personal Optimized**: Streamlined for solo development and use

## 🔧 Personal Development Commands

```bash
# Essential commands
make setup         # Complete development setup
make health        # Check system status
make run          # Start the system
make dev          # Development session (format + health)

# Development workflow
make quality       # Quick format + test (super fast)
make test-fast     # Test without coverage (quick)
make format        # Format code automatically

# Maintenance
make clean         # Clean temporary files
make clean-all     # Complete cleanup (sessions + logs)
make db-status     # Check MongoDB status
```

## 🚨 Troubleshooting

**Database issues:**
```bash
# Check and start MongoDB
make db-status     # Check if running
make db-start      # Start MongoDB container
# Or Docker: docker ps | grep mongo
```

**Authentication issues:**
```bash
make clean-sessions  # Clear Telegram sessions
make run
```

**Bot not responding:**
1. Verify bot token with @BotFather
2. Check logs: `tail -f logs/app.log`
3. Run health check: `make health`

## 🔒 Safety Settings

Start with conservative settings (already in .env.example):
```env
MIN_MESSAGE_DELAY=8
MAX_MESSAGE_DELAY=15  
MIN_CYCLE_DELAY_HOURS=2.0
MAX_CYCLE_DELAY_HOURS=3.0
MAX_GROUPS_PER_CYCLE=20
```

## 🐳 Docker Alternative

```bash
# Full Docker setup
cp .env.example .env    # Edit credentials
make docker-run         # Start everything with Docker
make docker-logs        # Check logs
make docker-stop        # Stop services
```

## 📚 Next Steps

### Personal Use
- **Start small**: Add a few groups and test
- **Monitor logs**: Check `logs/app.log` regularly
- **Use bot dashboard**: Most control via Telegram bot
- **Adjust timing**: Increase delays if getting restrictions

### Development
- **Read docs**: [Development Guide](CONTRIBUTING.md) for customization
- **Security**: Review [Security Guidelines](SECURITY.md)
- **Architecture**: [System Architecture](ARCHITECTURE.md) for deep dive

### Commands Reference
```bash
make help          # Show all available commands
make config        # Show current configuration
make first-time    # First-time setup guide
```

---

**Status**: Personal Project Ready 🟢 | **Version**: 2.0.3

**💡 Quick tip**: Start with `make dev` for development or `make run` for usage!