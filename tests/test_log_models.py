"""
Tests for Log Models
"""

import pytest
from src.models.log import Log, LogCreate, LogType, LogLevel


class TestLogType:
    """Test LogType enum"""

    def test_log_type_values(self):
        """Test LogType enum values"""
        assert LogType.SYSTEM == "system"
        assert LogType.MESSAGE_SENT == "message_sent"
        assert LogType.MESSAGE_FAILED == "message_failed"
        assert LogType.BLACKLIST_ADDED == "blacklist_added"
        assert LogType.CYCLE_STARTED == "cycle_started"
        assert LogType.CYCLE_COMPLETED == "cycle_completed"
        assert LogType.USER_ACTION == "user_action"


class TestLogLevel:
    """Test LogLevel enum"""

    def test_log_level_values(self):
        """Test LogLevel enum values"""
        assert LogLevel.INFO == "info"
        assert LogLevel.WARNING == "warning"
        assert LogLevel.ERROR == "error"


class TestLog:
    """Test Log model"""

    def test_log_creation_minimal(self):
        """Test creating log with minimal fields"""
        log = Log(
            log_type=LogType.SYSTEM,
            message="System started",
        )

        assert log.log_type == LogType.SYSTEM
        assert log.level == LogLevel.INFO  # Default value
        assert log.message == "System started"
        assert log.details is None
        assert log.group_id is None
        assert log.user_id is None

    def test_log_creation_full(self):
        """Test creating log with all fields"""
        details = {"status": "success", "duration": 1.5}
        
        log = Log(
            log_type=LogType.MESSAGE_SENT,
            level=LogLevel.INFO,
            message="Message sent successfully",
            details=details,
            group_id="-1001234567890",
            user_id="123456789",
        )

        assert log.log_type == LogType.MESSAGE_SENT
        assert log.level == LogLevel.INFO
        assert log.message == "Message sent successfully"
        assert log.details == details
        assert log.group_id == "-1001234567890"
        assert log.user_id == "123456789"

    def test_log_different_levels(self):
        """Test creating logs with different levels"""
        # INFO level
        info_log = Log(
            log_type=LogType.SYSTEM,
            level=LogLevel.INFO,
            message="Information message",
        )
        assert info_log.level == LogLevel.INFO

        # WARNING level
        warning_log = Log(
            log_type=LogType.SYSTEM,
            level=LogLevel.WARNING,
            message="Warning message",
        )
        assert warning_log.level == LogLevel.WARNING

        # ERROR level
        error_log = Log(
            log_type=LogType.MESSAGE_FAILED,
            level=LogLevel.ERROR,
            message="Error message",
        )
        assert error_log.level == LogLevel.ERROR

    def test_log_different_types(self):
        """Test creating logs with different types"""
        # System log
        system_log = Log(
            log_type=LogType.SYSTEM,
            message="System message",
        )
        assert system_log.log_type == LogType.SYSTEM

        # Message sent log
        sent_log = Log(
            log_type=LogType.MESSAGE_SENT,
            message="Message sent",
        )
        assert sent_log.log_type == LogType.MESSAGE_SENT

        # Message failed log
        failed_log = Log(
            log_type=LogType.MESSAGE_FAILED,
            message="Message failed",
        )
        assert failed_log.log_type == LogType.MESSAGE_FAILED

        # Blacklist added log
        blacklist_log = Log(
            log_type=LogType.BLACKLIST_ADDED,
            message="Group blacklisted",
        )
        assert blacklist_log.log_type == LogType.BLACKLIST_ADDED

        # Cycle started log
        cycle_start_log = Log(
            log_type=LogType.CYCLE_STARTED,
            message="Broadcast cycle started",
        )
        assert cycle_start_log.log_type == LogType.CYCLE_STARTED

        # Cycle completed log
        cycle_complete_log = Log(
            log_type=LogType.CYCLE_COMPLETED,
            message="Broadcast cycle completed",
        )
        assert cycle_complete_log.log_type == LogType.CYCLE_COMPLETED

        # User action log
        user_action_log = Log(
            log_type=LogType.USER_ACTION,
            message="User performed action",
        )
        assert user_action_log.log_type == LogType.USER_ACTION

    def test_log_with_complex_details(self):
        """Test log with complex details dictionary"""
        details = {
            "group_count": 100,
            "messages_sent": 85,
            "errors": [
                {"group_id": "-1001111111", "error": "ChatForbidden"},
                {"group_id": "-1002222222", "error": "FloodWait"},
            ],
            "duration": 120.5,
            "success_rate": 0.85,
        }
        
        log = Log(
            log_type=LogType.CYCLE_COMPLETED,
            level=LogLevel.INFO,
            message="Broadcast cycle completed",
            details=details,
        )

        assert log.details == details
        assert log.details["group_count"] == 100
        assert log.details["messages_sent"] == 85
        assert len(log.details["errors"]) == 2
        assert log.details["duration"] == 120.5
        assert log.details["success_rate"] == 0.85

    def test_log_with_group_context(self):
        """Test log with group context"""
        log = Log(
            log_type=LogType.MESSAGE_SENT,
            message="Message sent to group",
            group_id="-1001234567890",
        )

        assert log.group_id == "-1001234567890"

    def test_log_with_user_context(self):
        """Test log with user context"""
        log = Log(
            log_type=LogType.USER_ACTION,
            message="User added new message",
            user_id="123456789",
        )

        assert log.user_id == "123456789"

    def test_log_with_both_contexts(self):
        """Test log with both group and user context"""
        log = Log(
            log_type=LogType.MESSAGE_FAILED,
            level=LogLevel.ERROR,
            message="Failed to send message to group",
            group_id="-1001234567890",
            user_id="123456789",
        )

        assert log.group_id == "-1001234567890"
        assert log.user_id == "123456789"


