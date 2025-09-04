# Makefile for Otogram - Personal Project
# Essential commands only

.PHONY: help setup install install-dev test lint format health clean run

# Default target
help: ## Show available commands
	@echo "🤖 Otogram - Personal Development Commands"
	@echo "==========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
setup: install-dev ## Complete development setup
	@echo "✅ Personal development environment ready!"

install: ## Install production dependencies
	@echo "📦 Installing dependencies..."
	python -m pip install --upgrade pip
	pip install -e .

install-dev: ## Install development dependencies  
	@echo "📦 Installing dev dependencies..."
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

# Development Tools
health: ## Run system health check
	@echo "🩺 Running health check..."
	python scripts/health_check.py

test: ## Run tests (relaxed coverage for personal project)
	@echo "🧪 Running tests..."
	pytest tests/ -v --cov=src --cov-report=term-missing

test-fast: ## Run tests without coverage
	@echo "⚡ Running fast tests..."
	pytest tests/ -v

lint: ## Basic code quality checks
	@echo "🔍 Running lint checks..."
	ruff check src/ scripts/ tests/

format: ## Format code
	@echo "🎨 Formatting code..."
	ruff format src/ scripts/ tests/
	ruff check src/ scripts/ tests/ --fix

quality: ## Quick quality check (personal project)
	@echo "🔍 Quick quality check..."
	$(MAKE) format
	$(MAKE) test-fast

# Application Management
run: ## Run Otogram system
	@echo "🚀 Starting Otogram..."
	python main.py

setup-wizard: ## Run simple setup wizard
	@echo "🧙 Starting setup..."
	python scripts/setup.py

# Maintenance & Cleanup
clean: ## Clean temporary files
	@echo "🧹 Cleaning up..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.egg-info" -exec rm -rf {} +
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +
	find . -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage

clean-sessions: ## Clean Telegram session files
	@echo "🗑️ Cleaning session files..."
	rm -rf sessions/ && mkdir -p sessions

clean-logs: ## Clean application logs
	@echo "🗑️ Cleaning logs..."
	rm -f logs/*.log && mkdir -p logs

clean-all: clean clean-sessions clean-logs ## Complete cleanup

# Database
db-setup: ## MongoDB setup help
	@echo "🗄️ MongoDB Setup:"
	@echo "Docker: docker run -d -p 27017:27017 --name otogram-mongo mongo:7.0"
	@echo "Local: sudo apt install mongodb (Ubuntu) or brew install mongodb-community (macOS)"

# Info
config: ## Show current config
	@echo "⚙️ Otogram Configuration:"
	@echo "Python: $(shell python --version)"
	@echo "Version: $(shell grep '^version' pyproject.toml | cut -d'"' -f2)"

# Simple first-time guide
first-time: ## First time setup guide
	@echo "🎯 Otogram - First Time Setup"
	@echo "=============================="
	@echo "1. Install Python 3.11+"
	@echo "2. Run: make setup"
	@echo "3. Setup MongoDB: make db-setup"
	@echo "4. Configure: make setup-wizard"
	@echo "5. Run: make run"