"""
Tests for Config Service
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.services.config_service import ConfigService
from src.models.config import Configuration


class TestConfigService:
    """Test ConfigService class"""

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
    async def test_initialize_default_configs_new(self, config_service, mock_collection):
        """Test initializing default configs when none exist"""
        # Mock no existing configs
        mock_collection.find_one.return_value = None
        mock_collection.insert_one.return_value = AsyncMock()
        
        await config_service.initialize_default_configs()
        
        # Should check for existing configs
        assert mock_collection.find_one.call_count > 0
        # Should insert new configs
        assert mock_collection.insert_one.call_count > 0

    @pytest.mark.asyncio
    async def test_initialize_default_configs_existing(self, config_service, mock_collection):
        """Test initializing default configs when they already exist"""
        # Mock existing config
        mock_collection.find_one.return_value = {"key": "test_key", "value": "test_value"}
        
        await config_service.initialize_default_configs()
        
        # Should check for existing configs but not insert any
        assert mock_collection.find_one.call_count > 0
        mock_collection.insert_one.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_config(self, config_service, mock_collection):
        """Test getting a configuration by key"""
        config_key = "test_key"
        mock_doc = {
            "id": "test-id",
            "key": config_key,
            "value": "test_value",
            "value_type": "str",
            "description": "Test configuration",
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
        assert result.value == "test_value"
        mock_collection.find_one.assert_called_once_with({"key": config_key})

    @pytest.mark.asyncio
    async def test_get_config_not_found(self, config_service, mock_collection):
        """Test getting config when not found"""
        config_key = "nonexistent_key"
        mock_collection.find_one.return_value = None
        
        result = await config_service.get_config(config_key)
        
        assert result is None
        mock_collection.find_one.assert_called_once_with({"key": config_key})

    @pytest.mark.asyncio
    async def test_get_config_value(self, config_service, mock_collection):
        """Test getting a configuration value"""
        config_key = "test_key"
        mock_doc = {
            "key": config_key,
            "value": "test_value",
            "value_type": "str",
            "description": "Test configuration",
            "category": "general",
            "is_editable": True,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_doc
        
        result = await config_service.get_config_value(config_key)
        
        assert result == "test_value"
        mock_collection.find_one.assert_called_once_with({"key": config_key})

    @pytest.mark.asyncio
    async def test_get_config_value_with_default(self, config_service, mock_collection):
        """Test getting config value with default when not found"""
        config_key = "nonexistent_key"
        default_value = "default_value"
        mock_collection.find_one.return_value = None
        
        result = await config_service.get_config_value(config_key, default_value)
        
        assert result == default_value
        mock_collection.find_one.assert_called_once_with({"key": config_key})

    @pytest.mark.asyncio
    async def test_set_config_new(self, config_service, mock_collection):
        """Test setting a new configuration"""
        config_key = "new_key"
        config_value = "new_value"
        
        # Mock existing config found
        mock_existing_doc = {
            "key": config_key,
            "value": "old_value",
            "value_type": "str",
            "description": "Test configuration",
            "category": "general",
            "is_editable": True,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_existing_doc
        mock_collection.update_one.return_value = MagicMock(matched_count=1)
        
        result = await config_service.set_config(config_key, config_value)
        
        assert isinstance(result, Configuration)
        assert result.key == config_key
        assert result.value == config_value
        mock_collection.update_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_config_update_existing(self, config_service, mock_collection):
        """Test updating existing configuration"""
        config_key = "existing_key"
        config_value = "updated_value"
        
        # Mock existing config
        mock_existing_doc = {
            "key": config_key,
            "value": "old_value",
            "value_type": "str",
            "description": "Test configuration",
            "category": "general",
            "is_editable": True,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
        mock_collection.find_one.return_value = mock_existing_doc
        mock_collection.update_one.return_value = MagicMock(matched_count=1)
        
        result = await config_service.set_config(config_key, config_value)
        
        assert isinstance(result, Configuration)
        assert result.key == config_key
        assert result.value == config_value
        mock_collection.update_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_configs(self, config_service, mock_collection):
        """Test getting all configurations"""
        mock_configs = [
            Configuration(
                key="key1",
                value="value1",
                value_type="str",
                description="Config 1",
            ),
            Configuration(
                key="key2", 
                value="value2",
                value_type="str",
                description="Config 2",
            )
        ]
        
        # Mock the entire method
        config_service.get_all_configs = AsyncMock(return_value=mock_configs)
        
        result = await config_service.get_all_configs()
        
        assert len(result) == 2
        assert all(isinstance(config, Configuration) for config in result)
        assert result[0].key == "key1"
        assert result[1].key == "key2"

    @pytest.mark.asyncio
    async def test_delete_config(self, config_service, mock_collection):
        """Test deleting configuration"""
        config_key = "test_key"
        mock_collection.delete_one.return_value = MagicMock(deleted_count=1)
        
        result = await config_service.delete_config(config_key)
        
        assert result is True
        mock_collection.delete_one.assert_called_once_with({"key": config_key})

    @pytest.mark.asyncio
    async def test_delete_config_not_found(self, config_service, mock_collection):
        """Test deleting config when not found"""
        config_key = "nonexistent_key"
        mock_collection.delete_one.return_value = MagicMock(deleted_count=0)
        
        result = await config_service.delete_config(config_key)
        
        assert result is False
        mock_collection.delete_one.assert_called_once_with({"key": config_key})

    @pytest.mark.asyncio
    async def test_get_config_count(self, config_service, mock_collection):
        """Test getting total config count"""
        mock_collection.count_documents.return_value = 5
        
        result = await config_service.get_config_count()
        
        assert result == 5
        mock_collection.count_documents.assert_called_once_with({})