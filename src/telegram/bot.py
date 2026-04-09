import logging
import asyncio
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError
from src.config import Config
from src.models.token import TokenLaunch
from src.telegram.formatter import MessageFormatter

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Send notifications to Telegram"""

    def __init__(self, bot_token: str = None, chat_id: int = None):
        self.bot_token = bot_token or Config.TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or Config.TELEGRAM_CHAT_ID
        self.bot = Bot(token=self.bot_token)

    async def send_launch_notification(
        self,
        token: TokenLaunch,
        image_path: Optional[str] = None
    ) -> bool:
        """Send token launch notification to Telegram"""
        try:
            message = MessageFormatter.format_launch_message(token)

            if image_path:
                await self._send_photo_message(message, image_path)
            else:
                await self._send_text_message(message)

            logger.info(f"Sent notification for {token.name} ({token.symbol})")
            return True

        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return False

    async def _send_text_message(self, message: str) -> bool:
        """Send text message to Telegram"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="HTML",
                disable_web_page_preview=False
            )
            return True
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False

    async def _send_photo_message(self, message: str, image_path: str) -> bool:
        """Send photo message to Telegram"""
        try:
            with open(image_path, "rb") as photo:
                await self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=photo,
                    caption=message,
                    parse_mode="HTML"
                )
            return True
        except FileNotFoundError:
            logger.warning(f"Image file not found: {image_path}")
            return await self._send_text_message(message)
        except TelegramError as e:
            logger.error(f"Telegram error sending photo: {e}")
            return await self._send_text_message(message)

    async def send_test_message(self) -> bool:
        """Send test message to verify bot is working"""
        try:
            test_message = "✅ Liquid Protocol Launch Bot is running!"
            await self._send_text_message(test_message)
            logger.info("Test message sent successfully")
            return True
        except Exception as e:
            logger.error(f"Error sending test message: {e}")
            return False
