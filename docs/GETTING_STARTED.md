# 🚀 Quick Start Guide

> **Get Otogram running in 5 minutes**

## ⚡ Quick Setup

### 1. Install & Setup
```bash
# Clone and install
git clone https://github.com/dygje/Otogram.git
cd Otogram
make install-dev

# Setup MongoDB (choose one)
docker run -d -p 27017:27017 --name otogram-mongo mongo:7.0
# OR: make db-setup  # for local MongoDB
```

### 2. Configure Credentials
```bash
# Copy template and edit
cp .env.example .env
nano .env
```

Fill in these **required** credentials:
```env
# Get from https://my.telegram.org
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_here

# Get from @BotFather
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Your phone number
TELEGRAM_PHONE_NUMBER=+628123456789
```

### 3. Run & Verify
```bash
# Health check
make health
# Expected: "🎉 System is HEALTHY and ready to run!"

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

## 🔧 Common Commands

```bash
make health        # Check system status
make run          # Start the system
make clean        # Clean temporary files
make format       # Format code
make test         # Run tests
```

## 🚨 Troubleshooting

**Database issues:**
```bash
# Check MongoDB
sudo systemctl status mongod
# Or Docker: docker ps | grep mongo
```

**Authentication issues:**
```bash
make clean-sessions
make run
```

**Bot not responding:**
1. Verify bot token with @BotFather
2. Check logs: `tail -f logs/app.log`

## 🔒 Safety Settings

Start with conservative settings:
```env
MIN_MESSAGE_DELAY=8
MAX_MESSAGE_DELAY=15  
MIN_CYCLE_DELAY_HOURS=2.0
MAX_CYCLE_DELAY_HOURS=3.0
MAX_GROUPS_PER_CYCLE=20
```

## 📚 Next Steps

- **Production deployment**: Use `docker-compose.yml`
- **Advanced configuration**: Edit `.env` file settings
- **System monitoring**: Use `/status` command in bot
- **Security**: Review [Security Guidelines](SECURITY.md)

---

**Status**: Personal Project Ready 🟢 | **Version**: 2.0.2