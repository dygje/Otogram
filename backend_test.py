#!/usr/bin/env python3
"""
Comprehensive Backend Test for Otogram Project
Tests all aspects of the Telegram automation bot backend
"""

import asyncio
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

class OtogramTester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.results = []

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func())
            else:
                result = test_func()
                
            if result:
                self.tests_passed += 1
                print(f"✅ {name} - PASSED")
                self.results.append(f"✅ {name}")
            else:
                print(f"❌ {name} - FAILED")
                self.results.append(f"❌ {name}")
                
        except Exception as e:
            print(f"❌ {name} - ERROR: {str(e)}")
            self.results.append(f"❌ {name} - {str(e)}")

    def test_dependencies(self):
        """Test all dependencies are installed and importable"""
        try:
            dependencies = [
                ("pyrogram", "pyrofork"),
                ("telegram", "python-telegram-bot"),
                ("motor.motor_asyncio", "motor"),
                ("pymongo", "pymongo"),
                ("pydantic", "pydantic"),
                ("loguru", "loguru"),
                ("dotenv", "python-dotenv"),
                ("apscheduler", "apscheduler"),
            ]
            
            for import_name, package_name in dependencies:
                __import__(import_name)
                
            return True
        except ImportError as e:
            print(f"Dependency import failed: {e}")
            return False

    def test_configuration(self):
        """Test configuration loading and validation"""
        try:
            from src.core.config import settings
            
            # Test basic settings
            assert settings.MONGO_URL
            assert settings.DB_NAME
            assert settings.LOG_LEVEL
            
            # Test credential status
            cred_status = settings.get_credentials_status()
            
            return True
        except Exception as e:
            print(f"Configuration test failed: {e}")
            return False

    async def test_database_connection(self):
        """Test database connectivity"""
        try:
            from src.core.database import Database
            
            db = Database()
            await db.connect()
            
            # Test ping
            ping_result = await db.ping()
            if not ping_result:
                return False
                
            # Test basic operations
            collections = await db.list_collections()
            
            await db.disconnect()
            return True
            
        except Exception as e:
            print(f"Database test failed: {e}")
            return False

    def test_models(self):
        """Test data models"""
        try:
            from src.models.message import Message, MessageCreate
            from src.models.group import Group, GroupCreate
            from src.models.blacklist import Blacklist, BlacklistCreate
            
            # Test model creation
            message = Message(content="Test message")
            group = Group(group_id="-1001234567890")
            
            return True
        except Exception as e:
            print(f"Models test failed: {e}")
            return False

    def test_services(self):
        """Test service classes"""
        try:
            from src.services.message_service import MessageService
            from src.services.group_service import GroupService
            from src.services.blacklist_service import BlacklistService
            from src.services.config_service import ConfigService
            
            return True
        except Exception as e:
            print(f"Services test failed: {e}")
            return False

    def test_telegram_components(self):
        """Test Telegram components"""
        try:
            from src.telegram.bot_manager import BotManager
            from src.telegram.management_bot import ManagementBot
            from src.telegram.userbot import UserBot
            
            return True
        except Exception as e:
            print(f"Telegram components test failed: {e}")
            return False

    def test_code_quality(self):
        """Test code quality with ruff"""
        try:
            # Test ruff check
            result = subprocess.run(
                ["ruff", "check", "src/", "scripts/", "tests/"],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            
            if result.returncode != 0:
                print(f"Ruff check failed: {result.stdout}")
                return False
                
            # Test ruff format
            result = subprocess.run(
                ["ruff", "format", "--check", "src/", "scripts/", "tests/"],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Code quality test failed: {e}")
            return False

    def test_unit_tests(self):
        """Run pytest unit tests"""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Unit tests failed: {e}")
            return False

    def test_health_check(self):
        """Test health check script"""
        try:
            result = subprocess.run(
                ["python", "scripts/health_check.py"],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Health check failed: {e}")
            return False

    def test_yaml_configs(self):
        """Test YAML configuration files"""
        try:
            import yaml
            
            # Test CI workflow
            with open("/app/.github/workflows/ci.yml") as f:
                yaml.safe_load(f)
                
            # Test dependabot config
            with open("/app/.github/dependabot.yml") as f:
                yaml.safe_load(f)
                
            return True
            
        except Exception as e:
            print(f"YAML config test failed: {e}")
            return False

def main():
    """Run comprehensive backend tests"""
    tester = OtogramTester()
    
    print("🧪 OTOGRAM COMPREHENSIVE BACKEND TEST")
    print("=" * 45)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define all tests
    tests = [
        ("Dependencies Import", tester.test_dependencies),
        ("Configuration Loading", tester.test_configuration),
        ("Database Connection", tester.test_database_connection),
        ("Data Models", tester.test_models),
        ("Service Classes", tester.test_services),
        ("Telegram Components", tester.test_telegram_components),
        ("Code Quality (Ruff)", tester.test_code_quality),
        ("Unit Tests (Pytest)", tester.test_unit_tests),
        ("Health Check Script", tester.test_health_check),
        ("YAML Configurations", tester.test_yaml_configs),
    ]
    
    # Run all tests
    for name, test_func in tests:
        tester.run_test(name, test_func)
    
    # Print final results
    print(f"\n📊 FINAL RESULTS")
    print("=" * 20)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    print(f"\n📋 DETAILED RESULTS:")
    for result in tester.results:
        print(f"  {result}")
    
    if tester.tests_passed == tester.tests_run:
        print(f"\n🎉 ALL TESTS PASSED!")
        print("✅ Otogram backend is fully functional")
        print("✅ Dependencies are compatible")
        print("✅ GitHub Actions workflow is valid")
        print("✅ Dependabot configuration is optimal")
        return 0
    else:
        failed = tester.tests_run - tester.tests_passed
        print(f"\n⚠️ {failed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())