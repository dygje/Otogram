"""
Database Management
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from loguru import logger

from src.core.config import settings

if TYPE_CHECKING:
    pass


class Database:
    """Database connection manager"""

    def __init__(self) -> None:
        self.client: Any = None  # AsyncIOMotorClient | None
        self.db: Any = None  # AsyncIOMotorDatabase | None

    async def connect(self, mongo_url: str | None = None) -> None:
        """Connect to MongoDB"""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient

            url = mongo_url or settings.MONGO_URL
            self.client = AsyncIOMotorClient(url)
            self.db = self.client[settings.DB_NAME]

            # Test connection
            await self.client.admin.command("ping")
            logger.info(f"✅ Connected to MongoDB: {settings.DB_NAME}")

            # Create indexes
            await self.create_indexes()

        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()  # Note: close() is not async in motor
            self.client = None
            self.db = None
            logger.info("✅ Database disconnected")

    async def create_indexes(self) -> None:
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

    async def _create_indexes(self) -> None:
        """Legacy method - alias for create_indexes"""
        await self.create_indexes()

    async def ping(self) -> bool:
        """Ping database to check connection"""
        if not self.client:
            return False

        try:
            result = await self.client.admin.command("ping")
            return result.get("ok") == 1
        except Exception:
            return False

    async def get_database_stats(self) -> dict[str, Any]:
        """Get database statistics"""
        if not self.db:
            raise RuntimeError("Database not connected")

        try:
            stats = await self.db.command("dbStats")
            return {
                "db_name": stats.get("db"),
                "collections": stats.get("collections", 0),
                "data_size": stats.get("dataSize", 0),
                "storage_size": stats.get("storageSize", 0),
                "index_size": stats.get("indexSize", 0),
                "objects": stats.get("objects", 0),
            }
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            raise

    async def drop_collection(self, collection_name: str) -> bool:
        """Drop a collection"""
        if not self.db:
            raise RuntimeError("Database not connected")

        try:
            await self.db.drop_collection(collection_name)
            logger.info(f"Dropped collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to drop collection {collection_name}: {e}")
            return False

    async def list_collections(self) -> list[str]:
        """List all collections"""
        if not self.db:
            raise RuntimeError("Database not connected")

        try:
            collections = await self.db.list_collection_names()
            return collections
        except Exception as e:
            logger.error(f"Failed to list collections: {e}")
            return []

    async def collection_exists(self, collection_name: str) -> bool:
        """Check if collection exists"""
        collections = await self.list_collections()
        return collection_name in collections

    async def get_collection_size(self, collection_name: str) -> int:
        """Get collection document count"""
        if not self.db:
            raise RuntimeError("Database not connected")

        try:
            collection = self.db[collection_name]
            return await collection.count_documents({})
        except Exception as e:
            logger.error(f"Failed to get collection size for {collection_name}: {e}")
            return 0

    async def ensure_connection(self) -> None:
        """Ensure database connection is active"""
        if not self.client:
            await self.connect()
            return

        # Test existing connection
        if not await self.ping():
            logger.warning("Database connection lost, reconnecting...")
            await self.connect()

    async def bulk_insert(self, collection_name: str, documents: list[dict[str, Any]]) -> int:
        """Bulk insert documents"""
        if not self.db:
            raise RuntimeError("Database not connected")

        if not documents:
            return 0

        try:
            collection = self.db[collection_name]
            result = await collection.insert_many(documents)
            return len(result.inserted_ids)
        except Exception as e:
            logger.error(f"Bulk insert failed for {collection_name}: {e}")
            raise

    async def start_transaction(self):
        """Start a database transaction"""
        if not self.client:
            raise RuntimeError("Database not connected")

        return await self.client.start_session()

    async def comprehensive_health_check(self) -> dict[str, Any]:
        """Comprehensive health check"""
        health = {
            "connected": False,
            "ping_success": False,
            "collections": [],
            "stats": None,
            "error": None,
        }

        try:
            # Check connection
            health["connected"] = self.client is not None and self.db is not None

            if health["connected"]:
                # Check ping
                health["ping_success"] = await self.ping()

                # Get collections
                health["collections"] = await self.list_collections()

                # Get stats
                try:
                    health["stats"] = await self.get_database_stats()
                except Exception as stats_error:
                    health["stats"] = {"error": str(stats_error)}

        except Exception as e:
            health["error"] = str(e)

        return health

    async def health_check(self) -> bool:
        """Simple health check - returns True if database is connected and responding"""
        try:
            if self.client is None or self.db is None:
                return False
            return await self.ping()
        except Exception:
            return False

    def get_collection(self, name: str) -> Any:  # AsyncIOMotorCollection
        """Get a collection"""
        if self.db is None:
            raise RuntimeError("Database not connected")
        return self.db[name]


# Global database instance
database = Database()
