"""
Comprehensive tests for Core Database Module
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.database import Database, database


class TestDatabaseComprehensive:
    """Comprehensive test coverage for Database class"""

    @pytest.fixture
    def db_instance(self):
        """Database instance fixture"""
        return Database()

    @pytest.mark.asyncio
    async def test_connect_success(self, db_instance):
        """Test successful database connection"""
        with patch('motor.motor_asyncio.AsyncIOMotorClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_db = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.__getitem__.return_value = mock_db
            
            # Mock successful ping
            mock_client.admin.command.return_value = {"ok": 1}
            
            await db_instance.connect()
            
            assert db_instance.client is not None
            assert db_instance.db is not None
            mock_client.admin.command.assert_called_once_with("ping")

    @pytest.mark.asyncio
    async def test_connect_with_custom_url(self, db_instance):
        """Test connection with custom MongoDB URL"""
        custom_url = "mongodb://custom:27017"
        
        with patch('motor.motor_asyncio.AsyncIOMotorClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_db = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.__getitem__.return_value = mock_db
            mock_client.admin.command.return_value = {"ok": 1}
            
            await db_instance.connect(custom_url)
            
            mock_client_class.assert_called_once_with(custom_url)

    @pytest.mark.asyncio
    async def test_connect_failure(self, db_instance):
        """Test database connection failure"""
        with patch('motor.motor_asyncio.AsyncIOMotorClient') as mock_client_class:
            mock_client_class.side_effect = Exception("Connection failed")
            
            with pytest.raises(Exception):
                await db_instance.connect()

    @pytest.mark.asyncio
    async def test_disconnect(self, db_instance):
        """Test database disconnection"""
        mock_client = MagicMock()
        db_instance.client = mock_client
        db_instance.db = MagicMock()
        
        await db_instance.disconnect()
        
        mock_client.close.assert_called_once()
        assert db_instance.client is None
        assert db_instance.db is None

    @pytest.mark.asyncio
    async def test_disconnect_when_not_connected(self, db_instance):
        """Test disconnect when not connected"""
        await db_instance.disconnect()  # Should not raise error
        assert db_instance.client is None

    @pytest.mark.asyncio
    async def test_create_indexes_success(self, db_instance):
        """Test successful index creation"""
        mock_db = AsyncMock()
        db_instance.db = mock_db
        
        await db_instance.create_indexes()
        
        # Verify index creation calls
        mock_db.messages.create_index.assert_called()
        mock_db.groups.create_index.assert_called()
        mock_db.blacklists.create_index.assert_called()

    @pytest.mark.asyncio
    async def test_create_indexes_without_connection(self, db_instance):
        """Test index creation without connection"""
        await db_instance.create_indexes()  # Should handle gracefully
        # Should log error but not raise exception

    @pytest.mark.asyncio
    async def test_create_indexes_failure(self, db_instance):
        """Test index creation failure"""
        mock_db = AsyncMock()
        mock_db.messages.create_index.side_effect = Exception("Index creation failed")
        db_instance.db = mock_db
        
        await db_instance.create_indexes()  # Should handle gracefully
        # Should log warning but not raise exception

    @pytest.mark.asyncio
    async def test_ping_success(self, db_instance):
        """Test successful ping"""
        mock_client = AsyncMock()
        mock_client.admin.command.return_value = {"ok": 1}
        db_instance.client = mock_client
        
        result = await db_instance.ping()
        
        assert result is True
        mock_client.admin.command.assert_called_once_with("ping")

    @pytest.mark.asyncio
    async def test_ping_failure(self, db_instance):
        """Test ping failure"""
        mock_client = AsyncMock()
        mock_client.admin.command.side_effect = Exception("Ping failed")
        db_instance.client = mock_client
        
        result = await db_instance.ping()
        
        assert result is False

    @pytest.mark.asyncio
    async def test_ping_no_client(self, db_instance):
        """Test ping when no client"""
        result = await db_instance.ping()
        assert result is False

    @pytest.mark.asyncio
    async def test_get_database_stats_success(self, db_instance):
        """Test successful database stats retrieval"""
        mock_db = AsyncMock()
        mock_stats = {
            "db": "test_db",
            "collections": 5,
            "dataSize": 1024,
            "storageSize": 2048,
            "indexSize": 512,
            "objects": 100
        }
        mock_db.command.return_value = mock_stats
        db_instance.db = mock_db
        
        result = await db_instance.get_database_stats()
        
        assert result["db_name"] == "test_db"
        assert result["collections"] == 5
        assert result["data_size"] == 1024
        mock_db.command.assert_called_once_with("dbStats")

    @pytest.mark.asyncio
    async def test_get_database_stats_no_db(self, db_instance):
        """Test database stats when no db connection"""
        with pytest.raises(RuntimeError):
            await db_instance.get_database_stats()

    @pytest.mark.asyncio
    async def test_drop_collection_success(self, db_instance):
        """Test successful collection drop"""
        mock_db = AsyncMock()
        db_instance.db = mock_db
        
        result = await db_instance.drop_collection("test_collection")
        
        assert result is True
        mock_db.drop_collection.assert_called_once_with("test_collection")

    @pytest.mark.asyncio
    async def test_drop_collection_failure(self, db_instance):
        """Test collection drop failure"""
        mock_db = AsyncMock()
        mock_db.drop_collection.side_effect = Exception("Drop failed")
        db_instance.db = mock_db
        
        result = await db_instance.drop_collection("test_collection")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_list_collections_success(self, db_instance):
        """Test successful collection listing"""
        mock_db = AsyncMock()
        mock_db.list_collection_names.return_value = ["messages", "groups", "blacklists"]
        db_instance.db = mock_db
        
        result = await db_instance.list_collections()
        
        assert result == ["messages", "groups", "blacklists"]

    @pytest.mark.asyncio
    async def test_list_collections_failure(self, db_instance):
        """Test collection listing failure"""
        mock_db = AsyncMock()
        mock_db.list_collection_names.side_effect = Exception("List failed")
        db_instance.db = mock_db
        
        result = await db_instance.list_collections()
        
        assert result == []

    @pytest.mark.asyncio
    async def test_collection_exists_true(self, db_instance):
        """Test collection exists returns true"""
        db_instance.list_collections = AsyncMock(return_value=["messages", "groups"])
        
        result = await db_instance.collection_exists("messages")
        
        assert result is True

    @pytest.mark.asyncio
    async def test_collection_exists_false(self, db_instance):
        """Test collection exists returns false"""
        db_instance.list_collections = AsyncMock(return_value=["messages", "groups"])
        
        result = await db_instance.collection_exists("nonexistent")
        
        assert result is False

    @pytest.mark.asyncio
    async def test_get_collection_size_success(self, db_instance):
        """Test successful collection size retrieval"""
        mock_db = AsyncMock()
        mock_collection = AsyncMock()
        mock_collection.count_documents.return_value = 150
        mock_db.__getitem__.return_value = mock_collection
        db_instance.db = mock_db
        
        result = await db_instance.get_collection_size("messages")
        
        assert result == 150
        mock_collection.count_documents.assert_called_once_with({})

    @pytest.mark.asyncio
    async def test_get_collection_size_failure(self, db_instance):
        """Test collection size retrieval failure"""
        mock_db = AsyncMock()
        mock_collection = AsyncMock()
        mock_collection.count_documents.side_effect = Exception("Count failed")
        mock_db.__getitem__.return_value = mock_collection
        db_instance.db = mock_db
        
        result = await db_instance.get_collection_size("messages")
        
        assert result == 0

    @pytest.mark.asyncio
    async def test_ensure_connection_when_connected(self, db_instance):
        """Test ensure connection when already connected"""
        db_instance.client = MagicMock()
        db_instance.ping = AsyncMock(return_value=True)
        
        await db_instance.ensure_connection()
        
        db_instance.ping.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_connection_when_disconnected(self, db_instance):
        """Test ensure connection when disconnected"""
        db_instance.connect = AsyncMock()
        
        await db_instance.ensure_connection()
        
        db_instance.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_ensure_connection_ping_fails(self, db_instance):
        """Test ensure connection when ping fails"""
        db_instance.client = MagicMock()
        db_instance.ping = AsyncMock(return_value=False)
        db_instance.connect = AsyncMock()
        
        await db_instance.ensure_connection()
        
        db_instance.connect.assert_called_once()

    @pytest.mark.asyncio
    async def test_bulk_insert_success(self, db_instance):
        """Test successful bulk insert"""
        mock_db = AsyncMock()
        mock_collection = AsyncMock()
        mock_result = MagicMock()
        mock_result.inserted_ids = ["id1", "id2", "id3"]
        mock_collection.insert_many.return_value = mock_result
        mock_db.__getitem__.return_value = mock_collection
        db_instance.db = mock_db
        
        documents = [{"data": 1}, {"data": 2}, {"data": 3}]
        result = await db_instance.bulk_insert("test_collection", documents)
        
        assert result == 3
        mock_collection.insert_many.assert_called_once_with(documents)

    @pytest.mark.asyncio
    async def test_bulk_insert_empty_documents(self, db_instance):
        """Test bulk insert with empty documents"""
        mock_db = AsyncMock()
        db_instance.db = mock_db
        
        result = await db_instance.bulk_insert("test_collection", [])
        
        assert result == 0

    @pytest.mark.asyncio
    async def test_bulk_insert_no_db(self, db_instance):
        """Test bulk insert when no db connection"""
        with pytest.raises(RuntimeError):
            await db_instance.bulk_insert("test_collection", [{"data": 1}])

    @pytest.mark.asyncio
    async def test_start_transaction(self, db_instance):
        """Test starting transaction"""
        mock_client = AsyncMock()
        mock_session = AsyncMock()
        mock_client.start_session.return_value = mock_session
        db_instance.client = mock_client
        
        result = await db_instance.start_transaction()
        
        assert result == mock_session
        mock_client.start_session.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_transaction_no_client(self, db_instance):
        """Test starting transaction when no client"""
        with pytest.raises(RuntimeError):
            await db_instance.start_transaction()

    @pytest.mark.asyncio
    async def test_comprehensive_health_check_success(self, db_instance):
        """Test comprehensive health check success"""
        mock_client = MagicMock()
        mock_db = MagicMock()
        db_instance.client = mock_client
        db_instance.db = mock_db
        
        db_instance.ping = AsyncMock(return_value=True)
        db_instance.list_collections = AsyncMock(return_value=["messages", "groups"])
        db_instance.get_database_stats = AsyncMock(return_value={"collections": 2})
        
        result = await db_instance.comprehensive_health_check()
        
        assert result["connected"] is True
        assert result["ping_success"] is True
        assert result["collections"] == ["messages", "groups"]
        assert result["stats"]["collections"] == 2
        assert result["error"] is None

    @pytest.mark.asyncio
    async def test_comprehensive_health_check_failure(self, db_instance):
        """Test comprehensive health check with failure"""
        db_instance.client = None
        db_instance.db = None
        
        result = await db_instance.comprehensive_health_check()
        
        assert result["connected"] is False
        assert result["ping_success"] is False
        assert result["collections"] == []
        assert result["stats"] is None

    @pytest.mark.asyncio
    async def test_comprehensive_health_check_exception(self, db_instance):
        """Test comprehensive health check with exception"""
        mock_client = MagicMock()
        db_instance.client = mock_client
        db_instance.db = mock_client
        db_instance.ping = AsyncMock(side_effect=Exception("Health check failed"))
        
        result = await db_instance.comprehensive_health_check()
        
        assert "error" in result
        assert "Health check failed" in str(result["error"])

    def test_get_collection_success(self, db_instance):
        """Test successful get collection"""
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        db_instance.db = mock_db
        
        result = db_instance.get_collection("test_collection")
        
        assert result == mock_collection
        mock_db.__getitem__.assert_called_once_with("test_collection")

    def test_get_collection_no_db(self, db_instance):
        """Test get collection when no db connection"""
        with pytest.raises(RuntimeError):
            db_instance.get_collection("test_collection")

    def test_global_database_instance(self):
        """Test that global database instance exists"""
        assert database is not None
        assert isinstance(database, Database)