"""
Bot Manager - Manages Telegram Bot and Userbot
"""

from loguru import logger

from src.services.config_service import ConfigService
from src.telegram.management_bot import ManagementBot


class BotManager:
    """Manager for both management bot and userbot"""

    def __init__(self) -> None:
        self.management_bot = None
        self.userbot = None
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

            # TODO: Start userbot after authentication setup
            # self.userbot = UserBot()
            # await self.userbot.start()
            # logger.info("✅ Userbot started")

            self.running = True
            logger.info("🎯 Management bot running! (Userbot temporarily disabled for testing)")

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
