# 🏗️ Otogram Architecture Documentation

> **Comprehensive architecture overview of Otogram - Advanced Telegram Automation System**

## 📊 System Overview

Otogram is built using **Clean Architecture** principles with clear separation of concerns, ensuring maintainability, testability, and scalability.

```
┌─────────────────────────────────────────────────────────┐
│                    External Interfaces                  │
├─────────────────────────────────────────────────────────┤
│  Telegram API    │  Management Bot  │   UserBot        │
│  (Bot Interface) │  (Dashboard)     │   (Broadcasting) │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                 Interface Layer                         │
├─────────────────────────────────────────────────────────┤
│  • Command Handlers    • Callback Handlers             │
│  • Message Processing  • Error Handling                │
│  • Authentication      • Session Management            │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                Business Logic Layer                     │
├─────────────────────────────────────────────────────────┤
│  • Message Service     • Group Service                 │
│  • Blacklist Service   • Configuration Service         │
│  • Broadcasting Logic  • Analytics Service             │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│                 Domain Layer                            │
├─────────────────────────────────────────────────────────┤
│  • Message Models      • Group Models                  │
│  • Blacklist Models    • Configuration Models          │
│  • Log Models          • Base Models                   │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│               Infrastructure Layer                      │
├─────────────────────────────────────────────────────────┤
│  • Database (MongoDB)  • Configuration Management      │
│  • Logging System      • Session Storage               │
│  • External APIs       • File System                   │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Design Principles

### 1. Clean Architecture
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Single Responsibility**: Each component has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Separation of Concerns**: Clear boundaries between layers

### 2. Modular Design
```
src/
├── core/           # Infrastructure & Configuration
├── models/         # Domain Entities (Pure Business Logic)
├── services/       # Application Business Logic
└── telegram/       # External Interface Adapters
```

### 3. Async-First Architecture
- **Non-blocking I/O**: All database and network operations are async
- **Concurrent Processing**: Multiple operations can run simultaneously
- **Resource Efficiency**: Better memory and CPU utilization

## 🔧 Core Infrastructure

### Configuration Management

**Location**: `src/core/config.py`

```python
class Settings(BaseSettings):
    """Centralized configuration management"""
    
    # Environment-based configuration loading
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        validate_assignment=True
    )
    
    # Validation and type checking
    @field_validator("TELEGRAM_PHONE_NUMBER")
    @classmethod
    def validate_phone_number(cls, v):
        if v is not None and not v.startswith("+"):
            raise ValueError("Phone number must start with +")
        return v
```

**Key Features**:
- Environment variable loading with `.env` support
- Runtime validation with Pydantic
- Type safety and automatic conversion
- Configuration status checking
- Development/production environment support

### Database Layer

**Location**: `src/core/database.py`

```python
class Database:
    """MongoDB connection and management"""
    
    async def connect(self):
        """Establish database connection with automatic reconnection"""
        self.client = AsyncIOMotorClient(settings.MONGO_URL)
        self.db = self.client[settings.DB_NAME]
        
        # Test connection and create indexes
        await self.client.admin.command("ping")
        await self._create_indexes()
    
    async def _create_indexes(self):
        """Create optimized indexes for performance"""
        # Performance-critical indexes
        await self.db.messages.create_index("is_active")
        await self.db.groups.create_index("group_id", unique=True)
        await self.db.blacklists.create_index([
            ("group_id", 1),
            ("expires_at", 1)
        ])
```

**Key Features**:
- Async MongoDB operations with Motor
- Automatic index creation for performance
- Connection pooling and management
- Error handling and reconnection logic
- Health checking capabilities

## 📋 Domain Models

### Base Model Architecture

**Location**: `src/models/base.py`

```python
class BaseDocument(BaseModel):
    """Base class for all domain entities"""
    
    # Automatic ID generation with UUIDs (JSON serializable)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    
    # Automatic timestamp management
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # JSON serialization configuration
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    def update_timestamp(self):
        """Update modification timestamp"""
        self.updated_at = datetime.utcnow()
