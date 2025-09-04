"""
Tests for Configuration Models
"""

import pytest
from pydantic import ValidationError

from src.models.config import Configuration, ConfigUpdate, DEFAULT_CONFIGS


class TestConfiguration:
    """Test Configuration model"""

    def test_configuration_creation_minimal(self):
        """Test creating configuration with minimal fields"""
        config = Configuration(
            key="test_key",
            value="test_value",
            value_type="str"
        )
        
        assert config.key == "test_key"
        assert config.value == "test_value"
        assert config.value_type == "str"
        assert config.description is None
        assert config.category == "general"  # Default value
        assert config.is_editable is True    # Default value
        
        # Check inherited fields
        assert hasattr(config, 'id')
        assert hasattr(config, 'created_at')
        assert hasattr(config, 'updated_at')

    def test_configuration_creation_full(self):
        """Test creating configuration with all fields"""
        config = Configuration(
            key="full_config",
            value=42,
            value_type="int",
            description="A full configuration example",
            category="messaging",
            is_editable=False
        )
        
        assert config.key == "full_config"
        assert config.value == 42
        assert config.value_type == "int"
        assert config.description == "A full configuration example"
        assert config.category == "messaging"
        assert config.is_editable is False

    def test_configuration_default_values(self):
        """Test configuration default values"""
        config = Configuration(
            key="defaults_test",
            value="value",
            value_type="str"
        )
        
        assert config.category == "general"
        assert config.is_editable is True
        assert config.description is None

    def test_configuration_different_value_types(self):
        """Test configuration with different value types"""
        # String value
        str_config = Configuration(key="str_key", value="string_value", value_type="str")
        assert isinstance(str_config.value, str)
        
        # Integer value
        int_config = Configuration(key="int_key", value=123, value_type="int")
        assert isinstance(int_config.value, int)
        
        # Float value
        float_config = Configuration(key="float_key", value=3.14, value_type="float")
        assert isinstance(float_config.value, float)
        
        # Boolean value
        bool_config = Configuration(key="bool_key", value=True, value_type="bool")
        assert isinstance(bool_config.value, bool)

    def test_configuration_required_fields(self):
        """Test configuration required fields validation"""
        # Missing key
        with pytest.raises(ValidationError):
            Configuration(value="value", value_type="str")
        
        # Missing value
        with pytest.raises(ValidationError):
            Configuration(key="key", value_type="str")
        
        # Missing value_type
        with pytest.raises(ValidationError):
            Configuration(key="key", value="value")

    def test_get_typed_value_string(self):
        """Test get_typed_value for string type"""
        config = Configuration(key="str_test", value="test_string", value_type="str")
        result = config.get_typed_value()
        
        assert result == "test_string"
        assert isinstance(result, str)

    def test_get_typed_value_int(self):
        """Test get_typed_value for int type"""
        # Integer value stored as int
        config1 = Configuration(key="int_test", value=42, value_type="int")
        result1 = config1.get_typed_value()
        assert result1 == 42
        assert isinstance(result1, int)
        
        # Integer value stored as string
        config2 = Configuration(key="int_test", value="123", value_type="int")
        result2 = config2.get_typed_value()
        assert result2 == 123
        assert isinstance(result2, int)

    def test_get_typed_value_float(self):
        """Test get_typed_value for float type"""
        # Float value stored as float
        config1 = Configuration(key="float_test", value=3.14, value_type="float")
        result1 = config1.get_typed_value()
        assert result1 == 3.14
        assert isinstance(result1, float)
        
        # Float value stored as string
        config2 = Configuration(key="float_test", value="2.71", value_type="float")
        result2 = config2.get_typed_value()
        assert result2 == 2.71
        assert isinstance(result2, float)

    def test_get_typed_value_bool_true_variants(self):
        """Test get_typed_value for bool type (true variants)"""
        true_variants = ["true", "True", "TRUE", "1", "yes", "Yes", "YES"]
        
        for variant in true_variants:
            config = Configuration(key="bool_test", value=variant, value_type="bool")
            result = config.get_typed_value()
            assert result is True, f"Failed for variant: {variant}"

    def test_get_typed_value_bool_false_variants(self):
        """Test get_typed_value for bool type (false variants)"""
        false_variants = ["false", "False", "FALSE", "0", "no", "No", "NO", "anything_else"]
        
        for variant in false_variants:
            config = Configuration(key="bool_test", value=variant, value_type="bool")
            result = config.get_typed_value()
            assert result is False, f"Failed for variant: {variant}"

    def test_get_typed_value_bool_actual_boolean(self):
        """Test get_typed_value for bool type with actual boolean values"""
        # True boolean
        config_true = Configuration(key="bool_test", value=True, value_type="bool")
        result_true = config_true.get_typed_value()
        assert result_true is True
        
        # False boolean
        config_false = Configuration(key="bool_test", value=False, value_type="bool")
        result_false = config_false.get_typed_value()
        assert result_false is False

    def test_get_typed_value_unknown_type(self):
        """Test get_typed_value for unknown type"""
        config = Configuration(key="unknown_test", value="some_value", value_type="unknown")
        result = config.get_typed_value()
        
        # Should return string representation
        assert result == "some_value"
        assert isinstance(result, str)

    def test_configuration_serialization(self):
        """Test configuration serialization"""
        config = Configuration(
            key="serialization_test",
            value="test_value",
            value_type="str",
            description="Test description",
            category="test",
            is_editable=True
        )
        
        data = config.model_dump()
        assert isinstance(data, dict)
        assert data['key'] == "serialization_test"
        assert data['value'] == "test_value"
        assert data['value_type'] == "str"
        assert data['description'] == "Test description"
        assert data['category'] == "test"
        assert data['is_editable'] is True
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data

    def test_configuration_with_numeric_values(self):
        """Test configuration with various numeric values"""
        # Zero
        config_zero = Configuration(key="zero", value=0, value_type="int")
        assert config_zero.get_typed_value() == 0
        
        # Negative number
        config_neg = Configuration(key="negative", value=-42, value_type="int")
        assert config_neg.get_typed_value() == -42
        
        # Decimal
        config_decimal = Configuration(key="decimal", value=0.5, value_type="float")
        assert config_decimal.get_typed_value() == 0.5

    def test_configuration_categories(self):
        """Test configuration with different categories"""
        categories = ["general", "messaging", "system", "security", "custom"]
        
        for category in categories:
            config = Configuration(
                key=f"{category}_key",
                value="value",
                value_type="str",
                category=category
            )
            assert config.category == category

    def test_configuration_editable_flags(self):
        """Test configuration editable flags"""
        # Editable configuration
        editable_config = Configuration(
            key="editable",
            value="value",
            value_type="str",
            is_editable=True
        )
        assert editable_config.is_editable is True
        
        # Non-editable configuration
        readonly_config = Configuration(
            key="readonly",
            value="value",
            value_type="str",
            is_editable=False
        )
        assert readonly_config.is_editable is False

    def test_configuration_validation_required_fields(self):
        """Test configuration validation for required fields"""
        # All required fields present - should work
        config = Configuration(
            key="valid",
            value="value",
            value_type="str"
        )
        assert config.key == "valid"
        
        # Test individual missing fields
        with pytest.raises(ValidationError):
            Configuration(value="value", value_type="str")  # Missing key
        
        with pytest.raises(ValidationError):
            Configuration(key="key", value_type="str")      # Missing value
        
        with pytest.raises(ValidationError):
            Configuration(key="key", value="value")         # Missing value_type


