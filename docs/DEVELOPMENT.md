# 💻 Otogram Development Guide

> **Comprehensive development guide for contributing to Otogram**

## 🚀 Development Environment Setup

### Prerequisites

- **Python 3.11+** (3.12 recommended)
- **MongoDB 7.0+** 
- **Git** (latest version)
- **Docker** (optional, for containerized development)
- **Make** (for development commands)

### Quick Setup

```bash
# 1. Fork and clone
git clone https://github.com/your-username/Otogram.git
cd Otogram

# 2. Setup development environment
make setup

# 3. Verify installation
make health

# Expected: "🎉 System is HEALTHY and ready to run!"
```

### Manual Setup

```bash
# 1. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# 2. Install dependencies
pip install --upgrade pip
pip install -e ".[dev]"

# 3. Setup pre-commit hooks
pre-commit install

# 4. Configure environment
cp .env.example .env
# Edit .env with your development credentials
```

## 🏗️ Project Structure

```
Otogram/
├── src/                    # Source code
│   ├── core/              # Infrastructure layer
│   │   ├── config.py      # Configuration management
│   │   └── database.py    # Database abstraction
│   ├── models/            # Domain models (Pydantic)
│   │   ├── base.py        # Base model class
│   │   ├── message.py     # Message entities
│   │   ├── group.py       # Group entities
│   │   ├── blacklist.py   # Blacklist entities
│   │   └── ...
│   ├── services/          # Business logic layer
│   │   ├── message_service.py
│   │   ├── group_service.py
│   │   ├── blacklist_service.py
│   │   └── ...
│   └── telegram/          # Interface layer
│       ├── bot_manager.py     # Bot orchestration
│       ├── management_bot.py  # Dashboard bot
│       ├── userbot.py         # Broadcasting bot
│       └── handlers/          # Command handlers
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/              # Utility scripts
├── .github/              # GitHub workflows
├── pyproject.toml        # Project configuration
├── Makefile             # Development commands
├── docker-compose.yml   # Container orchestration
└── README.md
```

## 🛠️ Development Workflow

### Code Quality Standards

We maintain high code quality through modern Python tooling:

```bash
# Format code (automatic fixes)
make format

# Run linting (check code quality)
make lint

# Run security checks
make security

# Run all quality checks
make quality

# Run tests
make test
```

### Pre-commit Hooks

Pre-commit hooks automatically run on every commit:

- **Ruff** - Fast Python linter and formatter
- **Black** - Code formatting
- **isort** - Import sorting
- **MyPy** - Type checking
- **Bandit** - Security linting
- **Safety** - Dependency vulnerability checking

```bash
# Install hooks (done automatically with make setup)
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Git Workflow

We follow a standard Git workflow:

```bash
# 1. Create feature branch
git checkout -b feature/amazing-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add amazing feature"

# 3. Push branch
git push origin feature/amazing-feature

# 4. Create Pull Request on GitHub
```

### Commit Message Convention

We use [Conventional Commits](https://conventionalcommits.org/):

```
feat: add new broadcasting feature
fix: resolve database connection issue
docs: update API documentation
style: format code with new ruff rules
refactor: restructure service layer
test: add unit tests for message service
chore: update dependencies
```

## 🔧 Development Commands

### Essential Commands

```bash
# Show all available commands
make help

# Complete development setup
make setup

# Install dependencies
make install-dev        # Development dependencies
make install           # Production dependencies only

# Code quality
make format           # Format code (ruff + black + isort)
make lint            # Lint code (ruff + mypy)
make security        # Security checks (bandit + safety)
make quality         # All quality checks + fast tests

# Testing
make test            # Run tests with coverage
make test-fast       # Run tests without coverage

# Application
make run             # Start Otogram
make health          # Health check
make config          # Show configuration

# Maintenance
make clean           # Clean temporary files
make clean-logs      # Clean log files
make clean-sessions  # Clean Telegram sessions
make clean-all       # Full cleanup
```

### Docker Development

```bash
# Build development image
docker build -t otogram-dev .

# Run with docker-compose
docker-compose up -d

# Development with live reload
docker-compose -f docker-compose.dev.yml up

# Run tests in container
docker-compose exec otogram pytest

# Shell access
docker-compose exec otogram bash
```

## 🧪 Testing

### Test Structure

```
tests/
├── test_config.py         # Configuration tests
├── test_database.py       # Database tests
├── test_models.py         # Model validation tests
├── test_services/         # Service layer tests
├── test_telegram/         # Telegram integration tests
├── test_health_check.py   # Health check tests
└── conftest.py           # Pytest fixtures
```

### Running Tests

```bash
# All tests with coverage
make test

