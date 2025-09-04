"""
Tests for Blacklist Models
"""

import pytest
from datetime import datetime, timedelta

from src.models.blacklist import (
    Blacklist,
    BlacklistCreate,
    BlacklistType,
    BlacklistReason,
    determine_blacklist_from_error,
)


class TestBlacklistType:
    """Test BlacklistType enum"""

    def test_blacklist_type_values(self):
        """Test BlacklistType enum values"""
        assert BlacklistType.PERMANENT == "permanent"
        assert BlacklistType.TEMPORARY == "temporary"


class TestBlacklistReason:
    """Test BlacklistReason enum"""

    def test_permanent_reasons(self):
        """Test permanent blacklist reasons"""
        assert BlacklistReason.CHAT_FORBIDDEN == "ChatForbidden"
        assert BlacklistReason.CHAT_ID_INVALID == "ChatIdInvalid"
        assert BlacklistReason.USER_BLOCKED == "UserBlocked"
        assert BlacklistReason.PEER_ID_INVALID == "PeerIdInvalid"
        assert BlacklistReason.CHANNEL_INVALID == "ChannelInvalid"
        assert BlacklistReason.USER_BANNED_IN_CHANNEL == "UserBannedInChannel"
        assert BlacklistReason.CHAT_WRITE_FORBIDDEN == "ChatWriteForbidden"
        assert BlacklistReason.CHAT_RESTRICTED == "ChatRestricted"

    def test_temporary_reasons(self):
        """Test temporary blacklist reasons"""
        assert BlacklistReason.SLOW_MODE_WAIT == "SlowModeWait"
        assert BlacklistReason.FLOOD_WAIT == "FloodWait"

    def test_manual_reason(self):
        """Test manual blacklist reason"""
        assert BlacklistReason.MANUAL == "Manual"


class TestBlacklist:
    """Test Blacklist model"""

    def test_permanent_blacklist_creation(self):
        """Test creating permanent blacklist"""
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.CHAT_FORBIDDEN,
        )

        assert blacklist.group_id == "-1001234567890"
        assert blacklist.blacklist_type == BlacklistType.PERMANENT
        assert blacklist.reason == BlacklistReason.CHAT_FORBIDDEN
        assert blacklist.expires_at is None
        assert blacklist.duration_seconds is None

    def test_temporary_blacklist_creation(self):
        """Test creating temporary blacklist"""
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
            expires_at=expires_at,
            duration_seconds=3600,
        )

        assert blacklist.group_id == "-1001234567890"
        assert blacklist.blacklist_type == BlacklistType.TEMPORARY
        assert blacklist.reason == BlacklistReason.FLOOD_WAIT
        assert blacklist.expires_at == expires_at
        assert blacklist.duration_seconds == 3600

    def test_blacklist_with_identifier(self):
        """Test blacklist with group identifier"""
        blacklist = Blacklist(
            group_id="-1001234567890",
            group_identifier="@testgroup",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.CHAT_FORBIDDEN,
        )

        assert blacklist.group_identifier == "@testgroup"

    def test_blacklist_with_error_message(self):
        """Test blacklist with error message"""
        error_msg = "ChatForbidden: The user is banned from this chat"
        
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.CHAT_FORBIDDEN,
            error_message=error_msg,
        )

        assert blacklist.error_message == error_msg

    def test_is_expired_permanent(self):
        """Test is_expired for permanent blacklist"""
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.CHAT_FORBIDDEN,
        )

        assert blacklist.is_expired is False

    def test_is_expired_temporary_not_expired(self):
        """Test is_expired for temporary blacklist that hasn't expired"""
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
            expires_at=expires_at,
        )

        assert blacklist.is_expired is False

    def test_is_expired_temporary_expired(self):
        """Test is_expired for temporary blacklist that has expired"""
        expires_at = datetime.utcnow() - timedelta(hours=1)
        
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
            expires_at=expires_at,
        )

        assert blacklist.is_expired is True

    def test_is_expired_temporary_no_expiry(self):
        """Test is_expired for temporary blacklist without expiry time"""
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
        )

        assert blacklist.is_expired is True

    def test_time_remaining_permanent(self):
        """Test time_remaining for permanent blacklist"""
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.CHAT_FORBIDDEN,
        )

        assert blacklist.time_remaining is None

    def test_time_remaining_temporary_not_expired(self):
        """Test time_remaining for temporary blacklist"""
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
            expires_at=expires_at,
        )

        remaining = blacklist.time_remaining
        assert remaining is not None
        assert remaining.total_seconds() > 3500  # Should be close to 1 hour

    def test_time_remaining_temporary_expired(self):
        """Test time_remaining for expired temporary blacklist"""
        expires_at = datetime.utcnow() - timedelta(hours=1)
        
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
            expires_at=expires_at,
        )

        assert blacklist.time_remaining is None

    def test_time_remaining_temporary_no_expiry(self):
        """Test time_remaining for temporary blacklist without expiry"""
        blacklist = Blacklist(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
        )

        assert blacklist.time_remaining is None


