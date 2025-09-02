---
name: 🐛 Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: ['type: bug']
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## To Reproduce

Steps to reproduce the behavior:
1. Run command '...'
2. Configure setting '...'
3. Observe error '...'

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

What actually happened instead.

## Environment

**System Information:**
- OS: [e.g., Ubuntu 22.04, macOS 13, Windows 11]
- Python Version: [e.g., 3.11.13]
- Project Version: [e.g., 2.0.0]

**Health Check Results:**
```bash
# Please run: python scripts/health_check.py
# Paste output here
```

**Dependencies:**
```bash
# Please run: pip list | grep -E "(pyrogram|telegram|motor|pymongo|pydantic)"
# Paste output here
```

## Configuration

**Environment Variables (remove sensitive data):**
```bash
# .env file content (REMOVE API KEYS/TOKENS)
MONGO_URL=mongodb://localhost:27017
DB_NAME=telegram_automation
LOG_LEVEL=INFO
# ... other non-sensitive config
```

## Logs

**Error Logs:**
```bash
# Please include relevant log entries from logs/app.log
# Or output from terminal when error occurred
```

**Stack Trace (if available):**
```python
# Paste full stack trace here
```

## Screenshots

If applicable, add screenshots to help explain your problem.

## Additional Context

### Telegram-Specific Information
- [ ] Using bot commands
- [ ] Using userbot functionality  
- [ ] Database operations
- [ ] Configuration changes

### What You've Tried
- [ ] Restarted the application
- [ ] Ran health check
- [ ] Cleared sessions folder
- [ ] Checked MongoDB connection
- [ ] Reviewed logs for errors

### Impact
- [ ] Blocks core functionality
- [ ] Affects specific feature only
- [ ] Performance issue
- [ ] Data corruption/loss risk

### Frequency
- [ ] Happens every time
- [ ] Happens sometimes
- [ ] Happened once
- [ ] Happens under specific conditions

## Related Issues/PRs

Link any related issues or pull requests.

## Proposed Solution (optional)

If you have ideas on how to fix this, please share them here.