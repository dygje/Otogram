# Contributing to Telegram Automation System

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/Otogram.git
cd Otogram

# 2. Set up development environment
make setup

# 3. Install pre-commit hooks
make pre-commit

# 4. Run health check
make health

# 5. Create a feature branch
git checkout -b feature/amazing-feature
```

## 📋 Development Setup

### Requirements

- **Python**: 3.11+ (required)
- **MongoDB**: 4.4+ (for testing)
- **Git**: Latest version
- **Make**: For development commands

### Development Dependencies

The project uses modern Python tooling:

```bash
# Install development dependencies
pip install -e ".[dev]"
```

This includes:
- **pytest** - Testing framework
- **black** - Code formatting
- **isort** - Import sorting
- **mypy** - Type checking
- **pre-commit** - Git hooks
- **flake8** - Linting

## 🛠️ Development Workflow

### 1. Code Quality

We maintain high code quality standards:

```bash
# Format code
make format

# Run linting
make lint

# Type checking
mypy src/

# Run all checks
make ci-test
```

### 2. Testing

Write tests for new features:

```bash
# Run tests
make test

# Run specific test
pytest tests/test_specific.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

### 3. Pre-commit Hooks

Pre-commit hooks ensure code quality:

- **black** - Code formatting
- **isort** - Import sorting  
- **mypy** - Type checking
- **flake8** - Linting
- **bandit** - Security scanning
- **safety** - Dependency vulnerability check

## 📝 Coding Standards

### Python Style Guide

We follow **PEP 8** with these specifics:

- **Line length**: 100 characters
- **Docstrings**: Google style
- **Type hints**: Required for public APIs
- **Import sorting**: isort with black profile

### Code Structure

```python
"""
Module docstring explaining purpose.
"""
from typing import Optional, List
import asyncio

from external_lib import something
from src.core import config


class ExampleClass:
    """Class docstring explaining purpose."""
    
    def __init__(self, param: str) -> None:
        """Initialize with parameter."""
        self.param = param
    
    async def async_method(self, data: List[str]) -> Optional[str]:
        """
        Async method with proper typing.
        
        Args:
            data: List of strings to process
            
        Returns:
            Processed string or None if empty
        """
        if not data:
            return None
        return " ".join(data)
```

### Documentation

- **Docstrings**: Required for all public classes and functions
- **Type hints**: Required for public APIs
- **Comments**: For complex logic only
- **README updates**: For new features

## 🔍 Testing Guidelines

### Test Structure

```
tests/
├── test_core/          # Core functionality tests
├── test_models/        # Data model tests  
├── test_services/      # Business logic tests
├── test_telegram/      # Telegram integration tests
├── conftest.py         # Pytest fixtures
└── __init__.py
```

### Test Types

1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test component interactions
3. **Health Check Tests**: Validate system health

### Writing Tests

```python
import pytest
from src.models.message import Message


class TestMessage:
    """Test Message model."""
    
    def test_message_creation(self):
        """Test message creation with valid data."""
        message = Message(content="Test message")
        
        assert message.content == "Test message"
        assert message.is_active is True
        assert message.usage_count == 0
    
    def test_message_validation(self):
        """Test message validation."""
        with pytest.raises(ValidationError):
            Message(content="")  # Empty content should fail
```

## 🔧 Architecture Guidelines

### Clean Architecture

The project follows clean architecture:

```
src/
├── core/           # Infrastructure & configuration
├── models/         # Domain entities
├── services/       # Business logic
└── telegram/       # Interface adapters
```

### Dependency Rules

- **Core**: No dependencies on other layers
- **Models**: Only depend on core
- **Services**: Depend on models and core
- **Telegram**: Can depend on all layers

### Adding New Features

1. **Models**: Define data structures in `src/models/`
2. **Services**: Implement business logic in `src/services/`
3. **Handlers**: Add Telegram handlers in `src/telegram/handlers/`
4. **Tests**: Write comprehensive tests
5. **Docs**: Update documentation

## 📦 Submitting Changes

### Pull Request Process

1. **Create Issue**: Describe the problem/feature
2. **Fork Repository**: Create your own copy
3. **Create Branch**: Use descriptive name
4. **Make Changes**: Follow coding standards
5. **Write Tests**: Ensure good coverage
6. **Update Docs**: Keep documentation current
7. **Submit PR**: Use the template

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs
2. **Maintainer Review**: Code review by maintainers
3. **Testing**: Manual testing if needed
4. **Merge**: Approved changes get merged

## 🐛 Bug Reports

### Before Reporting

- Check existing issues
- Run health check: `python scripts/health_check.py`
- Collect system information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**  
What actually happens

**Environment**
- OS: [e.g. Ubuntu 20.04]
- Python: [e.g. 3.11.0] 
- Version: [e.g. 2.0.0]

**Logs**
Include relevant log files
```

## 💡 Feature Requests

### Before Requesting

- Check if already requested
- Consider if it fits project scope
- Think about implementation complexity

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other ways to solve this

**Additional Context**
Screenshots, examples, etc.
```

## 🏆 Recognition

Contributors are recognized in:

- **CHANGELOG.md**: Feature contributors
- **Contributors Graph**: GitHub automatically tracks
- **Special Thanks**: Major contributors get special mentions

## 📚 Resources

### Learning Materials

- **Clean Architecture**: [Clean Code Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- **Python Async**: [Real Python Async Guide](https://realpython.com/async-io-python/)
- **Telegram Bots**: [Official Bot API](https://core.telegram.org/bots/api)
- **MongoDB**: [Motor Documentation](https://motor.readthedocs.io/)

### Development Tools

- **VS Code**: Recommended editor with Python extension
- **PyCharm**: Professional Python IDE
- **Git**: Version control
- **MongoDB Compass**: Database management

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Maintain professional communication

### Communication Channels

- **Issues**: Bug reports and feature requests
- **Discussions**: General questions and ideas
- **Pull Requests**: Code contributions
- **Email**: Security issues only

---

**Thank you for contributing to making Telegram Automation System better!** 🎉