"""
Configuration Service - Handles system configuration
"""

from datetime import datetime
from typing import Any

from loguru import logger

from src.core.database import database
from src.models.config import DEFAULT_CONFIGS, Configuration


class ConfigService:
    """Service for managing configurations"""

    def __init__(self) -> None:
        self.collection: Any = database.get_collection("configurations")

    async def initialize_default_configs(self) -> int:
        """Initialize default configurations"""
        initialized_count = 0

        for config_data in DEFAULT_CONFIGS:
            existing = await self.collection.find_one({"key": config_data["key"]})

            if not existing:
                # Type cast for proper types
                value = config_data["value"]
                if not isinstance(value, str | int | float | bool):
                    value = str(value)

                description = config_data.get("description")
                if description is not None and not isinstance(description, str):
                    description = str(description)

                config = Configuration(
                    key=str(config_data["key"]),
                    created_at=datetime.utcnow(),
                    value=value,
                    value_type=str(config_data["value_type"]),
                    description=description,
                    category=str(config_data.get("category", "general")),
                    is_editable=bool(config_data.get("is_editable", True)),
                )
                await self.collection.insert_one(config.model_dump())
                logger.info(f"Initialized config: {config_data['key']}")
                initialized_count += 1

        return initialized_count

    async def get_config(self, key: str) -> Configuration | None:
        """Get configuration by key"""
        doc = await self.collection.find_one({"key": key})

        if doc:
            return Configuration(**doc)
        return None

    async def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value with proper type"""
        config = await self.get_config(key)

        if config:
            return config.get_typed_value()

        return default

    async def set_config(
        self, key: str, value: Any, description: str | None = None
    ) -> Configuration | None:
        """Set configuration value"""
        config = await self.get_config(key)

        if not config:
            # Create new config if it doesn't exist
            value_type = self._infer_value_type(value)
            config = Configuration(
                key=key,
                value=value,
                value_type=value_type,
                description=description,
                category="general",
                is_editable=True,
            )
            await self.collection.insert_one(config.model_dump())
            logger.info(f"Created new config {key}: {value}")
            return config

        if not config.is_editable:
            logger.warning(f"Configuration not editable: {key}")
            return None

        # Update configuration
        config.value = value
        if description is not None:
            config.description = description
        config.update_timestamp()

        await self.collection.update_one({"key": key}, {"$set": config.model_dump()})

        logger.info(f"Updated config {key}: {value}")
        return config

    async def update_config(self, key: str, update_data: dict[str, Any]) -> Configuration | None:
        """Update configuration with partial data"""
        config = await self.get_config(key)
        if not config:
            return None

        if not config.is_editable:
            logger.warning(f"Configuration not editable: {key}")
            return None

        # Update fields
        for field, value in update_data.items():
            if hasattr(config, field):
                setattr(config, field, value)

        config.update_timestamp()
        await self.collection.update_one({"key": key}, {"$set": config.model_dump()})

        logger.info(f"Updated config {key} with partial data")
        return config

    async def get_all_configs(self) -> list[Configuration]:
        """Get all configurations"""
        cursor = self.collection.find()
        configs = []

        async for doc in cursor:
            configs.append(Configuration(**doc))

        return configs

    async def get_configs_by_category(self, category: str) -> list[Configuration]:
        """Get configurations by category"""
        cursor = self.collection.find({"category": category})
        configs = []

        async for doc in cursor:
            configs.append(Configuration(**doc))

        return configs

    async def search_configs(self, search_term: str) -> list[Configuration]:
        """Search configurations by key or description"""
        query = {
            "$or": [
                {"key": {"$regex": search_term, "$options": "i"}},
                {"description": {"$regex": search_term, "$options": "i"}},
            ]
        }

        cursor = self.collection.find(query)
        configs = []

        async for doc in cursor:
            configs.append(Configuration(**doc))

        return configs

    async def bulk_update_configs(self, updates: dict[str, Any]) -> dict[str, bool]:
        """Bulk update multiple configurations"""
        results = {}

        for key, value in updates.items():
            try:
                config = await self.set_config(key, value)
                results[key] = config is not None
            except Exception as e:
                logger.error(f"Failed to update config {key}: {e}")
                results[key] = False

        return results

    async def reset_config_to_default(self, key: str) -> Configuration | None:
        """Reset configuration to default value"""
        # Find default config
        default_config = None
        for config_data in DEFAULT_CONFIGS:
            if config_data["key"] == key:
                default_config = config_data
                break

        if not default_config:
            logger.warning(f"No default found for config: {key}")
            return None

        # Reset to default
        description = default_config.get("description")
        description_str = str(description) if description is not None else None
        return await self.set_config(
            key, default_config["value"], description_str
        )

    async def get_config_history(self, key: str, limit: int = 10) -> list[dict[str, Any]]:
        """Get configuration change history"""
        history_collection = self._get_history_collection()
        cursor = history_collection.find({"key": key}).sort("timestamp", -1).limit(limit)

        history = []
        async for doc in cursor:
            history.append(doc)

        return history

    async def backup_all_configs(self) -> dict[str, Any]:
        """Backup all configurations"""
        configs = await self.get_all_configs()
        backup_data = {
            "timestamp": datetime.utcnow(),
            "configs": [config.model_dump() for config in configs],
        }

        backup_collection = self._get_backup_collection()
        result = await backup_collection.insert_one(backup_data)

        backup_id = str(result.inserted_id)
        logger.info(f"Created config backup: {backup_id}")

        return {
            "backup_id": backup_id,
            "timestamp": backup_data["timestamp"],
            "config_count": len(configs),
        }

    async def restore_from_backup(self, backup_id: str) -> bool:
        """Restore configurations from backup"""
        from bson import ObjectId

        backup_collection = self._get_backup_collection()
        backup = await backup_collection.find_one({"_id": ObjectId(backup_id)})

        if not backup:
            logger.warning(f"Backup not found: {backup_id}")
            return False

        try:
            # Clear current configs
            await self.collection.delete_many({})

            # Restore from backup
            configs_data = backup["configs"]
            if configs_data:
                await self.collection.insert_many(configs_data)

            logger.info(f"Restored {len(configs_data)} configs from backup: {backup_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to restore backup {backup_id}: {e}")
            return False

    def _validate_config_value(self, value_type: str, value: Any) -> bool:
        """Validate configuration value type"""
        try:
            if value_type == "int":
                int(value)
            elif value_type == "float":
                float(value)
            elif value_type == "bool":
                if not isinstance(value, bool) and str(value).lower() not in (
                    "true",
                    "false",
                    "1",
                    "0",
                ):
                    return False
            return True
        except (ValueError, TypeError):
            return False

    def _infer_value_type(self, value: Any) -> str:
        """Infer value type from value"""
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        else:
            return "str"

    def _get_history_collection(self):
        """Get history collection"""
        return database.get_collection("config_history")

    def _get_backup_collection(self):
        """Get backup collection"""
        return database.get_collection("config_backups")

    async def get_config_by_id(self, config_id: str) -> Configuration | None:
        """Get configuration by ID"""
        doc = await self.collection.find_one({"id": config_id})

        if doc:
            return Configuration(**doc)
        return None

    async def delete_config(self, key: str) -> bool:
        """Delete a configuration"""
        result = await self.collection.delete_one({"key": key})
        return result.deleted_count > 0

    async def get_config_count(self) -> int:
        """Get total configuration count"""
        return await self.collection.count_documents({})

    async def get_messaging_config(self) -> dict[str, Any]:
        """Get messaging-related configurations"""
        messaging_configs = await self.get_configs_by_category("messaging")

        config_dict = {}
        for config in messaging_configs:
            config_dict[config.key] = config.get_typed_value()

        return config_dict
