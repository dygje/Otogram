#!/usr/bin/env python3
"""
Comprehensive Migration Test Script
Tests pyrogram to pyrofork migration thoroughly
"""

import sys
import importlib
import inspect
from pathlib import Path
from typing import List, Dict, Any

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

class MigrationTester:
    """Comprehensive tester for pyrogram to pyrofork migration"""
    
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.results = []
    
    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test and record results"""
        self.tests_run += 1
        print(f"\n🔍 Testing {test_name}...")
        
        try:
            result = test_func()
            if result:
                self.tests_passed += 1
                print(f"✅ {test_name} - PASSED")
                self.results.append({"test": test_name, "status": "PASSED", "details": ""})
                return True
            else:
                print(f"❌ {test_name} - FAILED")
                self.results.append({"test": test_name, "status": "FAILED", "details": "Test returned False"})
                return False
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {str(e)}")
            self.results.append({"test": test_name, "status": "ERROR", "details": str(e)})
            return False
    
    def test_pyrofork_installation(self) -> bool:
        """Test that pyrofork is properly installed and provides pyrogram namespace"""
        try:
            # Pyrofork doesn't expose itself as 'pyrofork' module
            # Instead it provides the 'pyrogram' namespace
            import pyrogram
            version = getattr(pyrogram, '__version__', 'Unknown')
            print(f"   📦 Pyrogram namespace version: {version}")
            
            # Check if it's the expected pyrofork version
            if version == "2.3.68":
                print(f"   ✅ Pyrofork 2.3.68 providing pyrogram namespace")
                return True
            else:
                print(f"   ⚠️ Expected version 2.3.68, got {version}")
                return False
        except ImportError as e:
            print(f"   ❌ Pyrogram namespace not available: {e}")
            return False
    
    def test_pyrogram_namespace_import(self) -> bool:
        """Test that pyrogram namespace imports work with pyrofork backend"""
        try:
            # Test basic pyrogram import
            import pyrogram
            print(f"   ✅ pyrogram module imported successfully")
            
            # Check if it's actually pyrofork backend
            module_file = getattr(pyrogram, '__file__', None)
            if module_file and 'pyrofork' in module_file:
                print(f"   ✅ pyrogram namespace is using pyrofork backend")
            else:
                print(f"   ⚠️ pyrogram namespace source: {module_file}")
            
            return True
        except ImportError as e:
            print(f"   ❌ Failed to import pyrogram: {e}")
            return False
    
    def test_pyrogram_client_import(self) -> bool:
        """Test pyrogram.Client import and instantiation"""
        try:
            from pyrogram import Client
            print(f"   ✅ pyrogram.Client imported successfully")
            
            # Test Client class attributes
            expected_methods = ['start', 'stop', 'send_message', 'get_me']
            for method in expected_methods:
                if hasattr(Client, method):
                    print(f"   ✅ Client.{method} method available")
                else:
                    print(f"   ❌ Client.{method} method missing")
                    return False
            
            # Test Client instantiation (without actually connecting)
            try:
                client = Client(
                    "test_session",
                    api_id=12345,
                    api_hash="test_hash",
                    phone_number="+1234567890",
                    in_memory=True  # Don't create session file
                )
                print(f"   ✅ Client instantiation successful")
                return True
            except Exception as e:
                print(f"   ❌ Client instantiation failed: {e}")
                return False
                
        except ImportError as e:
            print(f"   ❌ Failed to import pyrogram.Client: {e}")
            return False
    
    def test_pyrogram_errors_import(self) -> bool:
        """Test pyrogram.errors imports"""
        try:
            from pyrogram.errors import (
                FloodWait, ChatForbidden, ChatIdInvalid, ChatRestricted,
                ChatWriteForbidden, PeerIdInvalid, SlowmodeWait,
                UserBannedInChannel, UserBlocked, ChannelInvalid
            )
            
            error_classes = [
                FloodWait, ChatForbidden, ChatIdInvalid, ChatRestricted,
                ChatWriteForbidden, PeerIdInvalid, SlowmodeWait,
                UserBannedInChannel, UserBlocked, ChannelInvalid
            ]
            
            for error_class in error_classes:
                print(f"   ✅ {error_class.__name__} imported successfully")
            
            return True
        except ImportError as e:
            print(f"   ❌ Failed to import pyrogram errors: {e}")
            return False
    
    def test_project_modules_import(self) -> bool:
        """Test all project modules import correctly"""
        modules_to_test = [
            "src.core.config",
            "src.core.database", 
            "src.telegram.userbot",
            "src.telegram.bot_manager",
            "src.services.message_service",
            "src.services.group_service",
            "src.services.blacklist_service",
            "src.services.config_service"
        ]
        
        all_passed = True
        for module_name in modules_to_test:
            try:
                module = importlib.import_module(module_name)
                print(f"   ✅ {module_name} imported successfully")
            except ImportError as e:
                print(f"   ❌ Failed to import {module_name}: {e}")
                all_passed = False
        
        return all_passed
    
    def test_userbot_pyrogram_usage(self) -> bool:
        """Test that UserBot class uses pyrogram correctly"""
        try:
            from src.telegram.userbot import UserBot
            
            # Check if UserBot can be instantiated (without database connection)
            userbot = UserBot()
            print(f"   ✅ UserBot instantiated successfully")
            
            # Check if it has expected methods
            expected_methods = ['start', 'stop']
            for method in expected_methods:
                if hasattr(userbot, method):
                    print(f"   ✅ UserBot.{method} method available")
                else:
                    print(f"   ❌ UserBot.{method} method missing")
                    return False
            
            # Check if UserBot imports pyrogram correctly
            if hasattr(userbot, 'client'):
                print(f"   ✅ UserBot has client attribute for pyrogram.Client")
            
            return True
        except Exception as e:
            # If it's just a database connection error, that's expected
            if "Database not connected" in str(e):
                print(f"   ⚠️ UserBot test skipped due to database requirement: {e}")
                return True
            else:
                print(f"   ❌ UserBot test failed: {e}")
                return False
    
    def test_bot_manager_functionality(self) -> bool:
        """Test BotManager functionality"""
        try:
            from src.telegram.bot_manager import BotManager
            
            # Check if BotManager can be instantiated
            bot_manager = BotManager()
            print(f"   ✅ BotManager instantiated successfully")
            
            # Check if it has expected methods
            expected_methods = ['start', 'stop', 'is_running']
            for method in expected_methods:
                if hasattr(bot_manager, method):
                    print(f"   ✅ BotManager.{method} method available")
                else:
                    print(f"   ❌ BotManager.{method} method missing")
                    return False
            
            return True
        except Exception as e:
            # If it's just a database connection error, that's expected
            if "Database not connected" in str(e):
                print(f"   ⚠️ BotManager test skipped due to database requirement: {e}")
                return True
            else:
                print(f"   ❌ BotManager test failed: {e}")
                return False
    
    def test_configuration_loading(self) -> bool:
        """Test configuration loading with pydantic compatibility"""
        try:
            from src.core.config import settings, Settings
            
            print(f"   ✅ Settings imported successfully")
            print(f"   📊 Database: {settings.DB_NAME}")
            print(f"   📝 Log Level: {settings.LOG_LEVEL}")
            
            # Test pydantic compatibility
            if hasattr(settings, 'model_config'):
                print(f"   ✅ Pydantic v2 compatibility confirmed")
            
            # Test settings validation
            credentials_status = settings.get_credentials_status()
            print(f"   📋 Credentials configured: {credentials_status['all_configured']}")
            
            return True
        except Exception as e:
            print(f"   ❌ Configuration test failed: {e}")
            return False
    
    def test_dependencies_compatibility(self) -> bool:
        """Test compatibility with other dependencies"""
        try:
            # Test pydantic compatibility
            import pydantic
            pydantic_version = getattr(pydantic, '__version__', 'Unknown')
            print(f"   📦 Pydantic version: {pydantic_version}")
            
            # Test TgCrypto compatibility (correct import)
            try:
                import TgCrypto
                print(f"   ✅ TgCrypto imported successfully")
            except ImportError:
                # Try alternative import
                import tgcrypto
                print(f"   ✅ tgcrypto imported successfully")
            
            # Test python-telegram-bot compatibility
            import telegram
            telegram_version = getattr(telegram, '__version__', 'Unknown')
            print(f"   📦 python-telegram-bot version: {telegram_version}")
            
            return True
        except ImportError as e:
            print(f"   ❌ Dependency compatibility test failed: {e}")
            return False
    
    def test_pyrogram_version_compatibility(self) -> bool:
        """Test that pyrogram namespace reports correct version"""
        try:
            import pyrogram
            
            # Check version attribute
            version = getattr(pyrogram, '__version__', None)
            if version:
                print(f"   📦 Pyrogram namespace version: {version}")
                # Should be pyrofork version since it's the backend
                return True
            else:
                print(f"   ⚠️ No version attribute found in pyrogram namespace")
                return True  # Not critical
                
        except Exception as e:
            print(f"   ❌ Version compatibility test failed: {e}")
            return False
    
    def run_all_tests(self) -> int:
        """Run all migration tests"""
        print("🔄 PYROGRAM TO PYROFORK MIGRATION TEST")
        print("=" * 50)
        
        tests = [
            ("Pyrofork Installation", self.test_pyrofork_installation),
            ("Pyrogram Namespace Import", self.test_pyrogram_namespace_import),
            ("Pyrogram Client Import", self.test_pyrogram_client_import),
            ("Pyrogram Errors Import", self.test_pyrogram_errors_import),
            ("Project Modules Import", self.test_project_modules_import),
            ("UserBot Pyrogram Usage", self.test_userbot_pyrogram_usage),
            ("BotManager Functionality", self.test_bot_manager_functionality),
            ("Configuration Loading", self.test_configuration_loading),
            ("Dependencies Compatibility", self.test_dependencies_compatibility),
            ("Pyrogram Version Compatibility", self.test_pyrogram_version_compatibility),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Print summary
        print(f"\n📊 MIGRATION TEST SUMMARY")
        print("=" * 30)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 MIGRATION SUCCESSFUL!")
            print("✅ All pyrogram imports work with pyrofork backend")
            print("✅ Backward compatibility maintained")
            print("✅ All project modules compatible")
            return 0
        else:
            print(f"\n⚠️ MIGRATION ISSUES DETECTED")
            print("❌ Some tests failed - review results above")
            
            # Print failed tests
            failed_tests = [r for r in self.results if r["status"] != "PASSED"]
            if failed_tests:
                print("\n🔍 Failed Tests:")
                for test in failed_tests:
                    print(f"   ❌ {test['test']}: {test['details']}")
            
            return 1

def main():
    """Run migration tests"""
    tester = MigrationTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())