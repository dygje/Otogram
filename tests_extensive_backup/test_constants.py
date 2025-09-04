"""
Tests for Application Constants
"""

from src.core.constants import (
    DEFAULT_MIN_MESSAGE_DELAY,
    DEFAULT_MAX_MESSAGE_DELAY,
    DEFAULT_MAX_GROUPS_PER_CYCLE,
    DEFAULT_MIN_CYCLE_DELAY_HOURS,
    DEFAULT_MAX_CYCLE_DELAY_HOURS,
    TEST_API_ID,
    TEST_VALUE_INITIAL,
    TEST_VALUE_UPDATED,
    PREVIEW_MESSAGE_LENGTH,
    PREVIEW_MESSAGE_LENGTH_SHORT,
    PREVIEW_MESSAGE_LENGTH_LONG,
    MAX_RECENT_ITEMS_DISPLAY,
    MAX_GROUPS_DISPLAY,
    MAX_MESSAGES_DISPLAY,
    MAX_BULK_SUCCESS_DISPLAY,
    TELEGRAM_MESSAGE_MAX_LENGTH,
    SECONDS_PER_HOUR,
    SLEEP_CHUNK_SIZE,
    ERROR_RETRY_DELAY,
    DEFAULT_SLOWMODE_DURATION,
    DEFAULT_FLOOD_DURATION,
    PERCENTAGE_MULTIPLIER,
    DB_PING_OK_VALUE,
    BROADCASTING_ERROR_SLEEP_SECONDS,
    TEST_CYCLE_DELAY_MIN,
    TEST_CYCLE_DELAY_MAX,
)


class TestDefaultConfigurationValues:
    """Test default configuration values"""

    def test_message_delay_values(self):
        """Test message delay constants"""
        assert DEFAULT_MIN_MESSAGE_DELAY == 5
        assert DEFAULT_MAX_MESSAGE_DELAY == 10
        assert DEFAULT_MIN_MESSAGE_DELAY < DEFAULT_MAX_MESSAGE_DELAY

    def test_cycle_values(self):
        """Test cycle-related constants"""
        assert DEFAULT_MAX_GROUPS_PER_CYCLE == 50
        assert DEFAULT_MIN_CYCLE_DELAY_HOURS == 1.0
        assert DEFAULT_MAX_CYCLE_DELAY_HOURS == 2.0
        assert DEFAULT_MIN_CYCLE_DELAY_HOURS < DEFAULT_MAX_CYCLE_DELAY_HOURS


class TestTestValues:
    """Test constants used for testing"""

    def test_test_api_values(self):
        """Test API-related test values"""
        assert TEST_API_ID == 12345678
        assert isinstance(TEST_API_ID, int)

    def test_test_configuration_values(self):
        """Test configuration test values"""
        assert TEST_VALUE_INITIAL == 123
        assert TEST_VALUE_UPDATED == 456
        assert TEST_VALUE_INITIAL != TEST_VALUE_UPDATED

    def test_test_cycle_delay_values(self):
        """Test cycle delay test values"""
        assert TEST_CYCLE_DELAY_MIN == 1.0
        assert TEST_CYCLE_DELAY_MAX == 2.0
        assert TEST_CYCLE_DELAY_MIN < TEST_CYCLE_DELAY_MAX


class TestDisplayLimits:
    """Test display-related constants"""

    def test_preview_message_lengths(self):
        """Test preview message length constants"""
        assert PREVIEW_MESSAGE_LENGTH == 30
        assert PREVIEW_MESSAGE_LENGTH_SHORT == 100
        assert PREVIEW_MESSAGE_LENGTH_LONG == 200
        
        # Test logical ordering
        assert PREVIEW_MESSAGE_LENGTH < PREVIEW_MESSAGE_LENGTH_SHORT
        assert PREVIEW_MESSAGE_LENGTH_SHORT < PREVIEW_MESSAGE_LENGTH_LONG

    def test_max_display_values(self):
        """Test maximum display values"""
        assert MAX_RECENT_ITEMS_DISPLAY == 3
        assert MAX_GROUPS_DISPLAY == 10
        assert MAX_MESSAGES_DISPLAY == 10
        assert MAX_BULK_SUCCESS_DISPLAY == 5
        
        # All should be positive integers
        assert all(isinstance(val, int) and val > 0 for val in [
            MAX_RECENT_ITEMS_DISPLAY,
            MAX_GROUPS_DISPLAY,
            MAX_MESSAGES_DISPLAY,
            MAX_BULK_SUCCESS_DISPLAY
        ])


