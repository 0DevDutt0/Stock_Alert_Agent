# 📈 Stock Agent - Autonomous Stock Monitoring System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> **An intelligent, autonomous stock monitoring agent that tracks portfolio performance in real-time and delivers instant alerts via Telegram when target prices are reached.**

## 🎯 Project Overview

Stock Agent is a production-ready financial monitoring system that combines real-time market data analysis with automated alerting. Built with modern Python technologies, it demonstrates proficiency in API development, asynchronous operations, and event-driven architecture.

### Key Features

- **🤖 Autonomous Monitoring**: Continuously tracks multiple stocks without manual intervention
- **📊 Real-Time Analysis**: Fetches live market data using Yahoo Finance API
- **🎯 Smart Alerts**: Telegram notifications when target prices are reached
- **⏰ Scheduled Updates**: Daily price reports at 12 PM IST
- **💾 Persistent Storage**: JSON-based stock portfolio management
- **🚀 RESTful API**: FastAPI-powered backend with automatic documentation
- **📈 Profit Tracking**: Real-time profit/loss calculations with percentage metrics

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Server                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Analyze    │  │  Track Stock │  │  Run Agent   │  │
│  │   Endpoint   │  │   Endpoint   │  │  (Cron Job)  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────────────┴──────────────────┘          │
│                            │                             │
│                    ┌───────▼────────┐                    │
│                    │  Stock Agent   │                    │
│                    │  (Core Logic)  │                    │
│                    └───────┬────────┘                    │
│                            │                             │
│         ┌──────────────────┼──────────────────┐          │
│         │                  │                  │          │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌───────▼──────┐  │
│  │ Stock Tool   │  │   Storage    │  │    Alerts    │  │
│  │ (yfinance)   │  │   (JSON)     │  │  (Telegram)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI | High-performance async API server |
| **Market Data** | yfinance | Real-time stock price fetching |
| **Alerts** | Telegram Bot API | Push notifications |
| **Storage** | JSON | Lightweight persistent data |
| **Timezone** | pytz | IST timezone handling |
| **Validation** | Pydantic | Request/response models |

---

## 📂 Project Structure

```
stock-agent/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── data/
│   └── stocks.json             # Stock tracking database
├── docs/
│   ├── ARCHITECTURE.md         # Architecture documentation
│   └── API.md                  # API documentation (future)
├── scripts/
│   ├── run_dev.sh              # Development server (Linux/macOS)
│   ├── run_dev.ps1             # Development server (Windows)
│   └── run_tests.sh            # Test execution script
├── src/
│   └── stock_agent/
│       ├── __init__.py
│       ├── __main__.py         # CLI entry point
│       ├── config.py           # Configuration management
│       ├── api/
│       │   ├── app.py          # FastAPI application
│       │   ├── dependencies.py # Dependency injection
│       │   └── routers/
│       │       ├── health.py   # Health check endpoint
│       │       ├── stocks.py   # Stock endpoints
│       │       └── agent.py    # Agent execution endpoint
│       ├── models/
│       │   ├── enums.py        # Enumerations
│       │   └── stock.py        # Pydantic models
│       ├── services/
│       │   ├── stock_service.py        # Business logic
│       │   ├── market_data_service.py  # Market data fetching
│       │   └── alert_service.py        # Telegram alerts
│       ├── repositories/
│       │   ├── stock_repository.py     # Repository interface
│       │   └── database_repository.py  # Future DB implementation
│       └── utils/
│           ├── logger.py       # Logging configuration
│           └── exceptions.py   # Custom exceptions
├── tests/
│   ├── conftest.py             # Test fixtures
│   ├── unit/
│   │   ├── test_stock_service.py
│   │   └── test_market_data_service.py
│   └── integration/
│       └── test_api.py
├── .dockerignore
├── .env.example                # Environment template
├── .gitignore
├── CONTRIBUTING.md             # Contribution guidelines
├── Dockerfile                  # Production Docker image
├── docker-compose.yml          # Local development
├── pytest.ini                  # Test configuration
├── README.md
├── requirements.txt            # Production dependencies
└── requirements-dev.txt        # Development dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (optional, for alerts)
- Internet connection for live market data

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-agent.git
   cd stock-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
   # For development (includes testing tools)
   pip install -r requirements-dev.txt
   ```

4. **Configure environment**
   
   Copy the environment template:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Telegram credentials (optional):
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

### Running the Application

**Option 1: Using Scripts (Recommended)**

```bash
# Linux/macOS
./scripts/run_dev.sh

# Windows PowerShell
.\scripts\run_dev.ps1
```

**Option 2: Manual Start**

```bash
cd src
python -m uvicorn stock_agent.api.app:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Using Docker**

```bash
# Build and run with docker-compose
docker-compose up --build

# Or build Docker image manually
docker build -t stock-agent .
docker run -p 8000:8000 --env-file .env stock-agent
```

The API will be available at `http://localhost:8000`

**Access interactive documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/health`

---

## 📖 API Documentation

### Endpoints

#### 1. Health Check
```http
GET /health
```
Returns API status and dependency health.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "dependencies": {
    "market_data": "healthy",
    "storage": "healthy",
    "telegram": "configured"
  }
}
```

---

#### 2. Analyze Stock (One-Time)
```http
POST /api/v1/stocks/analyze
```

Performs instant analysis on a stock without tracking it.

