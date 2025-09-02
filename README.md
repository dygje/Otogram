# 🤖 Telegram Automation System

Sistem otomatisasi pengiriman pesan massal ke grup Telegram menggunakan MTProto dengan manajemen lengkap melalui Telegram Bot.

## ✨ Fitur Utama

### 🔐 Otentikasi
- ✅ Menggunakan akun pengguna asli (non-bot) dengan MTProto API
- ✅ Login melalui nomor telepon dan OTP
- ✅ Mendukung Two-Factor Authentication (2FA)

### 📤 Pengiriman Pesan Otomatis
- ✅ **Pembersihan Blacklist**: Otomatis dihapus di awal setiap siklus
- ✅ Pesan hanya dikirim ke grup yang tidak di-blacklist
- ✅ Mendukung pesan teks (tanpa media)
- ✅ **Delay Antar Pesan**: Random 5-10 detik
- ✅ **Delay Antar Siklus**: Random 1.1-1.3 jam

### 🚫 Manajemen Blacklist Otomatis
- ✅ **Blacklist Permanen**: ChatForbidden, ChatIdInvalid, UserBlocked, dll.
- ✅ **Blacklist Sementara**: SlowModeWait, FloodWait dengan durasi otomatis
- ✅ **SlowMode Skip**: Grup terkena slowmode langsung di-skip dan masuk blacklist sementara
- ✅ **Auto Recovery**: Grup otomatis keluar dari blacklist ketika slowmode expired
- ✅ Auto cleanup blacklist yang kedaluwarsa

### 📝 Manajemen Pesan via Bot (NEW: Modern Interface!)
- ✅ **Modern Dashboard** - Control center dengan visual indicators
- ✅ **Quick Setup Wizard** - Setup step-by-step untuk pemula
- ✅ CRUD pesan lengkap (Create, Read, Update, Delete)
- ✅ Aktivasi/deaktivasi pesan dengan one-click
- ✅ Statistik penggunaan pesan real-time
- ✅ Bulk actions untuk management massal

### 👥 Manajemen Grup via Bot
- ✅ Tambah grup tunggal atau massal
- ✅ Support format: ID grup, username, link
- ✅ Aktifkan/nonaktifkan grup
- ✅ Statistik pesan per grup

### ⚙️ Konfigurasi via Bot
- ✅ Ubah delay pesan dan siklus
- ✅ Konfigurasi real-time tanpa restart
- ✅ Berbagai pengaturan sistem

## 🚀 Instalasi & Setup

### 1. Persiapan Credentials

#### a. Dapatkan Telegram API Credentials
1. Kunjungi https://my.telegram.org
2. Login dengan nomor telepon Anda
3. Pilih "API Development Tools"
4. Buat aplikasi baru, catat:
   - `API ID`
   - `API Hash`

