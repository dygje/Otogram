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

            # Note: Userbot authentication will be handled separately
            # due to verification code requirement
            logger.info("📱 Userbot authentication required - use /menu in Telegram bot for setup")

            self.running = True
            logger.info("🎯 Management bot is ready! Use your Telegram bot to complete setup.")

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

    async def start_userbot(self) -> bool:
        """Start userbot separately (requires interactive authentication)"""
        try:
            if self.userbot:
                logger.info("Userbot already running")
                return True
                
            logger.info("🔄 Starting userbot authentication...")
            self.userbot = UserBot()
            await self.userbot.start()
            logger.info("✅ Userbot started successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start userbot: {e}")
            if self.userbot:
                await self.userbot.stop()
                self.userbot = None
            return False
