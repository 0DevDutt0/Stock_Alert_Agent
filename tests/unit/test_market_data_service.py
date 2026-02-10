"""Unit tests for market data service"""

import pytest

from stock_agent.services.market_data_service import MarketDataService
from stock_agent.utils.exceptions import InvalidSymbolError


@pytest.mark.unit
def test_get_live_price_valid_symbol():
    """Test fetching price for valid symbol"""
    service = MarketDataService()
    
    # This will make a real API call - use a stable symbol
    price = service.get_live_price("AAPL")
    
    assert isinstance(price, float)
    assert price > 0


@pytest.mark.unit
def test_get_live_price_invalid_symbol():
    """Test fetching price for invalid symbol"""
    service = MarketDataService()
    
    with pytest.raises(InvalidSymbolError):
        service.get_live_price("INVALID_SYMBOL_XYZ123")


@pytest.mark.unit
def test_validate_symbol_valid():
    """Test symbol validation for valid symbol"""
    service = MarketDataService()
    
    assert service.validate_symbol("AAPL") is True


@pytest.mark.unit
def test_validate_symbol_invalid():
    """Test symbol validation for invalid symbol"""
    service = MarketDataService()
    
    assert service.validate_symbol("INVALID_XYZ123") is False
