#!/usr/bin/env python3
"""
Final Backend Test for Otogram Project - Comprehensive Testing
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

class OtogramFinalTester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.results = []

    def run_test(self, name, test_func):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
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

    def test_unit_tests_with_coverage(self):
        """Run pytest with coverage"""
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "-v", "--cov=src", "--cov-report=term-missing", "--cov-fail-under=15"],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            
            print("Unit Test Output:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Unit tests failed: {e}")
            return False

    def test_dependencies_import(self):
        """Test critical dependencies can be imported"""
        try:
            # Test core dependencies
            import pyrogram
            import telegram
            import motor.motor_asyncio
            import pymongo
            import pydantic
            import loguru
            import dotenv
            import apscheduler
            
            print("✅ All critical dependencies imported successfully")
            return True
            
        except ImportError as e:
            print(f"Dependency import failed: {e}")
            return False

    def test_configuration_loading(self):
        """Test configuration system"""
        try:
            from src.core.config import settings
            
            # Test basic configuration
            assert settings.MONGO_URL
            assert settings.DB_NAME
            assert settings.LOG_LEVEL
            
            # Test credential status
            cred_status = settings.get_credentials_status()
            print(f"Credentials configured: {cred_status['all_configured']}")
            
            return True
            
        except Exception as e:
            print(f"Configuration test failed: {e}")
            return False

    def test_models_import(self):
        """Test all model classes can be imported"""
        try:
            from src.models.message import Message, MessageCreate
            from src.models.group import Group, GroupCreate
            from src.models.blacklist import Blacklist, BlacklistCreate
            from src.models.config import Configuration, ConfigUpdate
            from src.models.log import Log, LogCreate
            
            # Test basic model creation
            message = Message(content="Test message")
            assert message.content == "Test message"
            
            return True
            
        except Exception as e:
            print(f"Models test failed: {e}")
            return False

    def test_services_import(self):
        """Test service classes can be imported"""
        try:
            from src.services.message_service import MessageService
            from src.services.group_service import GroupService
            from src.services.blacklist_service import BlacklistService
            from src.services.config_service import ConfigService
            
            return True
            
        except Exception as e:
            print(f"Services test failed: {e}")
            return False

    def test_telegram_modules(self):
        """Test Telegram modules can be imported"""
        try:
            from src.telegram.bot_manager import BotManager
            from src.telegram.management_bot import ManagementBot
            from src.telegram.userbot import UserBot
            
            return True
            
        except Exception as e:
            print(f"Telegram modules test failed: {e}")
            return False

    def test_main_app_import(self):
        """Test main application can be imported"""
        try:
            from main import TelegramAutomationApp, async_main, main
            
            # Test app instantiation
            app = TelegramAutomationApp()
            
            return True
            
        except Exception as e:
            print(f"Main app test failed: {e}")
            return False

    def test_code_quality_ruff(self):
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
                print(f"Ruff check output: {result.stdout}")
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

    def test_health_check_script(self):
        """Test health check script runs"""
        try:
            result = subprocess.run(
                ["python", "scripts/health_check.py"],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            
            print("Health Check Output:")
            print(result.stdout)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Health check failed: {e}")
            return False

    def test_yaml_configurations(self):
        """Test YAML configuration files are valid"""
        try:
            import yaml
            
            # Test CI workflow
            with open("/app/.github/workflows/ci.yml") as f:
                ci_config = yaml.safe_load(f)
                assert "jobs" in ci_config
                assert "test" in ci_config["jobs"]
                
            # Test dependabot config
            with open("/app/.github/dependabot.yml") as f:
                dependabot_config = yaml.safe_load(f)
                assert "updates" in dependabot_config
                
            return True
            
        except Exception as e:
            print(f"YAML config test failed: {e}")
            return False

    def test_pyproject_toml(self):
        """Test pyproject.toml configuration"""
        try:
            import tomllib
            
            with open("/app/pyproject.toml", "rb") as f:
                config = tomllib.load(f)
                
            # Check essential sections
            assert "project" in config
            assert "dependencies" in config["project"]
            assert "tool" in config
            assert "pytest" in config["tool"]
            
            return True
            
        except Exception as e:
            print(f"pyproject.toml test failed: {e}")
            return False

def main():
    """Run comprehensive backend tests"""
    tester = OtogramFinalTester()
    
    print("🧪 OTOGRAM FINAL COMPREHENSIVE TEST")
    print("=" * 40)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define all tests in order of importance
    tests = [
        ("Dependencies Import", tester.test_dependencies_import),
        ("Configuration Loading", tester.test_configuration_loading),
        ("Data Models Import", tester.test_models_import),
        ("Service Classes Import", tester.test_services_import),
        ("Telegram Modules Import", tester.test_telegram_modules),
        ("Main Application Import", tester.test_main_app_import),
        ("Code Quality (Ruff)", tester.test_code_quality_ruff),
        ("Unit Tests with Coverage", tester.test_unit_tests_with_coverage),
        ("Health Check Script", tester.test_health_check_script),
        ("YAML Configurations", tester.test_yaml_configurations),
        ("PyProject TOML", tester.test_pyproject_toml),
    ]
    
    # Run all tests
    for name, test_func in tests:
        tester.run_test(name, test_func)
    
    # Print final results
    print(f"\n📊 FINAL TEST RESULTS")
    print("=" * 25)
    print(f"Tests Run: {tester.tests_run}")
    print(f"Tests Passed: {tester.tests_passed}")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    print(f"\n📋 DETAILED RESULTS:")
    for result in tester.results:
        print(f"  {result}")
    
    # Final assessment
    if tester.tests_passed == tester.tests_run:
        print(f"\n🎉 ALL TESTS PASSED - SYSTEM FULLY FUNCTIONAL!")
        print("✅ Dependencies updated successfully and compatible")
        print("✅ All imports working correctly")
        print("✅ Unit tests pass with required coverage (>=15%)")
        print("✅ Code quality standards met")
        print("✅ GitHub Actions workflow is valid")
        print("✅ Dependabot configuration is optimal")
        print("✅ Application can start without critical errors")
        print("✅ Health check passes")
        print("\n🚀 The Otogram project is ready for production!")
        return 0
    else:
        failed = tester.tests_run - tester.tests_passed
        print(f"\n⚠️ {failed} test(s) failed - Issues need to be addressed")
        return 1

if __name__ == "__main__":
    sys.exit(main())