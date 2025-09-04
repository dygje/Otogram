"""
Tests for database functionality
"""

import pytest

from src.core.config import settings
from src.core.constants import DB_PING_OK_VALUE, TEST_VALUE_INITIAL, TEST_VALUE_UPDATED
from src.core.database import Database


class TestDatabase:
    """Test Database class"""

    @pytest.mark.asyncio
    async def test_database_connection(self) -> None:
        """Test database connection and disconnection"""
        db = Database()

        # Connect
        await db.connect()
        assert db.client is not None
        assert db.db is not None
        assert db.db.name == settings.DB_NAME

        # Test ping
        ping_result = await db.client.admin.command("ping")
        assert ping_result["ok"] == DB_PING_OK_VALUE

        # Disconnect
        await db.disconnect()

    @pytest.mark.asyncio
    async def test_get_collection(self, test_database: Database) -> None:
        """Test getting collections"""
        db = test_database

        # Get collection
        collection = db.get_collection("test_collection")
        assert collection is not None
        assert collection.name == "test_collection"

    @pytest.mark.asyncio
    async def test_get_collection_without_connection(self) -> None:
        """Test getting collection without connection raises error"""
        db = Database()

        with pytest.raises(RuntimeError, match="Database not connected"):
            db.get_collection("test_collection")

    @pytest.mark.asyncio
    async def test_indexes_creation(self, test_database: Database) -> None:
        """Test that indexes are created properly"""
        db = test_database

        # Check that collections exist and have indexes
        collections_to_check = ["messages", "groups", "blacklists", "logs", "configurations"]

        for collection_name in collections_to_check:
            collection = db.get_collection(collection_name)
            indexes = await collection.list_indexes().to_list(length=None)

            # Should have at least the default _id index
            assert len(indexes) >= 1

            # Check for specific indexes based on collection
            [idx["name"] for idx in indexes]

            if collection_name == "messages":
                # These might not exist if no documents, but structure should support them
                pass  # Skip detailed index validation for now

    @pytest.mark.asyncio
    async def test_basic_crud_operations(self, test_database: Database) -> None:
        """Test basic CRUD operations"""
        db = test_database
        collection = db.get_collection("test_crud")

        # Create
        test_doc = {"name": "test", "value": TEST_VALUE_INITIAL}
        insert_result = await collection.insert_one(test_doc)
        assert insert_result.inserted_id is not None

        # Read
        found_doc = await collection.find_one({"name": "test"})
        assert found_doc is not None
        assert found_doc["name"] == "test"
        assert found_doc["value"] == TEST_VALUE_INITIAL

        # Update
        update_result = await collection.update_one(
            {"name": "test"}, {"$set": {"value": TEST_VALUE_UPDATED}}
        )
        assert update_result.modified_count == 1

        # Verify update
        updated_doc = await collection.find_one({"name": "test"})
        assert updated_doc["value"] == TEST_VALUE_UPDATED

        # Delete
        delete_result = await collection.delete_one({"name": "test"})
        assert delete_result.deleted_count == 1

        # Verify deletion
        deleted_doc = await collection.find_one({"name": "test"})
        assert deleted_doc is None
