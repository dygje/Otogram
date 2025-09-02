"""
Database Management
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from loguru import logger
from src.core.config import settings


class Database:
    """Database connection manager"""
    
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db: AsyncIOMotorDatabase = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URL)
            self.db = self.client[settings.DB_NAME]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info(f"✅ Connected to MongoDB: {settings.DB_NAME}")
            
            # Create indexes
            await self._create_indexes()
            
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("✅ Database disconnected")
    
    async def _create_indexes(self):
        """Create necessary database indexes"""
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
    
    def get_collection(self, name: str):
        """Get a collection"""
        if not self.db:
            raise RuntimeError("Database not connected")
        return self.db[name]


# Global database instance
database = Database()