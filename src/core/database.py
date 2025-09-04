"""
Database Management
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from loguru import logger

from src.core.config import settings

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase


class Database:
    """Database connection manager"""

    def __init__(self) -> None:
        self.client: Any = None  # AsyncIOMotorClient | None
        self.db: Any = None      # AsyncIOMotorDatabase | None

    async def connect(self) -> None:
        """Connect to MongoDB"""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            
            self.client = AsyncIOMotorClient(settings.MONGO_URL)
            self.db = self.client[settings.DB_NAME]

            # Test connection
            await self.client.admin.command("ping")
            logger.info(f"✅ Connected to MongoDB: {settings.DB_NAME}")

            # Create indexes
            await self._create_indexes()

        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("✅ Database disconnected")

    async def _create_indexes(self) -> None:
        """Create necessary database indexes"""
        if self.db is None:
            logger.error("Database not connected, cannot create indexes")
            return

        try:
            # Messages collection
            await self.db.messages.create_index("is_active")
            await self.db.messages.create_index("created_at")

            # Groups collection
            await self.db.groups.create_index("group_id", unique=True)
            await self.db.groups.create_index("is_active")

            # Blacklists collection
            await self.db.blacklists.create_index("group_id")
            await self.db.blacklists.create_index("blacklist_type")
            await self.db.blacklists.create_index("expires_at")

            # Logs collection
            await self.db.logs.create_index("timestamp")
            await self.db.logs.create_index("log_type")

            # Configurations collection
            await self.db.configurations.create_index("key", unique=True)

            logger.info("✅ Database indexes created")

        except Exception as e:
            logger.warning(f"⚠️ Index creation warning: {e}")

    def get_collection(self, name: str) -> Any:  # AsyncIOMotorCollection
        """Get a collection"""
        if self.db is None:
            raise RuntimeError("Database not connected")
        return self.db[name]


# Global database instance
database = Database()
