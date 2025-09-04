#!/usr/bin/env python3
"""
Simple Application Startup Test
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_configuration():
    """Test configuration loading"""
    print("🔍 Testing configuration...")
    
    try:
        from src.core.config import settings
        
        print(f"✅ MongoDB URL: {settings.MONGO_URL}")
        print(f"✅ Database Name: {settings.DB_NAME}")
        print(f"✅ Log Level: {settings.LOG_LEVEL}")
        
        cred_status = settings.get_credentials_status()
        print(f"✅ Credentials configured: {cred_status['all_configured']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_app_import():
    """Test main app import"""
    print("\n🔍 Testing main app import...")
    
    try:
        from main import TelegramAutomationApp, async_main, main
        print("✅ Main app components imported successfully")
        
        # Test app instantiation
        app = TelegramAutomationApp()
        print("✅ App instance created")
        
        # Test credential check
        has_creds = app._check_credentials()
        print(f"✅ Credential check: {'Pass' if has_creds else 'Missing (expected in test)'}")
        
        return True
        
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_service_imports():
    """Test service imports"""
    print("\n🔍 Testing service imports...")
    
    try:
        from src.services.message_service import MessageService
        from src.services.group_service import GroupService
        from src.services.blacklist_service import BlacklistService
        from src.services.config_service import ConfigService
        
        print("✅ All service classes imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Service import failed: {e}")
        return False

def main():
    """Run startup tests"""
    print("🚀 SIMPLE STARTUP TEST")
    print("=" * 25)
    
    tests = [
        ("Configuration", test_configuration),
        ("App Import", test_app_import),
        ("Service Imports", test_service_imports),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} failed: {e}")
    
    print(f"\n📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Basic startup components WORKING!")
        return 0
    else:
        print("⚠️ Some startup tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())