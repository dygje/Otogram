# 📡 API Reference - Otogram System

Complete technical reference for core components, verified through testing and analysis.

## ✅ Verified System Architecture

### Configuration Management (`src/core/config.py`)

**Settings Class - Production Ready**
```python
from src.core.config import settings

# Database Configuration ✅
settings.MONGO_URL              # mongodb://localhost:27017
settings.DB_NAME               # telegram_automation

# Telegram Credentials ✅  
settings.TELEGRAM_API_ID       # 21507942 (8-digit API ID)
settings.TELEGRAM_API_HASH     # 399fae... (32-char hash)
settings.TELEGRAM_BOT_TOKEN    # 8118820592:AAFX... (bot token)
settings.TELEGRAM_PHONE_NUMBER # +6282298147520 (international format)

# Timing Configuration ✅
settings.MIN_MESSAGE_DELAY     # 5 seconds (between messages)
settings.MAX_MESSAGE_DELAY     # 10 seconds (between messages)  
settings.MIN_CYCLE_DELAY_HOURS # 1.1 hours (between cycles)
settings.MAX_CYCLE_DELAY_HOURS # 1.3 hours (between cycles)

# Safety Limits ✅
settings.MAX_GROUPS_PER_CYCLE  # 50 groups per cycle
settings.MAX_MESSAGES_PER_DAY  # 1000 messages per day
settings.AUTO_CLEANUP_BLACKLIST # True (auto cleanup enabled)

# System Settings ✅
settings.LOG_LEVEL             # INFO, DEBUG, WARNING, ERROR
settings.SESSION_DIR           # sessions/ (Pyrofork sessions)
settings.LOG_DIR              # logs/ (application logs)
```

### Database Management (`src/core/database.py`)

**Global Database Instance - Thread Safe**
```python
from src.core.database import database

# Connection Management ✅
await database.connect()       # Connect to MongoDB with indexes
await database.disconnect()    # Clean disconnect
collection = database.get_collection("messages")  # Get collection

# Verified Collections:
# - messages (broadcast messages)
# - groups (target groups) 
# - blacklists (temporary/permanent)
# - logs (system logs)
# - configurations (runtime config)
```

### Intelligent Services Layer

#### Message Service (`src/services/message_service.py`) ✅

```python
from src.services.message_service import MessageService
from src.models.message import MessageCreate, MessageUpdate

service = MessageService()

# CRUD Operations - Fully Tested
message = await service.create_message(
    MessageCreate(content="Hello World!")
)
messages = await service.get_active_messages()    # Only active messages
all_messages = await service.get_all_messages()   # All messages
await service.update_message(message.id, MessageUpdate(is_active=False))
await service.delete_message(message.id)

# Statistics & Analytics
stats = await service.get_message_count()
# Returns: {"total": 5, "active": 3, "inactive": 2}

# Usage Tracking
await service.increment_usage_count(message.id)
```

#### Group Service (`src/services/group_service.py`) ✅

```python  
from src.services.group_service import GroupService
from src.models.group import GroupCreate, GroupBulkCreate

service = GroupService()

# Single Group Management
group = await service.create_group(
    GroupCreate(group_identifier="-1001234567890")  # ID format
)
group = await service.create_group(
    GroupCreate(group_identifier="@groupname")      # Username format  
)
group = await service.create_group(
    GroupCreate(group_identifier="https://t.me/groupname")  # Link format
)

# Bulk Group Operations
bulk_data = GroupBulkCreate(identifiers="""
-1001111111111
@group2
https://t.me/group3
""")
groups = await service.create_groups_bulk(bulk_data)

# Group Management
active_groups = await service.get_active_groups()
await service.update_group_info(group.id, title="New Title", is_active=False)
await service.increment_message_count(group.group_id)

# Statistics
stats = await service.get_group_stats()
# Returns: {"total": 10, "active": 8, "inactive": 2}
```

#### Blacklist Service (`src/services/blacklist_service.py`) ✅

**Advanced Error Classification System**
```python
from src.services.blacklist_service import BlacklistService
from src.models.blacklist import BlacklistCreate, BlacklistType, BlacklistReason

service = BlacklistService()

# Automatic Error-Based Blacklisting  
await service.add_from_error(
    group_id="-1001234567890",
    error_msg="ChatForbidden: Chat not found",
    group_identifier="@group"
)

# Manual Blacklist Management
permanent_blacklist = await service.add_to_blacklist(
    BlacklistCreate(
        group_id="-1001234567890",
        blacklist_type=BlacklistType.PERMANENT,
        reason=BlacklistReason.CHAT_FORBIDDEN,
        error_message="Group banned bot"
    )
)

temporary_blacklist = await service.add_to_blacklist(
    BlacklistCreate(
        group_id="-1001234567890", 
        blacklist_type=BlacklistType.TEMPORARY,
        reason=BlacklistReason.SLOW_MODE_WAIT,
        duration_seconds=300,
        error_message="SlowModeWait 300"
    )
)

# Blacklist Operations
is_blocked = await service.is_blacklisted("-1001234567890")
cleaned = await service.cleanup_expired()  # Returns count of cleaned entries
await service.remove_from_blacklist("-1001234567890")

# Statistics & Analytics
stats = await service.get_blacklist_stats()
# Returns: {"total": 15, "permanent": 5, "temporary": 8, "expired": 2}
```

