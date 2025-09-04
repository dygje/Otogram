#!/usr/bin/env python3
"""
Basic Test Script untuk memverifikasi dependency dan konfigurasi
"""
import sys
import importlib.util

def test_imports():
    """Test semua import yang diperlukan"""
    imports_to_test = [
        ('loguru', 'loguru'),
        ('motor', 'motor'),
        ('pymongo', 'pymongo'), 
        ('pydantic', 'pydantic'),
        ('telegram', 'python-telegram-bot'),
        ('pyrogram', 'pyrofork'),
        ('TgCrypto', 'TgCrypto'),
        ('apscheduler', 'apscheduler'),
        ('aiofiles', 'aiofiles'),
        ('dateutil', 'python-dateutil')
    ]
    
    print("🔍 Testing imports...")
    failed = []
    
    for module_name in imports_to_test:
        try:
            if importlib.util.find_spec(module_name) is not None:
                print(f"✅ {module_name}")
            else:
                print(f"❌ {module_name} - Not found")
                failed.append(module_name)
        except ImportError as e:
            print(f"❌ {module_name} - Import error: {e}")
            failed.append(module_name)
    
    return len(failed) == 0

def test_config():
    """Test konfigurasi dasar"""
    print("\n🔍 Testing configuration...")
    try:
        from src.core.config import settings
        print(f"✅ Config loaded")
        print(f"✅ MongoDB URL: {settings.MONGO_URL}")
        print(f"✅ DB Name: {settings.DB_NAME}")
        print(f"✅ Log Level: {settings.LOG_LEVEL}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_database_connection():
    """Test koneksi database sederhana"""
    print("\n🔍 Testing database connection...")
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from src.core.config import settings
        
        client = AsyncIOMotorClient(settings.MONGO_URL, serverSelectionTimeoutMS=2000)
        print("✅ Database client created")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 OTOGRAM BASIC TEST")
    print("=" * 30)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Database Connection", test_database_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📝 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test PASSED")
        else:
            print(f"❌ {test_name} test FAILED")
    
    print(f"\n📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests PASSED! System is ready.")
        return 0
    else:
        print("⚠️ Some tests FAILED. Check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())