```

**Design Decisions**:
- **UUID4 over ObjectId**: Better JSON serialization, cross-system compatibility
- **Automatic Timestamps**: Consistent audit trail
- **Pydantic Validation**: Type safety and data validation
- **JSON Serializable**: Easy API integration

### Domain-Specific Models

#### Message Model
```python
class Message(BaseDocument):
    """Broadcast message entity"""
    
    content: str                    # Message content (validated)
    is_active: bool = True         # Active status flag
    usage_count: int = 0           # Broadcast usage counter
    
    # Business logic methods
    def toggle_active(self):
        """Toggle message active status"""
        self.is_active = not self.is_active
        self.update_timestamp()
    
    def increment_usage(self):
        """Track message usage"""
        self.usage_count += 1
        self.update_timestamp()
```

#### Group Model
```python
class Group(BaseDocument):
    """Telegram group entity"""
    
    group_id: str                  # Telegram group ID (unique)
    title: str = "Unknown"         # Human-readable group name
    username: str = None           # @username if available
    is_active: bool = True         # Broadcasting enabled flag
    member_count: int = 0          # Last known member count
    last_message_at: datetime = None # Last broadcast timestamp
    
    @classmethod
    def create_bulk(cls, identifiers: str):
        """Factory method for bulk group creation"""
        # Parse multiple formats: IDs, usernames, links
        # Return list of validated Group instances
```

#### Blacklist Model
```python
class Blacklist(BaseDocument):
    """Blacklist management entity"""
    
    group_id: str                  # Target group ID
    blacklist_type: BlacklistType  # permanent/temporary/slowmode
    reason: str                    # Blacklist reason code
    duration_seconds: int = None   # Duration for temporary blacklists
    expires_at: datetime = None    # Calculated expiration time
    
    def is_expired(self) -> bool:
        """Check if temporary blacklist has expired"""
        if self.blacklist_type != BlacklistType.TEMPORARY:
            return False
        return datetime.utcnow() > self.expires_at
```

## 🔄 Business Logic Layer

### Service Architecture Pattern

All business logic is encapsulated in service classes that:
- Implement specific business rules
- Handle data validation and transformation
- Manage database operations
- Provide clean interfaces for the presentation layer

#### Message Service
```python
class MessageService:
    """Message business logic"""
    
    async def create_message(self, content: str) -> Message:
        """Create and validate new message"""
        # Validation
        if len(content.strip()) == 0:
            raise ValueError("Message content cannot be empty")
        if len(content) > 4096:
            raise ValueError("Message too long (max 4096 characters)")
        
        # Create and persist
        message = Message(content=content.strip())
        await self._save_message(message)
        return message
    
    async def get_active_messages(self) -> List[Message]:
        """Get all active messages for broadcasting"""
        collection = database.get_collection("messages")
        cursor = collection.find({"is_active": True})
        messages = []
        async for doc in cursor:
            messages.append(Message(**doc))
        return messages
```

#### Group Service
```python
class GroupService:
    """Group management business logic"""
    
    async def create_groups_bulk(self, identifiers: str) -> dict:
        """Bulk group creation with validation"""
        results = {
            "success": [],
            "failed": [],
            "duplicates": []
        }
        
        # Parse different identifier formats
        groups = Group.create_bulk(identifiers)
        
        for group in groups:
            try:
                # Check for duplicates
                existing = await self.get_group_by_id(group.group_id)
                if existing:
                    results["duplicates"].append(group.group_id)
                    continue
                
                # Validate and save
                await self._save_group(group)
                results["success"].append(group.group_id)
                
            except Exception as e:
                results["failed"].append({
                    "group_id": group.group_id,
                    "error": str(e)
                })
        
        return results
```

#### Blacklist Service
```python
class BlacklistService:
    """Intelligent blacklist management"""
    
    async def add_from_error(self, group_id: str, error_msg: str) -> Blacklist:
        """Auto-blacklist based on Telegram error"""
        
        # Error pattern matching
        if "UserDeactivated" in error_msg:
            # Permanent blacklist
            blacklist_type = BlacklistType.PERMANENT
            reason = "UserDeactivated"
            
        elif "FloodWait" in error_msg:
            # Extract wait time from error message
            # "FloodWait: retry after 3600 seconds"
            wait_seconds = self._extract_flood_wait_time(error_msg)
            blacklist_type = BlacklistType.TEMPORARY
            reason = "FloodWait"
            duration_seconds = wait_seconds
            
        elif "SlowMode" in error_msg:
            # SlowMode temporary blacklist
            blacklist_type = BlacklistType.SLOWMODE
            reason = "SlowMode"
            duration_seconds = 3600  # 1 hour default
        
        # Create and persist blacklist entry
        blacklist = Blacklist(
            group_id=group_id,
            blacklist_type=blacklist_type,
            reason=reason,
            duration_seconds=duration_seconds
        )
        
        await self._save_blacklist(blacklist)
        return blacklist
