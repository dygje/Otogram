# 🚀 Getting Started with Otogram

> **Quick start guide to get Otogram running in minutes**

## 🎯 What is Otogram?

Otogram is a **production-ready Telegram automation system** that enables mass messaging with intelligent blacklist management. Built with modern Python practices and clean architecture, it provides:

- **📤 Mass Broadcasting**: Send messages to multiple Telegram groups automatically
- **🤖 Dual Bot System**: Management dashboard + broadcasting engine
- **🛡️ Smart Blacklist**: Automatic handling of Telegram limitations (FloodWait, SlowMode, etc.)
- **⚙️ Modern Interface**: Full control via Telegram bot dashboard
- **🔒 Production Ready**: Built for reliability, security, and scale

## ⚡ Quick Start (5 Minutes)

### Prerequisites
- **Python 3.11+** installed
- **MongoDB** running (local or cloud)
- **Telegram account** with phone number
- **Internet connection** for Telegram API

### 1. Clone & Install
```bash
# Clone repository
git clone https://github.com/dygje/Otogram.git
cd Otogram

# Install dependencies
make install-dev
# OR: pip install -e ".[dev]"
```

### 2. Setup Database
**Option A - Docker (Easiest):**
```bash
docker run -d --name otogram-mongo -p 27017:27017 mongo:7.0
```

**Option B - Local Install:**
```bash
# Ubuntu/Debian
sudo apt install mongodb

# macOS
brew install mongodb-community

# Start MongoDB
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS
```

### 3. Get Telegram Credentials

