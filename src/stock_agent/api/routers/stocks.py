"""Stock management router"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from stock_agent.api.dependencies import get_stock_service
from stock_agent.models.stock import StockAnalysis, StockCreate, StockInDB
from stock_agent.services.stock_service import StockService
from stock_agent.utils.exceptions import DuplicateStockError, InvalidSymbolError, MarketDataError

router = APIRouter(prefix="/api/v1/stocks", tags=["Stocks"])


@router.post("/analyze", response_model=StockAnalysis)
async def analyze_stock(
    stock: StockCreate,
    stock_service: StockService = Depends(get_stock_service)
):
    """
    Analyze a stock without tracking it
    
    Performs instant analysis on a stock to check current price,
    profit/loss, and decision (TARGET_REACHED, HOLD, BELOW_BUY_PRICE).
    """
    try:
        analysis = stock_service.analyze_stock(
            symbol=stock.symbol,
            buy_price=stock.buy_price,
            target_price=stock.target_price
        )
        return analysis
    except InvalidSymbolError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except MarketDataError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/track", response_model=dict)
async def track_stock(
    stock: StockCreate,
    stock_service: StockService = Depends(get_stock_service)
):
    """
    Add a stock to the tracking list
    
    The stock will be monitored continuously by the autonomous agent.
    """
    try:
        stock_service.track_stock(
            symbol=stock.symbol,
            buy_price=stock.buy_price,
            target_price=stock.target_price
        )
        return {"message": f"{stock.symbol} added successfully"}
    except DuplicateStockError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except InvalidSymbolError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("", response_model=List[StockInDB])
async def list_stocks(
    stock_service: StockService = Depends(get_stock_service)
):
    """
    Get all tracked stocks
    
    Returns the list of stocks currently being monitored.
    """
    try:
        stocks = stock_service.get_tracked_stocks()
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
