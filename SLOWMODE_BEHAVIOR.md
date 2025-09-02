# 🐌 SlowMode Handling - Behavior Documentation

## 📋 Behavior Overview

Sistem telah dikonfigurasi untuk menangani **SlowMode** dengan cara yang optimal:

### ⚡ **Immediate Skip Strategy**
1. ✅ Ketika grup terkena SlowMode → **LANGSUNG SKIP**
2. ✅ Tidak ada retry atau waiting
3. ✅ Lanjut ke grup selanjutnya
4. ✅ Masuk blacklist sementara dengan durasi dari Telegram

### 🔄 **Automatic Recovery**
1. ✅ Di awal siklus berikutnya → cleanup blacklist expired
2. ✅ Grup yang slowmode sudah habis → otomatis keluar dari blacklist
3. ✅ Grup bisa menerima pesan lagi di siklus tersebut

## 🔧 Technical Implementation

### 1. **SlowMode Detection**
```python
except SlowmodeWait as e:
    duration = e.value  # Durasi dalam detik dari Telegram
    # Skip immediately dan add to blacklist
```

### 2. **Blacklist Entry Creation**
```python
blacklist_entry = {
    "group_id": group_id,
    "blacklist_type": "temporary", 
    "reason": "SlowModeWait",
    "expires_at": now + timedelta(seconds=duration),
    "duration_seconds": duration
}
```

### 3. **Automatic Cleanup**
```python
# Di awal setiap siklus
await blacklist_service.cleanup_expired()
# Removes: expires_at <= current_time
```

## 📊 **Log Examples**

### SlowMode Detected
```
⏰ SlowModeWait detected for -1001234567890: 3600s (1h 0m) - SKIPPING and adding to temporary blacklist
```

### Cycle Start Cleanup
```
🧹 Cleaned up 3 expired blacklist entries
```

### Cycle Summary
```
✅ Broadcast cycle completed: 15 sent, 2 failed, 5 skipped (blacklisted), 8.5m duration
```

## 🕐 **Timeline Example**

### Cycle 1 (12:00)
- Grup A: ✅ Message sent
- Grup B: ⏰ SlowMode 30 menit → Skip + Blacklist
- Grup C: ✅ Message sent

### Cycle 2 (13:30) - 1.5 jam kemudian
- Cleanup: 🧹 Grup B removed from blacklist (30m expired)
- Grup A: ✅ Message sent  
- Grup B: ✅ Message sent (slowmode sudah habis)
- Grup C: ✅ Message sent

## 🎯 **Benefits**

### ⚡ **Efficiency**
- No wasted time waiting for slowmode
- Maximum throughput per cycle
- Optimal resource usage

### 🛡️ **Safety**
- Respects Telegram rate limits
- Automatic recovery mechanism
- No manual intervention needed

### 📈 **Scalability**
- Works with any number of groups
- Handles multiple slowmode durations
- Self-healing system

## 🔍 **Monitoring SlowMode**

### Via Bot Commands
```
/blacklist - Lihat grup yang terkena slowmode
/status - Overview sistem termasuk blacklist count
```

### Via Logs
```bash
# Monitor slowmode events
grep "SlowModeWait" logs/app.log

# Monitor cleanup
grep "Cleaned up" logs/app.log

# Monitor cycle summaries
grep "cycle completed" logs/app.log
```

### Example Log Analysis
```bash
# Count slowmode events today
grep "$(date +%Y-%m-%d)" logs/app.log | grep "SlowModeWait" | wc -l

# See slowmode durations
grep "SlowModeWait detected" logs/app.log | tail -10
```

## ⏱️ **Slowmode Duration Examples**

| Duration | Display | Typical Case |
|----------|---------|--------------|
| 30s | 0m | Light restriction |
| 300s | 5m | Moderate restriction |
| 900s | 15m | Heavy restriction |
| 3600s | 1h 0m | Very heavy restriction |

## 🚀 **Performance Impact**

### Before (Old Behavior)
- SlowMode → Wait duration → Continue
- Total cycle time: 2-3 hours
- Blocked by slowest group

### After (New Behavior)  
- SlowMode → Skip immediately → Continue
- Total cycle time: 30-60 minutes
- Never blocked by slowmode
- Auto-recovery next cycle

## 🔧 **Configuration**

Tidak perlu konfigurasi tambahan! Behavior ini automatic dan optimal.

### Relevant Settings
```bash
# Cycle delays (tidak terpengaruh slowmode)
MIN_CYCLE_DELAY_HOURS=1.1
MAX_CYCLE_DELAY_HOURS=1.3

# Message delays (untuk grup yang berhasil)
MIN_MESSAGE_DELAY=5
MAX_MESSAGE_DELAY=10
```

---

## 🎯 **Summary**

**SlowMode handling sudah optimal:**
- ⚡ **Skip immediate** → no time wasted
- 🔄 **Auto recovery** → no manual work  
- 📊 **Full tracking** → complete visibility
- 🛡️ **Safe operation** → respects limits

**Sistem akan automatically handle semua slowmode scenarios dengan cara yang paling efisien!**