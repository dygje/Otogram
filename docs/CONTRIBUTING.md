# 🛠️ Development Guide

> **Personal project development workflow - Optimized for solo development**

## 🚀 Development Setup

```bash
# Clone and setup
git clone https://github.com/dygje/Otogram.git
cd Otogram
make setup
make health
```

## 📝 Code Standards

- **Python 3.11+ or 3.12** (recommended) with type hints
- **Line length**: 100 characters
- **Format with**: `make format` (uses ruff)
- **Test with**: `make test-fast` (quick testing)

### Code Structure Example
```python
"""Clear module docstring."""
from typing import Optional
from src.core import config

class ExampleClass:
    """Class purpose."""
    
    def __init__(self, param: str) -> None:
        """Initialize with parameter."""
        self.param = param
    
    async def method(self) -> Optional[str]:
        """Method with clear docstring."""
        return self.param if self.param else None
```

## 🧪 Testing & Quality

```bash
# Quick development checks
make format       # Format code
make test-fast    # Run tests without coverage
make quality      # Format + quick test

# Full testing (when needed)
make test         # Full test with coverage
make lint         # Detailed code checks
```

## 🐳 Docker Development

```bash
# Local development with Docker
docker-compose up -d mongodb  # Just database
make run                      # Run app locally

# Full Docker setup
docker-compose up -d          # Everything in containers
```

## 🛠️ Personal Development Tips

### Quick Workflow
1. Make changes to code
2. Run `make format` (auto-format)
3. Run `make test-fast` (quick validation)
4. Commit changes

### Debugging
- Check logs: `tail -f logs/app.log`
- Health check: `make health`
- Clean start: `make clean-all && make run`

### Configuration
- All settings in `.env` file
- Test config: `make config`
- Reset sessions: `make clean-sessions`

## 🚨 Common Issues

**Service not starting:**
```bash
make health           # Check system status
make clean-sessions   # Clear Telegram sessions
docker ps            # Check MongoDB
```

**Code formatting:**
```bash
make format          # Auto-fix most issues
```

**Database issues:**
```bash
# Docker MongoDB
docker restart otogram-mongo

# Local MongoDB
sudo systemctl restart mongod
```

---

**Personal Project Focus**: Simple, functional, maintainable code over complex processes.