# 📚 Otogram Documentation

> **Personal Telegram automation - Simple and focused**

## 🎯 Quick Navigation

### "I'm New Here"
**[🚀 Getting Started](GETTING_STARTED.md)** - Get running in 5 minutes

### "I Want to Develop/Customize"
**[🛠️ Development Guide](CONTRIBUTING.md)** - Personal development workflow

### "I Want to Stay Safe"
**[🔒 Security Guidelines](SECURITY.md)** - Essential safety practices

### "I Want to Understand the System"
**[🏗️ System Architecture](ARCHITECTURE.md)** - Technical deep dive

## 📖 Documentation Overview

| Document | Purpose | Who It's For |
|----------|---------|--------------|
| **Getting Started** | Quick setup & basic usage | New users |
| **Development Guide** | Code, test, deploy workflow | Customization |
| **Security Guidelines** | Safe automation practices | All users |
| **Architecture** | Technical system design | Advanced users |
| **Changelog** | Version history & updates | Everyone |

## 🚨 Need Help?

### Common Issues
1. **Won't start**: Check `make health`
2. **Bot not responding**: Verify token with @BotFather  
3. **Database errors**: Ensure MongoDB is running
4. **Authentication failed**: Try `make clean-sessions`

### Check These First
- **Logs**: `tail -f logs/app.log`
- **Health**: `make health`
- **Config**: `make config`
- **Status**: Bot `/status` command

### Getting Support
- **GitHub Issues**: [Report bugs/issues](https://github.com/dygje/Otogram/issues)
- **Discussions**: General questions and tips
- **Documentation**: Most answers are in these docs

## 🔄 Quick Reference

### Essential Commands
```bash
make setup        # First-time setup
make health       # Check system status
make run         # Start Otogram
make clean       # Clean temporary files
make format      # Format code
```

### Bot Commands
```
/start           # Initialize bot
/menu           # Main dashboard
/status         # System status
/messages       # Manage messages
/groups         # Manage groups
```

---

**Status**: Personal Project | **Version**: 2.0.2 | **Last Updated**: January 2025