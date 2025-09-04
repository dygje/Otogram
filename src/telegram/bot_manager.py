"""
Bot Manager - Manages Telegram Bot and Userbot
"""

from typing import Any

from loguru import logger

from src.services.config_service import ConfigService
from src.telegram.management_bot import ManagementBot
from src.telegram.userbot import UserBot


class BotManager:
    """Manager for both management bot and userbot"""

    def __init__(self) -> None:
        self.management_bot: ManagementBot | None = None
        self.userbot: UserBot | None = None
        self.config_service = ConfigService()
        self.running = False

    async def start(self) -> None:
        """Start both bots"""
        try:
            logger.info("🤖 Starting Telegram services...")

            # Initialize default configurations
            await self.config_service.initialize_default_configs()

            # Start management bot
            self.management_bot = ManagementBot()
            await self.management_bot.start()
            logger.info("✅ Management bot started")

            # Start userbot for broadcasting
            self.userbot = UserBot()
            await self.userbot.start()
            logger.info("✅ Userbot started")

            self.running = True
            logger.info("🎯 Both management bot and userbot are now running!")

        except Exception as e:
            logger.error(f"❌ Failed to start Telegram services: {e}")
            await self.stop()
            raise

    async def stop(self) -> None:
        """Stop both bots"""
        logger.info("🛑 Stopping Telegram services...")
        self.running = False

        if self.userbot:
            await self.userbot.stop()
            logger.info("✅ Userbot stopped")

        if self.management_bot:
            await self.management_bot.stop()
            logger.info("✅ Management bot stopped")

    def is_running(self) -> bool:
        """Check if services are running"""
        return self.running
