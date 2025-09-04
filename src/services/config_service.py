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
        self.collection = database.get_collection("configurations")

    async def initialize_default_configs(self) -> None:
        """Initialize default configurations"""
        for config_data in DEFAULT_CONFIGS:
            existing = await self.collection.find_one({"key": config_data["key"]})

            if not existing:
                # Type cast for proper types
                value = config_data["value"]
                if not isinstance(value, (str, int, float, bool)):
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
                    is_editable=bool(config_data.get("is_editable", True))
                )
                await self.collection.insert_one(config.dict())
                logger.info(f"Initialized config: {config_data['key']}")

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

    async def set_config(self, key: str, value: Any) -> Configuration | None:
        """Set configuration value"""
        config = await self.get_config(key)

        if not config:
            logger.warning(f"Configuration not found: {key}")
            return None

        if not config.is_editable:
            logger.warning(f"Configuration not editable: {key}")
            return None

        # Update configuration
        config.value = value
        config.update_timestamp()

        await self.collection.update_one({"key": key}, {"$set": config.dict()})

        logger.info(f"Updated config {key}: {value}")
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

    async def get_config_by_id(self, config_id: str) -> Configuration | None:
        """Get configuration by ID"""
        doc = await self.collection.find_one({"id": config_id})

        if doc:
            return Configuration(**doc)
        return None

    async def get_messaging_config(self) -> dict:
        """Get messaging-related configurations"""
        messaging_configs = await self.get_configs_by_category("messaging")

        config_dict = {}
        for config in messaging_configs:
            config_dict[config.key] = config.get_typed_value()

        return config_dict
