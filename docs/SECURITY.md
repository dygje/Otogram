# 🔒 Security Guidelines

> **Essential security practices for personal Telegram automation - Keep it safe and simple**

## 🔒 Basic Security

### Credentials Protection
- **Never commit** `.env` files to git
- **Use strong passwords** for your Telegram account
- **Enable 2FA** on Telegram account
- **Keep API tokens secret** - never share or expose them

### Environment Variables
```env
# Required - Keep these secret
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash  
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_PHONE_NUMBER=your_phone

# Database - local/docker is fine for personal use
MONGO_URL=mongodb://localhost:27017
```

## 🛡️ Safe Usage Practices

### Telegram Automation
- **Start with conservative settings** (slow delays, few groups)
- **Monitor for restrictions** - check logs regularly
- **Respect rate limits** - let the blacklist system work
- **Don't spam** - use reasonable message content

### Default Safe Settings
```env
# Conservative timing for personal use
MIN_MESSAGE_DELAY=8
MAX_MESSAGE_DELAY=15
MIN_CYCLE_DELAY_HOURS=2.0
MAX_CYCLE_DELAY_HOURS=3.0
MAX_GROUPS_PER_CYCLE=20
```

## 🔧 System Security

### Database
- **Default MongoDB** (no auth needed for personal use)
- **Docker isolation** recommended for production
- **Regular backups** if data is important

### Application
- **Input validation** (built-in with Pydantic)
- **Error handling** (prevents crashes and data exposure)
- **Logging** (monitor system behavior)

## 🚨 If Things Go Wrong

### Account Restrictions
- **Temporary restrictions**: Wait it out, check blacklist
- **Permanent restrictions**: Stop using that group/account
- **FloodWait errors**: System handles automatically

### Security Issues
- **Compromised tokens**: Regenerate via @BotFather or my.telegram.org
- **Account issues**: Check Telegram app, may need phone verification

### System Issues
- **Check logs**: `tail -f logs/app.log`
- **Health check**: `make health`
- **Reset cleanly**: `make clean-all && make setup`

## 📊 Monitoring

### What to Watch
- **Error logs** - Look for repeated failures
- **Blacklist growth** - Too many = adjust settings
- **Success rates** - Use bot `/status` command

### Warning Signs
- Many FloodWait errors → Slow down
- Many UserDeactivated → Clean group list
- System crashes → Check logs and configuration

## 🎯 Personal Use Guidelines

### Good Practices
- Use your own groups/channels
- Send reasonable, non-spam content
- Monitor system behavior
- Keep backups of important data

### Avoid
- Mass adding random groups
- Sending commercial spam
- Ignoring Telegram restrictions
- Running 24/7 without monitoring

---

**Remember**: This is for personal automation. Be responsible and respect Telegram's terms.