# Changelog

All notable changes to Telegram Automation System.

## [2.0.1] - 2025-01-13

### Changed
- **MIGRATION**: Migrated from pyrogram to pyrofork for continued support
- Updated dependency from `pyrogram==2.0.106` to `pyrofork==2.3.68`
- Updated all documentation references from pyrogram to pyrofork
- Maintained full backward compatibility - no API changes required

### Technical
- Pyrofork maintains pyrogram namespace for seamless migration
- All existing code continues to work without modifications
- Enhanced with latest bug fixes and improvements from pyrofork community
- Verified compatibility with Python 3.11+ and all dependencies

### Migration Notes
- Zero-downtime migration - existing sessions and configurations remain valid
- No changes required to existing code or configuration files
- Pyrofork provides active maintenance and updates unlike archived pyrogram

## [2.0.0] - 2025-09-02

### Added
- Modern documentation strategy with ADRs
- Clean architecture implementation  
- Stable dependency management
- Health check automation
- Project structure reorganization

### Changed
- **BREAKING**: Moved utility scripts to `scripts/` directory
- **BREAKING**: Reorganized documentation structure
- Updated all dependencies to stable, compatible versions
- Improved README with minimal approach

### Removed
- Outdated AI-generated documentation
- Redundant markdown files
- Deprecated setup instructions

### Technical
- Python 3.11+ requirement
- TgCrypto integration for performance
- Clean architecture with layered approach
- ADR-based decision tracking

---

## Previous Versions

For historical versions prior to restructure, see git history.

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible