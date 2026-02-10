"""Repositories package"""

from stock_agent.repositories.stock_repository import (
    StockRepository,
    JSONStockRepository,
)

__all__ = [
    "StockRepository",
    "JSONStockRepository",
]
