# 📚 Otogram Documentation

> **Complete documentation for personal Telegram automation**

## 🎯 Quick Navigation

### New to Otogram?
**[🚀 Getting Started](GETTING_STARTED.md)** - Setup and running in 5 minutes

### Want to Develop/Customize?
**[🛠️ Development Guide](CONTRIBUTING.md)** - Personal development workflow

### Need Security Guidelines?
**[🔒 Security Guidelines](SECURITY.md)** - Essential safety practices

### Want Technical Details?
**[🏗️ System Architecture](ARCHITECTURE.md)** - Technical deep dive

### Track Changes?
**[📝 Changelog](CHANGELOG.md)** - Version history & updates

## 📖 Documentation Overview

| Document | Purpose | Target User |
|----------|---------|-------------|
| **Getting Started** | Quick setup & basic usage | New users |
| **Development Guide** | Code, test, deploy workflow | Customization |
| **Security Guidelines** | Safe automation practices | All users |
| **Architecture** | Technical system design | Advanced users |
| **Changelog** | Version history & updates | Everyone |

## 🚨 Need Help Quick?

### Common Issues
1. **Won't start**: Run `make health` to diagnose
2. **Bot not responding**: Verify token with @BotFather  
3. **Database errors**: Try `make db-start`
4. **Authentication failed**: Run `make clean-sessions`

### Essential Commands
```bash
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

## 🔧 Personal Project Optimizations

### Solo Development Features
- **Simplified Testing**: 5 essential tests vs 29 comprehensive
- **Personal Makefile**: 25+ commands optimized for single developer
- **Quick Development**: `make dev` and `make quality` for fast workflow
- **Essential Dependencies**: Core functionality only, optional extras

### Development Workflow
```bash
# Daily development
make dev          # Start development session (format + health)
make quality      # Quick quality check (format + fast test)

# Project management  
make clean-all    # Complete cleanup
make docker-run   # Full Docker deployment
```

---

**Status**: Personal Project | **Version**: 2.0.3 | **Last Updated**: September 2025