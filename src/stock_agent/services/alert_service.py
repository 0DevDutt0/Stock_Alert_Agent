"""Alert service for sending notifications"""

import requests

from stock_agent.config import Settings
from stock_agent.models.enums import AlertType
from stock_agent.models.stock import StockAnalysis
from stock_agent.utils.exceptions import AlertError
from stock_agent.utils.logger import get_logger

logger = get_logger(__name__)


class AlertService:
    """Service for sending alerts via Telegram"""
    
    def __init__(self, settings: Settings):
        """
        Initialize alert service
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.enabled = settings.telegram_configured
        
        if not self.enabled:
            logger.warning("Telegram not configured - alerts will be logged only")
        else:
            logger.info("Initialized AlertService with Telegram")
    
    def _send_telegram_message(self, message: str) -> None:
        """
        Send a message via Telegram Bot API
        
        Args:
            message: Message text to send
            
        Raises:
            AlertError: If sending fails
        """
        if not self.enabled:
            logger.info(f"[ALERT DISABLED] {message}")
            return
        
        url = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": self.settings.telegram_chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code != 200:
                error_msg = f"Telegram API error: {response.text}"
                logger.error(error_msg)
                raise AlertError(error_msg)
            
            logger.info("Telegram alert sent successfully")
            
        except requests.RequestException as e:
            error_msg = f"Failed to send Telegram alert: {e}"
            logger.error(error_msg)
            raise AlertError(error_msg)
    
    def send_target_alert(self, analysis: StockAnalysis) -> None:
        """
        Send target reached alert
        
        Args:
            analysis: Stock analysis result
        """
        message = (
            f"🎯 <b>TARGET REACHED!</b>\n\n"
            f"<b>Stock:</b> {analysis.symbol}\n"
            f"<b>Buy Price:</b> ${analysis.buy_price:.2f}\n"
            f"<b>Current Price:</b> ${analysis.current_price:.2f}\n"
            f"<b>Target Price:</b> ${analysis.target_price:.2f}\n"
            f"<b>Profit:</b> ${analysis.profit:.2f} ({analysis.profit_percent:.2f}%)"
        )
        
        try:
            self._send_telegram_message(message)
            logger.info(f"Sent target alert for {analysis.symbol}")
        except AlertError as e:
            logger.error(f"Failed to send target alert: {e}")
    
    def send_daily_update(self, analysis: StockAnalysis) -> None:
        """
        Send daily price update alert
        
        Args:
            analysis: Stock analysis result
        """
        message = (
            f"📊 <b>DAILY PRICE UPDATE (12 PM IST)</b>\n\n"
            f"<b>Stock:</b> {analysis.symbol}\n"
            f"<b>Buy Price:</b> ${analysis.buy_price:.2f}\n"
            f"<b>Current Price:</b> ${analysis.current_price:.2f}\n"
            f"<b>Target Price:</b> ${analysis.target_price:.2f}\n"
            f"<b>Profit/Loss:</b> ${analysis.profit:.2f} ({analysis.profit_percent:.2f}%)"
        )
        
        try:
            self._send_telegram_message(message)
            logger.info(f"Sent daily update for {analysis.symbol}")
        except AlertError as e:
            logger.error(f"Failed to send daily update: {e}")
    
    def send_custom_alert(self, message: str) -> None:
        """
        Send a custom alert message
        
        Args:
            message: Custom message to send
        """
        try:
            self._send_telegram_message(message)
            logger.info("Sent custom alert")
        except AlertError as e:
            logger.error(f"Failed to send custom alert: {e}")
