"""
Extended tests for Database to improve coverage
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.core.database import Database, database


class TestDatabaseExtended:
    """Extended test coverage for Database class"""

    @pytest.fixture
    def db_instance(self):
        """Database instance fixture"""
        return Database()

    @pytest.mark.asyncio
    async def test_connect_with_custom_url(self, db_instance):
        """Test database connection with custom URL"""
        custom_url = "mongodb://custom_host:27017"
        
        with patch('src.core.database.AsyncIOMotorClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_db = AsyncMock()
            mock_client.__getitem__ = MagicMock(return_value=mock_db)
            mock_client_class.return_value = mock_client
            
            await db_instance.connect(custom_url)
            
            # Verify client was created with custom URL
            mock_client_class.assert_called_once_with(custom_url)
            assert db_instance.client == mock_client
            assert db_instance.db == mock_db

    @pytest.mark.asyncio
    async def test_connect_already_connected(self, db_instance):
        """Test connecting when already connected"""
        # Mock already connected state
        mock_client = AsyncMock()
        db_instance.client = mock_client
        db_instance.db = AsyncMock()
        
        with patch('src.core.database.AsyncIOMotorClient') as mock_client_class:
            await db_instance.connect()
            
            # Should not create new client
            mock_client_class.assert_not_called()
            assert db_instance.client == mock_client

    @pytest.mark.asyncio
    async def test_disconnect_when_connected(self, db_instance):
        """Test disconnecting when connected"""
        mock_client = AsyncMock()
        db_instance.client = mock_client
        db_instance.db = AsyncMock()
        
        await db_instance.disconnect()
        
        # Verify close was called and references cleared
        mock_client.close.assert_called_once()
        assert db_instance.client is None
        assert db_instance.db is None

    @pytest.mark.asyncio
    async def test_disconnect_when_not_connected(self, db_instance):
        """Test disconnecting when not connected"""
        db_instance.client = None
        db_instance.db = None
        
        # Should not raise exception
        await db_instance.disconnect()
        
        assert db_instance.client is None
        assert db_instance.db is None

    @pytest.mark.asyncio
    async def test_get_collection_success(self, db_instance):
        """Test getting collection successfully"""
        collection_name = "test_collection"
        mock_db = AsyncMock()
        mock_collection = AsyncMock()
        mock_db.__getitem__ = MagicMock(return_value=mock_collection)
        
        db_instance.db = mock_db
        
        result = db_instance.get_collection(collection_name)
        
        assert result == mock_collection
        mock_db.__getitem__.assert_called_once_with(collection_name)

    def test_get_collection_without_connection(self, db_instance):
        """Test getting collection without database connection"""
        db_instance.db = None
        
        with pytest.raises(RuntimeError, match="Database not connected"):
            db_instance.get_collection("test_collection")

    @pytest.mark.asyncio
    async def test_create_indexes_success(self, db_instance):
        """Test creating indexes successfully"""
        mock_db = AsyncMock()
        
        # Mock collections and their create_index methods
        mock_collections = {}
        for collection_name in ["messages", "groups", "blacklist", "config", "logs"]:
            mock_collection = AsyncMock()
            mock_collections[collection_name] = mock_collection
        
        mock_db.__getitem__ = lambda name: mock_collections[name]
        db_instance.db = mock_db
        
        await db_instance.create_indexes()
        
        # Verify create_index was called for each collection
        for collection in mock_collections.values():
            assert collection.create_index.called

    @pytest.mark.asyncio
    async def test_create_indexes_without_connection(self, db_instance):
        """Test creating indexes without database connection"""
        db_instance.db = None
        
        with pytest.raises(RuntimeError, match="Database not connected"):
            await db_instance.create_indexes()

    @pytest.mark.asyncio
    async def test_ping_database_success(self, db_instance):
        """Test successful database ping"""
        mock_client = AsyncMock()
        mock_admin_db = AsyncMock()
        mock_admin_db.command.return_value = {"ok": 1}
        mock_client.admin = mock_admin_db
        
        db_instance.client = mock_client
        
        result = await db_instance.ping()
        
        assert result is True
        mock_admin_db.command.assert_called_once_with("ping")

    @pytest.mark.asyncio
    async def test_ping_database_failure(self, db_instance):
        """Test database ping failure"""
        mock_client = AsyncMock()
        mock_admin_db = AsyncMock()
        mock_admin_db.command.side_effect = Exception("Connection failed")
        mock_client.admin = mock_admin_db
        
        db_instance.client = mock_client
        
        result = await db_instance.ping()
        
        assert result is False

    @pytest.mark.asyncio
    async def test_ping_without_connection(self, db_instance):
        """Test ping without database connection"""
        db_instance.client = None
        
        result = await db_instance.ping()
        
        assert result is False

    @pytest.mark.asyncio
    async def test_get_database_stats(self, db_instance):
        """Test getting database statistics"""
        mock_db = AsyncMock()
        mock_stats = {
            "collections": 5,
            "dataSize": 1024000,
            "storageSize": 2048000,
            "indexes": 10
        }
        mock_db.command.return_value = mock_stats
        
        db_instance.db = mock_db
        
        result = await db_instance.get_database_stats()
        
        assert result == mock_stats
        mock_db.command.assert_called_once_with("dbStats")

    @pytest.mark.asyncio
    async def test_get_database_stats_error(self, db_instance):
        """Test getting database stats with error"""
        mock_db = AsyncMock()
        mock_db.command.side_effect = Exception("Stats unavailable")
        
        db_instance.db = mock_db
        
        result = await db_instance.get_database_stats()
        
        assert result == {}

    @pytest.mark.asyncio
    async def test_drop_collection(self, db_instance):
        """Test dropping a collection"""
        collection_name = "test_collection"
        mock_db = AsyncMock()
        
        db_instance.db = mock_db
        
        await db_instance.drop_collection(collection_name)
        
        mock_db.drop_collection.assert_called_once_with(collection_name)

    @pytest.mark.asyncio
    async def test_drop_collection_without_connection(self, db_instance):
        """Test dropping collection without connection"""
        db_instance.db = None
        
        with pytest.raises(RuntimeError, match="Database not connected"):
            await db_instance.drop_collection("test_collection")

    @pytest.mark.asyncio
    async def test_list_collections(self, db_instance):
        """Test listing all collections"""
        mock_db = AsyncMock()
        mock_collection_names = ["messages", "groups", "blacklist", "config"]
        mock_db.list_collection_names.return_value = mock_collection_names
        
        db_instance.db = mock_db
        
        result = await db_instance.list_collections()
        
        assert result == mock_collection_names
        mock_db.list_collection_names.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_collections_without_connection(self, db_instance):
        """Test listing collections without connection"""
        db_instance.db = None
        
        with pytest.raises(RuntimeError, match="Database not connected"):
            await db_instance.list_collections()

    @pytest.mark.asyncio
    async def test_collection_exists_true(self, db_instance):
        """Test checking if collection exists (true)"""
        collection_name = "existing_collection"
        mock_db = AsyncMock()
        mock_db.list_collection_names.return_value = [collection_name, "other_collection"]
        
        db_instance.db = mock_db
        
        result = await db_instance.collection_exists(collection_name)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_collection_exists_false(self, db_instance):
        """Test checking if collection exists (false)"""
        collection_name = "nonexistent_collection"
        mock_db = AsyncMock()
        mock_db.list_collection_names.return_value = ["other_collection", "another_collection"]
        
        db_instance.db = mock_db
        
        result = await db_instance.collection_exists(collection_name)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_get_collection_size(self, db_instance):
        """Test getting collection size"""
        collection_name = "test_collection"
        mock_collection = AsyncMock()
        mock_collection.count_documents.return_value = 150
        
        mock_db = AsyncMock()
        mock_db.__getitem__ = MagicMock(return_value=mock_collection)
        db_instance.db = mock_db
        
        result = await db_instance.get_collection_size(collection_name)
        
        assert result == 150
        mock_collection.count_documents.assert_called_once_with({})

    @pytest.mark.asyncio
    async def test_ensure_connection_when_connected(self, db_instance):
        """Test ensure connection when already connected"""
        mock_client = AsyncMock()
        mock_db = AsyncMock()
        db_instance.client = mock_client
        db_instance.db = mock_db
        
        # Mock successful ping
        mock_admin_db = AsyncMock()
        mock_admin_db.command.return_value = {"ok": 1}
        mock_client.admin = mock_admin_db
        
        await db_instance.ensure_connection()
        
        # Should not reconnect if ping succeeds
        assert db_instance.client == mock_client
        assert db_instance.db == mock_db

    @pytest.mark.asyncio
    async def test_ensure_connection_when_disconnected(self, db_instance):
        """Test ensure connection when disconnected"""
        db_instance.client = None
        db_instance.db = None
        
        with patch.object(db_instance, 'connect') as mock_connect:
            await db_instance.ensure_connection()
            
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_connection_ping_fails(self, db_instance):
        """Test ensure connection when ping fails"""
        mock_client = AsyncMock()
        db_instance.client = mock_client
        db_instance.db = AsyncMock()
        
        # Mock failed ping
        mock_admin_db = AsyncMock()
        mock_admin_db.command.side_effect = Exception("Ping failed")
        mock_client.admin = mock_admin_db
        
        with patch.object(db_instance, 'connect') as mock_connect:
            await db_instance.ensure_connection()
            
            # Should reconnect if ping fails
            mock_connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_database_singleton_instance(self):
        """Test that database is a singleton instance"""
        # The imported 'database' should be a Database instance
        assert isinstance(database, Database)
        
        # Multiple imports should return the same instance
        from src.core.database import database as database2
        assert database is database2

    @pytest.mark.asyncio
    async def test_basic_crud_operations_extended(self, db_instance):
        """Test additional CRUD operations"""
        collection_name = "test_collection"
        mock_collection = AsyncMock()
        mock_db = AsyncMock()
        mock_db.__getitem__ = MagicMock(return_value=mock_collection)
        
        db_instance.db = mock_db
        
        # Test bulk insert
        documents = [{"name": "doc1"}, {"name": "doc2"}]
        mock_collection.insert_many.return_value = AsyncMock()
        
        await db_instance.bulk_insert(collection_name, documents)
        mock_collection.insert_many.assert_called_once_with(documents)
        
        # Test bulk update
        filter_query = {"active": True}
        update_query = {"$set": {"updated": True}}
        mock_collection.update_many.return_value = MagicMock(modified_count=5)
        
        result = await db_instance.bulk_update(collection_name, filter_query, update_query)
        assert result == 5
        mock_collection.update_many.assert_called_once_with(filter_query, update_query)
        
        # Test bulk delete
        delete_query = {"active": False}
        mock_collection.delete_many.return_value = MagicMock(deleted_count=3)
        
        result = await db_instance.bulk_delete(collection_name, delete_query)
        assert result == 3
        mock_collection.delete_many.assert_called_once_with(delete_query)

    @pytest.mark.asyncio
    async def test_transaction_support(self, db_instance):
        """Test database transaction support"""
        mock_client = AsyncMock()
        mock_session = AsyncMock()
        mock_client.start_session.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_client.start_session.return_value.__aexit__ = AsyncMock(return_value=None)
        
        db_instance.client = mock_client
        
        async with db_instance.start_transaction() as session:
            assert session == mock_session
        
        mock_client.start_session.assert_called_once()

    @pytest.mark.asyncio
    async def test_health_check_comprehensive(self, db_instance):
        """Test comprehensive database health check"""
        mock_client = AsyncMock()
        mock_db = AsyncMock()
        
        # Mock successful ping
        mock_admin_db = AsyncMock()
        mock_admin_db.command.return_value = {"ok": 1}
        mock_client.admin = mock_admin_db
        
        # Mock collection listing
        mock_db.list_collection_names.return_value = ["messages", "groups"]
        
        db_instance.client = mock_client
        db_instance.db = mock_db
        
        health_result = await db_instance.comprehensive_health_check()
        
        assert health_result["connected"] is True
        assert health_result["ping_successful"] is True
        assert "collections" in health_result
        assert len(health_result["collections"]) == 2