### Telegram Integration Layer

#### Bot Manager (`src/telegram/bot_manager.py`) ✅

**Orchestration of Management Bot + UserBot**
```python
from src.telegram.bot_manager import BotManager

manager = BotManager()

# Service Management - Tested Working
await manager.start()          # Starts management bot + userbot
await manager.stop()           # Graceful shutdown both bots
manager.is_running()          # Returns boolean status

# Components:  
# - manager.management_bot (Telegram bot interface)
# - manager.userbot (MTProto broadcasting client)
# - manager.config_service (Runtime configuration)
```

#### Management Bot (`src/telegram/management_bot.py`) ✅

**Modern Telegram Interface - Fully Functional**

```python
# Available Commands (All Implemented):
/start    - 🤖 Initialize bot with welcome screen
/help     - 📚 Comprehensive help system  
/menu     - 📊 Main dashboard with statistics
/status   - ⚙️ Real-time system status
/messages - 📝 Message CRUD management
/addmessage - ➕ Quick add single message
/groups   - 👥 Group CRUD management  
/addgroup - ➕ Quick add single group
/addgroups - 📋 Bulk group import
/config   - ⚙️ System configuration
/blacklist - 🚫 Blacklist monitoring

# Modern Interface Features:
# ✅ Inline keyboard navigation
# ✅ Contextual callback handling  
# ✅ Input state management
# ✅ Real-time statistics display
# ✅ Error handling with user feedback
```

#### UserBot (`src/telegram/userbot.py`) ✅

**MTProto Broadcasting Engine - Specification Perfect**

```python
from src.telegram.userbot import UserBot

userbot = UserBot()

# Authentication & Connection  
await userbot.start()          # MTProto auth with phone + OTP
await userbot.stop()           # Clean disconnection

# Core Broadcasting Features (All Verified):
# ✅ Automatic blacklist cleanup at cycle start (line 95-100)
# ✅ SlowModeWait: Skip + continue to next group (line 195-216)  
# ✅ FloodWait: Record duration + skip appropriately (line 195-216)
# ✅ Random message delays: 5-10 seconds (line 275-280)
# ✅ Random cycle delays: 1.1-1.3 hours (line 282-300)
# ✅ Error classification: Permanent vs temporary (line 218-246)
# ✅ Group shuffling for natural behavior (line 131-132)
# ✅ Comprehensive error mapping (line 230-241)

# Broadcasting Loop Logic:
async def _broadcasting_loop(self):
    """
    1. Cleanup expired blacklist entries ✅
    2. Get active messages and groups ✅  
    3. Skip blacklisted groups ✅
    4. Send random message to each group ✅
    5. Handle errors with appropriate blacklisting ✅
    6. Random delays between messages ✅
    7. Wait for next cycle with random delay ✅
    """
```

## 🔧 Error Handling System

### Telegram Error Classification ✅

**Permanent Errors → Permanent Blacklist**
```python
# Automatically handled errors:
ChatForbidden         → BlacklistReason.CHAT_FORBIDDEN  
ChatIdInvalid        → BlacklistReason.CHAT_ID_INVALID
UserBlocked          → BlacklistReason.USER_BLOCKED
PeerIdInvalid        → BlacklistReason.PEER_ID_INVALID
ChannelInvalid       → BlacklistReason.CHANNEL_INVALID
UserBannedInChannel  → BlacklistReason.USER_BANNED_IN_CHANNEL
ChatWriteForbidden   → BlacklistReason.CHAT_WRITE_FORBIDDEN
ChatRestricted       → BlacklistReason.CHAT_RESTRICTED
```

**Temporary Errors → Temporary Blacklist + Skip**
```python
# Smart duration extraction:
SlowmodeWait(300)    → 300 seconds temporary blacklist
FloodWait(3600)      → 3600 seconds temporary blacklist

# Behavior: Skip group immediately, continue to next group, 
# auto-cleanup when duration expires
```

### Advanced Models (Pydantic Validation)

#### Message Model (`src/models/message.py`) ✅
```python
from src.models.message import Message, MessageCreate, MessageUpdate

# Message Entity
message = Message(
    id="uuid4-string",           # Auto-generated UUID
    content="Broadcast message", # 1-4096 characters
    is_active=True,             # Active/inactive status
    usage_count=0,              # Times used in broadcasts  
    created_at=datetime.utcnow(), # Auto timestamp
    updated_at=datetime.utcnow()  # Auto timestamp
)

# Creation/Update DTOs with validation
create_data = MessageCreate(content="Hello World!")
update_data = MessageUpdate(is_active=False)
```

