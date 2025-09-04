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
3. **Database errors**: Run `make db-start`
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
make dev         # Development session
make quality     # Quick format + test
```

### Bot Commands
```
/start           # Initialize bot
/menu           # Main dashboard
/status         # System status
/messages       # Manage messages
/groups         # Manage groups
```

## 🔧 Personal Project Features

### Optimized for Solo Development
- **Simplified Testing**: 5 essential tests vs 29 comprehensive
- **Personal Makefile**: 25+ commands optimized for solo developer
- **Quick Development**: `make dev` and `make quality` for fast workflow
- **Essential Dependencies**: Core functionality only, optional extras

### Development Workflow
```bash
# Daily development
make dev          # Start development session (format + health)
make quality      # Quick quality check (format + fast test)
make test-fast    # Testing without coverage (super fast)

# Project management  
make clean-all    # Complete cleanup
make docker-run   # Full Docker deployment
make db-start     # MongoDB via Docker
```

---

**Status**: Personal Project | **Version**: 2.0.3 | **Last Updated**: September 2025