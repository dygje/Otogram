#!/usr/bin/env python3
"""
Health Check Script for Telegram Automation System
Verifies all system components are working correctly
"""
import sys
import os
from pathlib import Path

# Add app directory to path - Updated untuk reorganisasi
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        ('pyrogram', 'pyrogram'),
        ('telegram', 'python-telegram-bot'), 
        ('motor', 'motor'),
        ('pymongo', 'pymongo'),
        ('pydantic', 'pydantic'),
        ('pydantic_settings', 'pydantic-settings'),
        ('loguru', 'loguru'),
        ('dotenv', 'python-dotenv')
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
        
        from src.core.config import settings
        print("✅ Core config - OK")
        
        from src.core.database import Database
        print("✅ Database module - OK")
        
        from src.services.message_service import MessageService
        from src.services.group_service import GroupService
        from src.services.blacklist_service import BlacklistService
        from src.services.config_service import ConfigService
        print("✅ All services - OK")
        
        from src.telegram.bot_manager import BotManager
        print("✅ Telegram components - OK")
        
        from main import TelegramAutomationApp
        print("✅ Main application - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def check_configuration():
    """Check configuration status"""
    try:
        from src.core.config import settings
        
        print(f"\n⚙️ Configuration status:")
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
        'main.py', 'requirements.txt', 'setup.py', '.env',
        'src/core/config.py', 'src/core/database.py',
        'src/services/message_service.py',
        'src/telegram/bot_manager.py'
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
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies), 
        ("File Structure", check_file_structure),
        ("Project Imports", check_imports),
        ("Configuration", check_configuration)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if check_func():
            passed += 1
        else:
            print(f"⚠️ {name} check failed")
    
    print(f"\n📊 HEALTH CHECK SUMMARY")
    print(f"{'=' * 30}")
    print(f"Passed: {passed}/{total} checks")
    
    if passed == total:
        print("🎉 System is HEALTHY and ready to run!")
        print("🚀 Next: Configure .env and run 'python main.py'")
        return 0
    else:
        print("⚠️ Some issues found. Please fix before running.")
        return 1

if __name__ == "__main__":
    sys.exit(main())