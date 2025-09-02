# ADR-0004: Modern Repository Structure and AI Context

**Status**: Accepted  
**Date**: 2025-09-02  
**Deciders**: Development Team

## Context

The repository needed comprehensive supporting files to:
1. Prevent AI assistants from making incorrect assumptions
2. Enable proper development workflow for contributors
3. Follow modern Python project standards
4. Ensure consistent code quality and security

## Decision

We will implement a complete modern repository structure with:

### Essential Repository Files
- **pyproject.toml**: Modern Python project configuration
- **CONTRIBUTING.md**: Comprehensive contribution guidelines
- **CODE_OF_CONDUCT.md**: Community standards
- **SECURITY.md**: Security policy and reporting
- **LICENSE**: MIT license for open source
- **.editorconfig**: Consistent code style across editors

### GitHub Integration
- **Pull Request templates**: Standardized PR format
- **Issue templates**: Bug reports, feature requests, questions
- **CODEOWNERS**: Automatic code review assignments
- **GitHub Discussions**: Community support integration

### Development Workflow
- **.pre-commit-config.yaml**: Automated code quality checks
- **Makefile**: Convenient development commands
- **.env.example**: Environment configuration template
- **.dockerignore**: Docker build optimization

## Rationale

### AI Assistant Clarity
Modern AI platforms (like Emergent.sh, ChatGPT, GitHub Copilot) understand projects through:
- **Clear documentation**: README.md, CONTRIBUTING.md, docs/ structure
- **Project metadata**: pyproject.toml with comprehensive configuration
- **Consistent structure**: Well-organized folders and clear naming
- **Self-documenting code**: Type hints, clear function names, docstrings

### Developer Experience
Contributing developers need clear guidance:
- **Onboarding**: `CONTRIBUTING.md` provides step-by-step process
- **Standards**: Code style, architecture rules, testing requirements
- **Automation**: Pre-commit hooks catch issues before review
- **Convenience**: Makefile provides common commands

### Project Governance
Professional projects require:
- **Legal clarity**: MIT license for open source usage
- **Community standards**: Code of conduct for inclusive environment
- **Security process**: Clear vulnerability reporting process
- **Quality assurance**: Automated checks and reviews

### Modern Python Standards
Python ecosystem best practices:
- **pyproject.toml**: Replace setup.py with modern configuration
- **Type hints**: MyPy configuration for type safety
- **Code formatting**: Black and isort for consistency
- **Security**: Bandit and safety checks for vulnerabilities

## Implementation

### Project Configuration (pyproject.toml)
```toml
[project]
name = "telegram-automation-system"
version = "2.0.0"
requires-python = ">=3.11"
dependencies = [...]

[tool.black]
line-length = 100

[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true
```

### Development Workflow (Makefile)
```makefile
setup: install pre-commit
health: ## Run system health check
	python scripts/health_check.py
format: ## Format code
	black src/ scripts/
	isort src/ scripts/
```

### Documentation Structure
```
docs/
├── README.md              # Documentation index
├── GETTING_STARTED.md     # Complete setup guide
├── API.md                 # Code interfaces
├── CHANGELOG.md           # Version history
└── decisions/             # Architecture Decision Records
```

## Consequences

### Positive
- ✅ **AI Accuracy**: Detailed context prevents AI misunderstandings
- ✅ **Developer Onboarding**: Clear contribution process
- ✅ **Code Quality**: Automated checks maintain standards
- ✅ **Professional Image**: Complete repository structure
- ✅ **Security**: Sensitive data protected from AI exposure
- ✅ **Consistency**: All developers use same tools and standards

### Negative
- ❌ **Initial Complexity**: More files to understand initially
- ❌ **Maintenance**: Files need to be kept current
- ❌ **Tool Dependencies**: Requires pre-commit, black, isort, etc.

### Risk Mitigation
- **Documentation**: Clear explanations in each file
- **Automation**: Pre-commit hooks enforce standards automatically
- **Templates**: Copy-paste examples for common scenarios
- **Health Check**: Validates project structure integrity

## File Responsibilities

### Repository Management
- **pyproject.toml**: Project metadata, dependencies, tool configuration
- **CONTRIBUTING.md**: How to contribute, coding standards, workflow
- **SECURITY.md**: Security policy, vulnerability reporting process
- **LICENSE**: Legal terms for usage and distribution

### Development Workflow  
- **Makefile**: Common development commands and shortcuts
- **.pre-commit-config.yaml**: Automated quality checks
- **.env.example**: Configuration template with documentation
- **.editorconfig**: Cross-editor consistency

### AI Integration
- **.cursorrules**: Comprehensive project context for AI assistants
- **.gptignore**: Files to exclude from AI analysis (security)
- **.aiignore**: Additional AI context control (performance)

### GitHub Integration
- **.github/**: Issue templates, PR templates, CODEOWNERS
- **CODE_OF_CONDUCT.md**: Community standards and enforcement

## Maintenance Guidelines

### Regular Updates
- **Monthly**: Review and update dependency versions
- **Quarterly**: Update pre-commit hook versions
- **Per release**: Update version numbers and changelogs
- **As needed**: Update AI context files when architecture changes

### Quality Assurance
- Health check validates file structure integrity
- Pre-commit hooks enforce standards automatically
- CODEOWNERS ensures proper review coverage
- Security scanning prevents vulnerable dependencies

## Related ADRs
- [0001-clean-architecture](0001-clean-architecture.md): Architecture this supports
- [0002-dependency-management](0002-dependency-management.md): Dependency strategy
- [0003-documentation-strategy](0003-documentation-strategy.md): Documentation approach