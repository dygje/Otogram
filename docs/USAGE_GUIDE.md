# 📚 Panduan Penggunaan Telegram Automation System

## 🚀 Quick Start

### 1. Setup Awal (Otomatis)
```bash
python setup.py
```
Script ini akan membantu Anda:
- ✅ Mengisi Telegram credentials
- ✅ Memvalidasi konfigurasi
- ✅ Menjalankan sistem

### 2. Setup Manual
Edit file `.env`:
```bash
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_PHONE_NUMBER=+628123456789
```

Jalankan sistem:
```bash
python main.py
```

## 🤖 Penggunaan Bot Telegram

### Langkah 1: Mulai Bot
1. Chat bot Telegram Anda
2. Kirim `/start`
3. Pilih menu yang tersedia

### Langkah 2: Tambah Pesan
1. Pilih "📝 Pesan" atau `/messages`
2. Klik "➕ Tambah Pesan"
3. Kirim teks pesan yang ingin di-broadcast
4. Pesan otomatis aktif untuk broadcasting

**Contoh pesan:**
```
🎉 Promo spesial hari ini!
Dapatkan diskon 50% untuk semua produk.
Berlaku sampai malam ini saja!

Info: @username
```

### Langkah 3: Tambah Grup Target
#### Satu Grup:
1. Pilih "👥 Grup" atau `/groups`
2. Klik "➕ Tambah Grup"
3. Kirim identifier grup:
   - ID: `-1001234567890`
   - Username: `@namagrup`
   - Link: `t.me/namagrup`

#### Massal (Banyak Grup):
1. Pilih "👥 Grup" atau `/addgroups`
2. Klik "📋 Tambah Massal"
3. Kirim daftar grup (satu per baris):
```
@grup1
@grup2
-1001234567890
t.me/grup3
@grup4
```

### Langkah 4: Konfigurasi (Opsional)
1. Pilih "⚙️ Konfigurasi" atau `/config`
2. Edit pengaturan yang diinginkan:
   - **min_message_delay**: Delay minimum antar pesan (detik)
   - **max_message_delay**: Delay maksimum antar pesan (detik)
   - **min_cycle_delay_hours**: Delay minimum antar siklus (jam)
   - **max_cycle_delay_hours**: Delay maksimum antar siklus (jam)

### Langkah 5: Monitor Sistem
1. Gunakan `/status` untuk melihat status
2. Pilih "🚫 Blacklist" untuk melihat grup yang di-blacklist
3. Check logs di `logs/app.log`

## 🔄 Cara Kerja Sistem

### Siklus Broadcasting
1. **Cleanup**: Hapus blacklist sementara yang expired
2. **Ambil Data**: Ambil pesan dan grup aktif
3. **Randomize**: Acak urutan grup dan pilih pesan random
4. **Kirim**: Kirim pesan dengan delay random 5-10 detik
5. **Blacklist**: Auto blacklist grup yang error
6. **Tunggu**: Tunggu 1.1-1.3 jam untuk siklus berikutnya

### Manajemen Blacklist Otomatis
#### Permanent (Dihapus manual):
- `ChatForbidden` - Bot diblokir dari grup
- `ChatIdInvalid` - ID grup tidak valid
- `UserBlocked` - User memblokir bot
- `PeerIdInvalid` - Peer tidak valid
- `ChannelInvalid` - Channel tidak valid
- `UserBannedInChannel` - User di-ban dari channel
- `ChatWriteForbidden` - Tidak bisa menulis di chat
- `ChatRestricted` - Chat dibatasi

#### Temporary (Auto cleanup):
- `SlowModeWait` - **Mode lambat aktif → LANGSUNG SKIP + blacklist sementara**
- `FloodWait` - Rate limit (durasi dari Telegram)

#### ⚡ SlowMode Behavior (NEW):
1. **Immediate Skip**: Grup terkena slowmode → langsung skip tanpa waiting
2. **Auto Blacklist**: Masuk blacklist sementara dengan durasi dari Telegram  
3. **Continue**: Lanjut ke grup selanjutnya tanpa delay
4. **Auto Recovery**: Di siklus berikutnya, jika slowmode expired → grup otomatis available lagi

## 📱 Perintah Bot Lengkap

### Perintah Utama
| Perintah | Fungsi |
|----------|--------|
| `/start` | Mulai menggunakan bot |
| `/menu` | Tampilkan menu utama |
| `/help` | Bantuan lengkap |
| `/status` | Status sistem real-time |

### Manajemen Pesan
| Perintah | Fungsi |
|----------|--------|
| `/messages` | Lihat semua pesan |
| `/addmessage` | Tambah pesan baru |

### Manajemen Grup
| Perintah | Fungsi |
|----------|--------|
| `/groups` | Lihat semua grup |
| `/addgroup` | Tambah satu grup |
| `/addgroups` | Tambah banyak grup |

### Lainnya
| Perintah | Fungsi |
|----------|--------|
| `/config` | Pengaturan sistem |
| `/blacklist` | Lihat blacklist |

## 🎯 Best Practices

### Pesan yang Efektif
✅ **DO:**
- Gunakan pesan yang relevan dan bermanfaat
- Buat pesan yang engaging
- Tambahkan call-to-action yang jelas
- Gunakan emoji untuk menarik perhatian
- Buat beberapa variasi pesan

❌ **DON'T:**
- Jangan spam dengan pesan yang sama terus
- Hindari pesan yang terlalu panjang
- Jangan gunakan ALL CAPS
- Hindari link suspicious
- Jangan melanggar ToS Telegram

### Manajemen Grup
✅ **DO:**
- Pastikan Anda admin/member grup target
- Gunakan grup yang relevan dengan konten
- Monitor blacklist secara berkala
- Remove grup yang tidak responsif

❌ **DON'T:**
- Jangan add grup random tanpa permission
- Hindari grup yang bukan target audience
- Jangan ignore blacklist warnings

### Konfigurasi Optimal
- **Message Delay**: 5-10 detik (default optimal)
- **Cycle Delay**: 1.1-1.3 jam (menghindari rate limit)
- **Monitor**: Check logs dan blacklist harian

## 🚨 Troubleshooting

### Error "Authentication failed"
**Penyebab**: Credentials salah atau session corrupt
**Solusi**:
1. Pastikan API ID/Hash benar
2. Check nomor telepon format (+628...)
3. Hapus folder `sessions/` dan login ulang

### Error "Database connection failed"
**Penyebab**: MongoDB tidak running
**Solusi**:
1. Start MongoDB service
2. Check connection string di `.env`
3. Pastikan port 27017 terbuka

### Bot tidak merespon
**Penyebab**: Bot token salah atau bot di-disable
**Solusi**:
1. Check bot token di `.env`
2. Chat @BotFather, pastikan bot aktif
3. Restart sistem

### Banyak grup di-blacklist
**Penyebab**: Rate limiting atau permission issues
**Solusi**:
1. Tunggu beberapa jam
2. Check apakah masih admin di grup
3. Kurangi frekuensi pengiriman
4. Clean up blacklist expired

### Session expired
**Penyebab**: Telegram session kedaluwarsa
**Solusi**:
1. Hapus file di folder `sessions/`
2. Restart sistem
3. Login ulang dengan OTP

## 📊 Monitoring & Analytics

### Via Bot
- `/status` - Status real-time
- `/messages` - Statistik pesan
- `/groups` - Statistik grup
- `/blacklist` - Status blacklist

### Via Logs
```bash
# Lihat log real-time
tail -f logs/app.log

# Cari error
grep "ERROR" logs/app.log

# Cari successful sends
grep "Message sent" logs/app.log
```

### Database Direct (Advanced)
```javascript
// MongoDB queries
use telegram_automation

// Count messages
db.messages.count({is_active: true})

// Count groups
db.groups.count({is_active: true})

// Check blacklist
db.blacklists.find({}).count()
```

---

## 🎓 Tips Advanced

### Multiple Message Variations
Buat beberapa versi pesan untuk variasi:
```
Pesan 1: "🎉 Promo hari ini! Diskon 50%..."
Pesan 2: "⚡ Flash Sale! Hemat hingga 50%..."
Pesan 3: "🔥 Penawaran terbatas! Diskon besar-besaran..."
```

### Target Segmentation
Kelompokkan grup berdasarkan kategori:
- Grup A: Produk elektronik
- Grup B: Fashion & lifestyle  
- Grup C: Makanan & minuman

### Optimal Timing
- **Peak Hours**: 19:00-22:00 WIB
- **Avoid**: 00:00-06:00 WIB
- **Weekend**: Lebih aktif

### Performance Monitoring
- Monitor CPU/Memory usage
- Watch database size growth
- Track message success rate
- Monitor blacklist growth

---

**🎯 Dengan mengikuti panduan ini, Anda dapat menggunakan sistem secara optimal dan aman sesuai best practices!**