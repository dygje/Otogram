# 🤖 Telegram Automation System

> **Sistem otomatisasi pengiriman pesan massal ke grup Telegram dengan manajemen lengkap melalui Telegram Bot.**

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup credentials  
python scripts/setup.py

# 3. Run system
python main.py
```

## 🏗️ Architecture

- **Language**: Python 3.11+
- **Framework**: Pyrogram (MTProto) + python-telegram-bot
- **Database**: MongoDB 
- **Pattern**: Clean Architecture

```
src/
├── core/           # Infrastructure (config, database)
├── models/         # Domain entities  
├── services/       # Business logic
└── telegram/       # Interface layer
```

## 📖 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [Getting Started](docs/GETTING_STARTED.md) | Setup & basic usage | New developers |
| [API Reference](docs/API.md) | Code interfaces | Contributors |
| [ADRs](docs/decisions/) | Architecture decisions | Technical leads |

## 🔧 Development

```bash
# Health check
python scripts/health_check.py

# Run tests (when available)
python -m pytest tests/

# Development mode
LOG_LEVEL=DEBUG python main.py
```

## ⚠️ Requirements

- Python 3.11+
- MongoDB 4.4+
- Telegram API credentials ([my.telegram.org](https://my.telegram.org))
- Bot token from [@BotFather](https://t.me/BotFather)

## 📊 Status

![Health Check](https://img.shields.io/badge/health-pass-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run health check (`python scripts/health_check.py`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

**Built with modern Python best practices & clean architecture**