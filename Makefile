# Makefile for Otogram - Personal Project
# Simple development commands

.PHONY: help setup install install-dev test lint format health clean run

# Default target
help: ## Show available commands
	@echo "🤖 Otogram - Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
setup: install-dev ## Complete development setup
	@echo "✅ Development environment ready!"
	@echo "Next: Run 'make health' to verify installation"

install: ## Install production dependencies
	@echo "📦 Installing production dependencies..."
	python -m pip install --upgrade pip
	pip install -e .

install-dev: ## Install development dependencies  
	@echo "📦 Installing development dependencies..."
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

# Development Tools
health: ## Run system health check
	@echo "🩺 Running health check..."
	python scripts/health_check.py

test: ## Run tests with coverage
	@echo "🧪 Running tests..."
	pytest tests/ -v --cov=src --cov-report=term-missing

test-fast: ## Run tests without coverage
	@echo "⚡ Running fast tests..."
	pytest tests/ -v

lint: ## Run code quality checks
	@echo "🔍 Running quality checks..."
	ruff check src/ scripts/ tests/
	mypy src/

format: ## Format code
	@echo "🎨 Formatting code..."
	ruff format src/ scripts/ tests/
	ruff check src/ scripts/ tests/ --fix

quality: ## Run all quality checks
	@echo "🔍 Running complete quality check..."
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test-fast

# Application Management
run: ## Run Otogram system
	@echo "🚀 Starting Otogram..."
	python main.py

# Maintenance & Cleanup
clean: ## Clean temporary files
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/
	rm -f .coverage coverage.xml

clean-sessions: ## Clean Telegram session files
	@echo "🗑️ Cleaning session files..."
	rm -rf sessions/
	mkdir -p sessions

clean-logs: ## Clean application logs
	@echo "🗑️ Cleaning log files..."
	rm -f logs/*.log
	mkdir -p logs

clean-all: clean clean-sessions clean-logs ## Complete cleanup
	@echo "🧹 Complete cleanup finished"

# Database Management
db-setup: ## MongoDB setup instructions
	@echo "🗄️ MongoDB Setup Options:"
	@echo "Docker (easiest): docker run -d -p 27017:27017 --name otogram-mongo mongo:7.0"
	@echo "Ubuntu/Debian: sudo apt-get install mongodb"
	@echo "macOS: brew install mongodb-community"

# Development Workflow
dev: clean install-dev health ## Prepare for development
	@echo "🚀 Development environment ready!"

# Utilities
config: ## Show current configuration
	@echo "⚙️ Current configuration:"
	@echo "Python: $(shell python --version)"
	@echo "Project: otogram $(shell grep '^version' pyproject.toml | cut -d'"' -f2)"

version: ## Show version information
	@echo "🤖 Otogram - Personal Telegram Automation"
	@echo "Version: $(shell grep '^version' pyproject.toml | cut -d'"' -f2)"
	@echo "Python: $(shell python --version)"

# First time setup
first-time: ## First time setup guide
	@echo "🎯 Otogram - First Time Setup"
	@echo "=============================="
	@echo "1. Install Python 3.11+: https://python.org/downloads/"
	@echo "2. Setup MongoDB: make db-setup"
	@echo "3. Install dependencies: make setup"
	@echo "4. Configure credentials: cp .env.example .env && nano .env"
	@echo "5. Run health check: make health"
	@echo "6. Start system: make run"