class TestMessageLimits:
    """Test message-related constants"""

    def test_telegram_message_max_length(self):
        """Test Telegram message maximum length"""
        assert TELEGRAM_MESSAGE_MAX_LENGTH == 4096
        assert isinstance(TELEGRAM_MESSAGE_MAX_LENGTH, int)
        assert TELEGRAM_MESSAGE_MAX_LENGTH > 0


class TestTimeConstants:
    """Test time-related constants"""

    def test_seconds_per_hour(self):
        """Test seconds per hour constant"""
        assert SECONDS_PER_HOUR == 3600
        assert SECONDS_PER_HOUR == 60 * 60  # 60 minutes * 60 seconds

    def test_sleep_and_delay_values(self):
        """Test sleep and delay constants"""
        assert SLEEP_CHUNK_SIZE == 60
        assert ERROR_RETRY_DELAY == 300
        assert BROADCASTING_ERROR_SLEEP_SECONDS == 300
        
        # All should be positive integers
        assert all(isinstance(val, int) and val > 0 for val in [
            SLEEP_CHUNK_SIZE,
            ERROR_RETRY_DELAY,
            BROADCASTING_ERROR_SLEEP_SECONDS
        ])

    def test_default_duration_values(self):
        """Test default duration constants"""
        assert DEFAULT_SLOWMODE_DURATION == 60  # 1 minute
        assert DEFAULT_FLOOD_DURATION == 3600   # 1 hour
        
        assert DEFAULT_SLOWMODE_DURATION < DEFAULT_FLOOD_DURATION
        assert isinstance(DEFAULT_SLOWMODE_DURATION, int)
        assert isinstance(DEFAULT_FLOOD_DURATION, int)


class TestMiscConstants:
    """Test miscellaneous constants"""

    def test_percentage_multiplier(self):
        """Test percentage multiplier constant"""
        assert PERCENTAGE_MULTIPLIER == 100
        assert isinstance(PERCENTAGE_MULTIPLIER, int)

    def test_db_ping_ok_value(self):
        """Test database ping OK value"""
        assert DB_PING_OK_VALUE == 1.0
        assert isinstance(DB_PING_OK_VALUE, float)


class TestConstantTypes:
    """Test that constants have expected types"""

    def test_integer_constants(self):
        """Test that integer constants are indeed integers"""
        integer_constants = [
            DEFAULT_MIN_MESSAGE_DELAY,
            DEFAULT_MAX_MESSAGE_DELAY,
            DEFAULT_MAX_GROUPS_PER_CYCLE,
            TEST_API_ID,
            TEST_VALUE_INITIAL,
            TEST_VALUE_UPDATED,
            PREVIEW_MESSAGE_LENGTH,
            PREVIEW_MESSAGE_LENGTH_SHORT,
            PREVIEW_MESSAGE_LENGTH_LONG,
            MAX_RECENT_ITEMS_DISPLAY,
            MAX_GROUPS_DISPLAY,
            MAX_MESSAGES_DISPLAY,
            MAX_BULK_SUCCESS_DISPLAY,
            TELEGRAM_MESSAGE_MAX_LENGTH,
            SECONDS_PER_HOUR,
            SLEEP_CHUNK_SIZE,
            ERROR_RETRY_DELAY,
            DEFAULT_SLOWMODE_DURATION,
            DEFAULT_FLOOD_DURATION,
            PERCENTAGE_MULTIPLIER,
            BROADCASTING_ERROR_SLEEP_SECONDS,
        ]
        
        for constant in integer_constants:
            assert isinstance(constant, int), f"Expected int, got {type(constant)} for {constant}"

    def test_float_constants(self):
        """Test that float constants are indeed floats"""
        float_constants = [
            DEFAULT_MIN_CYCLE_DELAY_HOURS,
            DEFAULT_MAX_CYCLE_DELAY_HOURS,
            DB_PING_OK_VALUE,
            TEST_CYCLE_DELAY_MIN,
            TEST_CYCLE_DELAY_MAX,
        ]
        
        for constant in float_constants:
            assert isinstance(constant, float), f"Expected float, got {type(constant)} for {constant}"


