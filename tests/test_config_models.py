"""
Tests for Configuration Models
"""

import pytest
from src.models.config import Configuration


class TestConfiguration:
    """Test Configuration model"""

    def test_configuration_creation(self):
        """Test configuration creation"""
        config = Configuration(
            key="test_key",
            value="test_value",
            value_type="str",
            description="Test configuration",
            category="test",
            is_editable=True
        )
        
        assert config.key == "test_key"
        assert config.value == "test_value"
        assert config.value_type == "str"
        assert config.description == "Test configuration"
        assert config.category == "test"
        assert config.is_editable is True
        assert config.id is not None
        assert config.created_at is not None
        assert config.updated_at is not None

    def test_configuration_defaults(self):
        """Test configuration with defaults"""
        config = Configuration(
            key="test_key",
            value="test_value",
            value_type="str"
        )
        
        assert config.category == "general"
        assert config.is_editable is True
        assert config.description is None

    def test_get_typed_value_string(self):
        """Test get_typed_value for string type"""
        config = Configuration(
            key="test_key",
            value="test_value",
            value_type="str"
        )
        
        result = config.get_typed_value()
        assert result == "test_value"
        assert isinstance(result, str)

    def test_get_typed_value_int(self):
        """Test get_typed_value for int type"""
        config = Configuration(
            key="test_key",
            value="42",
            value_type="int"
        )
        
        result = config.get_typed_value()
        assert result == 42
        assert isinstance(result, int)

    def test_get_typed_value_float(self):
        """Test get_typed_value for float type"""
        config = Configuration(
            key="test_key",
            value="3.14",
            value_type="float"
        )
        
        result = config.get_typed_value()
        assert result == 3.14
        assert isinstance(result, float)

    def test_get_typed_value_bool_true_variants(self):
        """Test get_typed_value for bool type - true variants"""
        true_values = ["true", "True", "TRUE", "1", "yes", "Yes", "YES"]
        
        for value in true_values:
            config = Configuration(
                key="test_key",
                value=value,
                value_type="bool"
            )
            
            result = config.get_typed_value()
            assert result is True
            assert isinstance(result, bool)

    def test_get_typed_value_bool_false_variants(self):
        """Test get_typed_value for bool type - false variants"""
        false_values = ["false", "False", "FALSE", "0", "no", "No", "NO", ""]
        
        for value in false_values:
            config = Configuration(
                key="test_key",
                value=value,
                value_type="bool"
            )
            
            result = config.get_typed_value()
            assert result is False
            assert isinstance(result, bool)

    def test_get_typed_value_unknown_type(self):
        """Test get_typed_value for unknown type defaults to string"""
        config = Configuration(
            key="test_key",
            value="some_value",
            value_type="unknown_type"
        )
        
        result = config.get_typed_value()
        assert result == "some_value"
        assert isinstance(result, str)

    def test_configuration_with_numeric_values(self):
        """Test configuration with numeric values stored as numbers"""
        # Test with actual int value
        config_int = Configuration(
            key="int_key",
            value=123,
            value_type="int"
        )
        assert config_int.value == 123
        
        # Test with actual float value  
        config_float = Configuration(
            key="float_key",
            value=12.34,
            value_type="float"
        )
        assert config_float.value == 12.34
        
        # Test with actual bool value
        config_bool = Configuration(
            key="bool_key",
            value=True,
            value_type="bool"
        )
        assert config_bool.value is True

    def test_configuration_validation_required_fields(self):
        """Test configuration validation for required fields"""
        # Missing key should raise validation error
        with pytest.raises(ValueError):
            Configuration(
                value="test_value",
                value_type="str"
            )
        
        # Missing value should raise validation error
        with pytest.raises(ValueError):
            Configuration(
                key="test_key",
                value_type="str"
            )
        
        # Missing value_type should raise validation error
        with pytest.raises(ValueError):
            Configuration(
                key="test_key",
                value="test_value"
            )