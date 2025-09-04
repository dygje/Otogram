# Use Python 3.12 slim image - Modern and stable
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml .
COPY README.md .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs sessions

# Create non-root user
RUN useradd --create-home --shell /bin/bash otogram \
    && chown -R otogram:otogram /app

USER otogram

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python scripts/health_check.py || exit 1

# Expose port (for monitoring/debugging)
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]