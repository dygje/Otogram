#!/usr/bin/env python3
"""
Telegram Automation System
Pure Telegram-based management without web interface or CLI
All operations managed through Telegram Bot
"""

import asyncio
import signal
import sys
from pathlib import Path
from typing import Any

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger

from src.core.config import settings
from src.core.database import Database, database
from src.telegram.bot_manager import BotManager


class TelegramAutomationApp:
    """Main Application Class"""

    def __init__(self) -> None:
        self.bot_manager: BotManager | None = None
        self.database: Database | None = None
        self.running: bool = False
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging system"""
        logger.remove()  # Remove default handler

        # Console logging
        logger.add(
            sys.stdout,
            format=(
                "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
                "<cyan>{name}</cyan> - <level>{message}</level>"
            ),
            level=settings.LOG_LEVEL,
        )

        # File logging
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        logger.add(
            log_dir / "app.log",
            rotation="1 day",
            retention="7 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name} - {message}",
            level=settings.LOG_LEVEL,
        )

    async def start(self) -> None:
        """Start the application"""
        try:
            logger.info("🚀 Starting Telegram Automation System")

            # Check required credentials
            if not self._check_credentials():
                logger.error("❌ Missing required Telegram credentials in .env file")
                return

            # Initialize database
            self.database = database
            await self.database.connect()
            logger.info("✅ Database connected")

            # Initialize bot manager
            self.bot_manager = BotManager()
            await self.bot_manager.start()
            logger.info("✅ Telegram services started")

            self.running = True
            logger.info("🎯 System ready! Use your Telegram bot to manage everything.")

            # Keep running
            while self.running:
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"❌ Failed to start: {e}")
            await self.stop()

    async def stop(self) -> None:
        """Stop the application"""
        logger.info("🛑 Shutting down...")
        self.running = False

        if self.bot_manager:
            await self.bot_manager.stop()

        if self.database:
            await self.database.disconnect()

        logger.info("✅ Shutdown complete")

    def _check_credentials(self) -> bool:
        """Check if required credentials are provided"""
        required = [
            settings.TELEGRAM_API_ID,
            settings.TELEGRAM_API_HASH,
            settings.TELEGRAM_BOT_TOKEN,
            settings.TELEGRAM_PHONE_NUMBER,
        ]
        return all(cred for cred in required)

    def signal_handler(self, signum: int, _frame: Any) -> None:
        """Handle shutdown signals"""
        logger.info(f"📡 Received signal {signum}")
        # Create task to stop the application (don't need to store reference)
        asyncio.create_task(self.stop())
        # We don't await here as this is a signal handler


async def async_main() -> None:
    """Async main entry point"""
    app = TelegramAutomationApp()

    # Setup signal handlers
    signal.signal(signal.SIGINT, app.signal_handler)
    signal.signal(signal.SIGTERM, app.signal_handler)

    try:
        await app.start()
    except KeyboardInterrupt:
        logger.info("👋 Keyboard interrupt received")
    finally:
        await app.stop()


def main() -> None:
    """Sync entry point for setuptools"""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
