# Contributing to Telegram Automation System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🚀 Quick Start

1. **Fork and clone** the repository
2. **Set up development environment**:
   ```bash
   pip install -r requirements.txt
   python scripts/health_check.py
   ```
3. **Create a feature branch**: `git checkout -b feature/amazing-feature`
4. **Make your changes** following our guidelines below
5. **Test your changes**: `python scripts/health_check.py`
6. **Submit a pull request**

## 📋 Development Guidelines

### Code Standards

- **Python Version**: 3.11+
- **Code Style**: Follow PEP 8
- **Type Hints**: Use type hints for function parameters and return values
- **Docstrings**: Use docstrings for public functions and classes
- **Imports**: Use absolute imports, organize with `src.` prefix

### Architecture

This project follows **Clean Architecture**:
- `src/core/`: Infrastructure (database, config)
- `src/models/`: Domain entities  
- `src/services/`: Business logic
- `src/telegram/`: Interface layer

See [ADR-0001](docs/decisions/0001-clean-architecture.md) for rationale.

### Testing

- Run health check: `python scripts/health_check.py`
- Test imports: `python -c "from src.core.config import settings; print('OK')"`
- Manual testing: Use `scripts/setup.py` for test environment

### Dependencies

- **Add new dependencies**: Update `requirements.txt` with specific versions
- **Research compatibility**: Ensure Python 3.11+ support
- **Document rationale**: Create ADR for major dependency changes

See [ADR-0002](docs/decisions/0002-dependency-management.md) for guidelines.

## 📝 Documentation

Follow our **Minimal Documentation Strategy**:

### When to Update Documentation

| Change Type | Action Required |
|-------------|-----------------|
| New public API | Update `docs/API.md` |
| Setup process change | Update `docs/GETTING_STARTED.md` |
| Breaking change | Update `CHANGELOG.md` + `README.md` |
| Architecture decision | Create new ADR in `docs/decisions/` |
| Bug fix | Usually no documentation change |

### Documentation Guidelines

- **Essential only**: Don't document implementation details
- **Clear language**: Write for humans, not robots
- **Living documents**: Update with code changes
- **Link to rationale**: Reference ADRs for context

See [ADR-0003](docs/decisions/0003-documentation-strategy.md) for full strategy.

## 🔄 Pull Request Process

### Before Submitting

1. **Health check passes**: `python scripts/health_check.py`
2. **Documentation updated**: If needed per guidelines above
3. **Clean commits**: Squash related commits, clear messages
4. **Branch updated**: Rebase on latest main if needed

### PR Template

Our PR template will guide you through:
- [ ] Description of changes
- [ ] Type of change (bug fix, feature, etc.)
- [ ] Testing performed
- [ ] Documentation updates
- [ ] Health check results

### Code Review

- **Automatic reviews**: CODEOWNERS will assign reviewers
- **Review criteria**: Code quality, architecture compliance, documentation
- **Response time**: We aim to review within 48 hours

## 🐛 Bug Reports

Use the bug report template in Issues:
- **Clear description**: What happened vs. what expected
- **Reproduction steps**: How to reproduce the issue
- **Environment**: Python version, OS, dependencies
- **Logs**: Include relevant log snippets

## ✨ Feature Requests

Use the feature request template in Issues:
- **Problem statement**: What problem does this solve?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought of
- **Additional context**: Screenshots, examples, etc.

## 🏗️ Architecture Changes

For significant architectural changes:

1. **Discuss first**: Open an issue to discuss the approach
2. **Create ADR**: Document the decision rationale
3. **Update documentation**: Ensure docs reflect changes
4. **Consider impact**: Breaking changes need version bump

## ❓ Questions & Support

- **Documentation**: Check `docs/` first
- **Issues**: Search existing issues for similar problems
- **Discussions**: Use GitHub Discussions for questions
- **Health Check**: Run `python scripts/health_check.py` for system issues

## 📊 Code Quality

We maintain high code quality through:
- **Clear architecture**: Well-defined layers and responsibilities
- **Type safety**: Type hints and validation
- **Error handling**: Comprehensive exception handling
- **Logging**: Structured logging with Loguru
- **Testing**: Health checks and integration testing

Thank you for contributing to make this project better! 🎉