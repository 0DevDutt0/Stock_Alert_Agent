"""Enumerations for stock agent"""

from enum import Enum


class DecisionType(str, Enum):
    """Stock analysis decision types"""
    
    TARGET_REACHED = "🎯 TARGET REACHED"
    HOLD = "⏳ HOLD"
    BELOW_BUY_PRICE = "🔻 BELOW BUY PRICE"
    
    def __str__(self) -> str:
        return self.value


class AlertType(str, Enum):
    """Alert notification types"""
    
    TARGET_REACHED = "target_reached"
    DAILY_UPDATE = "daily_update"
    CUSTOM = "custom"
    
    def __str__(self) -> str:
        return self.value
