"""
Comprehensive tests for Models
"""

import pytest
from datetime import datetime, timedelta
from src.models.config import Configuration, ConfigUpdate
from src.models.message import Message, MessageCreate, MessageUpdate
from src.models.group import Group, GroupCreate, GroupBulkCreate
from src.models.log import Log, LogCreate, LogType, LogLevel


class TestConfigurationModel:
    """Test Configuration model functionality"""

    def test_get_typed_value_int(self):
        """Test get_typed_value for integer"""
        config = Configuration(
            key="test_int",
            value="123",
            value_type="int",
            description="Test integer"
        )
        assert config.get_typed_value() == 123
        assert isinstance(config.get_typed_value(), int)

    def test_get_typed_value_float(self):
        """Test get_typed_value for float"""
        config = Configuration(
            key="test_float",
            value="123.45",
            value_type="float",
            description="Test float"
        )
        assert config.get_typed_value() == 123.45
        assert isinstance(config.get_typed_value(), float)

    def test_get_typed_value_bool_true(self):
        """Test get_typed_value for boolean true"""
        config = Configuration(
            key="test_bool",
            value="true",
            value_type="bool",
            description="Test boolean"
        )
        assert config.get_typed_value() is True

    def test_get_typed_value_bool_false(self):
        """Test get_typed_value for boolean false"""
        config = Configuration(
            key="test_bool",
            value="false",
            value_type="bool",
            description="Test boolean"
        )
        assert config.get_typed_value() is False

    def test_get_typed_value_bool_numeric(self):
        """Test get_typed_value for boolean numeric values"""
        config_true = Configuration(
            key="test_bool",
            value="1",
            value_type="bool",
            description="Test boolean"
        )
        assert config_true.get_typed_value() is True

        config_false = Configuration(
            key="test_bool",
            value="0",
            value_type="bool",
            description="Test boolean"
        )
        assert config_false.get_typed_value() is False

    def test_get_typed_value_string(self):
        """Test get_typed_value for string"""
        config = Configuration(
            key="test_string",
            value="hello world",
            value_type="str",
            description="Test string"
        )
        assert config.get_typed_value() == "hello world"
        assert isinstance(config.get_typed_value(), str)

    def test_get_typed_value_unknown_type(self):
        """Test get_typed_value for unknown type defaults to string"""
        config = Configuration(
            key="test_unknown",
            value="some value",
            value_type="unknown",
            description="Test unknown"
        )
        assert config.get_typed_value() == "some value"


class TestMessageModel:
    """Test Message model functionality"""

    def test_message_creation_with_defaults(self):
        """Test message creation with default values"""
        message = Message(content="Test message")
        
        assert message.content == "Test message"
        assert message.is_active is True
        assert message.usage_count == 0
        assert message.id is not None
        assert message.created_at is not None
        assert message.updated_at is not None

    def test_message_creation_with_custom_values(self):
        """Test message creation with custom values"""
        message = Message(
            content="Custom message",
            is_active=False,
            usage_count=5
        )
        
        assert message.content == "Custom message"
        assert message.is_active is False
        assert message.usage_count == 5

    def test_message_update_partial(self):
        """Test MessageUpdate with partial data"""
        update = MessageUpdate(content="Updated content")
        
        assert update.content == "Updated content"
        assert update.is_active is None

    def test_message_update_full(self):
        """Test MessageUpdate with full data"""
        update = MessageUpdate(
            content="Updated content",
            is_active=False
        )
        
        assert update.content == "Updated content"
        assert update.is_active is False

    def test_message_create_validation(self):
        """Test MessageCreate validation"""
        message_create = MessageCreate(content="Valid message")
        assert message_create.content == "Valid message"

        # Test empty content validation
        with pytest.raises(ValueError):
            MessageCreate(content="")


class TestGroupModel:
    """Test Group model functionality"""

    def test_group_creation_minimal(self):
        """Test group creation with minimal data"""
        group = Group()
        
        assert group.group_id is None
        assert group.group_username is None
        assert group.group_link is None
        assert group.group_title is None
        assert group.is_active is True
        assert group.message_count == 0

    def test_group_creation_with_id(self):
        """Test group creation with ID"""
        group = Group(group_id="-1001234567890")
        
        assert group.group_id == "-1001234567890"
        assert group.is_active is True

    def test_group_creation_with_username(self):
        """Test group creation with username"""
        group = Group(group_username="@testgroup")
        
        assert group.group_username == "@testgroup"

    def test_group_creation_with_link(self):
        """Test group creation with link"""
        group = Group(group_link="https://t.me/testgroup")
        
        assert group.group_link == "https://t.me/testgroup"

    def test_group_bulk_create_parsing(self):
        """Test GroupBulkCreate identifier parsing"""
        identifiers_text = """
        @group1
        -1001234567890
        https://t.me/group2
        @group3
        """
        
        bulk_create = GroupBulkCreate(identifiers=identifiers_text)
        identifiers_list = bulk_create.get_identifiers_list()
        
        assert "@group1" in identifiers_list
        assert "-1001234567890" in identifiers_list
        assert "https://t.me/group2" in identifiers_list
        assert "@group3" in identifiers_list
        assert len(identifiers_list) == 4

    def test_group_bulk_create_empty(self):
        """Test GroupBulkCreate with empty input"""
        bulk_create = GroupBulkCreate(identifiers="   \n  \n  ")
        identifiers_list = bulk_create.get_identifiers_list()
        
        assert identifiers_list == []

    def test_group_bulk_create_single(self):
        """Test GroupBulkCreate with single identifier"""
        bulk_create = GroupBulkCreate(identifiers="@singlegroup")
        identifiers_list = bulk_create.get_identifiers_list()
        
        assert identifiers_list == ["@singlegroup"]


