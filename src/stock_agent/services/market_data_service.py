"""Market data service for fetching stock prices"""

import time
from typing import Optional

import yfinance as yf

from stock_agent.utils.exceptions import InvalidSymbolError, MarketDataError
from stock_agent.utils.logger import get_logger

logger = get_logger(__name__)


class MarketDataService:
    """Service for fetching market data from Yahoo Finance"""
    
    def __init__(self, timeout: int = 10, retry_attempts: int = 3):
        """
        Initialize market data service
        
        Args:
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts on failure
        """
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        logger.info("Initialized MarketDataService")
    
    def get_live_price(self, symbol: str) -> float:
        """
        Fetch latest closing price for a stock symbol
        
        Args:
            symbol: Stock symbol (e.g., TCS.NS, INFY.NS, AAPL)
            
        Returns:
            Latest closing price
            
        Raises:
            InvalidSymbolError: If symbol is invalid
            MarketDataError: If data cannot be fetched
        """
        symbol = symbol.strip().upper()
        
        for attempt in range(1, self.retry_attempts + 1):
            try:
                logger.debug(f"Fetching price for {symbol} (attempt {attempt}/{self.retry_attempts})")
                
                stock = yf.Ticker(symbol)
                data = stock.history(period="1d")
                
                if data.empty:
                    raise InvalidSymbolError(
                        symbol,
                        "No data available - symbol may be invalid or market is closed"
                    )
                
                price = float(data["Close"].iloc[-1])
                logger.info(f"Fetched price for {symbol}: ${price:.2f}")
                return price
                
            except InvalidSymbolError:
                raise
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed for {symbol}: {e}")
                
                if attempt < self.retry_attempts:
                    time.sleep(1)  # Wait before retry
                else:
                    raise MarketDataError(symbol, str(e))
        
        raise MarketDataError(symbol, "Max retry attempts reached")
    
    def get_stock_info(self, symbol: str) -> Optional[dict]:
        """
        Get detailed stock information
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Stock information dictionary or None
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            logger.debug(f"Fetched info for {symbol}")
            return info
        except Exception as e:
            logger.error(f"Failed to fetch info for {symbol}: {e}")
            return None
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if a stock symbol exists
        
        Args:
            symbol: Stock symbol to validate
            
        Returns:
            True if symbol is valid, False otherwise
        """
        try:
            self.get_live_price(symbol)
            return True
        except (InvalidSymbolError, MarketDataError):
            return False
