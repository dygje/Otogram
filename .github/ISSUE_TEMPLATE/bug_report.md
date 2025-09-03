---
name: 🐛 Bug Report
about: Report a bug in Otogram Telegram automation system
title: '[BUG] '
labels: ['type: bug', 'needs-triage']
assignees: 'dygje'
---

## 🐛 Bug Description

Clear and concise description of the bug.

## 🔄 Steps to Reproduce

1. Run command: `...`
2. Configure setting: `...`
3. Observe behavior: `...`
4. Error occurs: `...`

## ✅ Expected Behavior

What should happen instead.

## ❌ Actual Behavior

What actually happened.

## 🖥️ Environment

**System Information:**
- OS: [e.g., Ubuntu 22.04, macOS 13, Windows 11]
- Python Version: [run `python --version`]
- Otogram Version: [check `git describe --tags` or latest commit]

**Telegram Configuration:**
- Using Bot: [ ] Yes [ ] No
- Using Userbot: [ ] Yes [ ] No
- Database: [ ] Local MongoDB [ ] MongoDB Atlas [ ] Other

## 🩺 Health Check Results

```bash
# Please run: python scripts/health_check.py
# Paste the complete output here
```

## ⚙️ Configuration (Remove Sensitive Data!)

**.env file (REMOVE ALL TOKENS/KEYS):**
```bash
# Example - DO NOT include real tokens
MONGO_URL=mongodb://localhost:27017
DB_NAME=telegram_automation
LOG_LEVEL=INFO
# ... other non-sensitive config
```

## 📋 Logs

**Error Messages:**
```bash
# Include relevant log entries from logs/app.log
# Or terminal output when error occurred
```

**Stack Trace (if available):**
```python
# Paste full Python stack trace here
```

## 📸 Screenshots

If applicable, add screenshots of the error or unexpected behavior.

## 🔍 Troubleshooting Done

**What I've already tried:**
- [ ] Restarted the application (`python main.py`)
- [ ] Ran health check (`python scripts/health_check.py`)
- [ ] Checked MongoDB is running (`mongod` or `systemctl status mongod`)
- [ ] Reviewed logs in `logs/app.log`
- [ ] Cleared Telegram sessions (if userbot issue)
- [ ] Verified .env configuration
- [ ] Updated dependencies (`pip install -e ".[dev]"`)

## 🎯 Component Affected

- [ ] 🤖 Management Bot (Telegram bot interface)
- [ ] 👤 Userbot (MTProto mass messaging)
- [ ] 🗄️ Database Operations (MongoDB)
- [ ] ⚙️ Configuration System
- [ ] 📊 Blacklist Management
- [ ] 📨 Message Broadcasting
- [ ] 👥 Group Management
- [ ] 🔧 Setup/Installation

## 🚨 Impact Level

- [ ] 🔴 Critical - System completely broken
- [ ] 🟡 High - Major feature not working
- [ ] 🟢 Medium - Minor feature issue
- [ ] 🔵 Low - Cosmetic or edge case

## 📈 Frequency

- [ ] Always happens
- [ ] Intermittent (sometimes works)
- [ ] Happened once
- [ ] Only under specific conditions

## 💡 Additional Context

Any other relevant information, recent changes, or context that might help debug this issue.

## 🔗 Related Issues

Link any related issues or mention if this might be connected to other problems.

---

**For faster resolution, please:**
1. ✅ Run the health check and include results
2. ✅ Check logs for relevant error messages  
3. ✅ Remove all sensitive data (tokens, phone numbers, etc.)
4. ✅ Include specific steps to reproduce the issue