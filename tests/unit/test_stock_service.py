"""Unit tests for stock service"""

import pytest

from stock_agent.models.enums import DecisionType
from stock_agent.models.stock import StockCreate
from stock_agent.repositories.stock_repository import JSONStockRepository
from stock_agent.services.stock_service import StockService


@pytest.mark.unit
def test_analyze_stock_target_reached(mock_market_service, mock_alert_service, tmp_path):
    """Test stock analysis when target is reached"""
    # Setup
    repo = JSONStockRepository(str(tmp_path / "stocks.json"))
    service = StockService(mock_market_service, mock_alert_service, repo)
    
    # Test
    result = service.analyze_stock("AAPL", buy_price=100.0, target_price=140.0)
    
    # Assertions
    assert result.symbol == "AAPL"
    assert result.current_price == 150.0
    assert result.decision == DecisionType.TARGET_REACHED
    assert result.profit == 50.0
    assert result.profit_percent == 50.0


@pytest.mark.unit
def test_analyze_stock_hold(mock_market_service, mock_alert_service, tmp_path):
    """Test stock analysis when holding"""
    # Setup
    repo = JSONStockRepository(str(tmp_path / "stocks.json"))
    service = StockService(mock_market_service, mock_alert_service, repo)
    
    # Test
    result = service.analyze_stock("AAPL", buy_price=100.0, target_price=200.0)
    
    # Assertions
    assert result.decision == DecisionType.HOLD
    assert result.profit == 50.0


@pytest.mark.unit
def test_analyze_stock_below_buy_price(mock_market_service, mock_alert_service, tmp_path):
    """Test stock analysis when below buy price"""
    # Setup
    repo = JSONStockRepository(str(tmp_path / "stocks.json"))
    service = StockService(mock_market_service, mock_alert_service, repo)
    
    # Test
    result = service.analyze_stock("AAPL", buy_price=200.0, target_price=250.0)
    
    # Assertions
    assert result.decision == DecisionType.BELOW_BUY_PRICE
    assert result.profit == -50.0


@pytest.mark.unit
def test_track_stock(mock_market_service, mock_alert_service, tmp_path):
    """Test adding a stock to tracking list"""
    # Setup
    repo = JSONStockRepository(str(tmp_path / "stocks.json"))
    service = StockService(mock_market_service, mock_alert_service, repo)
    
    # Test
    stock = service.track_stock("AAPL", buy_price=150.0, target_price=180.0)
    
    # Assertions
    assert stock.symbol == "AAPL"
    assert stock.buy_price == 150.0
    assert stock.target_price == 180.0


@pytest.mark.unit
def test_get_tracked_stocks(mock_market_service, mock_alert_service, tmp_path):
    """Test retrieving tracked stocks"""
    # Setup
    repo = JSONStockRepository(str(tmp_path / "stocks.json"))
    service = StockService(mock_market_service, mock_alert_service, repo)
    
    # Add stocks
    service.track_stock("AAPL", buy_price=150.0, target_price=180.0)
    service.track_stock("TCS.NS", buy_price=3500.0, target_price=4000.0)
    
    # Test
    stocks = service.get_tracked_stocks()
    
    # Assertions
    assert len(stocks) == 2
    assert stocks[0].symbol == "AAPL"
    assert stocks[1].symbol == "TCS.NS"
