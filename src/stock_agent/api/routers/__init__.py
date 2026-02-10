"""Routers package"""

from stock_agent.api.routers.health import router as health_router
from stock_agent.api.routers.stocks import router as stocks_router
from stock_agent.api.routers.agent import router as agent_router

__all__ = [
    "health_router",
    "stocks_router",
    "agent_router",
]
