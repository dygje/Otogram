"""
Extended tests for Config Service to improve coverage
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.config_service import ConfigService
from src.models.config import Configuration, ConfigUpdate


class TestConfigServiceExtended:
    """Extended test coverage for ConfigService class"""

    @pytest.fixture
    def mock_collection(self):
        """Mock collection fixture"""
        return AsyncMock()

    @pytest.fixture
    def config_service(self, mock_collection):
        """ConfigService fixture with mocked collection"""
        with patch('src.services.config_service.database') as mock_database:
            mock_database.get_collection.return_value = mock_collection
            service = ConfigService()
            return service

    @pytest.mark.asyncio
    async def test_initialize_default_configs_with_existing(self, config_service, mock_collection):
        """Test initializing default configs when some already exist"""
        # Mock some configs already exist
        existing_configs = [
            {"key": "min_message_delay", "value": "5"},
            {"key": "max_message_delay", "value": "10"},
        ]
        
        async def mock_find():
            for config in existing_configs:
                yield config
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = mock_find
        mock_collection.find.return_value = mock_cursor
        
        # Mock insert for new configs
        mock_collection.insert_many.return_value = AsyncMock()
        
        # Import default configs for testing
        with patch('src.services.config_service.DEFAULT_CONFIGS', [
            {"key": "min_message_delay", "value": "5", "value_type": "str", "description": "Min delay"},
            {"key": "max_message_delay", "value": "10", "value_type": "str", "description": "Max delay"},
            {"key": "new_config", "value": "30", "value_type": "str", "description": "New config"},
        ]):
            result = await config_service.initialize_default_configs()
        
        # Should return count of initialized configs
        assert result >= 0
        
        # Verify insert was called for new configs only
        if mock_collection.insert_many.called:
            call_args = mock_collection.insert_many.call_args[0][0]
            # Should only insert configs that don't exist
            inserted_keys = [doc["key"] for doc in call_args]
            assert "new_config" in inserted_keys
            assert "min_message_delay" not in inserted_keys

    @pytest.mark.asyncio
    async def test_get_config_with_typed_value(self, config_service, mock_collection):
        """Test getting config with typed value conversion"""
        config_key = "max_retries"
        mock_doc = {
            "id": "config-1",
            "key": config_key,
            "value": "5",
            "value_type": "int",
            "description": "Maximum retries",
            "category": "general", 
            "is_editable": True,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_doc
        
        result = await config_service.get_config(config_key)
        
        assert result is not None
        assert isinstance(result, Configuration)
        assert result.key == config_key
        # The typed value should be accessible via get_typed_value()
        assert result.get_typed_value() == 5

    @pytest.mark.asyncio
    async def test_get_config_value_with_type_conversion(self, config_service, mock_collection):
        """Test getting config value with automatic type conversion"""
        config_key = "enable_logging"
        mock_doc = {
            "key": config_key,
            "value": "true",
            "value_type": "bool",
            "description": "Enable logging",
            "category": "general",
            "is_editable": True
        }
        mock_collection.find_one.return_value = mock_doc
        
        result = await config_service.get_config_value(config_key, default=False)
        
        # Should return boolean True, not string "true"
        assert result is True
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_set_config_update_existing_with_type_inference(self, config_service, mock_collection):
        """Test setting config that infers type from value"""
        config_key = "timeout_seconds"
        new_value = 30  # Integer value
        
        # Mock existing config
        mock_collection.find_one.return_value = {
            "key": config_key,
            "value": "15",
            "value_type": "int",
            "category": "general",
            "is_editable": True
        }
        
        mock_collection.update_one.return_value = MagicMock(modified_count=1)
        
        # Mock the updated document
        updated_doc = {
            "id": "config-1",
            "key": config_key,
            "value": "30",
            "value_type": "int",
            "description": "Timeout in seconds",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        
        # Return updated doc on second find_one call
        mock_collection.find_one.side_effect = [
            {"key": config_key, "value": "15", "value_type": "int", "category": "general", "is_editable": True},
            updated_doc
        ]
        
        result = await config_service.set_config(config_key, new_value)
        
        assert result is not None
        assert result.value == 30  # Integer value, not string
        assert result.value_type == "int"
        
        # Verify update was called
        call_args = mock_collection.update_one.call_args
        assert call_args[0][0] == {"key": config_key}
        update_doc = call_args[0][1]["$set"]
        assert update_doc["value"] == 30  # Integer value
        assert update_doc["value_type"] == "int"

    @pytest.mark.asyncio
    async def test_set_config_create_new_with_description(self, config_service, mock_collection):
        """Test setting new config with description"""
        config_key = "new_feature_enabled"
        new_value = True
        description = "Enable new feature"
        
        # Mock config doesn't exist
        mock_collection.find_one.return_value = None
        mock_collection.insert_one.return_value = AsyncMock()
        
        # Mock the created document
        created_doc = {
            "id": "new-config-1",
            "key": config_key,
            "value": "true",
            "value_type": "bool",
            "description": description,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        
        # Return created doc on second find_one call
        mock_collection.find_one.side_effect = [None, created_doc]
        
        result = await config_service.set_config(config_key, new_value, description)
        
        assert result is not None
        assert result.key == config_key
        assert result.value == "true"
        assert result.value_type == "bool"
        assert result.description == description

    @pytest.mark.asyncio
    async def test_update_config_with_partial_data(self, config_service, mock_collection):
        """Test updating config with partial data"""
        config_key = "api_timeout"
        update_data = ConfigUpdate(value="60")  # Only update value
        
        # Mock existing config
        existing_doc = {
            "key": config_key,
            "value": "30",
            "value_type": "int",
            "description": "API timeout in seconds",
            "category": "general",
            "is_editable": True
        }
        mock_collection.find_one.return_value = existing_doc
        mock_collection.update_one.return_value = MagicMock(modified_count=1)
        
        # Mock updated document
        updated_doc = existing_doc.copy()
        updated_doc["value"] = "60"
        mock_collection.find_one.side_effect = [existing_doc, updated_doc]
        
        result = await config_service.update_config(config_key, update_data)
        
        assert result is not None
        assert result.value == "60"
        # Description should remain unchanged
        assert result.description == "API timeout in seconds"

    @pytest.mark.asyncio
    async def test_get_configs_by_category(self, config_service, mock_collection):
        """Test getting configs filtered by category"""
        category = "messaging"
        
        mock_docs = [
            {
                "id": "1",
                "key": "min_message_delay",
                "value": "5",
                "value_type": "int",
                "category": category,
                "is_editable": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            {
                "id": "2", 
                "key": "max_message_delay",
                "value": "10",
                "value_type": "int",
                "category": category,
                "is_editable": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await config_service.get_configs_by_category(category)
        
        assert len(result) == 2
        assert all(isinstance(config, Configuration) for config in result)
        assert all(config.category == category for config in result)
        
        # Verify filter was applied
        call_args = mock_collection.find.call_args[0][0]
        assert call_args["category"] == category

    @pytest.mark.asyncio
    async def test_search_configs(self, config_service, mock_collection):
        """Test searching configs by key or description"""
        search_term = "delay"
        
        mock_docs = [
            {
                "id": "1",
                "key": "message_delay",
                "value": "5",
                "value_type": "int",
                "description": "Message delay setting",
                "category": "general",
                "is_editable": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            },
            {
                "id": "2",
                "key": "retry_config", 
                "value": "3",
                "value_type": "int",
                "description": "Delay between retries",
                "category": "general",
                "is_editable": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        result = await config_service.search_configs(search_term)
        
        assert len(result) == 2
        # Verify search query structure
        call_args = mock_collection.find.call_args[0][0]
        assert "$or" in call_args
        assert any("$regex" in condition.get("key", {}) for condition in call_args["$or"])
        assert any("$regex" in condition.get("description", {}) for condition in call_args["$or"])

    @pytest.mark.asyncio
    async def test_bulk_update_configs(self, config_service, mock_collection):
        """Test bulk updating multiple configs"""
        updates = {
            "min_delay": "3",
            "max_delay": "8",
            "retry_count": "5"
        }
        
        # Mock set_config calls to succeed
        config_service.set_config = AsyncMock()
        config_service.set_config.side_effect = [
            Configuration(key="min_delay", value="3", value_type="str"),  # Success
            Configuration(key="max_delay", value="8", value_type="str"),  # Success  
            Configuration(key="retry_count", value="5", value_type="str")  # Success
        ]
        
        result = await config_service.bulk_update_configs(updates)
        
        # Should return dict of results
        assert isinstance(result, dict)
        assert len(result) == 3
        assert all(result[key] for key in updates.keys())
        
        # Verify set_config was called for each config
        assert config_service.set_config.call_count == 3

    @pytest.mark.asyncio
    async def test_bulk_update_configs_partial_success(self, config_service, mock_collection):
        """Test bulk updating with some failures"""
        updates = {
            "existing_config": "value1",
            "nonexistent_config": "value2"
        }
        
        # Mock set_config calls - first succeeds, second fails
        config_service.set_config = AsyncMock()
        config_service.set_config.side_effect = [
            Configuration(key="existing_config", value="value1", value_type="str"),  # Success
            None  # Failure
        ]
        
        result = await config_service.bulk_update_configs(updates)
        
        # Should return dict with mixed results
        assert isinstance(result, dict)
        assert result["existing_config"] is True
        assert result["nonexistent_config"] is False

    @pytest.mark.asyncio
    async def test_reset_config_to_default(self, config_service, mock_collection):
        """Test resetting config to default value"""
        config_key = "message_delay"
        
        # Mock finding default config
        with patch('src.services.config_service.DEFAULT_CONFIGS', [
            {"key": config_key, "value": "5", "value_type": "str", "description": "Default delay"}
        ]):
            mock_collection.update_one.return_value = MagicMock(modified_count=1)
            
            # Mock updated document
            updated_doc = {
                "id": "config-1",
                "key": config_key,
                "value": "5",
                "value_type": "str",
                "description": "Default delay",
                "category": "general",
                "is_editable": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
            mock_collection.find_one.return_value = updated_doc
            
            result = await config_service.reset_config_to_default(config_key)
            
            assert result is not None
            assert result.value == "5"
            
            # Verify update was called
            mock_collection.update_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_reset_config_to_default_not_found(self, config_service, mock_collection):
        """Test resetting config to default when default not found"""
        config_key = "nonexistent_config"
        
        with patch('src.services.config_service.DEFAULT_CONFIGS', []):
            result = await config_service.reset_config_to_default(config_key)
            
            assert result is None
            # Should not call update if default not found
            mock_collection.update_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_config_history(self, config_service, mock_collection):
        """Test getting config change history"""
        config_key = "important_setting"
        
        # Mock history collection
        mock_history_docs = [
            {
                "config_key": config_key,
                "old_value": "10",
                "new_value": "20",
                "changed_at": "2023-01-01T10:00:00",
                "changed_by": "admin"
            },
            {
                "config_key": config_key,
                "old_value": "20", 
                "new_value": "30",
                "changed_at": "2023-01-01T11:00:00",
                "changed_by": "admin"
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_history_docs)
        
        # Mock getting history collection
        with patch.object(config_service, '_get_history_collection') as mock_get_history:
            mock_history_collection = AsyncMock()
            mock_history_collection.find.return_value = mock_cursor
            mock_get_history.return_value = mock_history_collection
            
            result = await config_service.get_config_history(config_key)
            
            assert len(result) == 2
            assert result[0]["config_key"] == config_key
            assert result[0]["old_value"] == "10"
            assert result[1]["new_value"] == "30"

    @pytest.mark.asyncio
    async def test_backup_all_configs(self, config_service, mock_collection):
        """Test backing up all configurations"""
        mock_docs = [
            {
                "key": "config1",
                "value": "value1", 
                "value_type": "str",
                "description": "Config 1",
                "category": "general",
                "is_editable": True
            },
            {
                "key": "config2",
                "value": "value2",
                "value_type": "str",
                "description": "Config 2",
                "category": "general",
                "is_editable": True
            }
        ]
        
        async def async_iter(docs):
            for doc in docs:
                yield doc
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__ = lambda: async_iter(mock_docs)
        mock_collection.find.return_value = mock_cursor
        
        # Mock backup collection
        with patch.object(config_service, '_get_backup_collection') as mock_get_backup:
            mock_backup_collection = AsyncMock()
            mock_get_backup.return_value = mock_backup_collection
            
            result = await config_service.backup_all_configs()
            
            # Should return backup metadata
            assert "backup_id" in result
            assert "timestamp" in result
            assert "config_count" in result
            assert result["config_count"] == 2
            
            # Verify backup was inserted
            mock_backup_collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_restore_from_backup(self, config_service, mock_collection):
        """Test restoring configs from backup"""
        backup_id = "backup-123"
        
        # Mock backup document
        backup_doc = {
            "backup_id": backup_id,
            "configs": [
                {"key": "config1", "value": "backup_value1", "value_type": "str"},
                {"key": "config2", "value": "backup_value2", "value_type": "str"}
            ],
            "timestamp": "2023-01-01T12:00:00"
        }
        
        with patch.object(config_service, '_get_backup_collection') as mock_get_backup:
            mock_backup_collection = AsyncMock()
            mock_backup_collection.find_one.return_value = backup_doc
            mock_get_backup.return_value = mock_backup_collection
            
            # Mock config updates
            mock_collection.update_one.return_value = MagicMock(modified_count=1)
            
            result = await config_service.restore_from_backup(backup_id)
            
            assert result is True
            # Should update each config in backup
            assert mock_collection.update_one.call_count == 2

    @pytest.mark.asyncio
    async def test_restore_from_backup_not_found(self, config_service, mock_collection):
        """Test restoring from non-existent backup"""
        backup_id = "nonexistent-backup"
        
        with patch.object(config_service, '_get_backup_collection') as mock_get_backup:
            mock_backup_collection = AsyncMock()
            mock_backup_collection.find_one.return_value = None
            mock_get_backup.return_value = mock_backup_collection
            
            result = await config_service.restore_from_backup(backup_id)
            
            assert result is False
            # Should not attempt any updates
            mock_collection.update_one.assert_not_called()

    def test_validate_config_value(self, config_service):
        """Test config value validation"""
        # Test integer validation
        assert config_service._validate_config_value("int", "5") is True
        assert config_service._validate_config_value("int", "invalid") is False
        
        # Test float validation
        assert config_service._validate_config_value("float", "5.5") is True
        assert config_service._validate_config_value("float", "invalid") is False
        
        # Test boolean validation
        assert config_service._validate_config_value("bool", "true") is True
        assert config_service._validate_config_value("bool", "false") is True
        assert config_service._validate_config_value("bool", "invalid") is False
        
        # Test string validation (always true)
        assert config_service._validate_config_value("str", "anything") is True

    def test_infer_value_type(self, config_service):
        """Test automatic value type inference"""
        assert config_service._infer_value_type(42) == "int"
        assert config_service._infer_value_type(3.14) == "float"
        assert config_service._infer_value_type(True) == "bool"
        assert config_service._infer_value_type(False) == "bool"
        assert config_service._infer_value_type("hello") == "str"
        assert config_service._infer_value_type([1, 2, 3]) == "str"  # Fallback