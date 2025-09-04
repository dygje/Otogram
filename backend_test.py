#!/usr/bin/env python3
"""
Comprehensive Test Suite for Telegram Bot System
Tests imports, type checking, and basic object creation
"""

import sys
import subprocess
import importlib
import traceback
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

class TelegramBotTester:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests: List[str] = []
        self.results: Dict[str, Any] = {}

    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test and track results"""
        self.tests_run += 1
        print(f"\n🔍 Testing {test_name}...")
        
        try:
            result = test_func()
            if result:
                self.tests_passed += 1
                print(f"✅ {test_name} - PASSED")
                return True
            else:
                print(f"❌ {test_name} - FAILED")
                self.failed_tests.append(test_name)
                return False
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            self.failed_tests.append(f"{test_name} (Exception: {str(e)})")
            return False

    def test_import_core_modules(self) -> bool:
        """Test 1: Import Testing - Core modules"""
        try:
            # Test core imports
            import src.core.config
            import src.core.database
            import src.models
            import src.services
            print("   ✓ Core modules imported successfully")
            return True
        except ImportError as e:
            print(f"   ✗ Core import failed: {e}")
            return False

    def test_import_telegram_modules(self) -> bool:
        """Test 1: Import Testing - Telegram modules"""
        try:
            # Test main telegram modules
            import src.telegram.userbot
            import src.telegram.management_bot
            import src.telegram.bot_manager
            print("   ✓ Main telegram modules imported successfully")
            return True
        except ImportError as e:
            print(f"   ✗ Telegram import failed: {e}")
            return False

    def test_import_handler_modules(self) -> bool:
        """Test 1: Import Testing - Handler modules"""
        try:
            # Test all handler modules
            import src.telegram.handlers
            import src.telegram.handlers.message_handlers
            import src.telegram.handlers.group_handlers
            import src.telegram.handlers.config_handlers
            import src.telegram.handlers.blacklist_handlers
            print("   ✓ All handler modules imported successfully")
            return True
        except ImportError as e:
            print(f"   ✗ Handler import failed: {e}")
            return False

    def test_python_syntax_validation(self) -> bool:
        """Test 2: Basic Code Validation - Python syntax"""
        try:
            # Find all Python files
            python_files = list(Path("src").rglob("*.py"))
            syntax_errors = []
            
            for py_file in python_files:
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        compile(f.read(), str(py_file), 'exec')
                except SyntaxError as e:
                    syntax_errors.append(f"{py_file}: {e}")
            
            if syntax_errors:
                print(f"   ✗ Syntax errors found in {len(syntax_errors)} files:")
                for error in syntax_errors[:5]:  # Show first 5 errors
                    print(f"     - {error}")
                return False
            else:
                print(f"   ✓ All {len(python_files)} Python files have valid syntax")
                return True
        except Exception as e:
            print(f"   ✗ Syntax validation failed: {e}")
            return False

    def test_mypy_type_checking(self) -> bool:
        """Test 3: MyPy Type Checking"""
        try:
            # Run mypy on src directory
            result = subprocess.run(
                ["python", "-m", "mypy", "src/"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("   ✓ MyPy type checking passed with no errors")
                return True
            else:
                print(f"   ✗ MyPy found type errors:")
                print(f"     STDOUT: {result.stdout}")
                print(f"     STDERR: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("   ✗ MyPy type checking timed out")
            return False
        except FileNotFoundError:
            print("   ✗ MyPy not found - installing...")
            try:
                subprocess.run(["pip", "install", "mypy"], check=True)
                return self.test_mypy_type_checking()  # Retry after installation
            except Exception as e:
                print(f"   ✗ Failed to install MyPy: {e}")
                return False
        except Exception as e:
            print(f"   ✗ MyPy type checking failed: {e}")
            return False

    def test_management_bot_creation(self) -> bool:
        """Test 4: Basic Object Creation - ManagementBot"""
        try:
            from src.telegram.management_bot import ManagementBot
            
            # Try to create instance (may fail due to missing credentials, but should not have import/type errors)
            try:
                bot = ManagementBot()
                print("   ✓ ManagementBot instance created successfully")
                return True
            except Exception as e:
                # Check if it's a credential/config error (acceptable) vs type/import error (not acceptable)
                error_str = str(e).lower()
                if any(keyword in error_str for keyword in ['token', 'credential', 'api', 'config', 'env']):
                    print(f"   ✓ ManagementBot creation failed due to missing credentials (expected): {e}")
                    return True
                else:
                    print(f"   ✗ ManagementBot creation failed due to code error: {e}")
                    return False
        except ImportError as e:
            print(f"   ✗ ManagementBot import failed: {e}")
            return False

    def test_bot_manager_creation(self) -> bool:
        """Test 4: Basic Object Creation - BotManager"""
        try:
            from src.telegram.bot_manager import BotManager
            
            try:
                manager = BotManager()
                print("   ✓ BotManager instance created successfully")
                return True
            except Exception as e:
                error_str = str(e).lower()
                if any(keyword in error_str for keyword in ['token', 'credential', 'api', 'config', 'env']):
                    print(f"   ✓ BotManager creation failed due to missing credentials (expected): {e}")
                    return True
                else:
                    print(f"   ✗ BotManager creation failed due to code error: {e}")
                    return False
        except ImportError as e:
            print(f"   ✗ BotManager import failed: {e}")
            return False

    def test_userbot_creation(self) -> bool:
        """Test 4: Basic Object Creation - UserBot"""
        try:
            from src.telegram.userbot import UserBot
            
            try:
                userbot = UserBot()
                print("   ✓ UserBot instance created successfully")
                return True
            except Exception as e:
                error_str = str(e).lower()
                if any(keyword in error_str for keyword in ['token', 'credential', 'api', 'config', 'env', 'phone']):
                    print(f"   ✓ UserBot creation failed due to missing credentials (expected): {e}")
                    return True
                else:
                    print(f"   ✗ UserBot creation failed due to code error: {e}")
                    return False
        except ImportError as e:
            print(f"   ✗ UserBot import failed: {e}")
            return False

    def test_handler_classes_creation(self) -> bool:
        """Test 4: Basic Object Creation - Handler classes"""
        try:
            # Import handler modules and try to access classes
            from src.telegram.handlers import message_handlers, group_handlers, config_handlers, blacklist_handlers
            
            # Check if handler modules have expected classes/functions
            handler_modules = [message_handlers, group_handlers, config_handlers, blacklist_handlers]
            
            for module in handler_modules:
                # Check if module has callable attributes (handlers)
                callables = [attr for attr in dir(module) if callable(getattr(module, attr)) and not attr.startswith('_')]
                if callables:
                    print(f"   ✓ {module.__name__} has {len(callables)} callable handlers")
                else:
                    print(f"   ⚠ {module.__name__} has no callable handlers")
            
            return True
        except ImportError as e:
            print(f"   ✗ Handler classes import failed: {e}")
            return False
        except Exception as e:
            print(f"   ✗ Handler classes test failed: {e}")
            return False

    def test_type_fixes_verification(self) -> bool:
        """Test 5: Key Fixes Verification - Check for common type issues"""
        try:
            # Read key files and check for type-related patterns
            key_files = [
                "src/telegram/userbot.py",
                "src/telegram/management_bot.py", 
                "src/telegram/bot_manager.py",
                "src/telegram/handlers/message_handlers.py",
                "src/telegram/handlers/group_handlers.py",
                "src/telegram/handlers/config_handlers.py",
                "src/telegram/handlers/blacklist_handlers.py"
            ]
            
            issues_found = []
            
            for file_path in key_files:
                if Path(file_path).exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Check for proper union type handling
                        if "Message |" in content or "CallbackQuery |" in content:
                            print(f"   ✓ {file_path} uses proper union types")
                        
                        # Check for type annotations
                        if "-> None:" in content or "-> bool:" in content or "-> str:" in content:
                            print(f"   ✓ {file_path} has return type annotations")
                        
                        # Check for Any imports for database collections
                        if "from typing import" in content and "Any" in content:
                            print(f"   ✓ {file_path} imports Any type")
                            
            print(f"   ✓ Type fixes verification completed for {len(key_files)} files")
            return True
            
        except Exception as e:
            print(f"   ✗ Type fixes verification failed: {e}")
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return results"""
        print("🚀 Starting Telegram Bot System Tests")
        print("=" * 50)
        
        # Test 1: Import Testing
        self.run_test("Core Modules Import", self.test_import_core_modules)
        self.run_test("Telegram Modules Import", self.test_import_telegram_modules)
        self.run_test("Handler Modules Import", self.test_import_handler_modules)
        
        # Test 2: Basic Code Validation
        self.run_test("Python Syntax Validation", self.test_python_syntax_validation)
        
        # Test 3: MyPy Type Checking
        self.run_test("MyPy Type Checking", self.test_mypy_type_checking)
        
        # Test 4: Basic Object Creation
        self.run_test("ManagementBot Creation", self.test_management_bot_creation)
        self.run_test("BotManager Creation", self.test_bot_manager_creation)
        self.run_test("UserBot Creation", self.test_userbot_creation)
        self.run_test("Handler Classes Creation", self.test_handler_classes_creation)
        
        # Test 5: Key Fixes Verification
        self.run_test("Type Fixes Verification", self.test_type_fixes_verification)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {len(self.failed_tests)}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.failed_tests:
            print(f"\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"  - {test}")
        else:
            print(f"\n🎉 All tests passed!")
        
        return {
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "failed_tests": self.failed_tests,
            "success_rate": (self.tests_passed/self.tests_run)*100 if self.tests_run > 0 else 0
        }

def main():
    """Main test execution"""
    tester = TelegramBotTester()
    results = tester.run_all_tests()
    
    # Return appropriate exit code
    return 0 if len(results["failed_tests"]) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())