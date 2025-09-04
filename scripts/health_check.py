#!/usr/bin/env python3
"""
Personal Health Check - Otogram System Verification
Simple health check for personal Telegram automation
"""

import asyncio
import importlib
import sys
from dataclasses import dataclass
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings


@dataclass
class HealthCheckResult:
    """Health check result"""
    status: str  # ✅, ⚠️, or ❌
    message: str
    details: str | None = None


async def check_mongodb() -> HealthCheckResult:
    """Check MongoDB connection"""
    try:
        client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGO_URL)
        await client.admin.command("ping")
        client.close()

        return HealthCheckResult(
            status="✅",
            message="MongoDB connected",
            details=f"URL: {settings.MONGO_URL}"
        )
    except Exception as e:
        return HealthCheckResult(
            status="❌", 
            message="MongoDB connection failed", 
            details=str(e)
        )


def check_credentials() -> HealthCheckResult:
    """Check Telegram credentials"""
    try:
        creds = {
            "API ID": settings.TELEGRAM_API_ID,
            "API Hash": settings.TELEGRAM_API_HASH,
            "Bot Token": settings.TELEGRAM_BOT_TOKEN,
            "Phone": settings.TELEGRAM_PHONE_NUMBER,
        }

        missing = [name for name, value in creds.items() if not value]

        if not missing:
            return HealthCheckResult(
                status="✅",
                message="All credentials configured",
                details="Ready for automation"
            )
        else:
            return HealthCheckResult(
                status="❌",
                message="Missing credentials",
                details=f"Need: {', '.join(missing)}"
            )
    except Exception as e:
        return HealthCheckResult(
            status="❌", 
            message="Credential check failed", 
            details=str(e)
        )


def check_python() -> bool:
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor} - Perfect")
        return True
    elif version.major >= 3 and version.minor >= 8:
        print(f"⚠️ Python {version.major}.{version.minor} - Works (3.11+ recommended)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Too old (need 3.11+)")
        return False


def check_packages() -> bool:
    """Check essential packages"""
    packages = [
        ("pyrogram", "pyrofork"), 
        ("telegram", "python-telegram-bot"),
        ("motor", "motor"),
        ("pydantic", "pydantic"),
        ("loguru", "loguru"),
    ]

    missing = []
    for import_name, display_name in packages:
        try:
            importlib.import_module(import_name)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} - Missing")
            missing.append(display_name)

    return len(missing) == 0


def check_files() -> bool:
    """Check essential files exist"""
    essential_files = [
        "main.py",
        "pyproject.toml", 
        ".env",
        "src/core/config.py",
        "src/telegram/bot_manager.py",
    ]

    missing = []
    for file_path in essential_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)

    return len(missing) == 0


async def run_checks() -> int:
    """Run all health checks"""
    checks = [
        ("Python Version", check_python),
        ("Essential Packages", check_packages), 
        ("Project Files", check_files),
        ("Telegram Credentials", check_credentials),
        ("MongoDB Connection", check_mongodb),
    ]

    passed = 0
    total = len(checks)

    print("🩺 OTOGRAM HEALTH CHECK")
    print("=" * 30)

    for name, check_func in checks:
        print(f"\n🔍 {name}...")
        
        try:
            if asyncio.iscoroutinefunction(check_func):
                result = await check_func()
                if isinstance(result, HealthCheckResult):
                    print(f"{result.status} {result.message}")
                    if result.details:
                        print(f"   {result.details}")
                    if result.status == "✅":
                        passed += 1
                else:
                    if result:
                        passed += 1
            else:
                if check_func():
                    passed += 1
                    
        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n📊 RESULTS: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 System HEALTHY - Ready to run!")
        print("\n💡 Next steps:")
        print("   1. Run: python main.py")
        print("   2. Find your bot on Telegram")
        print("   3. Send /start command")
        return 0
    else:
        print("⚠️ Issues found - Please fix before running")
        if passed < total // 2:
            print("\n🔧 Quick fixes:")
            print("   - Install deps: pip install -e .")
            print("   - Setup creds: python scripts/setup.py")
            print("   - Start MongoDB: make db-start")
        return 1


def main() -> int:
    """Main health check entry"""
    return asyncio.run(run_checks())


if __name__ == "__main__":
    sys.exit(main())