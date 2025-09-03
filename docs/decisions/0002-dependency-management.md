# ADR-0002: Stable Dependency Management

**Status**: Accepted  
**Date**: 2025-09-02  
**Deciders**: Development Team

## Context

The project requires stable, compatible dependencies that work reliably with Python 3.11+ and don't introduce breaking changes or conflicts.

## Decision

We will use researched, stable versions of all dependencies with compatibility verification:

```
# Telegram Libraries
pyrofork==2.3.68            # Updated MTProto client (fork of pyrogram)
python-telegram-bot==20.8   # Latest stable Bot API
TgCrypto==1.2.5            # Performance enhancement

# Database  
motor==3.7.0               # Python 3.11 support
pymongo==4.11.0            # Stable MongoDB driver

# Core
pydantic==2.8.2            # Stable data validation
loguru==0.7.2              # Mature logging
```

## Rationale

### Research Findings
- **Pyrogram**: Original project discontinued, but 2.0.106 is last stable version
- **python-telegram-bot**: 20.8 is latest stable with Python 3.11 support
- **Motor/PyMongo**: 3.7.0/4.11.0 officially support Python 3.11
- **TgCrypto**: Essential for Pyrogram performance optimization

### Selection Criteria
1. **Stability**: Proven track record in production
2. **Compatibility**: Python 3.11+ support verified
3. **Maintenance**: Active or stable final versions
4. **Performance**: Optimized for production use

## Consequences

### Positive
- ✅ No dependency conflicts or version incompatibilities
- ✅ Stable performance in production
- ✅ Predictable behavior across environments
- ✅ Security updates available for maintained packages

### Negative
- ❌ May not have latest features from cutting-edge versions
- ❌ Requires periodic review for security updates

## Implementation

### Installation Process
```bash
# Always install exact versions
pip install -r requirements.txt

# Verify installation
python scripts/health_check.py
```

### Update Policy
- **Security updates**: Apply immediately after testing
- **Minor updates**: Quarterly review cycle
- **Major updates**: Annual review with full testing

### Monitoring
- Monthly dependency security scans
- Automated health checks in CI/CD
- Performance monitoring for regressions

## Related ADRs
- [0001-clean-architecture](0001-clean-architecture.md)
- [0003-documentation-strategy](0003-documentation-strategy.md)