"""Agent execution router"""

from datetime import datetime
from typing import List

import pytz
from fastapi import APIRouter, Depends, HTTPException

from stock_agent.api.dependencies import get_stock_service
from stock_agent.config import get_settings
from stock_agent.models.stock import AgentRunResult, StockAnalysis
from stock_agent.services.stock_service import StockService

router = APIRouter(prefix="/api/v1/agent", tags=["Agent"])


@router.get("/run", response_model=AgentRunResult)
async def run_agent(
    stock_service: StockService = Depends(get_stock_service)
):
    """
    Run the autonomous agent
    
    Analyzes all tracked stocks and sends alerts if:
    - Target price is reached
    - It's the daily update time (12 PM IST)
    
    This endpoint should be called periodically (e.g., via cron job)
    to enable autonomous monitoring.
    """
    try:
        settings = get_settings()
        timezone = pytz.timezone(settings.timezone)
        now_ist = datetime.now(timezone)
        
        results = stock_service.run_agent()
        
        return AgentRunResult(
            time_ist=now_ist.strftime("%Y-%m-%d %H:%M:%S"),
            total_stocks=len(results),
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")
