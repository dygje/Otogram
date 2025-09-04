# Otogram - Personal Project Makefile
# Simplified commands for personal development

.PHONY: help setup install install-dev test test-fast lint format quality health clean run

# Default target
help: ## Show available commands
	@echo "🤖 Otogram - Personal Development Commands"
	@echo "==========================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
setup: install-dev ## Complete development setup
	@echo "✅ Personal development environment ready!"
	@echo "💡 Next steps:"
	@echo "   1. Setup MongoDB: make db-setup"
	@echo "   2. Configure: cp .env.example .env && nano .env"
	@echo "   3. Health check: make health"
	@echo "   4. Run: make run"

install: ## Install production dependencies
	@echo "📦 Installing production dependencies..."
	python -m pip install --upgrade pip
	pip install -e .

install-dev: ## Install development dependencies  
	@echo "📦 Installing development dependencies..."
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

# Development Tools - Optimized for personal use
health: ## Run system health check
	@echo "🩺 Running health check..."
	python scripts/health_check.py

test: ## Run tests with coverage (full)
	@echo "🧪 Running tests with coverage..."
	pytest tests/ -v --cov=src --cov-report=term-missing

test-fast: ## Run tests without coverage (quick)
	@echo "⚡ Running fast tests..."
	pytest tests/ -v --tb=short

lint: ## Check code quality
	@echo "🔍 Running code quality checks..."
	ruff check src/ scripts/ tests/

format: ## Format code automatically
	@echo "🎨 Formatting code..."
	ruff format src/ scripts/ tests/
	ruff check src/ scripts/ tests/ --fix

quality: ## Quick quality check (format + fast test)
	@echo "🔍 Quick quality check for personal development..."
	$(MAKE) format
	$(MAKE) test-fast

# Application Management
run: ## Run Otogram system
	@echo "🚀 Starting Otogram..."
	@echo "💡 Tip: Use Ctrl+C to stop"
	python main.py

# Database Management
db-setup: ## Show MongoDB setup options
	@echo "🗄️ MongoDB Setup Options:"
	@echo "1. Docker (Recommended):"
	@echo "   docker run -d -p 27017:27017 --name otogram-mongo mongo:7.0"
	@echo ""
	@echo "2. Local Installation:"
	@echo "   Ubuntu: sudo apt install mongodb"
	@echo "   macOS: brew install mongodb-community"
	@echo "   Windows: Download from mongodb.com"

db-start: ## Start MongoDB (Docker)
	@echo "🗄️ Starting MongoDB container..."
	docker start otogram-mongo || docker run -d -p 27017:27017 --name otogram-mongo mongo:7.0

db-status: ## Check MongoDB status
	@echo "🗄️ MongoDB Status:"
	@docker ps --filter name=otogram-mongo --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || echo "❌ MongoDB container not found"

# Maintenance & Cleanup
clean: ## Clean temporary files
	@echo "🧹 Cleaning temporary files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage

clean-sessions: ## Clean Telegram session files
	@echo "🗑️ Cleaning Telegram session files..."
	rm -rf sessions/ && mkdir -p sessions
	@echo "💡 You'll need to re-authenticate when you run again"

clean-logs: ## Clean application logs
	@echo "🗑️ Cleaning application logs..."
	rm -f logs/*.log && mkdir -p logs

clean-all: clean clean-sessions clean-logs ## Complete cleanup

# Configuration & Info
config: ## Show current configuration
	@echo "⚙️ Otogram Configuration:"
	@echo "Python: $(shell python --version)"
	@echo "Version: $(shell grep '^version' pyproject.toml | cut -d'"' -f2)"
	@echo "Dependencies installed: $(shell pip list | grep -E '(pyrofork|python-telegram-bot|motor)' | wc -l)/3 core packages"

# Docker shortcuts
docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t otogram:latest .

docker-run: ## Run with Docker Compose
	@echo "🐳 Starting with Docker Compose..."
	docker-compose up -d

docker-logs: ## Show Docker logs
	@echo "🐳 Docker logs:"
	docker-compose logs -f

docker-stop: ## Stop Docker services
	@echo "🐳 Stopping Docker services..."
	docker-compose down

# Personal workflow shortcuts
dev: ## Start development session
	@echo "🔧 Starting development session..."
	$(MAKE) format
	$(MAKE) health
	@echo "✅ Ready for development!"

quick-start: ## Quick start from fresh clone
	@echo "⚡ Quick start setup..."
	$(MAKE) setup
	$(MAKE) db-start
	@echo "📝 Now edit .env file and run: make run"

# First-time user guide
first-time: ## First time setup guide
	@echo "🎯 Otogram - First Time Setup Guide"
	@echo "===================================="
	@echo "1. Install Python 3.11+ or 3.12 (recommended) and MongoDB"
	@echo "2. Clone and setup: make setup"
	@echo "3. Start database: make db-start"
	@echo "4. Configure: cp .env.example .env && nano .env"
	@echo "5. Health check: make health"
	@echo "6. Run system: make run"
	@echo ""
	@echo "📚 Documentation: README.md and docs/ folder"
	@echo "🚀 Quick start: make quick-start"