"""Custom exceptions for stock agent"""


class StockAgentException(Exception):
    """Base exception for stock agent"""
    pass


class StockNotFoundError(StockAgentException):
    """Raised when a stock is not found"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        super().__init__(f"Stock '{symbol}' not found")


class InvalidSymbolError(StockAgentException):
    """Raised when a stock symbol is invalid"""
    
    def __init__(self, symbol: str, reason: str = ""):
        self.symbol = symbol
        self.reason = reason
        message = f"Invalid stock symbol '{symbol}'"
        if reason:
            message += f": {reason}"
        super().__init__(message)


class MarketDataError(StockAgentException):
    """Raised when market data cannot be fetched"""
    
    def __init__(self, symbol: str, reason: str = ""):
        self.symbol = symbol
        self.reason = reason
        message = f"Failed to fetch market data for '{symbol}'"
        if reason:
            message += f": {reason}"
        super().__init__(message)


class AlertError(StockAgentException):
    """Raised when alert sending fails"""
    
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Failed to send alert: {reason}")


class StorageError(StockAgentException):
    """Raised when storage operations fail"""
    
    def __init__(self, operation: str, reason: str = ""):
        self.operation = operation
        self.reason = reason
        message = f"Storage operation '{operation}' failed"
        if reason:
            message += f": {reason}"
        super().__init__(message)


class DuplicateStockError(StockAgentException):
    """Raised when attempting to add a duplicate stock"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        super().__init__(f"Stock '{symbol}' already exists in tracking list")
