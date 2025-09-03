# 🚀 Complete Setup Guide - Otogram System

**Production-ready setup guide based on comprehensive testing and verification.**

## 📋 Pre-Setup Checklist

### ✅ System Requirements (Verified)
- [x] **Python 3.11+** (tested with 3.11.13)
- [x] **MongoDB 4.4+** (tested with 7.0.23)  
- [x] **RAM**: 1GB minimum, 2GB recommended
- [x] **OS**: Linux/macOS/Windows with bash support
- [x] **Network**: Stable internet for Telegram API access

### ✅ Telegram Requirements (Required)
- [x] **API Credentials** from [my.telegram.org](https://my.telegram.org)
- [x] **Bot Token** from [@BotFather](https://t.me/BotFather)
- [x] **Phone Number** in international format (+country_code)

## 🔧 Step-by-Step Installation

### Step 1: Environment Preparation
```bash
# Clone repository
git clone https://github.com/dygje/Otogram.git
cd Otogram

# Create necessary directories
mkdir -p sessions logs mongodb_data

# Install all dependencies (verified working)
pip install -e ".[dev]"
```

### Step 2: MongoDB Setup (Choose One Option)

**Option A: Local MongoDB (Recommended for Development)**
```bash
# Start MongoDB with custom data directory
mongod --dbpath ./mongodb_data --port 27017 --bind_ip 127.0.0.1 --logpath ./logs/mongodb.log &

# Verify MongoDB is running
mongosh --eval "db.stats()"
```

**Option B: System MongoDB Service**
```bash
# If MongoDB is installed as system service
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify status
sudo systemctl status mongod
```

**Option C: Docker MongoDB**
```bash
# Using Docker (if preferred)
docker run -d -p 27017:27017 --name otogram-mongo mongo:4.4

# Verify container
docker ps | grep otogram-mongo
```

### Step 3: Telegram Credentials Setup

**Get API Credentials from my.telegram.org:**
1. Visit [my.telegram.org](https://my.telegram.org)
2. Login with your phone number + SMS code
3. Go to "API Development Tools"
4. Click "Create new application"
5. Fill out the form and submit
6. **Save the API ID and API Hash**

**Create Management Bot via BotFather:**
1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. **Save the Bot Token** (format: `1234567890:ABC-DEF...`)
5. Optional: Set bot commands with `/setcommands`

### Step 4: Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration file
nano .env
```

**Required Configuration (.env):**
```env
# Telegram API Credentials (from my.telegram.org)
TELEGRAM_API_ID=21507942
TELEGRAM_API_HASH=399fae9734796b25b068050f5f03b698

# Bot Token (from @BotFather)  
TELEGRAM_BOT_TOKEN=8118820592:AAFX05zaXmmW3nWY2pM7s90Pbqn8f1ptc0M

# Phone Number (international format)
TELEGRAM_PHONE_NUMBER=+6282298147520

# Database Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=telegram_automation

# Broadcasting Configuration (Optimized)
MIN_MESSAGE_DELAY=5
MAX_MESSAGE_DELAY=10
MIN_CYCLE_DELAY_HOURS=1.1
MAX_CYCLE_DELAY_HOURS=1.3

# Safety Configuration
MAX_GROUPS_PER_CYCLE=50
MAX_MESSAGES_PER_DAY=1000
AUTO_CLEANUP_BLACKLIST=true

# System Configuration
LOG_LEVEL=INFO
SESSION_DIR=sessions
LOG_DIR=logs
```

### Step 5: System Verification

```bash
# Run comprehensive health check
python scripts/health_check.py
```

**Expected Output:**
```
🩺 TELEGRAM AUTOMATION SYSTEM - HEALTH CHECK
=======================================================

🔍 Checking Python Version...
✅ Python 3.11.13 - OK

🔍 Checking Dependencies...
✅ pyrofork - Installed
✅ python-telegram-bot - Installed
✅ motor - Installed
[... all dependencies ...]

🔍 Checking MongoDB Connection...
✅ MongoDB connection successful

📊 HEALTH CHECK SUMMARY
==============================
Passed: 7/7 checks
🎉 System is HEALTHY and ready to run!
```

## 🚀 First Run & Authentication

### Start the System
```bash
# Start the automation system
python main.py
```

**Expected Startup Sequence:**
```
10:07:27 | INFO | 🚀 Starting Telegram Automation System
10:07:27 | INFO | ✅ Connected to MongoDB: telegram_automation  
10:07:27 | INFO | ✅ Database indexes created
10:07:27 | INFO | ✅ Database connected
10:07:28 | INFO | 🤖 Management bot is running
10:07:28 | INFO | ✅ Management bot started
Welcome to Pyrogram (version 2.3.68)
Enter confirmation code: [WAITING FOR YOUR INPUT]
```

### MTProto Authentication (First Time Only)
1. **OTP Code**: Check your Telegram app for verification code
2. **Enter Code**: Input the 5-digit code when prompted
3. **2FA Password**: If you have two-factor authentication enabled, enter your password
4. **Success**: System will create session file and continue startup

### Verify Management Bot
1. **Find Your Bot**: Search for your bot username in Telegram
2. **Start Conversation**: Send `/start` to your bot
3. **Test Interface**: Try `/menu` to see the dashboard
4. **Verify Commands**: Test `/help`, `/status`, `/messages`, `/groups`

## 🎛️ Initial System Configuration

### Add Your First Message
```
In Telegram bot:
/addmessage
> Type your broadcast message
> ✅ Message added successfully!
```

### Add Target Groups
```
Single group:
/addgroup
> -1001234567890 (group ID)
> OR @groupname (username)  
> OR https://t.me/groupname (link)

Bulk groups:
/addgroups
> -1001111111111
> @group2
> https://t.me/group3
> ✅ Groups added successfully!
```

### Configure Broadcasting Settings
```
/config
> Adjust message delays, cycle intervals, safety limits
> Changes applied in real-time!
```

## 📊 System Monitoring

### Check System Status
```
/status
> View active messages, groups, blacklist statistics
> Monitor broadcasting cycles and performance
```

### View Dashboard
```
/menu
> Modern interface with:
> - System statistics
> - Quick actions
> - Component health
> - Broadcasting analytics
```

## 🛠️ Troubleshooting

### Common Issues & Solutions

**Issue: "Database not connected"**
```bash
# Check MongoDB status
mongosh --eval "db.stats()"

# If failed, restart MongoDB
mongod --dbpath ./mongodb_data --fork --logpath ./logs/mongodb.log
```

**Issue: "EOF when reading a line" (UserBot)**
```bash  
# This is normal on first run - system is waiting for OTP
# Make sure you can input the verification code interactively
```

**Issue: Bot not responding**
```bash
# Verify bot token
curl "https://api.telegram.org/bot<YOUR_TOKEN>/getMe"

# Check network connectivity  
ping api.telegram.org
```

**Issue: Authentication failed**
```bash
# Clear sessions and restart
rm -rf sessions/*
python main.py
```

### Health Check Debug
```bash
# Detailed system diagnosis
python scripts/health_check.py

# View application logs
tail -f logs/app.log

# View MongoDB logs
tail -f logs/mongodb.log
```

## 🔒 Security Best Practices

### Environment Security
- Never commit `.env` file to version control
- Use strong, unique credentials for all services
- Regularly rotate API keys and tokens
- Enable 2FA on your Telegram account

### Operational Security  
- Monitor broadcasting rates and limits
- Review blacklist entries regularly
- Keep logs for audit purposes
- Update dependencies regularly

### Network Security
- Use HTTPS/TLS for all API communications
- Consider VPN for sensitive deployments
- Monitor for unusual network activity
- Implement rate limiting and throttling

## 📈 Performance Optimization

### MongoDB Optimization
```bash
# Enable MongoDB profiling (optional)
mongosh --eval "db.setProfilingLevel(1, {slowms: 100})"

# Monitor query performance
mongosh --eval "db.system.profile.find().sort({ts: -1}).limit(5)"
```

### System Monitoring
```bash
# Monitor system resources
htop

# Monitor application performance
python scripts/health_check.py

# View detailed logs
tail -f logs/app.log | grep "ERROR\|WARNING"
```

## 🎯 Production Deployment

### Recommended Production Setup
1. **Use Process Manager**: pm2, supervisor, or systemd
2. **Log Rotation**: Configure loguru with rotation
3. **Monitoring**: Set up health check endpoints
4. **Backup**: Regular MongoDB backups
5. **Security**: Firewall, fail2ban, security updates

### Example Systemd Service
```ini
[Unit]
Description=Otogram Telegram Automation
After=network.target mongod.service

[Service]
Type=simple
User=otogram
WorkingDirectory=/home/otogram/Otogram
ExecStart=/home/otogram/Otogram/.venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 📞 Support & Resources

### Documentation
- **API Reference**: `docs/API.md`
- **Architecture**: `src/README.md`
- **Changelog**: `docs/CHANGELOG.md`

### Getting Help
- **Health Check**: `python scripts/health_check.py`
- **System Logs**: `tail -f logs/app.log`
- **MongoDB Logs**: `tail -f logs/mongodb.log`
- **Bot Interface**: Use `/help` in your Telegram bot

### Community & Updates
- Monitor Pyrofork updates for security patches
- Keep dependencies updated with `pip install -U -e ".[dev]"`
- Review logs regularly for any issues

---

**🎉 Congratulations! Your Otogram system is now ready for production use.**

**Next Steps:**
1. Add your broadcast messages: `/addmessage`
2. Add target groups: `/addgroup` or `/addgroups`  
3. Configure settings: `/config`
4. Monitor system: `/status` and `/menu`
5. Let the system automatically broadcast with intelligent error handling!