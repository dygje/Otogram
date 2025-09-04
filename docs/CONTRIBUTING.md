# Contributing Guide

> **Simple contribution guidelines for personal project**

## 🚀 Quick Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/your-username/Otogram.git
cd Otogram

# 2. Development setup
make setup
make health

# 3. Create feature branch
git checkout -b feature/your-feature
```

## 📝 Code Standards

- **Python 3.11+** with type hints
- **Line length**: 100 characters
- **Format with**: `make format` (uses ruff)
- **Test with**: `make test`

### Code Structure
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

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_specific.py -v

# Quality checks
make format
make lint
```

## 📦 Pull Requests

### Before Submitting
- [ ] Tests pass: `make test`
- [ ] Code formatted: `make format`
- [ ] Health check: `make health`
- [ ] Clear commit messages

### PR Template
```markdown
## What Changed
Brief description of changes

## Type
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactor

## Testing
- [ ] Tests added/updated
- [ ] Manual testing done
- [ ] Health check passes
```

## 🐛 Bug Reports

Include in your issue:
1. **Steps to reproduce**
2. **Expected vs actual behavior**
3. **System info** (OS, Python version)
4. **Logs** from `logs/app.log`
5. **Health check output**: `make health`

## 💡 Feature Requests

Consider:
- Does it fit project scope?
- Can it be implemented simply?
- Is there a use case for personal automation?

---

**Keep it simple** - This is a personal project focused on functionality over process.