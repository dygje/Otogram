# 📚 Documentation Index

Welcome to Telegram Automation System documentation. Our documentation follows **minimal documentation strategy** - essential information only, always up-to-date.

## 🚀 Quick Navigation

| Document | Purpose | Audience | Updated |
|----------|---------|----------|---------|
| [Getting Started](GETTING_STARTED.md) | Complete setup guide | New developers | 2025-09-02 |
| [API Reference](API.md) | Code interfaces & examples | Contributors | 2025-09-02 |
| [Changelog](CHANGELOG.md) | Version history | All users | 2025-09-02 |
| [Architecture Decisions](decisions/) | Technical decisions & rationale | Technical leads | 2025-09-02 |

## 📋 Documentation Principles

This documentation follows our **ADR-0003: Minimal Documentation Strategy**:

### ✅ What We Document
- **Setup & Usage**: Essential for getting started
- **API Interfaces**: What developers need to contribute
- **Architecture Decisions**: Why we made technical choices
- **Breaking Changes**: Version compatibility info

### ❌ What We Don't Document
- Implementation details (in code comments)
- Temporary issues or fixes
- Step-by-step code walkthroughs
- AI-generated filler content

## 🎯 Getting Started

**New to the project?** Start here:
1. [Getting Started](GETTING_STARTED.md) - Complete setup guide
2. [API Reference](API.md) - Understand the codebase
3. [Architecture Decisions](decisions/) - Learn why decisions were made

**Need help?** Check the root [README.md](../README.md) for quick commands.

## 🏗️ Architecture Overview

```
src/
├── core/           # Infrastructure (config, database)
├── models/         # Domain entities
├── services/       # Business logic  
└── telegram/       # Interface layer
```

For detailed architecture rationale, see [ADR-0001: Clean Architecture](decisions/0001-clean-architecture.md).

## 🔄 Maintenance

This documentation is maintained following **Documentation-as-Code** principles:

- **Version Control**: All docs in git with code
- **Living Documents**: Updated with code changes
- **Review Process**: Changes reviewed like code
- **Automated Checks**: Health check validates structure

### When to Update

| Change Type | Action Required |
|-------------|-----------------|
| New feature | Update API.md if public interface changes |
| Setup change | Update GETTING_STARTED.md |
| Breaking change | Update CHANGELOG.md + README.md |
| Architecture decision | Create new ADR |
| Bug fix | Usually no doc change needed |

## 📊 Quality Metrics

Our documentation health is tracked by:

```bash
# System health (includes doc structure)
python scripts/health_check.py

# Check for broken references
grep -r "TODO\|FIXME\|DEPRECATED" docs/

# Validate all essential docs exist
find docs -name "*.md" | wc -l  # Should be 7 files
```

## 🤝 Contributing to Documentation

1. **Follow minimal approach**: Ask "Is this essential?"
2. **Update with code**: Don't let docs drift
3. **Use clear language**: Write for humans, not robots
4. **Reference ADRs**: Link to decision rationale
5. **Test your changes**: Ensure health check passes

---

**Remember**: Good documentation is like good code - clear, concise, and maintainable.