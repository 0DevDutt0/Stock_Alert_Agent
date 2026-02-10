"""Health check router"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from stock_agent.api.dependencies import get_market_service, get_repository
from stock_agent.config import get_settings
from stock_agent.services.market_data_service import MarketDataService
from stock_agent.repositories.stock_repository import StockRepository

router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    version: str
    environment: str
    dependencies: dict


@router.get("", response_model=HealthResponse)
async def health_check(
    market_service: MarketDataService = Depends(get_market_service),
    repository: StockRepository = Depends(get_repository)
):
    """
    Health check endpoint
    
    Returns system status and dependency health
    """
    settings = get_settings()
    
    # Check dependencies
    dependencies = {
        "market_data": "healthy",
        "storage": "healthy",
        "telegram": "configured" if settings.telegram_configured else "not_configured"
    }
    
    # Test market data service
    try:
        # Try to validate a known symbol
        market_service.validate_symbol("AAPL")
    except Exception:
        dependencies["market_data"] = "unhealthy"
    
    # Test repository
    try:
        repository.get_all()
    except Exception:
        dependencies["storage"] = "unhealthy"
    
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
        dependencies=dependencies
    )