class TestConfigUpdate:
    """Test ConfigUpdate model"""

    def test_config_update_string_value(self):
        """Test ConfigUpdate with string value"""
        update = ConfigUpdate(value="updated_string")
        
        assert update.value == "updated_string"
        assert isinstance(update.value, str)

    def test_config_update_int_value(self):
        """Test ConfigUpdate with int value"""
        update = ConfigUpdate(value=42)
        
        assert update.value == 42
        assert isinstance(update.value, int)

    def test_config_update_float_value(self):
        """Test ConfigUpdate with float value"""
        update = ConfigUpdate(value=3.14)
        
        assert update.value == 3.14
        assert isinstance(update.value, float)

    def test_config_update_bool_value(self):
        """Test ConfigUpdate with bool value"""
        # True value
        update_true = ConfigUpdate(value=True)
        assert update_true.value is True
        
        # False value
        update_false = ConfigUpdate(value=False)
        assert update_false.value is False

    def test_config_update_required_field(self):
        """Test that value is required in ConfigUpdate"""
        with pytest.raises(ValidationError):
            ConfigUpdate()

    def test_config_update_serialization(self):
        """Test ConfigUpdate serialization"""
        update = ConfigUpdate(value="test_update")
        
        data = update.model_dump()
        assert isinstance(data, dict)
        assert data['value'] == "test_update"

    def test_config_update_different_types(self):
        """Test ConfigUpdate with different value types"""
        # String
        str_update = ConfigUpdate(value="string")
        assert isinstance(str_update.value, str)
        
        # Integer
        int_update = ConfigUpdate(value=123)
        assert isinstance(int_update.value, int)
        
        # Float
        float_update = ConfigUpdate(value=1.23)
        assert isinstance(float_update.value, float)
        
        # Boolean
        bool_update = ConfigUpdate(value=True)
        assert isinstance(bool_update.value, bool)


