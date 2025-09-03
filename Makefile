# Makefile for Otogram - Telegram Automation System
# Provides convenient commands for development and maintenance

.PHONY: help setup install install-dev test lint format health clean build docs pre-commit ruff

# Default target
help: ## Show this help message
	@echo "🤖 Otogram - Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
setup: install-dev pre-commit ## Complete development setup
	@echo "✅ Development environment setup complete!"
	@echo "Run 'make health' to verify installation"

install: ## Install production dependencies
	@echo "📦 Installing production dependencies..."
	python -m pip install --upgrade pip
	pip install -e .
	@echo "✅ Production dependencies installed"

install-dev: ## Install development dependencies  
	@echo "📦 Installing development dependencies..."
	python -m pip install --upgrade pip
	pip install -e ".[dev]"
	@echo "✅ Development dependencies installed"

# Development Tools
health: ## Run system health check
	@echo "🩺 Running health check..."
	python scripts/health_check.py

test: ## Run tests with coverage
	@echo "🧪 Running tests..."
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

test-fast: ## Run tests without coverage
	@echo "⚡ Running fast tests..."
	pytest tests/ -v

ruff: ## Run ruff linting and formatting
	@echo "🦀 Running ruff..."
	ruff check src/ scripts/ tests/ --fix
	ruff format src/ scripts/ tests/

lint: ## Run all linting tools
	@echo "🔍 Running linting..."
	ruff check src/ scripts/ tests/
	black --check --diff src/ scripts/ tests/
	isort --check-only --diff src/ scripts/ tests/
	mypy src/

format: ## Format code with ruff, black and isort
	@echo "🎨 Formatting code..."
	ruff format src/ scripts/ tests/
	black src/ scripts/ tests/
	isort src/ scripts/ tests/
	@echo "✅ Code formatted"

quality: ## Run all quality checks
	@echo "🔍 Running quality checks..."
	$(MAKE) lint
	$(MAKE) test-fast
	@echo "✅ Quality checks complete"

# Security & Quality
security: ## Run security checks
	@echo "🔐 Running security checks..."
	@if command -v bandit >/dev/null 2>&1; then \
		bandit -r src/ -f json -o bandit-report.json; \
		echo "✅ Bandit security scan complete"; \
	else \
		echo "⚠️ Install bandit: pip install bandit"; \
	fi
	@if command -v safety >/dev/null 2>&1; then \
		safety check --json --output safety-report.json; \
		echo "✅ Safety dependency scan complete"; \
	else \
		echo "⚠️ Install safety: pip install safety"; \
	fi

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
run: ## Run the Otogram system
	@echo "🚀 Starting Otogram - Telegram Automation System..."
	python main.py

setup-wizard: ## Run interactive setup wizard
	@echo "🧙 Starting setup wizard..."
	python scripts/setup.py

config: ## Show current configuration
	@echo "⚙️ Current configuration:"
	@echo "Python: $(shell python --version)"
	@echo "Project: otogram"
	@echo "Version: $(shell grep '^version' pyproject.toml | cut -d'"' -f2)"

# Documentation
docs: ## View documentation
	@echo "📚 Documentation available:"
	@echo "  • README.md - Main project documentation"
	@echo "  • docs/CONTRIBUTING.md - Contribution guidelines"
	@echo "  • docs/SECURITY.md - Security policy"
	@echo "  • docs/CHANGELOG.md - Version history"
	@echo "  • docs/API.md - API reference"
	@echo "  • docs/GETTING_STARTED.md - Setup guide"

# Maintenance & Cleanup
clean: ## Clean up temporary files
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build/ dist/ site/ htmlcov/
	rm -f .coverage coverage.xml bandit-report.json safety-report.json
	@echo "✅ Cleanup complete"

clean-sessions: ## Clean Pyrofork session files
	@echo "🗑️ Cleaning session files..."
	rm -rf sessions/
	mkdir -p sessions
	@echo "✅ Session files cleaned"

clean-logs: ## Clean application logs
	@echo "🗑️ Cleaning log files..."
	rm -f logs/*.log
	mkdir -p logs
	@echo "✅ Log files cleaned"

clean-all: clean clean-sessions clean-logs ## Full cleanup
	@echo "🧹 Complete cleanup finished"

# Build and Distribution
build: clean ## Build distribution packages
	@echo "🏗️ Building distribution packages..."
	python -m build
	@echo "✅ Build complete"

check-build: build ## Check if build is valid
	@echo "🔍 Checking build..."
	python -m twine check dist/*
	@echo "✅ Build validation complete"

# Development Workflow
dev: clean install-dev health ## Prepare for development
	@echo "🚀 Development environment ready!"
	@echo "Next steps:"
	@echo "1. Run 'make setup-wizard' to configure"
	@echo "2. Run 'make run' to start Otogram"

# CI/CD helpers
ci-install: ## Install dependencies for CI
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

ci-test: ## Run CI tests and checks
	python scripts/health_check.py
	ruff check src/ scripts/ tests/
	black --check src/ scripts/ tests/
	isort --check-only src/ scripts/ tests/
	mypy src/
	pytest tests/ -v --cov=src

# Database Management
db-setup: ## MongoDB setup instructions
	@echo "🗄️ MongoDB Setup Instructions:"
	@echo "Ubuntu/Debian: sudo apt-get install mongodb"
	@echo "macOS: brew install mongodb-community"
	@echo "Windows: Download from https://www.mongodb.com/try/download/community"
	@echo "Docker: docker run -d -p 27017:27017 --name otogram-mongo mongo:7.0"

# Utilities
check-deps: ## Check for dependency updates
	@echo "🔍 Checking for dependency updates..."
	python scripts/update_deps.py

update-deps: ## Update dependencies
	@echo "📦 Updating dependencies..."
	python -m pip install --upgrade pip
	pip install --upgrade -e ".[dev]"
	@echo "✅ Dependencies updated. Run 'make test' to verify."

version: ## Show version information
	@echo "🤖 Otogram - Telegram Automation System"
	@echo "========================================"
	@echo "Project Version: $(shell grep '^version' pyproject.toml | cut -d'"' -f2)"
	@echo "Python Version: $(shell python --version)"
	@echo "Key Dependencies:"
	@pip list | grep -E "(pyrofork|telegram|motor|pymongo|pydantic)" || echo "Dependencies not installed"

# Help & Setup
first-time: ## First time setup guide
	@echo "🎯 Otogram - First Time Setup Guide"
	@echo "===================================="
	@echo "1. Install Python 3.11+: https://python.org/downloads/"
	@echo "2. Install MongoDB: make db-setup"
	@echo "3. Setup project: make setup"
	@echo "4. Configure app: make setup-wizard"
	@echo "5. Run health check: make health"
	@echo "6. Start Otogram: make run"
	@echo ""
	@echo "For detailed instructions, see: docs/GETTING_STARTED.md"