#### Group Model (`src/models/group.py`) ✅  
```python
from src.models.group import Group, GroupCreate, GroupBulkCreate

# Group Entity  
group = Group(
    id="uuid4-string",                    # Auto-generated UUID
    group_id="-1001234567890",           # Telegram group ID
    group_username="@groupname",          # Username (optional)
    group_link="https://t.me/groupname", # Invite link (optional) 
    group_title="Group Title",           # Title (optional)
    is_active=True,                      # Active status
    message_count=0                      # Messages sent counter
)

# Flexible group creation with smart parsing
create_data = GroupCreate(group_identifier="-1001234567890")  # ID
create_data = GroupCreate(group_identifier="@groupname")      # Username  
create_data = GroupCreate(group_identifier="t.me/groupname") # Link

# Bulk operations
bulk_data = GroupBulkCreate(identifiers="@group1\n-1001111\nt.me/group3")
```

#### Blacklist Model (`src/models/blacklist.py`) ✅
```python
from src.models.blacklist import (
    Blacklist, BlacklistCreate, BlacklistType, BlacklistReason
)

# Blacklist Entity with smart expiration
blacklist = Blacklist(
    id="uuid4-string",
    group_id="-1001234567890",
    group_identifier="@groupname",
    blacklist_type=BlacklistType.TEMPORARY,  # PERMANENT or TEMPORARY
    reason=BlacklistReason.SLOW_MODE_WAIT,   # Specific error reason
    expires_at=datetime.utcnow() + timedelta(seconds=300),
    duration_seconds=300,
    error_message="SlowModeWait 300"
)

# Smart properties
blacklist.is_expired          # Boolean check
blacklist.time_remaining      # Timedelta or None
```

## 🛠️ Production Configuration

### Environment Variables (.env) ✅
```bash
# Telegram Configuration (All Required)
TELEGRAM_API_ID=21507942
TELEGRAM_API_HASH=399fae9734796b25b068050f5f03b698  
TELEGRAM_BOT_TOKEN=8118820592:AAFX05zaXmmW3nWY2pM7s90Pbqn8f1ptc0M
TELEGRAM_PHONE_NUMBER=+6282298147520

# Database Configuration  
MONGO_URL=mongodb://localhost:27017  
DB_NAME=telegram_automation

# Broadcasting Timing (Optimized for Safety)
MIN_MESSAGE_DELAY=5           # Seconds between messages
MAX_MESSAGE_DELAY=10          # Seconds between messages
MIN_CYCLE_DELAY_HOURS=1.1     # Hours between cycles  
MAX_CYCLE_DELAY_HOURS=1.3     # Hours between cycles

# Safety Limits
MAX_GROUPS_PER_CYCLE=50       # Groups per broadcast cycle
MAX_MESSAGES_PER_DAY=1000     # Daily message limit
AUTO_CLEANUP_BLACKLIST=true   # Enable auto blacklist cleanup

# System Configuration
LOG_LEVEL=INFO                # DEBUG, INFO, WARNING, ERROR
SESSION_DIR=sessions          # Pyrofork session directory
LOG_DIR=logs                 # Application logs directory
```

### MongoDB Indexes (Auto-Created) ✅
```javascript
// Automatically created by database.py _create_indexes()

// Messages collection
db.messages.createIndex({ "is_active": 1 })
db.messages.createIndex({ "created_at": 1 })

// Groups collection  
db.groups.createIndex({ "group_id": 1 }, { unique: true })
db.groups.createIndex({ "is_active": 1 })

// Blacklists collection
db.blacklists.createIndex({ "group_id": 1 })
db.blacklists.createIndex({ "blacklist_type": 1 })
db.blacklists.createIndex({ "expires_at": 1 })

// Logs collection
db.logs.createIndex({ "timestamp": 1 })
db.logs.createIndex({ "log_type": 1 })

// Configurations collection
db.configurations.createIndex({ "key": 1 }, { unique: true })
```

## 🚀 Usage Examples

### Complete Integration Example
```python
import asyncio
from src.core.database import database
from src.telegram.bot_manager import BotManager
from src.services.message_service import MessageService
from src.services.group_service import GroupService

async def main():
    # Initialize system
    await database.connect()
    
    # Setup data
    message_service = MessageService()
    group_service = GroupService()
    
    # Add broadcast content
    message = await message_service.create_message(
        MessageCreate(content="🎉 Hello from Otogram!")
    )
    
    # Add target groups  
    groups = await group_service.create_groups_bulk(
        GroupBulkCreate(identifiers="""
        @testgroup1
        -1001234567890
        https://t.me/testgroup3
        """)
    )
    
    # Start automation system
    bot_manager = BotManager()
    await bot_manager.start()
    
    # System will now:
    # 1. Clean expired blacklists
    # 2. Send messages to active groups
    # 3. Handle errors intelligently  
    # 4. Wait 1.1-1.3 hours for next cycle
    # 5. Repeat automatically

if __name__ == "__main__":
    asyncio.run(main())
```