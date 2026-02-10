"""Test configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient

from stock_agent.api.app import create_app
from stock_agent.config import Settings
from stock_agent.repositories.stock_repository import StockRepository
from stock_agent.services.alert_service import AlertService
from stock_agent.services.market_data_service import MarketDataService
from stock_agent.services.stock_service import StockService


@pytest.fixture
def test_settings():
    """Create test settings"""
    return Settings(
        environment="testing",
        telegram_bot_token="test_token",
        telegram_chat_id="test_chat_id",
        data_file_path="test_data/stocks.json",
        log_level="DEBUG"
    )


@pytest.fixture
def mock_market_service():
    """Create mock market data service"""
    class MockMarketDataService(MarketDataService):
        def get_live_price(self, symbol: str) -> float:
            # Return mock prices
            mock_prices = {
                "AAPL": 150.0,
                "TCS.NS": 3750.0,
                "INFY.NS": 1520.0
            }
            return mock_prices.get(symbol.upper(), 100.0)
    
    return MockMarketDataService()


@pytest.fixture
def mock_alert_service(test_settings):
    """Create mock alert service"""
    class MockAlertService(AlertService):
        def __init__(self, settings):
            super().__init__(settings)
            self.sent_alerts = []
        
        def _send_telegram_message(self, message: str) -> None:
            self.sent_alerts.append(message)
    
    return MockAlertService(test_settings)


@pytest.fixture
def test_client():
    """Create test client"""
    app = create_app()
    return TestClient(app)