class TestConstantValues:
    """Test specific constant values and relationships"""

    def test_positive_values(self):
        """Test that all numeric constants are positive"""
        all_numeric_constants = [
            DEFAULT_MIN_MESSAGE_DELAY,
            DEFAULT_MAX_MESSAGE_DELAY,
            DEFAULT_MAX_GROUPS_PER_CYCLE,
            DEFAULT_MIN_CYCLE_DELAY_HOURS,
            DEFAULT_MAX_CYCLE_DELAY_HOURS,
            TEST_API_ID,
            TEST_VALUE_INITIAL,
            TEST_VALUE_UPDATED,
            PREVIEW_MESSAGE_LENGTH,
            PREVIEW_MESSAGE_LENGTH_SHORT,
            PREVIEW_MESSAGE_LENGTH_LONG,
            MAX_RECENT_ITEMS_DISPLAY,
            MAX_GROUPS_DISPLAY,
            MAX_MESSAGES_DISPLAY,
            MAX_BULK_SUCCESS_DISPLAY,
            TELEGRAM_MESSAGE_MAX_LENGTH,
            SECONDS_PER_HOUR,
            SLEEP_CHUNK_SIZE,
            ERROR_RETRY_DELAY,
            DEFAULT_SLOWMODE_DURATION,
            DEFAULT_FLOOD_DURATION,
            PERCENTAGE_MULTIPLIER,
            DB_PING_OK_VALUE,
            BROADCASTING_ERROR_SLEEP_SECONDS,
            TEST_CYCLE_DELAY_MIN,
            TEST_CYCLE_DELAY_MAX,
        ]
        
        for constant in all_numeric_constants:
            assert constant > 0, f"Expected positive value, got {constant}"

    def test_logical_relationships(self):
        """Test logical relationships between constants"""
        # Message delays
        assert DEFAULT_MIN_MESSAGE_DELAY < DEFAULT_MAX_MESSAGE_DELAY
        
        # Cycle delays
        assert DEFAULT_MIN_CYCLE_DELAY_HOURS < DEFAULT_MAX_CYCLE_DELAY_HOURS
        
        # Test values
        assert TEST_VALUE_INITIAL != TEST_VALUE_UPDATED
        assert TEST_CYCLE_DELAY_MIN < TEST_CYCLE_DELAY_MAX
        
        # Preview lengths
        assert PREVIEW_MESSAGE_LENGTH < PREVIEW_MESSAGE_LENGTH_SHORT < PREVIEW_MESSAGE_LENGTH_LONG
        
        # Duration values
        assert DEFAULT_SLOWMODE_DURATION < DEFAULT_FLOOD_DURATION
        
        # All preview length values should be less than Telegram's max
        assert PREVIEW_MESSAGE_LENGTH < TELEGRAM_MESSAGE_MAX_LENGTH
        assert PREVIEW_MESSAGE_LENGTH_SHORT < TELEGRAM_MESSAGE_MAX_LENGTH
        assert PREVIEW_MESSAGE_LENGTH_LONG < TELEGRAM_MESSAGE_MAX_LENGTH


class TestConstantImmutability:
    """Test that constants are properly defined and accessible"""

    def test_constants_exist(self):
        """Test that all expected constants exist and are accessible"""
        # This test ensures all constants are properly imported and accessible
        constants_to_check = [
            'DEFAULT_MIN_MESSAGE_DELAY',
            'DEFAULT_MAX_MESSAGE_DELAY',
            'DEFAULT_MAX_GROUPS_PER_CYCLE',
            'DEFAULT_MIN_CYCLE_DELAY_HOURS',
            'DEFAULT_MAX_CYCLE_DELAY_HOURS',
            'TEST_API_ID',
            'TEST_VALUE_INITIAL',
            'TEST_VALUE_UPDATED',
            'PREVIEW_MESSAGE_LENGTH',
            'PREVIEW_MESSAGE_LENGTH_SHORT',
            'PREVIEW_MESSAGE_LENGTH_LONG',
            'MAX_RECENT_ITEMS_DISPLAY',
            'MAX_GROUPS_DISPLAY',
            'MAX_MESSAGES_DISPLAY',
            'MAX_BULK_SUCCESS_DISPLAY',
            'TELEGRAM_MESSAGE_MAX_LENGTH',
            'SECONDS_PER_HOUR',
            'SLEEP_CHUNK_SIZE',
            'ERROR_RETRY_DELAY',
            'DEFAULT_SLOWMODE_DURATION',
            'DEFAULT_FLOOD_DURATION',
            'PERCENTAGE_MULTIPLIER',
            'DB_PING_OK_VALUE',
            'BROADCASTING_ERROR_SLEEP_SECONDS',
            'TEST_CYCLE_DELAY_MIN',
            'TEST_CYCLE_DELAY_MAX',
        ]
        
        import src.core.constants as constants_module
        
        for constant_name in constants_to_check:
            assert hasattr(constants_module, constant_name), f"Constant {constant_name} not found"
            constant_value = getattr(constants_module, constant_name)
            assert constant_value is not None, f"Constant {constant_name} is None"