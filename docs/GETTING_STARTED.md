# 🚀 Getting Started with Otogram

Welcome to Otogram! This guide will help you get up and running with the Telegram automation system quickly.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- **MongoDB** (local or Atlas)
- **Telegram API credentials** from [my.telegram.org](https://my.telegram.org)
- **Bot token** from [@BotFather](https://t.me/BotFather)

## ⚡ Quick Setup

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/dygje/Otogram.git
cd Otogram

# Install dependencies
pip install -e ".[dev]"
```

### 2. Database Setup

Choose one option:

**Option A: Local MongoDB**
```bash
mkdir -p mongodb_data
mongod --dbpath mongodb_data --fork --logpath logs/mongodb.log
```

**Option B: System MongoDB**
```bash
sudo systemctl start mongod
```

**Option C: Docker MongoDB**
```bash
docker run -d -p 27017:27017 --name otogram-mongo mongo:4.4
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required .env variables:**
```env
# Telegram API (from my.telegram.org)
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

# Bot token (from @BotFather)  
TELEGRAM_BOT_TOKEN=your_bot_token

# Phone number (international format)
TELEGRAM_PHONE_NUMBER=+your_phone_number

# Database
MONGO_URL=mongodb://localhost:27017
```

### 4. Health Check

```bash
python scripts/health_check.py
```

Expected output:
```
🎉 System is HEALTHY and ready to run!
```

### 5. Run the System

```bash
python main.py
```

## 🎯 First Steps

### 1. Start Your Bot
Find your bot on Telegram and send `/start`

### 2. Add Messages
Use `/messages` to add your broadcast content

### 3. Add Groups
Use `/groups` to add target groups (supports ID, username, or links)

### 4. Configure Settings
Use `/config` to set delays and safety limits

### 5. Monitor System
Use `/status` to track performance and health

## 🎮 Basic Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot interface |
| `/menu` | Main dashboard |
| `/messages` | Manage broadcast messages |
| `/groups` | Manage target groups |
| `/config` | System configuration |
| `/status` | Real-time statistics |

## 🔍 Troubleshooting

### Common Issues

**MongoDB Connection Error**
```bash
# Check MongoDB status
sudo systemctl status mongod

# Or restart MongoDB
sudo systemctl restart mongod
```

**Authentication Failed**
```bash
# Clear sessions and restart
rm -rf sessions/
python main.py
```

**Bot Not Responding**
1. Verify bot token with [@BotFather](https://t.me/BotFather)
2. Check network: `ping api.telegram.org`
3. Run health check: `python scripts/health_check.py`

### Getting Help

- 📚 [Full Documentation](../README.md)
- 🔧 [Setup Guide](SETUP_GUIDE.md)
- 🐛 [Report Issues](https://github.com/dygje/Otogram/issues)

## 🚀 Next Steps

Once you have the basic setup working:

1. 📖 Read the [Full Documentation](../README.md)
2. ⚙️ Check [Configuration Guide](SETUP_GUIDE.md)
3. 🏗️ Understand the [Architecture](decisions/0001-clean-architecture.md)
4. 🤝 Learn about [Contributing](CONTRIBUTING.md)

---

**Happy automating with Otogram!** 🤖✨