# 📚 Otogram API Documentation

> **Comprehensive API reference for Otogram - Advanced Telegram Automation System**

## 🏗️ Architecture Overview

Otogram follows **Clean Architecture** principles with clear separation of concerns:

```
src/
├── core/           # Infrastructure & Configuration
├── models/         # Domain Entities (Pydantic Models)
├── services/       # Business Logic Layer
└── telegram/       # Interface Layer (Bot + UserBot)
```

## 🔧 Core Configuration

### Settings Class

**Location**: `src/core/config.py`

```python
from src.core.config import settings

# Database Configuration
settings.MONGO_URL          # MongoDB connection string
settings.DB_NAME            # Database name (default: "otogram")

# Telegram Credentials
settings.TELEGRAM_API_ID    # API ID from my.telegram.org
settings.TELEGRAM_API_HASH  # API Hash from my.telegram.org
settings.TELEGRAM_BOT_TOKEN # Bot token from @BotFather
settings.TELEGRAM_PHONE_NUMBER # Phone number for userbot

# System Settings
settings.LOG_LEVEL          # Logging level (default: "INFO")
settings.ENABLE_DEBUG       # Debug mode (default: False)

# Message Timing
settings.MIN_MESSAGE_DELAY  # Min delay between messages (default: 5s)
settings.MAX_MESSAGE_DELAY  # Max delay between messages (default: 10s)
settings.MIN_CYCLE_DELAY_HOURS # Min delay between cycles (default: 1.1h)
settings.MAX_CYCLE_DELAY_HOURS # Max delay between cycles (default: 1.3h)

# Safety Limits
settings.MAX_GROUPS_PER_CYCLE    # Max groups per cycle (default: 50)
settings.MAX_MESSAGES_PER_DAY    # Daily message limit (default: 1000)
settings.AUTO_CLEANUP_BLACKLIST  # Auto cleanup blacklist (default: True)
```

### Database Connection

**Location**: `src/core/database.py`

```python
from src.core.database import database

# Connect to database
await database.connect()

# Get collection
collection = database.get_collection("messages")

# Disconnect
await database.disconnect()
```

## 📊 Data Models

### Base Document

**Location**: `src/models/base.py`

```python
from src.models.base import BaseDocument

class BaseDocument(BaseModel):
    id: str                    # UUID4 string
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last update timestamp
    
    def update_timestamp(self): # Update timestamp method
```

### Message Model

**Location**: `src/models/message.py`

```python
from src.models.message import Message

class Message(BaseDocument):
    content: str               # Message content
    is_active: bool = True     # Active status
    usage_count: int = 0       # Usage counter
    
    def toggle_active(self):   # Toggle active status
    def increment_usage(self): # Increment usage count
```

**Example Usage**:
```python
# Create message
message = Message(content="Hello World!")

# Toggle active status
message.toggle_active()

# Increment usage
message.increment_usage()
```

### Group Model

**Location**: `src/models/group.py`

```python
from src.models.group import Group

class Group(BaseDocument):
    group_id: str              # Telegram group ID
    title: str = "Unknown"     # Group title
    username: str = None       # Group username (@username)
    is_active: bool = True     # Active status
    member_count: int = 0      # Member count
    last_message_at: datetime = None # Last message timestamp
    
    @classmethod
    def create_bulk(cls, identifiers: str) # Create multiple groups
```

**Example Usage**:
```python
# Single group
group = Group(
    group_id="-1001234567890",
    title="My Group",
    username="mygroup"
)

# Bulk creation
groups_text = """
-1001234567890
@mygroup
https://t.me/anothergroup
"""
groups = Group.create_bulk(groups_text)
```

### Blacklist Model

**Location**: `src/models/blacklist.py`

```python
from src.models.blacklist import Blacklist, BlacklistType

class Blacklist(BaseDocument):
    group_id: str              # Group ID
    blacklist_type: BlacklistType # permanent/temporary/slowmode
    reason: str                # Blacklist reason
    duration_seconds: int = None # Duration for temporary
    expires_at: datetime = None  # Expiration time
    group_identifier: str = None # Original identifier
    
    def is_expired(self) -> bool # Check if expired
```

**Blacklist Types**:
```python
class BlacklistType(str, Enum):
    PERMANENT = "permanent"    # Permanent blacklist
    TEMPORARY = "temporary"    # Temporary blacklist
    SLOWMODE = "slowmode"      # SlowMode restriction
```

**Example Usage**:
```python
# Permanent blacklist
blacklist = Blacklist(
    group_id="-1001234567890",
    blacklist_type=BlacklistType.PERMANENT,
    reason="UserDeactivated"
)

# Temporary blacklist (1 hour)
temp_blacklist = Blacklist(
    group_id="-1001234567890",
    blacklist_type=BlacklistType.TEMPORARY,
    reason="FloodWait",
    duration_seconds=3600
)

# Check if expired
if temp_blacklist.is_expired():
    print("Blacklist has expired")
```