**Request Body:**
```json
{
  "symbol": "TCS.NS",
  "buy_price": 3500.00,
  "target_price": 4000.00
}
```

**Response:**
```json
{
  "symbol": "TCS.NS",
  "buy_price": 3500.0,
  "current_price": 3750.25,
  "target_price": 4000.0,
  "profit": 250.25,
  "profit_percent": 7.15,
  "decision": "⏳ HOLD"
}
```

**Decision Types:**
- `🎯 TARGET REACHED` - Current price ≥ target price
- `⏳ HOLD` - Current price between buy and target
- `🔻 BELOW BUY PRICE` - Current price < buy price

---

#### 3. Track Stock (Persistent)
```http
POST /api/v1/stocks/track
```

Adds a stock to the monitoring list for continuous tracking.

**Request Body:**
```json
{
  "symbol": "INFY.NS",
  "buy_price": 1450.00,
  "target_price": 1600.00
}
```

**Response:**
```json
{
  "message": "INFY.NS added successfully"
}
```

---

#### 4. List Tracked Stocks
```http
GET /api/v1/stocks
```

Returns all stocks currently being monitored.

**Response:**
```json
[
  {
    "symbol": "TCS.NS",
    "buy_price": 3500.0,
    "target_price": 4000.0
  },
  {
    "symbol": "INFY.NS",
    "buy_price": 1450.0,
    "target_price": 1600.0
  }
]
```

---

#### 5. Run Agent (Autonomous Check)
```http
GET /api/v1/agent/run
```

Executes the monitoring agent to check all tracked stocks and send alerts.

**Response:**
```json
{
  "time_ist": "2026-02-10 12:00:00",
  "total_stocks": 2,
  "results": [
    {
      "symbol": "TCS.NS",
      "buy_price": 3500.0,
      "current_price": 4050.0,
      "target_price": 4000.0,
      "profit": 550.0,
      "profit_percent": 15.71,
      "decision": "🎯 TARGET REACHED"
    }
  ]
}
```

**Alert Triggers:**
1. **Target Reached**: Instant Telegram notification
2. **Daily Update**: Every day at 12:00 PM IST (within 5-minute window)

---

## 🔧 Usage Examples

### Example 1: Quick Stock Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/stocks/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "buy_price": 150.00,
    "target_price": 180.00
  }'
```

### Example 2: Set Up Automated Monitoring

```python
import requests

# Add stocks to tracking list
stocks = [
    {"symbol": "TCS.NS", "buy_price": 3500, "target_price": 4000},
    {"symbol": "INFY.NS", "buy_price": 1450, "target_price": 1600},
    {"symbol": "RELIANCE.NS", "buy_price": 2400, "target_price": 2700}
]

for stock in stocks:
    response = requests.post(
        "http://localhost:8000/api/v1/stocks/track",
        json=stock
    )
    print(response.json())
```

### Example 3: Schedule Autonomous Checks

Use a cron job or task scheduler to hit the `/run-agent` endpoint:

**Linux/macOS (crontab):**
```bash
# Check every 5 minutes during market hours (9 AM - 4 PM IST)
*/5 9-16 * * 1-5 curl http://localhost:8000/api/v1/agent/run
```

**Windows (Task Scheduler):**
```powershell
# PowerShell script
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agent/run" -Method Get
```

---

## 🎨 Telegram Alert Examples

### Target Reached Alert
```
🎯 TARGET REACHED!

Stock: TCS.NS
Buy Price: 3500.0
Current Price: 4050.0
Target Price: 4000.0
Profit: 550.0 (15.71%)
```

### Daily Update Alert
```
📊 DAILY PRICE UPDATE (12 PM IST)

Stock: INFY.NS
Buy Price: 1450.0
Current Price: 1520.0
Target Price: 1600.0
```

---

## 🧪 Testing

### Manual Testing via Swagger UI

1. Navigate to `http://localhost:8000/docs`
2. Click on any endpoint
3. Click "Try it out"
4. Enter parameters and execute

### Stock Symbol Format

- **Indian Stocks**: Add `.NS` suffix (e.g., `TCS.NS`, `INFY.NS`, `RELIANCE.NS`)
- **US Stocks**: Use ticker directly (e.g., `AAPL`, `GOOGL`, `TSLA`)
- **Other Markets**: Check [Yahoo Finance](https://finance.yahoo.com/) for correct symbols

---

## 🛠️ Development Roadmap

### Phase 1 ✅ (Current)
- [x] Core stock analysis logic
- [x] FastAPI REST API
- [x] Telegram alerts
- [x] JSON-based storage
- [x] Autonomous agent execution

### Phase 2 🚧 (Planned)
- [ ] Database migration (PostgreSQL/MongoDB)
- [ ] User authentication & multi-user support
- [ ] Web dashboard (React/Vue.js)
- [ ] Advanced technical indicators (RSI, MACD, Moving Averages)
- [ ] Historical performance charts
- [ ] Portfolio diversification analysis

### Phase 3 🔮 (Future)
- [ ] Machine learning price predictions
- [ ] News sentiment analysis
- [ ] Multi-exchange support
- [ ] Mobile app (React Native)
- [ ] Webhook integrations (Discord, Slack)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance market data
- [Telegram Bot API](https://core.telegram.org/bots/api) - Messaging platform

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/stock-agent?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/stock-agent?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/stock-agent)

---

<div align="center">
  <strong>Built with ❤️ for smarter investing</strong>
</div>