**API Credentials:**
1. Go to [my.telegram.org](https://my.telegram.org)
2. Login → API Development Tools
3. Create app → Copy **API ID** and **API Hash**

**Bot Token:**
1. Message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` → Choose name → Copy **token**

### 4. Configure Environment
```bash
# Copy configuration template
cp .env.example .env

# Edit with your credentials
nano .env  # or your preferred editor
```

Fill in your details:
```env
# Required credentials
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_PHONE_NUMBER=+1234567890
```

### 5. Verify & Run
```bash
# Health check
make health

# Expected output: "🎉 System is HEALTHY and ready to run!"

# Start Otogram
make run
```

### 6. Initial Setup via Bot
1. **Find your bot** on Telegram (name from @BotFather)
2. **Send `/start`** → See dashboard
3. **Add messages**: Click "📝 Messages" → "➕ Add Message"
4. **Add groups**: Click "👥 Groups" → "➕ Add Group"  
5. **Start broadcasting**: "⚙️ System Control" → "🚀 Start Broadcasting"

## 🎛️ Management Dashboard

Access everything through your Telegram bot:

### 📊 **Main Dashboard**
- System status overview
- Quick action buttons
- Real-time statistics

### 📝 **Message Management**
- Add/edit/delete broadcast messages
- Toggle message active status
- View usage statistics

### 👥 **Group Management**
- Add single groups (ID, @username, or link)
- Bulk import multiple groups
- View group status and statistics

### 🚫 **Blacklist Management**
- View blacklisted groups
- Auto-cleanup expired entries
- Manual blacklist management

### ⚙️ **System Settings**
- Configure message delays
- Set safety limits
- View system information

## 🔧 Basic Configuration

### Message Timing (Safety First)
```env
# Conservative settings (recommended for beginners)
MIN_MESSAGE_DELAY=8
MAX_MESSAGE_DELAY=15
MIN_CYCLE_DELAY_HOURS=2.0
MAX_CYCLE_DELAY_HOURS=3.0

# Faster settings (higher risk)
MIN_MESSAGE_DELAY=5
MAX_MESSAGE_DELAY=10
MIN_CYCLE_DELAY_HOURS=1.1
MAX_CYCLE_DELAY_HOURS=1.3
```

### Safety Limits
```env
# Small scale (safer)
MAX_GROUPS_PER_CYCLE=20
MAX_MESSAGES_PER_DAY=500

# Medium scale
MAX_GROUPS_PER_CYCLE=50
MAX_MESSAGES_PER_DAY=1000

# Large scale (requires careful monitoring)
MAX_GROUPS_PER_CYCLE=100
MAX_MESSAGES_PER_DAY=2000
```

## 📚 Understanding the System

### How It Works
1. **Add Messages**: Create broadcast messages via bot
2. **Add Groups**: Import target Telegram groups
3. **Auto Broadcasting**: System sends messages on schedule
4. **Smart Blacklisting**: Auto-handles Telegram restrictions
5. **Monitoring**: Real-time stats and health monitoring

### Group Format Support
```
# Group ID (most reliable)
-1001234567890

# Username (public groups)
@publicgroup

# Invite links
https://t.me/joinchat/xxxxx
https://t.me/publicgroup
```

### Intelligent Error Handling
- **FloodWait**: Auto-blacklist for specified duration
- **SlowMode**: Skip temporarily, retry later
- **UserDeactivated**: Permanent blacklist
- **ChatDeactivated**: Permanent blacklist
- **Network Errors**: Automatic retry with backoff

## 🛠️ Development Commands

```bash
# Core commands
make help          # Show all commands
make health        # System health check
make run           # Start application
make setup         # Complete development setup

# Code quality
make format        # Format code (ruff + black)
make lint          # Run linting checks
make test          # Run test suite
make security      # Security scanning

# Maintenance
make clean         # Clean temporary files
make clean-logs    # Clean log files
make clean-sessions # Reset Telegram sessions
```

## 📊 Monitoring Your System

### Health Checks
```bash
# Complete system check
make health

# View logs
tail -f logs/app.log

# Check service status
systemctl status otogram  # If using systemd
```

### Bot Commands
- `/status` - System status and statistics
- `/menu` - Return to main dashboard
- `/help` - Help and tutorials

### Key Metrics to Monitor
- **Messages sent per day**
- **Group success rate**  
- **Blacklist growth**
- **Error frequency**

## 🚨 Troubleshooting

### Common Issues

**❌ "Database connection failed"**
```bash
# Check MongoDB status
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod

# Or with Docker
docker start otogram-mongo
```

**❌ "Authentication failed"**
```bash
# Clear sessions and restart
make clean-sessions
make run
```

**❌ "Bot not responding"**
1. Verify bot token with @BotFather
2. Check network: `ping api.telegram.org`
3. Review logs: `tail -f logs/app.log`

**❌ "Import errors"**
```bash
# Reinstall dependencies
make clean
make install-dev
```

### Getting Help
- **Health Check**: `make health` - Diagnoses most issues
- **Documentation**: Check `docs/` folder for detailed guides
- **GitHub Issues**: Report bugs and get community help
- **Logs**: Always check `logs/app.log` for error details

## 🔒 Security Best Practices

### Credential Security
- Never share your `.env` file
- Use strong, unique passwords
- Regularly rotate API keys
- Use dedicated Telegram account for automation

### Operational Security
- Start with conservative settings
- Monitor blacklist patterns
- Set appropriate rate limits
- Regular backups of database

### Production Deployment
- Use environment variables instead of `.env` file
- Enable MongoDB authentication
- Use HTTPS for any web interfaces
- Set up proper logging and monitoring

## 🚀 Next Steps

### For Beginners
1. **Start Small**: Use conservative settings initially
2. **Monitor Closely**: Watch system behavior and logs
3. **Gradual Scaling**: Increase limits as you gain experience
4. **Backup Regular**: Keep database and session backups

### For Advanced Users
1. **Docker Deployment**: Use `docker-compose.yml` for production
2. **Custom Configuration**: Fine-tune settings for your use case
3. **Monitoring Setup**: Implement comprehensive monitoring
4. **Scaling**: Consider horizontal scaling for high volume

### Useful Resources
- **[Setup Guide](SETUP_GUIDE.md)**: Detailed installation instructions
- **[API Documentation](API.md)**: Complete API reference
- **[Architecture Guide](ARCHITECTURE.md)**: System design and patterns
- **[Deployment Guide](DEPLOYMENT.md)**: Production deployment
- **[Contributing](CONTRIBUTING.md)**: How to contribute to the project

## 💡 Pro Tips

### Optimization
- Use group IDs instead of usernames for better reliability
- Monitor your daily message limits
- Keep your message content engaging and valuable
- Regular cleanup of inactive groups

### Automation
- Use the built-in scheduling system
- Let the system handle error recovery automatically
- Trust the intelligent blacklist management
- Monitor analytics for optimization opportunities

### Scaling
- Start with 1-2 messages and 10-20 groups
- Gradually increase based on performance
- Monitor Telegram's response patterns
- Consider multiple instances for very high volume

---

**🎉 Congratulations!** You now have Otogram running and understand the basics. 

**Status**: 🟢 Ready to start broadcasting safely and efficiently!

For detailed technical information, check out our comprehensive [documentation](API.md) or join the community for support and tips.

---

**Last Updated**: January 2025 | **Version**: 2.0.3