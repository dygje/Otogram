#!/usr/bin/env python3
"""
Application Startup Test
Test if the application can start without critical errors
"""

import asyncio
import signal
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.config import settings
from src.core.database import Database


async def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        db = Database()
        await db.connect()
        
        # Test ping
        ping_result = await db.ping()
        if ping_result:
            print("✅ Database connection successful")
        else:
            print("❌ Database ping failed")
            return False
            
        # Test basic operations
        collections = await db.list_collections()
        print(f"✅ Database collections: {len(collections)} found")
        
        await db.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_configuration():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        # Test basic settings
        print(f"✅ MongoDB URL: {settings.MONGO_URL}")
        print(f"✅ Database Name: {settings.DB_NAME}")
        print(f"✅ Log Level: {settings.LOG_LEVEL}")
        
        # Test credential status
        cred_status = settings.get_credentials_status()
        print(f"✅ Credentials configured: {cred_status['all_configured']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


async def test_app_initialization():
    """Test application initialization without starting services"""
    print("\n🔍 Testing application initialization...")
    
    try:
        # Import main app components
        from main import TelegramAutomationApp
        
        # Create app instance
        app = TelegramAutomationApp()
        print("✅ App instance created")
        
        # Test credential check
        has_creds = app._check_credentials()
        print(f"✅ Credential check: {'Pass' if has_creds else 'Missing (expected in test)'}")
        
        return True
        
    except Exception as e:
        print(f"❌ App initialization failed: {e}")
        return False


async def test_service_imports():
    """Test service class imports and instantiation"""
    print("\n🔍 Testing service instantiation...")
    
    try:
        # Test database for services
        db = Database()
        await db.connect()
        
        # Test service imports and instantiation
        from src.services.message_service import MessageService
        from src.services.group_service import GroupService
        from src.services.blacklist_service import BlacklistService
        from src.services.config_service import ConfigService
        
        message_service = MessageService(db)
        group_service = GroupService(db)
        blacklist_service = BlacklistService(db)
        config_service = ConfigService(db)
        
        print("✅ All services instantiated successfully")
        
        await db.disconnect()
        return True
        
    except Exception as e:
        print(f"❌ Service instantiation failed: {e}")
        return False


async def main():
    """Run all startup tests"""
    print("🚀 APPLICATION STARTUP TEST")
    print("=" * 35)
    
    tests = [
        ("Configuration Loading", test_configuration),
        ("Database Connection", test_database_connection),
        ("Service Instantiation", test_service_imports),
        ("App Initialization", test_app_initialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
                
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {name} failed: {e}")
    
    print(f"\n📊 RESULTS: {passed}/{total} startup tests passed")
    
    if passed == total:
        print("🎉 Application startup SUCCESSFUL!")
        print("\n💡 The application is ready to run with:")
        print("   python main.py")
        return 0
    else:
        print("⚠️ Some startup tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))