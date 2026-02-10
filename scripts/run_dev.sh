#!/bin/bash
# Development server startup script for Linux/macOS

set -e

echo "🚀 Starting Stock Agent Development Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration!"
fi

# Run the server
echo "✅ Starting FastAPI server..."
cd src
python -m uvicorn stock_agent.api.app:app --reload --host 0.0.0.0 --port 8000