class TestLogModel:
    """Test Log model functionality"""

    def test_log_creation_minimal(self):
        """Test log creation with minimal data"""
        log = Log(
            message="Test log message",
            log_type=LogType.SYSTEM,
            level=LogLevel.INFO
        )
        
        assert log.message == "Test log message"
        assert log.log_type == LogType.SYSTEM
        assert log.level == LogLevel.INFO
        assert log.details is None
        assert log.group_id is None
        assert log.user_id is None

    def test_log_creation_full(self):
        """Test log creation with full data"""
        details = {"error_code": 500, "endpoint": "/api/test"}
        log = Log(
            message="Error occurred",
            log_type=LogType.ERROR,
            level=LogLevel.ERROR,
            details=details,
            group_id="-1001234567890",
            user_id="123456789"
        )
        
        assert log.message == "Error occurred"
        assert log.log_type == LogType.ERROR
        assert log.level == LogLevel.ERROR
        assert log.details == details
        assert log.group_id == "-1001234567890"
        assert log.user_id == "123456789"

    def test_log_create_model(self):
        """Test LogCreate model"""
        log_create = LogCreate(
            message="New log entry",
            log_type=LogType.BROADCAST,
            level=LogLevel.WARNING
        )
        
        assert log_create.message == "New log entry"
        assert log_create.log_type == LogType.BROADCAST
        assert log_create.level == LogLevel.WARNING

    def test_log_types_enum(self):
        """Test LogType enum values"""
        assert LogType.SYSTEM == "system"
        assert LogType.BROADCAST == "broadcast"
        assert LogType.USER_ACTION == "user_action"
        assert LogType.ERROR == "error"
        assert LogType.DEBUG == "debug"

    def test_log_levels_enum(self):
        """Test LogLevel enum values"""
        assert LogLevel.DEBUG == "debug"
        assert LogLevel.INFO == "info"
        assert LogLevel.WARNING == "warning"
        assert LogLevel.ERROR == "error"
        assert LogLevel.CRITICAL == "critical"


class TestModelIntegration:
    """Test model integration scenarios"""

    def test_configuration_with_real_scenarios(self):
        """Test configuration model with real-world scenarios"""
        # Test messaging configuration
        delay_config = Configuration(
            key="message_delay",
            value="5",
            value_type="int",
            description="Delay between messages in seconds",
            category="messaging"
        )
        
        assert delay_config.get_typed_value() == 5
        assert delay_config.category == "messaging"

        # Test boolean configuration
        enabled_config = Configuration(
            key="auto_cleanup",
            value="true",
            value_type="bool",
            description="Enable automatic cleanup",
            category="system"
        )
        
        assert enabled_config.get_typed_value() is True

    def test_message_lifecycle(self):
        """Test message model lifecycle"""
        # Create message
        message = Message(content="Lifecycle test message")
        initial_usage = message.usage_count
        
        # Simulate usage increment
        message.usage_count += 1
        assert message.usage_count == initial_usage + 1
        
        # Simulate deactivation
        message.is_active = False
        assert message.is_active is False

    def test_group_management_scenarios(self):
        """Test group model in management scenarios"""
        # Create group with different identifiers
        id_group = Group(group_id="-1001234567890")
        username_group = Group(group_username="@testgroup")
        link_group = Group(group_link="https://t.me/testgroup")
        
        assert id_group.group_id is not None
        assert username_group.group_username is not None
        assert link_group.group_link is not None
        
        # Test message count increment
        id_group.message_count += 1
        assert id_group.message_count == 1

    def test_log_categorization(self):
        """Test log model categorization"""
        # System log
        system_log = Log(
            message="System started",
            log_type=LogType.SYSTEM,
            level=LogLevel.INFO
        )
        
        # Error log with details
        error_log = Log(
            message="Broadcast failed",
            log_type=LogType.ERROR,
            level=LogLevel.ERROR,
            details={"group_id": "-1001234567890", "error": "Permission denied"},
            group_id="-1001234567890"
        )
        
        # User action log
        user_log = Log(
            message="User added new message",
            log_type=LogType.USER_ACTION,
            level=LogLevel.INFO,
            user_id="123456789"
        )
        
        assert system_log.log_type == LogType.SYSTEM
        assert error_log.details["error"] == "Permission denied"
        assert user_log.user_id == "123456789"