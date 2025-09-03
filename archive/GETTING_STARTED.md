# 🚀 Getting Started with Otogram

Complete setup guide for the Telegram Automation System based on latest testing and verification.

## ✅ Prerequisites Verification

### System Requirements (Tested)
- **Python**: 3.11+ (tested with 3.11.13) ✅
- **MongoDB**: 4.4+ (tested with 7.0.23) ✅
- **RAM**: 1GB minimum, 2GB recommended ✅
- **OS**: Linux (Ubuntu/CentOS), macOS, Windows ✅

### Telegram Setup Requirements

#### 1. Get API Credentials ✅
1. Visit [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Go to "API Development Tools"
4. Create new application and note:
   - **API ID** (8 digits, e.g., 21507942)
   - **API Hash** (32 characters, e.g., 399fae...)

#### 2. Create Management Bot ✅
1. Message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow instructions and save **Bot Token**
4. Format: `8118820592:AAFX05zaXmmW3nWY2pM7s90Pbqn8f1ptc0M`

## 🔧 Installation (Verified Working)

### 1. System Setup
```bash
# Clone and navigate
git clone https://github.com/dygje/Otogram.git
cd Otogram

# Install dependencies (all tested working)
pip install -e ".[dev]"

# Create necessary directories
mkdir -p sessions logs mongodb_data
```

### 2. MongoDB Setup (Multiple Options)
```bash
# Option A: Local MongoDB with custom data directory
mongod --dbpath ./mongodb_data --port 27017 --bind_ip 127.0.0.1 --logpath ./logs/mongodb.log &

# Option B: System MongoDB (if installed)
sudo systemctl start mongod

# Option C: Docker MongoDB
docker run -d -p 27017:27017 --name otogram-mongo mongo:4.4

# Verify MongoDB is running
mongosh --eval "db.stats()"
```

### 3. Environment Configuration
```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env
```

**Required .env configuration:**
```env
# Telegram API Credentials (from my.telegram.org)
TELEGRAM_API_ID=21507942
TELEGRAM_API_HASH=399fae9734796b25b068050f5f03b698

# Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN=8118820592:AAFX05zaXmmW3nWY2pM7s90Pbqn8f1ptc0M

# Phone Number (international format)
TELEGRAM_PHONE_NUMBER=+6282298147520

# Database Connection
MONGO_URL=mongodb://localhost:27017
DB_NAME=telegram_automation

# System Settings (pre-configured optimally)
MIN_MESSAGE_DELAY=5
MAX_MESSAGE_DELAY=10
MIN_CYCLE_DELAY_HOURS=1.1
MAX_CYCLE_DELAY_HOURS=1.3
```

### 4. System Verification
```bash
# Run comprehensive health check
python scripts/health_check.py

# Expected output:
🎉 System is HEALTHY and ready to run!
```

## First Run

### Start System
```bash
python main.py
```

### Initial Authentication
On first run, system will prompt:
1. **OTP Code**: Check Telegram for verification code
2. **2FA Password**: If two-factor auth is enabled

### Bot Management
1. Find your bot in Telegram
2. Send `/start` to begin
3. Use `/menu` for available commands

## Basic Usage

### Add Messages
```
/addmessage
> Enter your broadcast message
```

### Add Groups  
```
/addgroup
> Group ID: -1001234567890
> Or username: @groupname
> Or link: https://t.me/groupname
```

### View Status
```
/status
> Shows active messages, groups, blacklist
```

### Configure Settings
```
/config
> Adjust delays, cycles, cleanup settings
```

## Common Issues

### Authentication Failed
```bash
# Clear sessions and retry
rm -rf sessions/
python main.py
```

### Database Connection Error
```bash
# Check MongoDB status
sudo systemctl status mongod

# Or use Docker
docker run -d -p 27017:27017 mongo:4.4
```

### Bot Not Responding
1. Verify bot token with [@BotFather](https://t.me/BotFather)
2. Check network: `ping api.telegram.org`
3. Test token:
```bash
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

## Next Steps

- [API Reference](API.md) - Code interfaces
- [Architecture Decisions](decisions/) - Technical rationale
- [Troubleshooting](../scripts/health_check.py) - System diagnostics

## Support

- 🩺 Health check: `python scripts/health_check.py`
- 📝 Logs: `tail -f logs/app.log`
- 🤖 Bot help: `/help` in Telegram