class TestLogCreate:
    """Test LogCreate model"""

    def test_log_create_minimal(self):
        """Test LogCreate with minimal fields"""
        data = LogCreate(
            log_type=LogType.SYSTEM,
            message="System message",
        )

        assert data.log_type == LogType.SYSTEM
        assert data.level == LogLevel.INFO  # Default value
        assert data.message == "System message"
        assert data.details is None
        assert data.group_id is None
        assert data.user_id is None

    def test_log_create_full(self):
        """Test LogCreate with all fields"""
        details = {"status": "error", "code": 500}
        
        data = LogCreate(
            log_type=LogType.MESSAGE_FAILED,
            level=LogLevel.ERROR,
            message="Message sending failed",
            details=details,
            group_id="-1001234567890",
            user_id="123456789",
        )

        assert data.log_type == LogType.MESSAGE_FAILED
        assert data.level == LogLevel.ERROR
        assert data.message == "Message sending failed"
        assert data.details == details
        assert data.group_id == "-1001234567890"
        assert data.user_id == "123456789"

    def test_log_create_validation(self):
        """Test LogCreate field validation"""
        # Test that message is required
        with pytest.raises(ValueError):
            LogCreate(log_type=LogType.SYSTEM)

        # Test that log_type is required
        with pytest.raises(ValueError):
            LogCreate(message="Test message")

    def test_log_create_default_level(self):
        """Test that LogCreate defaults to INFO level"""
        data = LogCreate(
            log_type=LogType.USER_ACTION,
            message="User action performed",
        )

        assert data.level == LogLevel.INFO

    def test_log_create_different_levels(self):
        """Test LogCreate with different log levels"""
        # Warning level
        warning_data = LogCreate(
            log_type=LogType.SYSTEM,
            level=LogLevel.WARNING,
            message="Warning message",
        )
        assert warning_data.level == LogLevel.WARNING

        # Error level
        error_data = LogCreate(
            log_type=LogType.MESSAGE_FAILED,
            level=LogLevel.ERROR,
            message="Error message",
        )
        assert error_data.level == LogLevel.ERROR

    def test_log_create_with_empty_details(self):
        """Test LogCreate with empty details dictionary"""
        data = LogCreate(
            log_type=LogType.SYSTEM,
            message="System message",
            details={},
        )

        assert data.details == {}

    def test_log_create_with_none_details(self):
        """Test LogCreate with None details"""
        data = LogCreate(
            log_type=LogType.SYSTEM,
            message="System message",
            details=None,
        )

        assert data.details is None