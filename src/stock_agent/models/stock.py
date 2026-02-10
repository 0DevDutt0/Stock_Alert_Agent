"""Stock data models"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from stock_agent.models.enums import DecisionType


class StockBase(BaseModel):
    """Base stock model with common fields"""
    
    symbol: str = Field(..., description="Stock symbol (e.g., TCS.NS, AAPL)")
    buy_price: float = Field(..., gt=0, description="Purchase price")
    target_price: float = Field(..., gt=0, description="Target selling price")
    
    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        """Validate and normalize stock symbol"""
        return v.strip().upper()
    
    @field_validator("target_price")
    @classmethod
    def validate_target_price(cls, v: float, info) -> float:
        """Ensure target price is greater than buy price"""
        if "buy_price" in info.data and v <= info.data["buy_price"]:
            raise ValueError("Target price must be greater than buy price")
        return v


class StockCreate(StockBase):
    """Model for creating a new stock"""
    pass


class StockInDB(StockBase):
    """Model for stock stored in database"""
    
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class StockAnalysis(BaseModel):
    """Stock analysis result"""
    
    symbol: str
    buy_price: float
    current_price: float
    target_price: float
    profit: float
    profit_percent: float
    decision: DecisionType
    analyzed_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentRunResult(BaseModel):
    """Result from agent execution"""
    
    time_ist: str
    total_stocks: int
    results: List[StockAnalysis]
    errors: Optional[List[dict]] = None
