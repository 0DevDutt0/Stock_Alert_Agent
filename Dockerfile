# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 stockagent && \
    mkdir -p /app/data /app/logs && \
    chown -R stockagent:stockagent /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/stockagent/.local

# Copy application code
COPY --chown=stockagent:stockagent src/ ./src/
COPY --chown=stockagent:stockagent .env.example .env.example

# Set environment variables
ENV PATH=/home/stockagent/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER stockagent

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)"

# Run application
CMD ["python", "-m", "uvicorn", "stock_agent.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
