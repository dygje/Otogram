#!/usr/bin/env python3
"""
Backend Testing for Otogram - Telegram Automation System
Tests core functionality, imports, and system health after dependency updates
"""

import asyncio
import sys
import traceback
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

class OtogramSystemTester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.errors = []

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            result = test_func()
            if asyncio.iscoroutine(result):
                result = asyncio.run(result)
            
            if result:
                self.tests_passed += 1
                print(f"✅ Passed - {name}")
                return True
            else:
                print(f"❌ Failed - {name}")
                return False
                
        except Exception as e:
            print(f"❌ Failed - {name}: {str(e)}")
            self.errors.append(f"{name}: {str(e)}")
            return False

    def test_python_version(self):
        """Test Python version compatibility"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 11:
            print(f"   Python {version.major}.{version.minor}.{version.micro}")
            return True
        return False

    def test_core_imports(self):
        """Test core module imports"""
        try:
            from src.core.config import settings, Settings
            from src.core.database import Database, database
            from src.core.constants import DEFAULT_MIN_MESSAGE_DELAY, TELEGRAM_MESSAGE_MAX_LENGTH
            print("   Core modules imported successfully")
            return True
        except ImportError as e:
            print(f"   Import error: {e}")
            return False

    def test_model_imports(self):
        """Test model imports"""
        try:
            from src.models.message import Message
            from src.models.group import Group
            from src.models.blacklist import Blacklist
            print("   Model classes imported successfully")
            return True
        except ImportError as e:
            print(f"   Import error: {e}")
            return False

    def test_service_imports(self):
        """Test service imports"""
        try:
            from src.services.message_service import MessageService
            from src.services.group_service import GroupService
            from src.services.blacklist_service import BlacklistService
            print("   Service classes imported successfully")
            return True
        except ImportError as e:
            print(f"   Import error: {e}")
            return False

    def test_telegram_imports(self):
        """Test Telegram module imports"""
        try:
            from src.telegram.bot_manager import BotManager
            print("   Telegram modules imported successfully")
            return True
        except ImportError as e:
            print(f"   Import error: {e}")
            return False

    def test_config_loading(self):
        """Test configuration loading"""
        try:
            from src.core.config import settings
            
            # Test basic config values
            assert hasattr(settings, 'MONGO_URL')
            assert hasattr(settings, 'DB_NAME')
            assert hasattr(settings, 'LOG_LEVEL')
            
            print(f"   Config loaded - DB: {settings.DB_NAME}, Log Level: {settings.LOG_LEVEL}")
            return True
        except Exception as e:
            print(f"   Config error: {e}")
            return False

    async def test_database_connection(self):
        """Test database connection"""
        try:
            from src.core.database import Database
            
            db = Database()
            await db.connect()
            
            # Test ping
            ping_result = await db.ping()
            if not ping_result:
                return False
                
            print("   Database connection successful")
            await db.disconnect()
            return True
            
        except Exception as e:
            print(f"   Database error: {e}")
            return False

    def test_main_app_import(self):
        """Test main application import"""
        try:
            from main import TelegramAutomationApp
            
            # Try to instantiate (without starting)
            app = TelegramAutomationApp()
            assert app is not None
            
            print("   Main application class imported and instantiated")
            return True
        except Exception as e:
            print(f"   Main app error: {e}")
            return False

    def test_essential_packages(self):
        """Test essential package imports"""
        packages = [
            ("pyrofork", "pyrogram"),
            ("telegram", "python-telegram-bot"),
            ("motor.motor_asyncio", "motor"),
            ("pydantic", "pydantic"),
            ("loguru", "loguru"),
            ("dotenv", "python-dotenv"),
        ]
        
        missing = []
        for import_name, display_name in packages:
            try:
                __import__(import_name)
                print(f"   ✅ {display_name}")
            except ImportError:
                print(f"   ❌ {display_name}")
                missing.append(display_name)
        
        return len(missing) == 0

    async def test_model_instantiation(self):
        """Test model class instantiation"""
        try:
            from src.models.message import Message
            from src.models.group import Group
            from src.models.blacklist import Blacklist
            from datetime import datetime
            
            # Test Message
            message = Message(
                content="Test message",
                is_active=True,
                created_at=datetime.now()
            )
            assert message.content == "Test message"
            
            # Test Group  
            group = Group(
                group_id=-1001234567890,
                title="Test Group",
                username="testgroup"
            )
            assert group.group_id == -1001234567890
            
            print("   Model instantiation successful")
            return True
            
        except Exception as e:
            print(f"   Model instantiation error: {e}")
            return False

    def run_all_tests(self):
        """Run all tests"""
        print("🧪 OTOGRAM SYSTEM TESTING")
        print("=" * 40)
        print("Testing system after dependency updates...")
        
        # Test sequence
        tests = [
            ("Python Version Compatibility", self.test_python_version),
            ("Essential Package Imports", self.test_essential_packages),
            ("Core Module Imports", self.test_core_imports),
            ("Model Imports", self.test_model_imports),
            ("Service Imports", self.test_service_imports),
            ("Telegram Module Imports", self.test_telegram_imports),
            ("Configuration Loading", self.test_config_loading),
            ("Database Connection", self.test_database_connection),
            ("Main Application Import", self.test_main_app_import),
            ("Model Instantiation", self.test_model_instantiation),
        ]
        
        for name, test_func in tests:
            self.run_test(name, test_func)
        
        # Print results
        print(f"\n📊 TEST RESULTS")
        print("=" * 40)
        print(f"Tests passed: {self.tests_passed}/{self.tests_run}")
        
        if self.errors:
            print(f"\n❌ ERRORS FOUND:")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ System is healthy after dependency updates")
            print("✅ Python 3.11/3.12 compatibility confirmed")
            print("✅ All imports and core functionality working")
            return 0
        else:
            print(f"\n⚠️ {self.tests_run - self.tests_passed} tests failed")
            print("❌ Issues found that need attention")
            return 1

def main():
    """Main test entry point"""
    tester = OtogramSystemTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())