"""Stock repository implementations"""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from stock_agent.models.stock import StockCreate, StockInDB
from stock_agent.utils.exceptions import DuplicateStockError, StorageError, StockNotFoundError
from stock_agent.utils.logger import get_logger

logger = get_logger(__name__)


class StockRepository(ABC):
    """Abstract base class for stock repository"""
    
    @abstractmethod
    def add(self, stock: StockCreate) -> StockInDB:
        """Add a new stock to the repository"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[StockInDB]:
        """Get all stocks from the repository"""
        pass
    
    @abstractmethod
    def get_by_symbol(self, symbol: str) -> Optional[StockInDB]:
        """Get a stock by its symbol"""
        pass
    
    @abstractmethod
    def delete(self, symbol: str) -> bool:
        """Delete a stock by its symbol"""
        pass
    
    @abstractmethod
    def update(self, symbol: str, stock: StockCreate) -> StockInDB:
        """Update a stock by its symbol"""
        pass


class JSONStockRepository(StockRepository):
    """JSON file-based stock repository implementation"""
    
    def __init__(self, file_path: str):
        """
        Initialize JSON repository
        
        Args:
            file_path: Path to JSON storage file
        """
        self.file_path = Path(file_path)
        self._ensure_file_exists()
        logger.info(f"Initialized JSON repository at {self.file_path}")
    
    def _ensure_file_exists(self) -> None:
        """Ensure the JSON file and its directory exist"""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.file_path.exists():
                self._save_stocks([])
                logger.info(f"Created new storage file at {self.file_path}")
        except Exception as e:
            raise StorageError("initialize", str(e))
    
    def _load_stocks(self) -> List[dict]:
        """Load stocks from JSON file"""
        try:
            if not self.file_path.exists():
                return []
            
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Loaded {len(data)} stocks from storage")
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON file: {e}")
            raise StorageError("load", f"Invalid JSON format: {e}")
        except Exception as e:
            logger.error(f"Failed to load stocks: {e}")
            raise StorageError("load", str(e))
    
    def _save_stocks(self, stocks: List[dict]) -> None:
        """Save stocks to JSON file"""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(stocks, f, indent=2, ensure_ascii=False)
                logger.debug(f"Saved {len(stocks)} stocks to storage")
        except Exception as e:
            logger.error(f"Failed to save stocks: {e}")
            raise StorageError("save", str(e))
    
    def add(self, stock: StockCreate) -> StockInDB:
        """Add a new stock to the repository"""
        stocks = self._load_stocks()
        
        # Check for duplicates
        if any(s["symbol"] == stock.symbol for s in stocks):
            logger.warning(f"Attempted to add duplicate stock: {stock.symbol}")
            raise DuplicateStockError(stock.symbol)
        
        # Create StockInDB instance
        stock_in_db = StockInDB(**stock.model_dump())
        
        # Add to list and save
        stocks.append(stock_in_db.model_dump())
        self._save_stocks(stocks)
        
        logger.info(f"Added stock: {stock.symbol}")
        return stock_in_db
    
    def get_all(self) -> List[StockInDB]:
        """Get all stocks from the repository"""
        stocks = self._load_stocks()
        return [StockInDB(**stock) for stock in stocks]
    
    def get_by_symbol(self, symbol: str) -> Optional[StockInDB]:
        """Get a stock by its symbol"""
        stocks = self._load_stocks()
        
        for stock in stocks:
            if stock["symbol"] == symbol.upper():
                return StockInDB(**stock)
        
        return None
    
    def delete(self, symbol: str) -> bool:
        """Delete a stock by its symbol"""
        stocks = self._load_stocks()
        original_count = len(stocks)
        
        stocks = [s for s in stocks if s["symbol"] != symbol.upper()]
        
        if len(stocks) == original_count:
            logger.warning(f"Stock not found for deletion: {symbol}")
            raise StockNotFoundError(symbol)
        
        self._save_stocks(stocks)
        logger.info(f"Deleted stock: {symbol}")
        return True
    
    def update(self, symbol: str, stock: StockCreate) -> StockInDB:
        """Update a stock by its symbol"""
        stocks = self._load_stocks()
        
        for i, s in enumerate(stocks):
            if s["symbol"] == symbol.upper():
                # Update the stock
                updated_stock = StockInDB(**stock.model_dump())
                stocks[i] = updated_stock.model_dump()
                self._save_stocks(stocks)
                logger.info(f"Updated stock: {symbol}")
                return updated_stock
        
        logger.warning(f"Stock not found for update: {symbol}")
        raise StockNotFoundError(symbol)