### Log Model

**Location**: `src/models/log.py`

```python
from src.models.log import LogEntry, LogType, LogLevel

class LogEntry(BaseDocument):
    log_type: LogType          # Log type
    level: LogLevel            # Log level
    message: str               # Log message
    group_id: str = None       # Related group ID
    details: dict = {}         # Additional details
```

## 🔄 Business Logic Services

### Message Service

**Location**: `src/services/message_service.py`

```python
from src.services.message_service import MessageService

service = MessageService()

# CRUD Operations
message = await service.create_message("Hello World!")
messages = await service.get_all_messages()
active_messages = await service.get_active_messages()
message = await service.get_message_by_id("message_id")
updated = await service.update_message("message_id", content="New content")
deleted = await service.delete_message("message_id")

# Status Operations
toggled = await service.toggle_message_status("message_id")
incremented = await service.increment_usage("message_id")

# Statistics
stats = await service.get_message_stats()
# Returns: {"total": 10, "active": 8, "inactive": 2}
```

### Group Service

**Location**: `src/services/group_service.py`

```python
from src.services.group_service import GroupService

service = GroupService()

# CRUD Operations
group = await service.create_group("-1001234567890", "Group Title")
groups = await service.get_all_groups()
active_groups = await service.get_active_groups()
group = await service.get_group_by_id("group_id")
updated = await service.update_group_info("group_id", title="New Title")
deleted = await service.delete_group("group_id")

# Bulk Operations
results = await service.create_groups_bulk("group1\ngroup2\ngroup3")
# Returns: {"success": [...], "failed": [...], "duplicates": [...]}

# Status Operations
toggled = await service.toggle_group_status("group_id")
updated = await service.update_last_message_time("group_id")

# Statistics
stats = await service.get_group_stats()
# Returns: {"total": 15, "active": 12, "inactive": 3}
```

### Blacklist Service

**Location**: `src/services/blacklist_service.py`

```python
from src.services.blacklist_service import BlacklistService

service = BlacklistService()

# CRUD Operations
blacklist = await service.add_to_blacklist(
    group_id="-1001234567890",
    blacklist_type="permanent",
    reason="UserDeactivated"
)

blacklists = await service.get_all_blacklists()
active_blacklists = await service.get_active_blacklists()
blacklist = await service.get_blacklist_by_group("group_id")
removed = await service.remove_from_blacklist("group_id")

# Cleanup Operations
count = await service.cleanup_expired_blacklists()

# Error-based Blacklisting
blacklist = await service.add_from_error(
    group_id="-1001234567890",
    error_msg="FloodWait: retry after 3600 seconds",
    group_identifier="@mygroup"
)

# Check Operations
is_blacklisted = await service.is_blacklisted("group_id")
# Returns: (True/False, reason_or_none)
```

### Configuration Service

**Location**: `src/services/config_service.py`

```python
from src.services.config_service import ConfigService

service = ConfigService()

# Configuration Management
config = await service.get_config("min_message_delay")
updated = await service.set_config("min_message_delay", 7)
all_configs = await service.get_all_configs()

# System Information
system_info = await service.get_system_info()
# Returns detailed system information dict
```

## 🤖 Telegram Integration

### Bot Manager

**Location**: `src/telegram/bot_manager.py`

```python
from src.telegram.bot_manager import BotManager

bot_manager = BotManager()

# Lifecycle Management
await bot_manager.start()    # Start both bots
await bot_manager.stop()     # Stop both bots
is_running = bot_manager.is_running()

# Component Access
management_bot = bot_manager.management_bot
userbot = bot_manager.userbot
```

### Management Bot

**Location**: `src/telegram/management_bot.py`

The management bot provides a modern Telegram interface for system control.

**Key Features**:
- Modern dashboard with inline keyboards
- Message CRUD operations
- Group management (single and bulk)
- Blacklist management
- System configuration
- Real-time status monitoring
- Interactive tutorials

**Main Commands**:
- `/start` - Initialize bot interface
- `/menu` - Main dashboard
- `/status` - System status
- `/help` - Help center

### UserBot (Broadcasting Engine)

**Location**: `src/telegram/userbot.py`

```python
from src.telegram.userbot import UserBot

userbot = UserBot()

# Lifecycle
await userbot.start()
await userbot.stop()

# Broadcasting Operations
await userbot.start_broadcasting()  # Start broadcast cycle
await userbot.stop_broadcasting()   # Stop broadcasting
is_broadcasting = userbot.is_broadcasting()

# Manual Operations
success = await userbot.send_message_to_group("group_id", "message")
```

## 🎛️ Handler Classes

### Message Handlers

**Location**: `src/telegram/handlers/message_handlers.py`