#### b. Buat Telegram Bot
1. Chat dengan [@BotFather](https://t.me/BotFather)
2. Kirim `/newbot`
3. Ikuti instruksi, catat `Bot Token`

### 2. Konfigurasi Environment

Edit file `.env`:

```bash
# Database Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=telegram_automation

# Telegram API Credentials (WAJIB DIISI)
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_PHONE_NUMBER=+628123456789

# System Settings
LOG_LEVEL=INFO
ENABLE_DEBUG=false

# Default Message Settings
MIN_MESSAGE_DELAY=5
MAX_MESSAGE_DELAY=10
MIN_CYCLE_DELAY_HOURS=1.1
MAX_CYCLE_DELAY_HOURS=1.3
```

### 3. Menjalankan Sistem

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan sistem
python main.py
```

### 4. Setup Awal

1. **Otentikasi Userbot**: Saat pertama kali jalan, sistem akan meminta:
   - Kode OTP dari Telegram
   - Password 2FA (jika aktif)

2. **Mulai Management**: Chat bot Telegram Anda dengan `/start`

## 📱 Penggunaan Bot

### Perintah Utama
- `/start` - Mulai menggunakan bot
- `/menu` - Menu utama
- `/help` - Bantuan lengkap
- `/status` - Status sistem

### Manajemen Pesan
- `/messages` - Lihat semua pesan
- `/addmessage` - Tambah pesan baru

### Manajemen Grup
- `/groups` - Lihat semua grup
- `/addgroup` - Tambah grup tunggal
- `/addgroups` - Tambah grup massal

Format grup yang didukung:
- **ID Grup**: `-1001234567890`
- **Username**: `@namagrup`
- **Link**: `t.me/namagrup`

### Konfigurasi
- `/config` - Pengaturan sistem
- Parameter yang bisa diubah:
  - Delay antar pesan (5-10 detik)
  - Delay antar siklus (1.1-1.3 jam)
  - Auto cleanup blacklist

### Blacklist
- `/blacklist` - Lihat daftar blacklist
- Sistem otomatis mengelola blacklist berdasarkan error

## 🏗️ Arsitektur Sistem

```
/app/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .env                      # Configuration
├── src/
│   ├── core/                 # Core configuration
│   │   ├── config.py        # Settings management
│   │   └── database.py      # MongoDB connection
│   ├── models/              # Data models
│   │   ├── message.py       # Message models
│   │   ├── group.py         # Group models
│   │   ├── blacklist.py     # Blacklist models
│   │   └── config.py        # Configuration models
│   ├── services/            # Business logic
│   │   ├── message_service.py
│   │   ├── group_service.py
│   │   ├── blacklist_service.py
│   │   └── config_service.py
│   └── telegram/            # Telegram components
│       ├── bot_manager.py   # Main manager
│       ├── management_bot.py # Bot interface
│       ├── userbot.py       # MTProto userbot
│       └── handlers/        # Bot handlers
├── sessions/                # Pyrogram sessions
└── logs/                   # Application logs
```

## 🔧 Fitur Teknis

### Clean Architecture
- ✅ Separation of concerns
- ✅ Dependency injection
- ✅ Repository pattern
- ✅ Service layer pattern

### Modern Python
- ✅ Type hints
- ✅ Async/await
- ✅ Pydantic models
- ✅ Structured logging
- ✅ Error handling

### Database
- ✅ MongoDB dengan Motor (async)
- ✅ Indexes untuk performa optimal
- ✅ UUID-based identifiers

### Error Handling
- ✅ Comprehensive Telegram error handling
- ✅ Automatic blacklist management
- ✅ Graceful degradation

## ⚠️ Penting untuk Diketahui

### Compliance
- ✅ Gunakan hanya untuk keperluan legitimate
- ✅ Patuhi Terms of Service Telegram
- ✅ Jangan spam atau mengganggu pengguna

### Best Practices
- ✅ Random delays untuk menghindari deteksi
- ✅ Automatic blacklist management
- ✅ Respect rate limits
- ✅ Monitor logs secara berkala

### Security
- ✅ Jangan share credentials
- ✅ Gunakan nomor telepon yang dedicated
- ✅ Backup session files
- ✅ Monitor blacklist secara berkala

## 📊 Monitoring

### Logs
- File log: `logs/app.log`
- Rotasi harian, retensi 7 hari
- Level: INFO, WARNING, ERROR

### Status via Bot
- Total pesan aktif
- Total grup aktif
- Status blacklist
- Waktu siklus terakhir
- Estimasi siklus berikutnya

## 🛠️ Troubleshooting

### Error Authentication
- Pastikan API ID/Hash benar
- Pastikan nomor telepon format internasional
- Check session files di folder `sessions/`

### Error Database
- Pastikan MongoDB running
- Check connection string di `.env`
- Verify database permissions

### Error Bot
- Pastikan bot token valid
- Check network connectivity
- Verify bot permissions

## 📈 Pengembangan Lanjutan

### Fitur yang Bisa Ditambahkan
- [ ] Support media (gambar, video)
- [ ] Template pesan dengan variables
- [ ] Scheduling pesan khusus
- [ ] Analytics dan reporting
- [ ] Multi-account support
- [ ] Web dashboard

### Performance Optimization
- [ ] Connection pooling
- [ ] Batch operations
- [ ] Caching layer
- [ ] Queue system

---

## 🤝 Support

Untuk bantuan teknis atau pertanyaan, silakan:
1. Check logs di `logs/app.log`
2. Gunakan `/help` di bot untuk panduan
3. Review konfigurasi di `.env`

**Sistem ini dibangun dengan Modern Python Best Practices dan Clean Architecture untuk maintainability dan extensibility yang optimal.**