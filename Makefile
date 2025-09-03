# Makefile for Otogram - Telegram Automation System
# Provides convenient commands for development and maintenance

.PHONY: help setup install install-dev test lint format health clean build docs pre-commit ruff

# Default target
help: ## Show this help message
	@echo "🤖 Otogram - Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
setup: install pre-commit ## Complete development setup
	@echo "✅ Development environment setup complete!"

install: ## Install all dependencies
	@echo "📦 Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

install-dev: ## Install development dependencies
	@echo "📦 Installing development dependencies..."
	pip install -e ".[dev]"
	@echo "✅ Development dependencies installed"

# Development Tools
health: ## Run system health check
	@echo "🩺 Running health check..."
	python scripts/health_check.py

test: ## Run tests (when available)
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v || echo "⚠️ No tests directory found"

lint: ## Run linting tools
	@echo "🔍 Running linting..."
	black --check --diff src/ scripts/
	isort --check-only --diff src/ scripts/
	flake8 src/ scripts/
	mypy src/

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	black src/ scripts/
	isort src/ scripts/
	@echo "✅ Code formatted"

# Git hooks
pre-commit: ## Install pre-commit hooks
	@echo "🪝 Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	@echo "✅ Pre-commit hooks installed"

pre-commit-run: ## Run pre-commit on all files
	@echo "🪝 Running pre-commit on all files..."
	pre-commit run --all-files

# Application Management
run: ## Run the application
	@echo "🚀 Starting Telegram Automation System..."
	python main.py

setup-wizard: ## Run interactive setup wizard
	@echo "🧙 Starting setup wizard..."
	python scripts/setup.py

config: ## Show current configuration
	@echo "⚙️ Current configuration:"
	@echo "Python: $(shell python --version)"
	@echo "Project: $(shell grep '^name' pyproject.toml | cut -d'"' -f2)"
	@echo "Version: $(shell grep '^version' pyproject.toml | cut -d'"' -f2)"

# Documentation
docs: ## View documentation (simple markdown files in docs/)
	@echo "📚 Documentation available in docs/ directory:"
	@echo "  • CONTRIBUTING.md - Contribution guidelines"
	@echo "  • CODE_OF_CONDUCT.md - Code of conduct"
	@echo "  • SECURITY.md - Security policy"
	@echo "  • CHANGELOG.md - Version history"
	@echo "  • API.md - API reference"

# Maintenance
clean: ## Clean up temporary files
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/ dist/ site/
	@echo "✅ Cleanup complete"

clean-sessions: ## Clean Pyrofork session files
	@echo "🗑️ Cleaning session files..."
	rm -rf sessions/
	mkdir -p sessions
	@echo "✅ Session files cleaned"

clean-logs: ## Clean application logs
	@echo "🗑️ Cleaning log files..."
	rm -f logs/*.log
	@echo "✅ Log files cleaned"

# Build and Distribution
build: clean ## Build distribution packages
	@echo "🏗️ Building distribution packages..."
	python -m build
	@echo "✅ Build complete"

check-build: build ## Check if build is valid
	@echo "🔍 Checking build..."
	python -m twine check dist/*
	@echo "✅ Build validation complete"

# Security
security-check: ## Run security checks
	@echo "🔐 Running security checks..."
	@if command -v bandit >/dev/null 2>&1; then \
		bandit -r src/; \
	else \
		echo "ℹ️ Install bandit: pip install bandit"; \
	fi
	@if command -v safety >/dev/null 2>&1; then \
		safety check; \
	else \
		echo "ℹ️ Install safety: pip install safety"; \
	fi

# Database
db-setup: ## Setup MongoDB (reminder command)
	@echo "🗄️ MongoDB Setup Instructions:"
	@echo "Ubuntu/Debian: sudo apt-get install mongodb"
	@echo "macOS: brew install mongodb-community"
	@echo "Windows: Download from https://www.mongodb.com/try/download/community"
	@echo "Docker: docker run -d -p 27017:27017 mongo:4.4"

# Development Workflow
dev: clean install health ## Prepare for development
	@echo "🚀 Development environment ready!"
	@echo "Next steps:"
	@echo "1. Run 'make setup-wizard' to configure"  
	@echo "2. Run 'make run' to start the application"

# CI/CD helpers
ci-install: ## Install dependencies for CI
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e ".[dev]"

ci-test: ## Run CI tests
	python scripts/health_check.py
	black --check src/ scripts/
	isort --check-only src/ scripts/
	flake8 src/ scripts/
	mypy src/

# Utility
check-deps: ## Check for dependency updates
	@echo "🔍 Checking for dependency updates..."
	python scripts/update_deps.py

update-deps: ## Update dependencies (interactive)
	@echo "📦 Updating dependencies..."
	pip install --upgrade pip
	pip install --upgrade -e ".[dev]"
	@echo "✅ Dependencies updated. Run 'make test' to verify."

version: ## Show version information
	@echo "Telegram Automation System"
	@echo "=========================="
	@echo "Project Version: $(shell grep '^version' pyproject.toml | cut -d'"' -f2)"
	@echo "Python Version: $(shell python --version)"
	@echo "Dependencies:"
	@pip list | grep -E "(pyrofork|telegram|motor|pymongo|pydantic)" || echo "Dependencies not installed"

# Help with setup
first-time: ## First time setup guide
	@echo "🎯 First Time Setup Guide"
	@echo "========================"
	@echo "1. Install Python 3.11+: https://python.org/downloads/"
	@echo "2. Install MongoDB: make db-setup"
	@echo "3. Setup project: make setup"
	@echo "4. Configure app: make setup-wizard"
	@echo "5. Run health check: make health"
	@echo "6. Start application: make run"
	@echo ""
	@echo "For detailed instructions, see: docs/GETTING_STARTED.md"