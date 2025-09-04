#!/usr/bin/env python3
"""
Import Test - Verify all dependencies can be imported correctly
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_core_imports():
    """Test core module imports"""
    print("🔍 Testing core imports...")
    
    try:
        from src.core.config import settings
        print("✅ src.core.config")
        
        from src.core.database import Database, database
        print("✅ src.core.database")
        
        from src.core.constants import DEFAULT_MIN_MESSAGE_DELAY, TELEGRAM_MESSAGE_MAX_LENGTH
        print("✅ src.core.constants")
        
        from src.core.security import SecurityManager
        print("✅ src.core.security")
        
        return True
    except Exception as e:
        print(f"❌ Core imports failed: {e}")
        return False

def test_model_imports():
    """Test model imports"""
    print("\n🔍 Testing model imports...")
    
    try:
        from src.models.message import Message, MessageCreate
        print("✅ src.models.message")
        
        from src.models.group import Group, GroupCreate
        print("✅ src.models.group")
        
        from src.models.blacklist import Blacklist, BlacklistCreate
        print("✅ src.models.blacklist")
        
        from src.models.config import ConfigModel
        print("✅ src.models.config")
        
        from src.models.log import LogEntry
        print("✅ src.models.log")
        
        return True
    except Exception as e:
        print(f"❌ Model imports failed: {e}")
        return False

def test_service_imports():
    """Test service imports"""
    print("\n🔍 Testing service imports...")
    
    try:
        from src.services.message_service import MessageService
        print("✅ src.services.message_service")
        
        from src.services.group_service import GroupService
        print("✅ src.services.group_service")
        
        from src.services.blacklist_service import BlacklistService
        print("✅ src.services.blacklist_service")
        
        from src.services.config_service import ConfigService
        print("✅ src.services.config_service")
        
        return True
    except Exception as e:
        print(f"❌ Service imports failed: {e}")
        return False

def test_telegram_imports():
    """Test telegram module imports"""
    print("\n🔍 Testing telegram imports...")
    
    try:
        from src.telegram.bot_manager import BotManager
        print("✅ src.telegram.bot_manager")
        
        from src.telegram.management_bot import ManagementBot
        print("✅ src.telegram.management_bot")
        
        from src.telegram.userbot import UserBot
        print("✅ src.telegram.userbot")
        
        return True
    except Exception as e:
        print(f"❌ Telegram imports failed: {e}")
        return False

def test_external_dependencies():
    """Test external dependency imports"""
    print("\n🔍 Testing external dependencies...")
    
    dependencies = [
        ("pyrofork", "pyrofork"),
        ("telegram", "python-telegram-bot"),
        ("motor.motor_asyncio", "motor"),
        ("pymongo", "pymongo"),
        ("pydantic", "pydantic"),
        ("pydantic_settings", "pydantic-settings"),
        ("loguru", "loguru"),
        ("python_dotenv", "python-dotenv"),
        ("apscheduler", "apscheduler"),
        ("aiofiles", "aiofiles"),
        ("dateutil", "python-dateutil"),
    ]
    
    failed = []
    for import_name, package_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError as e:
            print(f"❌ {package_name}: {e}")
            failed.append(package_name)
    
    return len(failed) == 0

def main():
    """Run all import tests"""
    print("📦 DEPENDENCY IMPORT TEST")
    print("=" * 30)
    
    tests = [
        ("Core Modules", test_core_imports),
        ("Data Models", test_model_imports),
        ("Services", test_service_imports),
        ("Telegram Modules", test_telegram_imports),
        ("External Dependencies", test_external_dependencies),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
    
    print(f"\n📊 RESULTS: {passed}/{total} import tests passed")
    
    if passed == total:
        print("🎉 All imports SUCCESSFUL!")
        return 0
    else:
        print("⚠️ Some imports failed - check dependencies")
        return 1

if __name__ == "__main__":
    sys.exit(main())