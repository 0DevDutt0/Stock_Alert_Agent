"""Dependency injection for FastAPI"""

from functools import lru_cache

from stock_agent.config import Settings, get_settings
from stock_agent.repositories.stock_repository import JSONStockRepository, StockRepository
from stock_agent.services.alert_service import AlertService
from stock_agent.services.market_data_service import MarketDataService
from stock_agent.services.stock_service import StockService


@lru_cache()
def get_market_service() -> MarketDataService:
    """Get market data service instance"""
    settings = get_settings()
    return MarketDataService(
        timeout=settings.market_data_timeout,
        retry_attempts=settings.market_data_retry_attempts
    )


@lru_cache()
def get_alert_service() -> AlertService:
    """Get alert service instance"""
    settings = get_settings()
    return AlertService(settings)


@lru_cache()
def get_repository() -> StockRepository:
    """Get stock repository instance"""
    settings = get_settings()
    return JSONStockRepository(settings.data_file_path)


def get_stock_service(
    market_service: MarketDataService = None,
    alert_service: AlertService = None,
    repository: StockRepository = None
) -> StockService:
    """
    Get stock service instance with dependency injection
    
    Args:
        market_service: Market data service (optional, will use cached if not provided)
        alert_service: Alert service (optional, will use cached if not provided)
        repository: Stock repository (optional, will use cached if not provided)
        
    Returns:
        StockService instance
    """
    if market_service is None:
        market_service = get_market_service()
    
    if alert_service is None:
        alert_service = get_alert_service()
    
    if repository is None:
        repository = get_repository()
    
    return StockService(market_service, alert_service, repository)
