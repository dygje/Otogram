# 📁 Project Structure Guide

Dokumentasi struktur project Telegram Automation System yang telah direorganisasi.

## 🎯 Overview

Project ini telah direstrukturisasi untuk mengikuti best practices pengembangan aplikasi enterprise Python dengan Clean Architecture principles.

## 📂 Directory Structure

```
/app/
├── 🚀 main.py                    # Entry point aplikasi
├── 📦 requirements.txt           # Python dependencies (stable versions)
├── ⚙️ .env                      # Environment configuration
├── 📖 README.md                 # Quick start guide
├── 
├── 📚 docs/                     # 📁 DOCUMENTATION
│   ├── README_FULL.md           # ✨ Dokumentasi lengkap aplikasi
│   ├── USAGE_GUIDE.md           # 🎯 Panduan penggunaan
│   ├── CHANGELOG.md             # 📝 Riwayat perubahan
│   ├── CLEANUP_REPORT.md        # 🧹 Laporan cleanup
│   ├── MODERN_BOT_INTERFACE.md  # 🎨 Interface modern
│   ├── SLOWMODE_BEHAVIOR.md     # ⏰ Behavior slowmode
│   └── PROJECT_STRUCTURE.md     # 📁 Struktur project (file ini)
├──
├── 🛠️ scripts/                  # 📁 UTILITY SCRIPTS  
│   ├── setup.py                # 🔧 Wizard setup interaktif
│   └── health_check.py         # 🩺 System health checker
├──
├── 💻 src/                     # 📁 SOURCE CODE
│   ├── core/                   # ⚡ Core system
│   │   ├── config.py          # ⚙️ Configuration management
│   │   └── database.py        # 🗄️ MongoDB connection
│   ├── models/                 # 📊 Data models
│   │   ├── base.py            # 🏗️ Base model
│   │   ├── message.py         # 💬 Message models
│   │   ├── group.py           # 👥 Group models
│   │   ├── blacklist.py       # 🚫 Blacklist models  
│   │   ├── config.py          # ⚙️ Config models
│   │   └── log.py             # 📝 Logging models
│   ├── services/               # 🔧 Business logic
│   │   ├── message_service.py # 💬 Message management
│   │   ├── group_service.py   # 👥 Group management
│   │   ├── blacklist_service.py # 🚫 Blacklist management
│   │   └── config_service.py  # ⚙️ Config management
│   └── telegram/               # 📱 Telegram integration
│       ├── bot_manager.py     # 🤖 Main bot manager
│       ├── userbot.py         # 👤 MTProto userbot
│       ├── management_bot.py  # 🎛️ Management interface
│       └── handlers/          # 📨 Bot message handlers
├──
├── 📝 logs/                    # 📁 APPLICATION LOGS
├── 🔐 sessions/                # 📁 PYROGRAM SESSIONS
└── 🧪 tests/                   # 📁 FUTURE TESTS
```

## 🎨 Design Principles

### 1. **Separation of Concerns**
- **`src/`**: Semua kode aplikasi
- **`docs/`**: Semua dokumentasi  
- **`scripts/`**: Utility dan tools
- **`logs/`**, **`sessions/`**: Runtime data

### 2. **Clean Architecture**
- **`core/`**: Infrastructure layer
- **`models/`**: Entity layer
- **`services/`**: Use case layer
- **`telegram/`**: Interface layer

### 3. **Enterprise Standards**
- Root directory bersih dari clutter
- Dokumentasi terorganisir
- Scripts utility terpisah
- Struktur yang mudah di-navigate

## 🚀 Getting Started (Developer)

### 1. Clone & Setup
```bash
git clone <repository>
cd telegram-automation-system
pip install -r requirements.txt
```

### 2. Health Check
```bash
python scripts/health_check.py
```

### 3. Configuration  
```bash
python scripts/setup.py
```

### 4. Run Application
```bash
python main.py
```

## 📋 File Responsibilities

### **Root Level**
- **`main.py`**: Entry point utama aplikasi
- **`requirements.txt`**: Semua dependencies dengan versi stable
- **`.env`**: Environment variables dan konfigurasi
- **`README.md`**: Quick start guide untuk developer

### **docs/**
- **`README_FULL.md`**: Dokumentasi lengkap untuk end user
- **`USAGE_GUIDE.md`**: Panduan penggunaan detail  
- **`CHANGELOG.md`**: Riwayat perubahan versi
- **`PROJECT_STRUCTURE.md`**: Dokumentasi ini

### **scripts/**
- **`setup.py`**: Interactive setup wizard untuk credentials
- **`health_check.py`**: Komprehensif system health checker

### **src/**
- **`core/`**: Database, configuration, logging
- **`models/`**: Pydantic models untuk data structure
- **`services/`**: Business logic dan data processing
- **`telegram/`**: Telegram Bot API dan MTProto integration

## 🔧 Development Guidelines

### Adding New Features
1. **Models**: Tambah di `src/models/`
2. **Business Logic**: Tambah di `src/services/`  
3. **Telegram Handlers**: Tambah di `src/telegram/handlers/`
4. **Documentation**: Update di `docs/`

### Testing
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- End-to-end tests: `tests/e2e/`

### Dependencies
- Semua dependencies menggunakan versi stable yang kompatibel Python 3.11
- Update dilakukan dengan research compatibility terlebih dahulu
- Dokumentasi perubahan di `CHANGELOG.md`

## 📊 Migration Guide

Jika Anda punya kode lama yang menggunakan struktur sebelumnya:

### Import Changes
```python
# OLD
from setup import main
from health_check import check_system

# NEW  
from scripts.setup import main
from scripts.health_check import check_system
```

### Path Changes
```bash
# OLD
python setup.py
python health_check.py

# NEW
python scripts/setup.py  
python scripts/health_check.py
```

## 🤝 Contributing

1. **Follow structure**: Ikuti organisasi folder yang ada
2. **Documentation**: Update docs/ untuk setiap perubahan besar
3. **Health check**: Pastikan `python scripts/health_check.py` pass
4. **Clean imports**: Periksa tidak ada broken imports

---

**Structure ini mengikuti industry best practices dan memudahkan maintenance untuk developer yang akan melanjutkan project.**