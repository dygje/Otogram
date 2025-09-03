"""
Application Constants
Contains all magic numbers and constant values used throughout the application
"""

# Default Configuration Values
DEFAULT_MIN_MESSAGE_DELAY = 5
DEFAULT_MAX_MESSAGE_DELAY = 10
DEFAULT_MAX_GROUPS_PER_CYCLE = 50
DEFAULT_MIN_CYCLE_DELAY_HOURS = 1.0
DEFAULT_MAX_CYCLE_DELAY_HOURS = 2.0

# Test Values
TEST_API_ID = 12345678
TEST_VALUE_INITIAL = 123
TEST_VALUE_UPDATED = 456

# Display Limits
PREVIEW_MESSAGE_LENGTH = 30
MAX_RECENT_ITEMS_DISPLAY = 3

# Time Constants
SECONDS_PER_HOUR = 3600
SLEEP_CHUNK_SIZE = 60  # seconds
ERROR_RETRY_DELAY = 300  # 5 minutes

# Percentage Calculation
PERCENTAGE_MULTIPLIER = 100

# Database Connection Test Values
DB_PING_OK_VALUE = 1.0

# Sleep Interval for Broadcasting Loop
BROADCASTING_ERROR_SLEEP_SECONDS = 300