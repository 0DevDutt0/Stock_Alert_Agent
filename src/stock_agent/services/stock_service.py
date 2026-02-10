"""Stock service for business logic"""

from datetime import datetime
from typing import List

import pytz

from stock_agent.config import Settings
from stock_agent.models.enums import DecisionType
from stock_agent.models.stock import StockAnalysis, StockCreate, StockInDB
from stock_agent.repositories.stock_repository import StockRepository
from stock_agent.services.alert_service import AlertService
from stock_agent.services.market_data_service import MarketDataService
from stock_agent.utils.logger import get_logger

logger = get_logger(__name__)


class StockService:
    """Service for stock analysis and management"""
    
    def __init__(
        self,
        market_service: MarketDataService,
        alert_service: AlertService,
        repository: StockRepository,
        settings: Settings = None
    ):
        """
        Initialize stock service
        
        Args:
            market_service: Market data service
            alert_service: Alert service
            repository: Stock repository
            settings: Application settings (optional)
        """
        self.market_service = market_service
        self.alert_service = alert_service
        self.repository = repository
        
        if settings is None:
            from stock_agent.config import get_settings
            settings = get_settings()
        
        self.settings = settings
        self.timezone = pytz.timezone(settings.timezone)
        logger.info("Initialized StockService")
    
    def analyze_stock(
        self,
        symbol: str,
        buy_price: float,
        target_price: float
    ) -> StockAnalysis:
        """
        Analyze a stock and determine decision
        
        Args:
            symbol: Stock symbol
            buy_price: Purchase price
            target_price: Target selling price
            
        Returns:
            Stock analysis result
        """
        logger.info(f"Analyzing stock: {symbol}")
        
        # Fetch current price
        current_price = self.market_service.get_live_price(symbol)
        
        # Calculate profit
        profit = current_price - buy_price
        profit_percent = (profit / buy_price) * 100
        
        # Determine decision
        if current_price >= target_price:
            decision = DecisionType.TARGET_REACHED
        elif current_price < buy_price:
            decision = DecisionType.BELOW_BUY_PRICE
        else:
            decision = DecisionType.HOLD
        
        analysis = StockAnalysis(
            symbol=symbol,
            buy_price=buy_price,
            current_price=round(current_price, 2),
            target_price=target_price,
            profit=round(profit, 2),
            profit_percent=round(profit_percent, 2),
            decision=decision
        )
        
        logger.info(f"Analysis complete for {symbol}: {decision}")
        return analysis
    
    def track_stock(
        self,
        symbol: str,
        buy_price: float,
        target_price: float
    ) -> StockInDB:
        """
        Add a stock to the tracking list
        
        Args:
            symbol: Stock symbol
            buy_price: Purchase price
            target_price: Target selling price
            
        Returns:
            Created stock record
        """
        logger.info(f"Adding stock to tracking: {symbol}")
        
        stock_create = StockCreate(
            symbol=symbol,
            buy_price=buy_price,
            target_price=target_price
        )
        
        stock = self.repository.add(stock_create)
        logger.info(f"Stock added successfully: {symbol}")
        return stock
    
    def get_tracked_stocks(self) -> List[StockInDB]:
        """
        Get all tracked stocks
        
        Returns:
            List of tracked stocks
        """
        stocks = self.repository.get_all()
        logger.debug(f"Retrieved {len(stocks)} tracked stocks")
        return stocks
    
    def run_agent(self) -> List[StockAnalysis]:
        """
        Run autonomous agent to analyze all tracked stocks
        
        Returns:
            List of analysis results
        """
        logger.info("Running autonomous agent")
        
        stocks = self.get_tracked_stocks()
        now_ist = datetime.now(self.timezone)
        
        if not stocks:
            logger.info("No stocks to analyze")
            return []
        
        results = []
        
        for stock in stocks:
            try:
                # Analyze stock
                analysis = self.analyze_stock(
                    symbol=stock.symbol,
                    buy_price=stock.buy_price,
                    target_price=stock.target_price
                )
                
                # Send target alert if reached
                if analysis.decision == DecisionType.TARGET_REACHED:
                    self.alert_service.send_target_alert(analysis)
                
                # Send daily update if within time window
                if self._is_daily_update_time(now_ist):
                    self.alert_service.send_daily_update(analysis)
                
                results.append(analysis)
                
            except Exception as e:
                logger.error(f"Failed to analyze {stock.symbol}: {e}")
                # Continue with other stocks
                continue
        
        logger.info(f"Agent run complete: analyzed {len(results)} stocks")
        return results
    
    def _is_daily_update_time(self, current_time: datetime) -> bool:
        """
        Check if current time is within daily update window
        
        Args:
            current_time: Current time in IST
            
        Returns:
            True if within update window
        """
        target_hour = self.settings.daily_update_hour
        target_minute = self.settings.daily_update_minute
        window_minutes = self.settings.daily_update_window_minutes
        
        # Check if hour matches
        if current_time.hour != target_hour:
            return False
        
        # Check if within minute window
        minute_diff = abs(current_time.minute - target_minute)
        return minute_diff < window_minutes
