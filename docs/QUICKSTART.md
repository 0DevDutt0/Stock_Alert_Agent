# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
# Clone and navigate to project
git clone https://github.com/yourusername/stock-agent.git
cd stock-agent

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env (optional - for Telegram alerts)
# Add your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
```

### 3. Run the Server

```bash
# Option 1: Using script (recommended)
.\scripts\run_dev.ps1  # Windows
./scripts/run_dev.sh   # Linux/macOS

# Option 2: Manual
cd src
python -m uvicorn stock_agent.api.app:app --reload --port 8000
```

### 4. Test the API

Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Analyze Your First Stock

Using the Swagger UI at http://localhost:8000/docs:

1. Click on `POST /api/v1/stocks/analyze`
2. Click "Try it out"
3. Enter:
   ```json
   {
     "symbol": "AAPL",
     "buy_price": 150,
     "target_price": 180
   }
   ```
4. Click "Execute"

You'll get a response with current price, profit, and decision!

## 📊 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/stock_agent --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser
```

## 🐳 Using Docker

```bash
# Build and run
docker-compose up --build

# Access API at http://localhost:8000
```

## 🔧 CLI Usage

```bash
# Analyze a stock
python -m stock_agent analyze --symbol AAPL --buy-price 150 --target-price 180

# Track a stock
python -m stock_agent track --symbol TCS.NS --buy-price 3500 --target-price 4000

# List tracked stocks
python -m stock_agent list

# Run agent
python -m stock_agent run
```

## 📚 Next Steps

- Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand the design
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Set up Telegram alerts for real-time notifications
- Deploy to production using Docker

## ❓ Troubleshooting

**Issue**: Module not found errors
- **Solution**: Make sure you're in the `src/` directory or run from project root with `python -m stock_agent`

**Issue**: Port 8000 already in use
- **Solution**: Change port with `--port 8001` flag

**Issue**: Telegram alerts not working
- **Solution**: Verify `.env` has correct `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

## 🎯 What's Next?

Check out the [README.md](README.md) for:
- Complete API documentation
- Advanced usage examples
- Deployment strategies
- Development roadmap
