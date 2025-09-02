# 🤖 Telegram Automation System

Sistem otomatisasi pengiriman pesan massal ke grup Telegram dengan manajemen lengkap melalui Telegram Bot.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Credentials
```bash
python scripts/setup.py
```

### 3. Run System
```bash
python main.py
```

## 📁 Project Structure

```
/app/
├── main.py                    # 🚀 Entry point aplikasi
├── requirements.txt           # 📦 Dependencies
├── .env                      # ⚙️ Configuration
├── README.md                 # 📖 Quick guide (file ini) 
├── docs/                     # 📚 Dokumentasi lengkap
│   ├── README_FULL.md        # Detail documentation
│   ├── USAGE_GUIDE.md        # Panduan penggunaan
│   ├── CHANGELOG.md          # Riwayat perubahan
│   ├── CLEANUP_REPORT.md     # Laporan cleanup
│   ├── MODERN_BOT_INTERFACE.md # Interface modern
│   └── SLOWMODE_BEHAVIOR.md  # Behavior slowmode
├── scripts/                  # 🛠️ Utility scripts
│   ├── setup.py             # Setup wizard
│   └── health_check.py      # Health checker
├── src/                     # 💻 Source code
│   ├── core/                # Core configuration & database
│   ├── models/              # Data models
│   ├── services/            # Business logic
│   └── telegram/            # Telegram components
├── logs/                    # 📝 Application logs
├── sessions/                # 🔐 Pyrogram sessions  
└── tests/                   # 🧪 Future tests
```

## ✨ Features

- ✅ **Broadcast otomatis** ke grup Telegram
- ✅ **Management via Bot** - Control penuh lewat Telegram
- ✅ **Blacklist otomatis** - Skip grup bermasalah
- ✅ **Modern interface** - Dashboard visual
- ✅ **Clean architecture** - Mudah dikembangkan

## 🔧 System Requirements

- **Python**: 3.8+ (Recommended: 3.11+)
- **MongoDB**: 4.4+ (Local atau Cloud)
- **RAM**: 1GB minimum (2GB recommended)
- **OS**: Ubuntu, macOS, Windows, CentOS

## 📚 Documentation

- **Full Documentation**: [docs/README_FULL.md](docs/README_FULL.md)
- **Usage Guide**: [docs/USAGE_GUIDE.md](docs/USAGE_GUIDE.md)
- **Changelog**: [docs/CHANGELOG.md](docs/CHANGELOG.md)

## 🩺 Health Check

Sebelum menjalankan, verifikasi sistem:

```bash
python scripts/health_check.py
```

## ⚠️ Important Notes

1. **Credentials**: Diperlukan API ID/Hash dari https://my.telegram.org
2. **Bot Token**: Buat bot baru di @BotFather
3. **Phone Number**: Gunakan nomor yang dedicated
4. **Compliance**: Patuhi Terms of Service Telegram

## 🤝 Support

- Check logs: `logs/app.log` 
- Health check: `python scripts/health_check.py`
- Bot help: `/help` di Telegram Bot

---

**Built with Modern Python Best Practices & Clean Architecture**