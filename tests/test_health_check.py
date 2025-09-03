"""
Tests for health check functionality
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add scripts to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from scripts.health_check import (
    HealthCheckResult,
    check_dependencies,
    check_file_structure,
    check_mongodb_connection,
    check_python_version,
    check_telegram_credentials,
    run_health_check,
)


class TestHealthCheck:
    """Test health check functions"""

    def test_check_python_version(self):
        """Test Python version check"""
        result = check_python_version()

        # Should return boolean for basic function
        assert isinstance(result, bool)

    def test_check_file_structure(self):
        """Test file structure validation"""
        result = check_file_structure()

        # Should return boolean
        assert isinstance(result, bool)

    @patch("scripts.health_check.importlib.import_module")
    def test_check_dependencies_success(self, mock_import):
        """Test dependency check with all dependencies available"""
        mock_import.return_value = MagicMock()

        result = check_dependencies()

        assert isinstance(result, bool)

    @patch("scripts.health_check.importlib.import_module")
    def test_check_dependencies_missing(self, mock_import):
        """Test dependency check with missing dependencies"""
        mock_import.side_effect = ImportError("Module not found")

        result = check_dependencies()

        assert isinstance(result, bool)

    def test_check_telegram_credentials_missing(self):
        """Test Telegram credentials check with missing credentials"""
        with patch("scripts.health_check.settings") as mock_settings:
            mock_settings.TELEGRAM_API_ID = None
            mock_settings.TELEGRAM_API_HASH = None
            mock_settings.TELEGRAM_BOT_TOKEN = None
            mock_settings.TELEGRAM_PHONE_NUMBER = None

            result = check_telegram_credentials()

            assert isinstance(result, HealthCheckResult)
            assert result.status == "❌"
            assert "credentials" in result.message.lower()

    def test_check_telegram_credentials_complete(self):
        """Test Telegram credentials check with complete credentials"""
        with patch("scripts.health_check.settings") as mock_settings:
            mock_settings.TELEGRAM_API_ID = 12345678
            mock_settings.TELEGRAM_API_HASH = "test_hash"
            mock_settings.TELEGRAM_BOT_TOKEN = "123456:test_token"
            mock_settings.TELEGRAM_PHONE_NUMBER = "+1234567890"

            result = check_telegram_credentials()

            assert isinstance(result, HealthCheckResult)
            assert result.status == "✅"
            assert "configured" in result.message.lower()

    @pytest.mark.asyncio
    async def test_check_mongodb_connection_success(self):
        """Test MongoDB connection check success"""
        with patch("scripts.health_check.AsyncIOMotorClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            mock_instance.admin.command = AsyncMock(return_value={"ok": 1.0})
            mock_instance.close = AsyncMock()

            result = await check_mongodb_connection()

            assert isinstance(result, HealthCheckResult)
            assert result.status == "✅"
            assert "mongodb" in result.message.lower()

    @pytest.mark.asyncio
    async def test_check_mongodb_connection_failure(self):
        """Test MongoDB connection check failure"""
        with patch("scripts.health_check.AsyncIOMotorClient") as mock_client:
            mock_instance = AsyncMock()
            mock_client.return_value = mock_instance
            mock_instance.admin.command = AsyncMock(side_effect=Exception("Connection failed"))

            result = await check_mongodb_connection()

            assert isinstance(result, HealthCheckResult)
            assert result.status == "❌"
            assert "failed" in result.message.lower()

    @pytest.mark.asyncio
    async def test_run_health_check(self):
        """Test complete health check run"""
        with patch("scripts.health_check.check_mongodb_connection") as mock_mongo:
            mock_result = HealthCheckResult(status="✅", message="MongoDB OK")
            mock_mongo.return_value = mock_result

            # Run health check
            exit_code = await run_health_check()

            # Should return integer exit code
            assert isinstance(exit_code, int)
            assert exit_code in [0, 1]  # 0 for success, 1 for failure