# Fast tests (no coverage)
make test-fast

# Specific test file
pytest tests/test_models.py -v

# Specific test method
pytest tests/test_models.py::TestMessage::test_message_creation -v

# Integration tests only
pytest tests/ -m integration

# Unit tests only
pytest tests/ -m unit
```

### Writing Tests

```python
import pytest
from src.models.message import Message
from src.services.message_service import MessageService

class TestMessage:
    """Test Message model"""
    
    def test_message_creation(self):
        """Test message creation with valid data"""
        message = Message(content="Test message")
        
        assert message.content == "Test message"
        assert message.is_active is True
        assert message.usage_count == 0
    
    def test_message_validation(self):
        """Test message validation"""
        with pytest.raises(ValueError):
            Message(content="")  # Empty content should fail

class TestMessageService:
    """Test MessageService business logic"""
    
    @pytest.fixture
    async def message_service(self):
        """Create message service for testing"""
        return MessageService()
    
    async def test_create_message(self, message_service):
        """Test message creation via service"""
        message = await message_service.create_message("Test content")
        
        assert message.content == "Test content"
        assert message.is_active is True
```

### Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = [
    "--strict-markers",
    "--strict-config", 
    "--verbose",
    "--tb=short",
    "--asyncio-mode=auto",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=80",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "telegram: marks tests that require Telegram credentials",
]
```

## 🏛️ Architecture Guidelines

### Clean Architecture

Follow clean architecture principles:

```python
# ✅ Good: Dependencies point inward
from src.core.config import settings
from src.models.message import Message
from src.services.message_service import MessageService

class TelegramHandler:
    def __init__(self):
        self.message_service = MessageService()
    
    async def handle_add_message(self, content: str):
        message = await self.message_service.create_message(content)
        return message

# ❌ Bad: Business logic depends on external interface
from telegram import Update
from src.core.database import database

class MessageService:
    async def create_message_from_telegram(self, update: Update):
        # Business logic shouldn't know about Telegram Update objects
        pass
```

### Dependency Rules

1. **Core** → No dependencies on other layers
2. **Models** → Only depend on core
3. **Services** → Depend on models and core
4. **Telegram** → Can depend on all layers

### Code Style

```python
# Type hints are required
async def create_message(self, content: str) -> Message:
    """Create new message with validation."""
    
# Use descriptive names
user_messages = await self.get_active_messages()
blacklisted_groups = await self.filter_blacklisted_groups(groups)

# Handle errors appropriately
try:
    message = await self.send_message(group_id, content)
except TelegramError as e:
    await self.handle_telegram_error(e, group_id)
    return False

# Use async/await properly
async def broadcast_to_groups(self, message: str, groups: List[Group]):
    """Broadcast message to multiple groups concurrently."""
    tasks = [
        self.send_to_group(group, message) 
        for group in groups
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## 📊 Performance Guidelines

### Database Operations

```python
# ✅ Good: Use indexes and efficient queries
async def get_active_messages(self) -> List[Message]:
    collection = database.get_collection("messages")
    cursor = collection.find(
        {"is_active": True},  # Indexed field
        sort=[("created_at", -1)]  # Indexed sort
    )
    return [Message(**doc) async for doc in cursor]

# ❌ Bad: Unindexed queries
async def search_messages(self, term: str) -> List[Message]:
    collection = database.get_collection("messages") 
    cursor = collection.find({
        "content": {"$regex": term}  # Full table scan
    })
    return [Message(**doc) async for doc in cursor]
```

### Async Best Practices

```python
# ✅ Good: Concurrent operations
async def process_groups_concurrently(self, groups: List[Group]):
    semaphore = asyncio.Semaphore(10)  # Limit concurrency
    
    async def process_group(group):
        async with semaphore:
            return await self.send_to_group(group)
    
    results = await asyncio.gather(
        *[process_group(group) for group in groups],
        return_exceptions=True
    )
    return results

# ❌ Bad: Sequential operations
async def process_groups_sequentially(self, groups: List[Group]):
    results = []
    for group in groups:  # Slow sequential processing
        result = await self.send_to_group(group)
        results.append(result)
    return results
```

### Memory Management

```python
# ✅ Good: Stream large datasets
async def process_all_groups(self):
    collection = database.get_collection("groups")
    async for group_doc in collection.find({}):
        group = Group(**group_doc)
        await self.process_group(group)

# ❌ Bad: Load all data into memory
async def process_all_groups_bad(self):
    groups = await self.get_all_groups()  # Could be thousands
    for group in groups:  # High memory usage
        await self.process_group(group)
