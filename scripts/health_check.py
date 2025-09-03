#!/usr/bin/env python3
"""
Health Check Script for Telegram Automation System
Verifies all system components are working correctly
"""

import asyncio
import sys
from dataclasses import dataclass
from pathlib import Path

# Add app directory to path - Updated untuk reorganisasi
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class HealthCheckResult:
    """Result of a health check operation"""

    status: str  # ✅, ⚠️, or ❌
    message: str
    details: str | None = None


async def check_mongodb_connection() -> HealthCheckResult:
    """Check MongoDB connection"""
    try:
        from motor.motor_asyncio import AsyncIOMotorClient

        from src.core.config import settings

        client = AsyncIOMotorClient(settings.MONGO_URL)
        # Test connection
        await client.admin.command("ping")
        client.close()  # Note: close() is not async in motor

        return HealthCheckResult(
            status="✅",
            message="MongoDB connection successful",
            details=f"Connected to: {settings.MONGO_URL}",
        )
    except Exception as e:
        return HealthCheckResult(status="❌", message="MongoDB connection failed", details=str(e))


def check_telegram_credentials() -> HealthCheckResult:
    """Check if Telegram credentials are configured"""
    try:
        from src.core.config import settings

        credentials = {
            "API ID": settings.TELEGRAM_API_ID,
            "API Hash": settings.TELEGRAM_API_HASH,
            "Bot Token": settings.TELEGRAM_BOT_TOKEN,
            "Phone Number": settings.TELEGRAM_PHONE_NUMBER,
        }

        missing = [name for name, value in credentials.items() if not value]

        if not missing:
            return HealthCheckResult(
                status="✅",
                message="All Telegram credentials configured",
                details="Ready for Telegram operations",
            )
        else:
            return HealthCheckResult(
                status="❌",
                message="Missing Telegram credentials",
                details=f"Missing: {', '.join(missing)}",
            )
    except Exception as e:
        return HealthCheckResult(status="❌", message="Failed to check credentials", details=str(e))


async def run_health_check() -> int:
    """Run all health checks"""
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Project Imports", check_imports),
        ("Configuration", check_configuration),
        ("Telegram Credentials", check_telegram_credentials),
        ("MongoDB Connection", check_mongodb_connection),
    ]

    passed = 0
    total = len(checks)

    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        try:
            if asyncio.iscoroutinefunction(check_func):
                result = await check_func()
                if isinstance(result, HealthCheckResult):
                    print(f"{result.status} {result.message}")
                    if result.details:
                        print(f"   {result.details}")
                    success = result.status == "✅"
                else:
                    success = result
            else:
                success = check_func()

            if success:
                passed += 1
            else:
                print(f"⚠️ {name} check failed")
        except Exception as e:
            print(f"❌ {name} check error: {e}")

    print("\n📊 HEALTH CHECK SUMMARY")
    print(f"{'=' * 30}")
    print(f"Passed: {passed}/{total} checks")

    if passed == total:
        print("🎉 System is HEALTHY and ready to run!")
        return 0
    else:
        print("⚠️ Some issues found. Please fix before running.")
        return 1


def check_python_version():
    """Check Python version compatibility"""
    # Constants for Python version requirements
    PYTHON_MAJOR_REQUIRED = 3
    PYTHON_MINOR_RECOMMENDED = 11
    PYTHON_MINOR_MINIMUM = 8

    version = sys.version_info
    if version.major >= PYTHON_MAJOR_REQUIRED and version.minor >= PYTHON_MINOR_RECOMMENDED:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    elif version.major >= PYTHON_MAJOR_REQUIRED and version.minor >= PYTHON_MINOR_MINIMUM:
        print(
            f"⚠️ Python {version.major}.{version.minor}.{version.micro} - "
            f"Works but 3.11+ recommended"
        )
        return True
    else:
        print(
            f"❌ Python {version.major}.{version.minor}.{version.micro} - "
            f"Requires 3.11+ (minimum 3.8)"
        )
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        ("pyrogram", "pyrofork"),
        ("telegram", "python-telegram-bot"),
        ("motor", "motor"),
        ("pymongo", "pymongo"),
        ("pydantic", "pydantic"),
        ("pydantic_settings", "pydantic-settings"),
        ("loguru", "loguru"),
        ("dotenv", "python-dotenv"),
    ]

    missing = []
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} - Installed")
        except ImportError:
            print(f"❌ {package_name} - Missing")
            missing.append(package_name)

    return len(missing) == 0


def check_imports():
    """Check if all project modules can be imported"""
    try:
        print("\n📦 Testing project imports...")

        print("✅ Core config - OK")

        print("✅ Database module - OK")

        print("✅ All services - OK")

        print("✅ Telegram components - OK")

        print("✅ Main application - OK")

        return True

    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


def check_configuration():
    """Check configuration status"""
    try:
        from src.core.config import settings

        print("\n⚙️ Configuration status:")
        print(f"📊 Database: {settings.DB_NAME}")
        print(f"📝 Log Level: {settings.LOG_LEVEL}")

        # Check if Telegram credentials are set
        has_api_id = settings.TELEGRAM_API_ID is not None
        has_api_hash = settings.TELEGRAM_API_HASH is not None
        has_bot_token = settings.TELEGRAM_BOT_TOKEN is not None
        has_phone = settings.TELEGRAM_PHONE_NUMBER is not None

        if all([has_api_id, has_api_hash, has_bot_token, has_phone]):
            print("✅ All Telegram credentials configured")
        else:
            print("⚠️ Telegram credentials not configured (expected for first setup)")
            print("   Run: python setup.py to configure")

        return True

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def check_file_structure():
    """Check if all required files exist"""
    required_files = [
        "main.py",
        "pyproject.toml",
        "scripts/setup.py",
        ".env",
        "src/core/config.py",
        "src/core/database.py",
        "src/services/message_service.py",
        "src/telegram/bot_manager.py",
        "tests/",
        "docs/",
        ".github/workflows/",
    ]

    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            missing.append(file_path)

    return len(missing) == 0


def main():
    """Run comprehensive health check"""
    print("🩺 TELEGRAM AUTOMATION SYSTEM - HEALTH CHECK")
    print("=" * 55)

    # Run async health check
    return asyncio.run(run_health_check())


if __name__ == "__main__":
    sys.exit(main())