- `list_messages()` - Show all messages
- `add_message_prompt()` - Add new message
- `handle_new_message()` - Process new message
- `show_message_detail()` - Show message details
- `delete_message_confirm()` - Delete confirmation

### Group Handlers

**Location**: `src/telegram/handlers/group_handlers.py`

- `list_groups()` - Show all groups
- `add_group_prompt()` - Add new group
- `handle_new_group()` - Process new group
- `add_groups_bulk_prompt()` - Bulk add groups
- `show_group_detail()` - Show group details

### Blacklist Handlers

**Location**: `src/telegram/handlers/blacklist_handlers.py`

- `show_blacklist()` - Show blacklist entries
- `cleanup_blacklist()` - Clean expired entries
- `remove_from_blacklist()` - Remove specific entry

### Configuration Handlers

**Location**: `src/telegram/handlers/config_handlers.py`

- `show_config()` - Show system configuration
- `update_config()` - Update configuration values

## 🔍 Error Handling

### Telegram Error Mapping

The system automatically handles Telegram API errors:

```python
# Permanent Errors (auto-blacklist forever)
- "UserDeactivated" - User deleted account
- "ChatDeactivated" - Chat was deleted
- "UserBlocked" - User blocked the bot
- "ChatAdminRequired" - Need admin rights

# Temporary Errors (auto-blacklist with timer)
- "FloodWait" - Rate limiting (respects wait time)
- "SlowMode" - Chat has slow mode enabled
- "ChatWriteForbidden" - Temporarily can't write

# Recoverable Errors (retry)
- "NetworkError" - Connection issues
- "ServerError" - Telegram server issues
```

## 📈 Statistics and Monitoring

### Message Statistics
```python
stats = await message_service.get_message_stats()
# {
#   "total": 25,
#   "active": 20,
#   "inactive": 5,
#   "total_usage": 150
# }
```

### Group Statistics
```python
stats = await group_service.get_group_stats()
# {
#   "total": 100,
#   "active": 85,
#   "inactive": 15,
#   "avg_members": 250
# }
```

### System Health
```python
health = await config_service.get_system_info()
# {
#   "database_status": "connected",
#   "userbot_status": "running",
#   "management_bot_status": "running",
#   "last_broadcast_cycle": "2025-01-20T10:30:00",
#   "messages_sent_today": 45,
#   "uptime": "2 days, 5 hours"
# }
```

## 🔐 Security Features

### Rate Limiting
- Message delays: 5-10 seconds between messages
- Cycle delays: 1.1-1.3 hours between broadcast cycles
- Daily limits: Maximum 1000 messages per day

### Automatic Blacklist Management
- **Permanent**: UserDeactivated, ChatDeactivated, UserBlocked
- **Temporary**: FloodWait (respects Telegram's wait time)
- **SlowMode**: Automatic detection and skip

### Error Recovery
- Automatic retry for network errors
- Graceful degradation on API limits
- Complete error logging for debugging

## 🚀 Usage Examples

### Complete Broadcasting Workflow
```python
from src.telegram.bot_manager import BotManager
from src.services.message_service import MessageService
from src.services.group_service import GroupService

# Initialize services
bot_manager = BotManager()
message_service = MessageService()
group_service = GroupService()

# Start system
await bot_manager.start()

# Add messages
msg1 = await message_service.create_message("Hello from Otogram!")
msg2 = await message_service.create_message("Check out our updates!")

# Add groups
groups_text = """
-1001234567890
@publicgroup
https://t.me/anothergroup
"""
result = await group_service.create_groups_bulk(groups_text)
print(f"Added {len(result['success'])} groups successfully")

# Start broadcasting
await bot_manager.userbot.start_broadcasting()
```

### Manual Message Sending
```python
from src.telegram.userbot import UserBot

userbot = UserBot()
await userbot.start()

# Send to specific group
success = await userbot.send_message_to_group(
    group_id="-1001234567890",
    message="Test message"
)

if success:
    print("Message sent successfully!")
else:
    print("Failed to send message")
```

## 🐛 Debugging

### Enable Debug Mode
```bash
# In .env file
LOG_LEVEL=DEBUG
ENABLE_DEBUG=true
```

### Check Logs
```bash
# Application logs
tail -f logs/app.log

# Or use make command
make clean-logs  # Clean old logs
```

### Health Check
```bash
# Full system health check
make health

# Or run directly
python scripts/health_check.py
```

## 📚 Additional Resources

- **Setup Guide**: [docs/SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Contributing**: [docs/CONTRIBUTING.md](CONTRIBUTING.md) 
- **Security**: [docs/SECURITY.md](SECURITY.md)
- **Changelog**: [docs/CHANGELOG.md](CHANGELOG.md)

---

**Last Updated**: January 2025 | **Version**: 2.0.3  
**Status**: 🟢 Production Ready with Modern Standards