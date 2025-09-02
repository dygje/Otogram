# 📡 API Reference

Technical reference for core components and interfaces.

## Core Components

### Configuration (`src/core/config.py`)

```python
from src.core.config import settings

# Database
settings.MONGO_URL          # MongoDB connection string
settings.DB_NAME           # Database name

# Telegram
settings.TELEGRAM_API_ID   # API ID from my.telegram.org
settings.TELEGRAM_API_HASH # API Hash 
settings.TELEGRAM_BOT_TOKEN # Bot token from @BotFather
settings.TELEGRAM_PHONE_NUMBER # Phone number for userbot

# System
settings.LOG_LEVEL         # Logging level (INFO, DEBUG, WARNING)
settings.ENABLE_DEBUG      # Debug mode flag
```

### Database (`src/core/database.py`)

```python
from src.core.database import Database

db = Database()
await db.connect()      # Connect to MongoDB
await db.disconnect()   # Disconnect
```

## Services

### Message Service (`src/services/message_service.py`)

```python
from src.services.message_service import MessageService

service = MessageService()

# CRUD operations
message = await service.create(text="Hello World", is_active=True)
messages = await service.get_all_active()
await service.update(message_id, {"text": "Updated"})
await service.delete(message_id)

# Utility
count = await service.get_active_count()
```

### Group Service (`src/services/group_service.py`)

```python
from src.services.group_service import GroupService

service = GroupService()

# Add groups
group = await service.add_group(
    chat_id=-1001234567890,
    title="Group Name",
    username="groupname"
)

# Bulk operations  
await service.add_groups_bulk([
    {"chat_id": -1001111111, "title": "Group 1"},
    {"chat_id": -1002222222, "title": "Group 2"}
])

# Management
groups = await service.get_all_active()
await service.toggle_group(group_id, is_active=False)
stats = await service.get_stats()
```

### Blacklist Service (`src/services/blacklist_service.py`)

```python
from src.services.blacklist_service import BlacklistService

service = BlacklistService()

# Blacklist management
await service.add_permanent(chat_id, reason="ChatForbidden")
await service.add_temporary(chat_id, duration=3600, reason="SlowModeWait")

# Cleanup
await service.cleanup_expired()
expired = await service.get_expired()

# Status
blacklisted = await service.get_all()
is_blacklisted = await service.is_blacklisted(chat_id)
```

## Telegram Components

### Bot Manager (`src/telegram/bot_manager.py`)

```python
from src.telegram.bot_manager import BotManager

manager = BotManager()
await manager.start()       # Start all bots
await manager.stop()        # Stop all bots
await manager.broadcast()   # Execute broadcast cycle
```

### Management Bot (`src/telegram/management_bot.py`)

Main bot interface for user interaction. Handles commands:

- `/start` - Initialize bot
- `/menu` - Main menu
- `/messages` - Message management  
- `/groups` - Group management
- `/config` - System configuration
- `/status` - System status
- `/blacklist` - Blacklist overview

### Userbot (`src/telegram/userbot.py`)

MTProto client for sending messages to groups.

```python
from src.telegram.userbot import UserBot

userbot = UserBot()
await userbot.start()
await userbot.send_message(chat_id, "Hello World")
await userbot.stop()
```

## Models

### Message Model (`src/models/message.py`)

```python
from src.models.message import Message

message = Message(
    id=str(uuid.uuid4()),
    text="Broadcast message",
    is_active=True,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow(),
    usage_count=0
)
```

### Group Model (`src/models/group.py`)

```python
from src.models.group import Group

group = Group(
    id=str(uuid.uuid4()),
    chat_id=-1001234567890,
    title="Group Name",
    username="groupname",  # Optional
    is_active=True,
    message_count=0,
    last_message_at=None
)
```

### Blacklist Model (`src/models/blacklist.py`)

```python
from src.models.blacklist import BlacklistEntry

entry = BlacklistEntry(
    id=str(uuid.uuid4()),
    chat_id=-1001234567890,
    reason="SlowModeWait",
    is_permanent=False,
    expires_at=datetime.utcnow() + timedelta(hours=1)
)
```

## Error Handling

### Telegram Errors

Common errors handled automatically:

- `ChatForbidden` → Permanent blacklist
- `UserBannedInChannel` → Permanent blacklist  
- `SlowModeWait` → Temporary blacklist
- `FloodWait` → Temporary blacklist with duration

### Custom Exceptions

```python
from src.core.exceptions import (
    DatabaseError,
    ConfigurationError,  
    TelegramError
)

try:
    await service.operation()
except DatabaseError as e:
    logger.error(f"Database error: {e}")
except TelegramError as e:
    logger.error(f"Telegram error: {e}")
```

## Logging

```python
from loguru import logger

# Log levels
logger.debug("Debug message")
logger.info("Info message") 
logger.warning("Warning message")
logger.error("Error message")

# Structured logging
logger.info("Broadcast sent", extra={
    "chat_id": chat_id,
    "message_id": message_id,
    "duration": duration
})
```

## Configuration Examples

### Environment Variables
```bash
# .env
MONGO_URL=mongodb://localhost:27017
DB_NAME=telegram_automation
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_PHONE_NUMBER=+628123456789
LOG_LEVEL=INFO
MIN_MESSAGE_DELAY=5
MAX_MESSAGE_DELAY=10
MIN_CYCLE_DELAY_HOURS=1.1
MAX_CYCLE_DELAY_HOURS=1.3
```

### MongoDB Indexes

Required indexes for optimal performance:

```javascript
// Groups collection
db.groups.createIndex({ "chat_id": 1 }, { unique: true })
db.groups.createIndex({ "is_active": 1 })

// Messages collection  
db.messages.createIndex({ "is_active": 1 })

// Blacklist collection
db.blacklist.createIndex({ "chat_id": 1 })
db.blacklist.createIndex({ "expires_at": 1 })
db.blacklist.createIndex({ "is_permanent": 1 })
```