#!/bin/bash
# Test execution script with coverage

set -e

echo "🧪 Running Stock Agent Tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
echo "📊 Running tests with coverage..."
pytest --cov=src/stock_agent --cov-report=term-missing --cov-report=html --cov-report=xml -v

echo "✅ Tests complete!"
echo "📈 Coverage report generated in htmlcov/index.html"