```

## 🤖 Telegram Integration Layer

### Dual Bot Architecture

Otogram uses a dual bot architecture for separation of concerns:

1. **Management Bot**: User interface and system control
2. **UserBot**: Message broadcasting and automation

#### Bot Manager
```python
class BotManager:
    """Orchestrates both Telegram bots"""
    
    def __init__(self):
        self.management_bot = ManagementBot()  # python-telegram-bot
        self.userbot = UserBot()               # pyrofork
        self.running = False
    
    async def start(self):
        """Start both bots concurrently"""
        try:
            # Start management bot (non-blocking)
            await self.management_bot.start()
            
            # Start userbot (non-blocking)
            await self.userbot.start()
            
            self.running = True
            logger.info("✅ Both bots started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start bots: {e}")
            await self.stop()
            raise
    
    async def stop(self):
        """Graceful shutdown of both bots"""
        self.running = False
        
        # Stop bots concurrently
        await asyncio.gather(
            self.management_bot.stop(),
            self.userbot.stop(),
            return_exceptions=True
        )
```

#### Management Bot (Dashboard Interface)
```python
class ManagementBot:
    """Modern Telegram dashboard interface"""
    
    def __init__(self):
        self.application = Application.builder().token(
            settings.TELEGRAM_BOT_TOKEN
        ).build()
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register command and callback handlers"""
        
        # Command handlers
        self.application.add_handler(
            CommandHandler("start", self.start_command)
        )
        self.application.add_handler(
            CommandHandler("menu", self.main_menu)
        )
        
        # Callback query handlers (inline keyboards)
        self.application.add_handler(
            CallbackQueryHandler(self.handle_callback)
        )
        
        # Message handlers for user input
        self.application.add_handler(
            MessageHandler(filters.TEXT, self.handle_text_input)
        )
    
    async def main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Modern dashboard with inline keyboard"""
        
        # Get system statistics
        stats = await self._get_system_stats()
        
        text = f"""
🤖 **Otogram Dashboard**

📊 **System Status**
• Messages: {stats['messages']['active']}/{stats['messages']['total']} active
• Groups: {stats['groups']['active']}/{stats['groups']['total']} active
• Blacklisted: {stats['blacklisted']} groups
• Last Broadcast: {stats['last_broadcast']}

🎛️ **Quick Actions**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📝 Messages", callback_data="messages_menu"),
                InlineKeyboardButton("👥 Groups", callback_data="groups_menu")
            ],
            [
                InlineKeyboardButton("🚫 Blacklist", callback_data="blacklist_menu"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings_menu")
            ],
            [
                InlineKeyboardButton("🚀 Start Broadcasting", callback_data="start_broadcast"),
                InlineKeyboardButton("🛑 Stop Broadcasting", callback_data="stop_broadcast")
            ],
            [
                InlineKeyboardButton("📈 Analytics", callback_data="analytics"),
                InlineKeyboardButton("🆘 Help", callback_data="help_menu")
            ]
        ]
        
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
```

#### UserBot (Broadcasting Engine)
```python
class UserBot:
    """MTProto-based broadcasting engine"""
    
    def __init__(self):
        self.client = Client(
            "otogram_userbot",
            api_id=settings.TELEGRAM_API_ID,
            api_hash=settings.TELEGRAM_API_HASH,
            phone_number=settings.TELEGRAM_PHONE_NUMBER,
            workdir=settings.SESSION_DIR
        )
        
        self.is_broadcasting = False
        self.current_cycle_task = None
    
    async def start_broadcasting(self):
        """Start automated broadcast cycles"""
        if self.is_broadcasting:
            logger.warning("Broadcasting already in progress")
            return
        
        self.is_broadcasting = True
        self.current_cycle_task = asyncio.create_task(
            self._broadcast_loop()
        )
        
        logger.info("🚀 Broadcasting started")
    
    async def _broadcast_loop(self):
        """Main broadcasting loop with intelligent error handling"""
        
        while self.is_broadcasting:
            try:
                # Get active messages and groups
                messages = await self.message_service.get_active_messages()
                groups = await self.group_service.get_active_groups()
                
                if not messages or not groups:
                    logger.info("No active messages or groups, waiting...")
                    await asyncio.sleep(300)  # Wait 5 minutes
                    continue
                
                # Cleanup expired blacklists
                await self.blacklist_service.cleanup_expired_blacklists()
                
                # Filter out blacklisted groups
                active_groups = []
                for group in groups:
                    is_blacklisted, _ = await self.blacklist_service.is_blacklisted(
                        group.group_id
                    )
                    if not is_blacklisted:
                        active_groups.append(group)
                
                # Broadcast to groups
                await self._broadcast_to_groups(messages, active_groups)
                
                # Wait for next cycle (with random delay)
                delay_hours = random.uniform(
                    settings.MIN_CYCLE_DELAY_HOURS,
                    settings.MAX_CYCLE_DELAY_HOURS
                )
                delay_seconds = delay_hours * 3600
                
                logger.info(f"⏱️ Next broadcast cycle in {delay_hours:.1f} hours")
                await asyncio.sleep(delay_seconds)
                
            except asyncio.CancelledError:
                logger.info("📡 Broadcasting cancelled")
                break
            except Exception as e:
                logger.error(f"❌ Broadcasting error: {e}")
                await asyncio.sleep(600)  # Wait 10 minutes on error
    
    async def _broadcast_to_groups(self, messages: List[Message], groups: List[Group]):
        """Send messages to groups with intelligent error handling"""
        
        message = random.choice(messages)  # Random message selection
        successful_sends = 0
        
        # Limit groups per cycle for safety
        groups_to_process = groups[:settings.MAX_GROUPS_PER_CYCLE]
        
        for group in groups_to_process:
            try:
                # Send message
                await self.client.send_message(
                    chat_id=group.group_id,
                    text=message.content
                )
                
                successful_sends += 1
                
                # Update statistics
                await self.message_service.increment_usage(message.id)
                await self.group_service.update_last_message_time(group.group_id)
                
                # Random delay between messages
                delay = random.uniform(
                    settings.MIN_MESSAGE_DELAY,
                    settings.MAX_MESSAGE_DELAY
                )
                await asyncio.sleep(delay)
                
            except Exception as e:
                # Intelligent error handling
                await self._handle_send_error(group.group_id, str(e))
        
        logger.info(f"📤 Broadcast cycle complete: {successful_sends}/{len(groups_to_process)} successful")
    
    async def _handle_send_error(self, group_id: str, error_msg: str):
        """Intelligent error handling with auto-blacklisting"""
        
        # Auto-blacklist based on error type
        await self.blacklist_service.add_from_error(group_id, error_msg)
        
        # Log error for monitoring
        logger.warning(f"⚠️ Send error for {group_id}: {error_msg}")
```

## 📊 Data Flow Architecture

### Request Flow (Management Bot)

```
User Input (Telegram) 
    ↓
Command/Callback Handler
    ↓
Input Validation
    ↓
Service Layer Method
    ↓
Business Logic Processing
    ↓
Database Operations
    ↓
Response Generation
    ↓
Telegram API Response
```

### Broadcasting Flow (UserBot)

```
Broadcast Trigger
    ↓
Get Active Messages/Groups
    ↓
Filter Blacklisted Groups
    ↓
Select Random Message
    ↓
For Each Group:
    ├── Send Message
    ├── Handle Errors → Auto-Blacklist
    ├── Update Statistics
    └── Random Delay
    ↓
Cycle Complete
    ↓
Wait for Next Cycle
```

## 🔐 Security Architecture

### Authentication & Authorization

```python
# Multiple authentication layers
class SecurityManager:
    
    async def authenticate_userbot(self):
        """MTProto authentication with 2FA support"""
        # Phone number verification
        # SMS/Call code verification  
        # 2FA password if enabled
        # Session persistence
    
    async def authenticate_management_bot(self):
        """Bot token authentication"""
        # Token validation with Telegram
        # Bot permissions verification
        # Rate limiting setup
    
    def validate_user_access(self, user_id: int) -> bool:
        """Validate user access to management bot"""
        # Owner/admin user validation
        # Permission level checking
        # Rate limiting enforcement
```

### Data Security

```python
class DataSecurity:
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize user input"""
        # XSS prevention
        # SQL injection prevention (though we use NoSQL)
        # Command injection prevention
        # Length validation
        
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive configuration data"""
        # API tokens encryption
        # Session data protection
        # Database connection strings
        
    def validate_group_identifier(self, identifier: str) -> bool:
        """Validate Telegram group identifiers"""
        # Format validation (ID, username, link)
        # Malicious link detection
        # Rate limiting for bulk operations
```

## 📈 Performance Architecture

### Caching Strategy

```python
class CacheManager:
    """Redis-based caching for performance optimization"""
    
    async def cache_active_groups(self, groups: List[Group]):
        """Cache frequently accessed group lists"""
        # TTL: 5 minutes for active groups
        # Invalidate on group status changes
        
    async def cache_system_stats(self, stats: dict):
        """Cache dashboard statistics"""
        # TTL: 1 minute for real-time feel
        # Refresh on major system events
        
    async def cache_blacklist_status(self, group_id: str, status: bool):
        """Cache blacklist checks"""
        # TTL: 30 minutes for blacklisted groups
        # Immediate invalidation on blacklist changes
```

### Database Optimization

```javascript
// MongoDB performance indexes
db.messages.createIndex({ "is_active": 1, "created_at": -1 })
db.groups.createIndex({ "group_id": 1 }, { unique: true })
db.groups.createIndex({ "is_active": 1, "last_message_at": -1 })
db.blacklists.createIndex({ "group_id": 1, "expires_at": 1 })
db.logs.createIndex({ "timestamp": -1 }, { expireAfterSeconds: 2592000 }) // 30 days TTL
```

### Async Performance

```python
class PerformanceManager:
    
    async def concurrent_group_processing(self, groups: List[Group]):
        """Process multiple groups concurrently"""
        # Semaphore-based concurrency control
        # Error isolation per group
        # Resource usage monitoring
        
        semaphore = asyncio.Semaphore(10)  # Max 10 concurrent operations
        
        async def process_group(group):
            async with semaphore:
                return await self._send_to_group(group)
        
        # Execute concurrently with proper error handling
        results = await asyncio.gather(
            *[process_group(group) for group in groups],
            return_exceptions=True
        )
        
        return results
```

## 🔍 Monitoring & Observability

### Logging Architecture

```python
class LoggingManager:
    """Structured logging with multiple outputs"""
    
    def setup_logging(self):
        """Configure multi-level logging"""
        
        # Console logging (development)
        logger.add(
            sys.stdout,
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
            level=settings.LOG_LEVEL
        )
        
        # File logging (production)
        logger.add(
            "logs/app.log",
            rotation="1 day",
            retention="7 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
            level="INFO"
        )
        
        # Error logging (critical issues)
        logger.add(
            "logs/errors.log",
            rotation="1 week",
            retention="4 weeks",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
            level="ERROR"
        )
```

### Health Monitoring

```python
class HealthMonitor:
    """System health monitoring and alerting"""
    
    async def check_system_health(self) -> dict:
        """Comprehensive health check"""
        return {
            "database": await self._check_database_health(),
            "telegram_api": await self._check_telegram_connectivity(),
            "disk_space": self._check_disk_space(),
            "memory_usage": self._check_memory_usage(),
            "active_broadcasts": self._check_broadcasting_status(),
        }
    
    async def _check_database_health(self) -> dict:
        """MongoDB health check"""
        try:
            # Connection test
            await database.client.admin.command("ping")
            
            # Performance test
            start_time = time.time()
            await database.get_collection("messages").count_documents({})
            query_time = time.time() - start_time
            
            return {
                "status": "healthy",
                "connection": True,
                "query_time_ms": query_time * 1000
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
```

## 🚀 Scalability Architecture

### Horizontal Scaling Design

```python
class ScalabilityManager:
    """Horizontal scaling coordination"""
    
    def __init__(self):
        self.instance_id = str(uuid.uuid4())
        self.coordinator = DistributedCoordinator()
    
    async def coordinate_broadcasting(self):
        """Coordinate broadcasting across multiple instances"""
        
        # Distributed lock for broadcasting coordination
        async with self.coordinator.acquire_lock("broadcast_cycle"):
            
            # Check if another instance is already broadcasting
            active_broadcaster = await self.coordinator.get_active_broadcaster()
            
            if active_broadcaster and active_broadcaster != self.instance_id:
                logger.info(f"Instance {active_broadcaster} is broadcasting, waiting...")
                return
            
            # Claim broadcasting responsibility
            await self.coordinator.set_active_broadcaster(self.instance_id)
            
            # Perform broadcasting
            await self.userbot.start_broadcasting()
    
    async def distribute_groups(self, groups: List[Group]) -> List[Group]:
        """Distribute groups across instances"""
        
        # Get all active instances
        instances = await self.coordinator.get_active_instances()
        
        # Calculate this instance's share
        instance_index = instances.index(self.instance_id)
        groups_per_instance = len(groups) // len(instances)
        
        start_index = instance_index * groups_per_instance
        end_index = start_index + groups_per_instance
        
        return groups[start_index:end_index]
```

### Load Balancing Strategy

```nginx
# Nginx configuration for load balancing
upstream otogram_backend {
    least_conn;  # Use least connections algorithm
    
    server otogram-1:8000 weight=3 max_fails=3 fail_timeout=30s;
    server otogram-2:8000 weight=3 max_fails=3 fail_timeout=30s;
    server otogram-3:8000 weight=2 max_fails=3 fail_timeout=30s;  # Backup instance
}

server {
    listen 80;
    
    location /health {
        proxy_pass http://otogram_backend;
        proxy_set_header Host $host;
        proxy_connect_timeout 5s;
        proxy_read_timeout 10s;
    }
    
    location / {
        proxy_pass http://otogram_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Health check for upstream
        proxy_next_upstream error timeout http_500 http_502 http_503;
    }
}
```

## 🔄 Error Handling Architecture

### Error Classification & Recovery

```python
class ErrorHandler:
    """Intelligent error classification and recovery"""
    
    ERROR_CATEGORIES = {
        "PERMANENT": [
            "UserDeactivated",
            "ChatDeactivated", 
            "UserBlocked",
            "BotBlocked"
        ],
        "TEMPORARY": [
            "FloodWait",
            "SlowMode",
            "ChatWriteForbidden"
        ],
        "RECOVERABLE": [
            "NetworkError",
            "TimeoutError",
            "ConnectionError"
        ]
    }
    
    async def handle_telegram_error(self, error: Exception, context: dict):
        """Classify and handle Telegram API errors"""
        
        error_msg = str(error)
        error_category = self._classify_error(error_msg)
        
        if error_category == "PERMANENT":
            # Auto-blacklist permanently
            await self.blacklist_service.add_to_blacklist(
                group_id=context["group_id"],
                blacklist_type="permanent",
                reason=self._extract_error_reason(error_msg)
            )
            
        elif error_category == "TEMPORARY":
            # Auto-blacklist with timer
            duration = self._extract_wait_time(error_msg)
            await self.blacklist_service.add_to_blacklist(
                group_id=context["group_id"], 
                blacklist_type="temporary",
                reason=self._extract_error_reason(error_msg),
                duration_seconds=duration
            )
            
        elif error_category == "RECOVERABLE":
            # Implement retry logic with exponential backoff
            retry_count = context.get("retry_count", 0)
            if retry_count < 3:
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                return await self._retry_operation(context, retry_count + 1)
            else:
                # Max retries reached, log and continue
                logger.error(f"Max retries reached for {context['group_id']}: {error_msg}")
```

---

**Last Updated**: September 2025 | **Version**: 2.0.3  
**Status**: 🟢 Production Ready | **Python**: 3.11 | 3.12

This architecture documentation provides a comprehensive overview of Otogram's design principles, implementation patterns, and scalability considerations. The system is built for maintainability, performance, and production reliability.