```

## 🔐 Security Guidelines

### Input Validation

```python
# ✅ Good: Validate all inputs
async def create_message(self, content: str) -> Message:
    # Sanitize input
    content = content.strip()
    
    # Validate length
    if not content:
        raise ValueError("Message content cannot be empty")
    if len(content) > 4096:
        raise ValueError("Message too long (max 4096 characters)")
    
    # Create message
    return Message(content=content)

# ❌ Bad: No validation
async def create_message_bad(self, content: str) -> Message:
    return Message(content=content)  # Could be empty or too long
```

### Credential Handling

```python
# ✅ Good: Use environment variables
from src.core.config import settings

async def authenticate_bot():
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        raise ValueError("Bot token not configured")
    return token

# ❌ Bad: Hardcoded credentials
async def authenticate_bot_bad():
    token = "123456:ABC-DEF..."  # Never do this!
    return token
```

### Error Handling

```python
# ✅ Good: Don't expose sensitive information
async def handle_database_error(self, error: Exception):
    logger.error(f"Database operation failed: {type(error).__name__}")
    raise DatabaseError("Database operation failed")  # Generic message

# ❌ Bad: Exposing internal details
async def handle_database_error_bad(self, error: Exception):
    raise DatabaseError(f"MongoDB failed: {str(error)}")  # Exposes internal details
```

## 🐛 Debugging

### Logging

```python
from loguru import logger

# Different log levels
logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical system error")

# Structured logging
logger.info(
    "Message sent successfully",
    extra={
        "group_id": group.group_id,
        "message_id": message.id,
        "user_id": user_id
    }
)
```

### Debug Mode

```bash
# Enable debug mode
export LOG_LEVEL=DEBUG
export ENABLE_DEBUG=true

# Run with debugging
make run
```

### Common Debug Scenarios

```python
# Database connection issues
async def debug_database():
    try:
        await database.connect()
        logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

# Telegram API issues  
async def debug_telegram_api():
    try:
        await client.get_me()
        logger.info("Telegram API connection successful")
    except Exception as e:
        logger.error(f"Telegram API error: {e}")

# Performance debugging
import time

async def debug_performance():
    start_time = time.time()
    result = await expensive_operation()
    elapsed = time.time() - start_time
    logger.info(f"Operation took {elapsed:.2f} seconds")
    return result
```

## 📈 Performance Monitoring

### Profiling

```python
import cProfile
import pstats

def profile_function():
    """Profile a specific function"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    result = expensive_function()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('tottime')
    stats.print_stats(10)  # Top 10 functions
    
    return result
```

### Memory Monitoring

```python
import psutil
import tracemalloc

def monitor_memory():
    """Monitor memory usage"""
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    logger.info(f"Memory usage: {memory_mb:.1f} MB")
    
    # Memory profiling
    tracemalloc.start()
    # ... code to profile ...
    current, peak = tracemalloc.get_traced_memory()
    logger.info(f"Memory: current={current/1024/1024:.1f}MB, peak={peak/1024/1024:.1f}MB")
    tracemalloc.stop()
```

## 🚀 Contributing Guidelines

### Before Contributing

1. **Read the documentation** - Understand the architecture
2. **Check existing issues** - Avoid duplicating work
3. **Discuss major changes** - Open an issue first
4. **Follow coding standards** - Use our tools and conventions

### Pull Request Process

1. **Fork** the repository
2. **Create feature branch** from `main`
3. **Make changes** following our guidelines
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Ensure all checks pass** (`make ci-test`)
7. **Submit pull request** with clear description

### Code Review Checklist

- [ ] Code follows project conventions
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact considered
- [ ] Backward compatibility maintained

## 🔧 IDE Configuration

### VS Code

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.path": "isort",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        ".mypy_cache": true,
        ".ruff_cache": true
    }
}
```

### PyCharm

1. **Interpreter**: Set to `./venv/bin/python`
2. **Code Style**: Import from `pyproject.toml`
3. **Inspections**: Enable type checking
4. **External Tools**: Configure ruff, black, pytest

## 📚 Learning Resources

### Python & Async
- [Real Python Async Guide](https://realpython.com/async-io-python/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Architecture
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://realpython.com/solid-principles-python/)

### Telegram APIs
- [Pyrogram Documentation](https://docs.pyrogram.org/)
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

### Database
- [Motor Documentation](https://motor.readthedocs.io/)
- [MongoDB Best Practices](https://docs.mongodb.com/manual/administration/production-notes/)

---

**Happy coding!** 🚀

For questions or help, open an issue or start a discussion on GitHub.

---

**Last Updated**: January 2025 | **Version**: 2.0.3