class TestDefaultConfigs:
    """Test DEFAULT_CONFIGS constant"""

    def test_default_configs_exist(self):
        """Test that DEFAULT_CONFIGS is defined and not empty"""
        assert DEFAULT_CONFIGS is not None
        assert isinstance(DEFAULT_CONFIGS, list)
        assert len(DEFAULT_CONFIGS) > 0

    def test_default_configs_structure(self):
        """Test DEFAULT_CONFIGS structure"""
        required_keys = {"key", "value", "value_type"}
        
        for config_data in DEFAULT_CONFIGS:
            assert isinstance(config_data, dict)
            # Check required keys are present
            for key in required_keys:
                assert key in config_data, f"Missing required key '{key}' in config: {config_data}"

    def test_default_configs_valid(self):
        """Test that all DEFAULT_CONFIGS are valid Configuration objects"""
        for config_data in DEFAULT_CONFIGS:
            # Should not raise validation error
            config = Configuration(**config_data)
            
            # Verify basic structure
            assert config.key is not None
            assert config.value is not None
            assert config.value_type is not None

    def test_default_configs_messaging_category(self):
        """Test messaging category configs in DEFAULT_CONFIGS"""
        messaging_configs = [
            config for config in DEFAULT_CONFIGS 
            if config.get("category") == "messaging"
        ]
        
        assert len(messaging_configs) > 0
        
        # Check for expected messaging configs
        messaging_keys = [config["key"] for config in messaging_configs]
        expected_keys = [
            "min_message_delay",
            "max_message_delay", 
            "min_cycle_delay_hours",
            "max_cycle_delay_hours"
        ]
        
        for expected_key in expected_keys:
            assert expected_key in messaging_keys

    def test_default_configs_system_category(self):
        """Test system category configs in DEFAULT_CONFIGS"""
        system_configs = [
            config for config in DEFAULT_CONFIGS 
            if config.get("category") == "system"
        ]
        
        assert len(system_configs) > 0
        
        # Check for auto_cleanup_blacklist config
        system_keys = [config["key"] for config in system_configs]
        assert "auto_cleanup_blacklist" in system_keys

    def test_default_configs_value_types(self):
        """Test value types in DEFAULT_CONFIGS"""
        for config_data in DEFAULT_CONFIGS:
            value_type = config_data["value_type"]
            value = config_data["value"]
            
            # Verify value matches its declared type
            if value_type == "int":
                assert isinstance(value, int)
            elif value_type == "float":
                assert isinstance(value, (int, float))
            elif value_type == "bool":
                assert isinstance(value, bool)
            elif value_type == "str":
                assert isinstance(value, str)

    def test_default_configs_descriptions(self):
        """Test that DEFAULT_CONFIGS have descriptions"""
        for config_data in DEFAULT_CONFIGS:
            assert "description" in config_data
            assert config_data["description"] is not None
            assert len(config_data["description"]) > 0

    def test_specific_default_config_values(self):
        """Test specific values in DEFAULT_CONFIGS"""
        config_dict = {config["key"]: config["value"] for config in DEFAULT_CONFIGS}
        
        # Check message delay values
        assert config_dict["min_message_delay"] == 5
        assert config_dict["max_message_delay"] == 10
        assert config_dict["min_message_delay"] < config_dict["max_message_delay"]
        
        # Check cycle delay values
        assert config_dict["min_cycle_delay_hours"] == 1.1
        assert config_dict["max_cycle_delay_hours"] == 1.3
        assert config_dict["min_cycle_delay_hours"] < config_dict["max_cycle_delay_hours"]
        
        # Check boolean config
        assert config_dict["auto_cleanup_blacklist"] is True

    def test_default_configs_uniqueness(self):
        """Test that all config keys in DEFAULT_CONFIGS are unique"""
        keys = [config["key"] for config in DEFAULT_CONFIGS]
        unique_keys = set(keys)
        
        assert len(keys) == len(unique_keys), "Duplicate keys found in DEFAULT_CONFIGS"

    def test_default_configs_categories_valid(self):
        """Test that all categories in DEFAULT_CONFIGS are valid"""
        valid_categories = {"general", "messaging", "system", "security"}
        
        for config_data in DEFAULT_CONFIGS:
            category = config_data.get("category", "general")
            assert category in valid_categories, f"Invalid category: {category}"


class TestConfigurationModelIntegration:
    """Test integration between Configuration models"""

    def test_configuration_update_scenario(self):
        """Test updating configuration with ConfigUpdate"""
        # Original configuration
        config = Configuration(
            key="update_test",
            value="original_value",
            value_type="str"
        )
        
        # Update data
        update_data = ConfigUpdate(value="updated_value")
        
        # Apply update (simulated)
        config.value = update_data.value
        config.update_timestamp()
        
        assert config.value == "updated_value"

    def test_configuration_type_conversion(self):
        """Test type conversion scenarios"""
        # Create config with string value but int type
        config = Configuration(
            key="type_test",
            value="42",
            value_type="int"
        )
        
        # get_typed_value should convert to int
        typed_value = config.get_typed_value()
        assert typed_value == 42
        assert isinstance(typed_value, int)

    def test_default_config_instantiation(self):
        """Test creating Configuration objects from DEFAULT_CONFIGS"""
        created_configs = []
        
        for config_data in DEFAULT_CONFIGS:
            config = Configuration(**config_data)
            created_configs.append(config)
        
        assert len(created_configs) == len(DEFAULT_CONFIGS)
        
        # Test that get_typed_value works for all
        for config in created_configs:
            typed_value = config.get_typed_value()
            assert typed_value is not None