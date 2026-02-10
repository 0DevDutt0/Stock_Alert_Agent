"""Configuration management using Pydantic Settings"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = Field(default="Stock Agent", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    environment: str = Field(default="development", description="Environment (development/staging/production)")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_reload: bool = Field(default=True, description="Enable auto-reload")
    
    # Telegram Configuration
    telegram_bot_token: Optional[str] = Field(default=None, description="Telegram bot token")
    telegram_chat_id: Optional[str] = Field(default=None, description="Telegram chat ID")
    
    # Data Storage
    data_file_path: str = Field(default="data/stocks.json", description="Path to JSON storage file")
    
    # Market Data
    market_data_timeout: int = Field(default=10, description="Market data API timeout in seconds")
    market_data_retry_attempts: int = Field(default=3, description="Number of retry attempts for market data")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file_path: str = Field(default="logs/stock_agent.log", description="Log file path")
    log_max_bytes: int = Field(default=10485760, description="Max log file size (10MB)")
    log_backup_count: int = Field(default=5, description="Number of log backups to keep")
    
    # Timezone
    timezone: str = Field(default="Asia/Kolkata", description="Timezone for scheduled tasks")
    
    # Alert Settings
    daily_update_hour: int = Field(default=12, description="Hour for daily updates (24-hour format)")
    daily_update_minute: int = Field(default=0, description="Minute for daily updates")
    daily_update_window_minutes: int = Field(default=5, description="Alert window tolerance in minutes")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"
    
    @property
    def telegram_configured(self) -> bool:
        """Check if Telegram is properly configured"""
        return bool(self.telegram_bot_token and self.telegram_chat_id)
    
    def ensure_directories(self) -> None:
        """Ensure required directories exist"""
        # Create data directory
        data_dir = Path(self.data_file_path).parent
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logs directory
        log_dir = Path(self.log_file_path).parent
        log_dir.mkdir(parents=True, exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    settings.ensure_directories()
    return settings