class TestBlacklistCreate:
    """Test BlacklistCreate model"""

    def test_blacklist_create_minimal(self):
        """Test BlacklistCreate with minimal fields"""
        data = BlacklistCreate(
            group_id="-1001234567890",
            blacklist_type=BlacklistType.PERMANENT,
            reason=BlacklistReason.CHAT_FORBIDDEN,
        )

        assert data.group_id == "-1001234567890"
        assert data.blacklist_type == BlacklistType.PERMANENT
        assert data.reason == BlacklistReason.CHAT_FORBIDDEN
        assert data.group_identifier is None
        assert data.duration_seconds is None
        assert data.error_message is None

    def test_blacklist_create_full(self):
        """Test BlacklistCreate with all fields"""
        data = BlacklistCreate(
            group_id="-1001234567890",
            group_identifier="@testgroup",
            blacklist_type=BlacklistType.TEMPORARY,
            reason=BlacklistReason.FLOOD_WAIT,
            duration_seconds=3600,
            error_message="FloodWait: wait 3600 seconds",
        )

        assert data.group_id == "-1001234567890"
        assert data.group_identifier == "@testgroup"
        assert data.blacklist_type == BlacklistType.TEMPORARY
        assert data.reason == BlacklistReason.FLOOD_WAIT
        assert data.duration_seconds == 3600
        assert data.error_message == "FloodWait: wait 3600 seconds"


class TestDetermineBlacklistFromError:
    """Test determine_blacklist_from_error function"""

    def test_chat_forbidden_error(self):
        """Test ChatForbidden error detection"""
        error_msg = "ChatForbidden: The user is banned from this chat"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.CHAT_FORBIDDEN

    def test_chat_id_invalid_error(self):
        """Test ChatIdInvalid error detection"""
        error_msg = "ChatIdInvalid: Invalid chat ID"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.CHAT_ID_INVALID

    def test_user_blocked_error(self):
        """Test UserBlocked error detection"""
        error_msg = "UserBlocked: User has blocked the bot"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.USER_BLOCKED

    def test_peer_id_invalid_error(self):
        """Test PeerIdInvalid error detection"""
        error_msg = "PeerIdInvalid: The peer ID is invalid"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.PEER_ID_INVALID

    def test_channel_invalid_error(self):
        """Test ChannelInvalid error detection"""
        error_msg = "ChannelInvalid: The channel is invalid"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.CHANNEL_INVALID

    def test_user_banned_in_channel_error(self):
        """Test UserBannedInChannel error detection"""
        error_msg = "UserBannedInChannel: User is banned in this channel"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.USER_BANNED_IN_CHANNEL

    def test_chat_write_forbidden_error(self):
        """Test ChatWriteForbidden error detection"""
        error_msg = "ChatWriteForbidden: You can't write to this chat"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.CHAT_WRITE_FORBIDDEN

    def test_chat_restricted_error(self):
        """Test ChatRestricted error detection"""
        error_msg = "ChatRestricted: The chat is restricted"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.CHAT_RESTRICTED

    def test_slow_mode_wait_error(self):
        """Test SlowModeWait error detection"""
        error_msg = "SlowModeWait: You must wait before sending another message"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.TEMPORARY
        assert reason == BlacklistReason.SLOW_MODE_WAIT

    def test_slow_mode_with_space_error(self):
        """Test 'slow mode' error detection"""
        error_msg = "You must respect the slow mode restrictions"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.TEMPORARY
        assert reason == BlacklistReason.SLOW_MODE_WAIT

    def test_flood_wait_error(self):
        """Test FloodWait error detection"""
        error_msg = "FloodWait: Too many requests, wait 3600 seconds"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.TEMPORARY
        assert reason == BlacklistReason.FLOOD_WAIT

    def test_unknown_error_default(self):
        """Test unknown error defaults to permanent ChatForbidden"""
        error_msg = "SomeUnknownError: This is an unknown error"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.CHAT_FORBIDDEN

    def test_case_insensitive_matching(self):
        """Test that error matching is case-insensitive"""
        error_msg = "CHATFORBIDDEN: THE USER IS BANNED"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.CHAT_FORBIDDEN

    def test_partial_string_matching(self):
        """Test that partial string matching works"""
        error_msg = "The chatforbidden error occurred while processing"
        blacklist_type, reason = determine_blacklist_from_error(error_msg)
        
        assert blacklist_type == BlacklistType.PERMANENT
        assert reason == BlacklistReason.CHAT_FORBIDDEN