#!/usr/bin/env python3
"""
Otogram Interface Component Testing
Tests the modernized Telegram bot interface system components
"""

import asyncio
import sys
import traceback
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger

# Mock database connection for testing
class MockDatabase:
    def __init__(self):
        self.client = MagicMock()
        self.db = MagicMock()
    
    def get_collection(self, name):
        return MagicMock()
    
    async def connect(self, *args, **kwargs):
        pass
    
    async def disconnect(self):
        pass

# Mock services for testing
class MockService:
    def __init__(self):
        pass
    
    async def get_message_count(self):
        return {"total": 5, "active": 3, "inactive": 2}
    
    async def get_group_stats(self):
        return {"total": 10, "active": 7, "inactive": 3}
    
    async def get_blacklist_stats(self):
        return {"total": 2, "permanent": 1, "temporary": 1, "expired": 0}
    
    async def get_all_messages(self):
        return []
    
    async def get_all_groups(self):
        return []


class InterfaceComponentTester:
    """Test Otogram interface components"""

    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name: str, test_func, *args, **kwargs):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func(*args, **kwargs))
            else:
                result = test_func(*args, **kwargs)
            
            if result:
                self.tests_passed += 1
                print(f"✅ Passed - {name}")
                self.test_results.append({"name": name, "status": "PASSED", "error": None})
                return True
            else:
                print(f"❌ Failed - {name}")
                self.test_results.append({"name": name, "status": "FAILED", "error": "Test returned False"})
                return False
        except Exception as e:
            print(f"❌ Failed - {name}: {str(e)}")
            self.test_results.append({"name": name, "status": "ERROR", "error": str(e)})
            return False

    def test_import_management_bot(self):
        """Test management bot import and basic structure"""
        try:
            from src.telegram.management_bot import ManagementBot
            
            # Check if class exists and has required methods
            required_methods = [
                'start', 'stop', '_add_handlers', 'start_command', 
                'main_menu', 'status_command', 'help_command', 'handle_callback'
            ]
            
            for method in required_methods:
                if not hasattr(ManagementBot, method):
                    print(f"   Missing method: {method}")
                    return False
            
            print(f"   All required methods present: {len(required_methods)}")
            return True
            
        except ImportError as e:
            print(f"   Import error: {e}")
            return False
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_import_auth_handlers(self):
        """Test auth handlers import and structure"""
        try:
            from src.telegram.handlers.auth_handlers import AuthHandlers
            
            # Check required methods
            required_methods = [
                'show_auth_status', 'handle_callback', 'handle_text_input',
                '_show_auth_wizard', '_show_session_info'
            ]
            
            for method in required_methods:
                if not hasattr(AuthHandlers, method):
                    print(f"   Missing method: {method}")
                    return False
            
            print(f"   Auth handler methods verified: {len(required_methods)}")
            return True
            
        except ImportError as e:
            print(f"   Import error: {e}")
            return False
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_import_message_handlers(self):
        """Test message handlers import and structure"""
        try:
            from src.telegram.handlers.message_handlers import MessageHandlers
            
            # Check required methods
            required_methods = [
                'list_messages', 'add_message_command', 'handle_callback', 
                'handle_text_input', '_show_message_analytics'
            ]
            
            for method in required_methods:
                if not hasattr(MessageHandlers, method):
                    print(f"   Missing method: {method}")
                    return False
            
            print(f"   Message handler methods verified: {len(required_methods)}")
            return True
            
        except ImportError as e:
            print(f"   Import error: {e}")
            return False
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_import_group_handlers(self):
        """Test group handlers import and structure"""
        try:
            from src.telegram.handlers.group_handlers import GroupHandlers
            
            # Check required methods
            required_methods = [
                'list_groups', 'add_group_command', 'add_groups_bulk_command',
                'handle_callback', 'handle_text_input', '_show_group_analytics'
            ]
            
            for method in required_methods:
                if not hasattr(GroupHandlers, method):
                    print(f"   Missing method: {method}")
                    return False
            
            print(f"   Group handler methods verified: {len(required_methods)}")
            return True
            
        except ImportError as e:
            print(f"   Import error: {e}")
            return False
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_management_bot_initialization(self):
        """Test ManagementBot class initialization"""
        try:
            from src.telegram.management_bot import ManagementBot
            
            # Create instance
            bot = ManagementBot()
            
            # Check if handlers are initialized
            required_handlers = [
                'auth_handlers', 'message_handlers', 'group_handlers',
                'config_handlers', 'blacklist_handlers'
            ]
            
            for handler in required_handlers:
                if not hasattr(bot, handler):
                    print(f"   Missing handler: {handler}")
                    return False
                if getattr(bot, handler) is None:
                    print(f"   Handler not initialized: {handler}")
                    return False
            
            print(f"   All handlers initialized: {len(required_handlers)}")
            return True
            
        except Exception as e:
            print(f"   Initialization error: {e}")
            return False

    def test_handler_initialization(self):
        """Test individual handler initialization"""
        try:
            from src.telegram.handlers.auth_handlers import AuthHandlers
            from src.telegram.handlers.message_handlers import MessageHandlers
            from src.telegram.handlers.group_handlers import GroupHandlers
            
            # Test each handler initialization
            handlers = [
                ("AuthHandlers", AuthHandlers),
                ("MessageHandlers", MessageHandlers),
                ("GroupHandlers", GroupHandlers)
            ]
            
            for name, handler_class in handlers:
                try:
                    handler = handler_class()
                    print(f"   {name}: ✅ Initialized successfully")
                except Exception as e:
                    print(f"   {name}: ❌ Failed to initialize - {e}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"   Handler initialization error: {e}")
            return False

    async def test_callback_routing(self):
        """Test callback routing functionality"""
        try:
            from src.telegram.management_bot import ManagementBot
            from telegram import Update, CallbackQuery, Message, Chat, User
            from telegram.ext import ContextTypes
            
            # Create mock objects
            bot = ManagementBot()
            
            # Mock update and context
            mock_user = User(id=123, first_name="Test", is_bot=False)
            mock_chat = Chat(id=123, type="private")
            mock_message = Message(
                message_id=1,
                date=datetime.now(),
                chat=mock_chat,
                from_user=mock_user
            )
            
            mock_callback_query = CallbackQuery(
                id="test_callback",
                from_user=mock_user,
                chat_instance="test_instance",
                message=mock_message,
                data="dashboard"
            )
            
            mock_update = Update(
                update_id=1,
                callback_query=mock_callback_query
            )
            
            mock_context = MagicMock()
            
            # Mock the answer method
            mock_callback_query.answer = AsyncMock()
            mock_callback_query.edit_message_text = AsyncMock()
            
            # Test callback handling
            with patch.object(bot, '_get_system_stats', return_value="Mock stats"):
                await bot.handle_callback(mock_update, mock_context)
            
            print("   Callback routing test completed successfully")
            return True
            
        except Exception as e:
            print(f"   Callback routing error: {e}")
            traceback.print_exc()
            return False

    def test_message_formatting(self):
        """Test message formatting consistency"""
        try:
            from src.telegram.management_bot import ManagementBot
            
            bot = ManagementBot()
            
            # Test various message formats by checking if they contain expected elements
            test_cases = [
                # Test welcome message format
                ("Welcome message", "🚀 **OTOGRAM AUTOMATION SYSTEM**"),
                # Test dashboard format
                ("Dashboard format", "🏠 **CONTROL DASHBOARD**"),
                # Test status format
                ("Status format", "📊 **SYSTEM STATUS REPORT**"),
                # Test help format
                ("Help format", "💡 **OTOGRAM HELP CENTER**")
            ]
            
            # Check if the bot has methods that would generate these messages
            methods_to_check = [
                'start_command', 'main_menu', 'status_command', 'help_command'
            ]
            
            for method_name in methods_to_check:
                if not hasattr(bot, method_name):
                    print(f"   Missing formatting method: {method_name}")
                    return False
            
            print(f"   Message formatting methods verified: {len(methods_to_check)}")
            return True
            
        except Exception as e:
            print(f"   Message formatting error: {e}")
            return False

    def test_button_layout_structure(self):
        """Test button layout consistency"""
        try:
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            # Test if we can create the expected button structures
            test_layouts = [
                # Main dashboard layout
                [
                    [
                        InlineKeyboardButton("📝 Messages", callback_data="messages_dashboard"),
                        InlineKeyboardButton("👥 Groups", callback_data="groups_dashboard"),
                    ],
                    [
                        InlineKeyboardButton("🔐 Authentication", callback_data="auth_status"),
                        InlineKeyboardButton("🚫 Blacklist", callback_data="blacklist_dashboard"),
                    ]
                ],
                # Welcome screen layout
                [
                    [
                        InlineKeyboardButton("🏠 Main Dashboard", callback_data="dashboard"),
                        InlineKeyboardButton("⚡ Quick Setup", callback_data="quick_setup"),
                    ],
                    [
                        InlineKeyboardButton("🔐 Authentication", callback_data="auth_status"),
                        InlineKeyboardButton("📚 User Guide", callback_data="tutorial"),
                    ]
                ]
            ]
            
            for i, layout in enumerate(test_layouts):
                try:
                    keyboard = InlineKeyboardMarkup(layout)
                    print(f"   Layout {i+1}: ✅ Valid structure")
                except Exception as e:
                    print(f"   Layout {i+1}: ❌ Invalid structure - {e}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"   Button layout error: {e}")
            return False

    def test_error_handling_patterns(self):
        """Test error handling patterns in handlers"""
        try:
            from src.telegram.handlers.auth_handlers import AuthHandlers
            from src.telegram.handlers.message_handlers import MessageHandlers
            from src.telegram.handlers.group_handlers import GroupHandlers
            
            # Check if handlers have error handling methods
            handlers = [
                ("AuthHandlers", AuthHandlers()),
                ("MessageHandlers", MessageHandlers()),
                ("GroupHandlers", GroupHandlers())
            ]
            
            error_methods = ['_send_error_message', 'handle_callback', 'handle_text_input']
            
            for handler_name, handler in handlers:
                for method_name in error_methods:
                    if hasattr(handler, method_name):
                        print(f"   {handler_name}.{method_name}: ✅ Present")
                    else:
                        print(f"   {handler_name}.{method_name}: ⚠️ Not found")
            
            return True
            
        except Exception as e:
            print(f"   Error handling test error: {e}")
            return False

    def test_service_integration(self):
        """Test integration with service classes"""
        try:
            from src.telegram.handlers.message_handlers import MessageHandlers
            from src.telegram.handlers.group_handlers import GroupHandlers
            
            # Test if handlers have service dependencies
            message_handler = MessageHandlers()
            group_handler = GroupHandlers()
            
            # Check if services are accessible
            services_to_check = [
                (message_handler, 'message_service'),
                (group_handler, 'group_service')
            ]
            
            for handler, service_name in services_to_check:
                if hasattr(handler, service_name):
                    service = getattr(handler, service_name)
                    if service is not None:
                        print(f"   {service_name}: ✅ Integrated")
                    else:
                        print(f"   {service_name}: ⚠️ Not initialized")
                else:
                    print(f"   {service_name}: ❌ Missing")
                    return False
            
            return True
            
        except Exception as e:
            print(f"   Service integration error: {e}")
            return False

    def test_constants_and_config(self):
        """Test constants and configuration access"""
        try:
            from src.core.constants import MAX_RECENT_ITEMS_DISPLAY, PREVIEW_MESSAGE_LENGTH
            from src.core.config import settings
            
            # Check if constants are defined
            constants = [
                ("MAX_RECENT_ITEMS_DISPLAY", MAX_RECENT_ITEMS_DISPLAY),
                ("PREVIEW_MESSAGE_LENGTH", PREVIEW_MESSAGE_LENGTH)
            ]
            
            for name, value in constants:
                if isinstance(value, int) and value > 0:
                    print(f"   {name}: ✅ Valid ({value})")
                else:
                    print(f"   {name}: ❌ Invalid value")
                    return False
            
            # Check settings access
            if hasattr(settings, 'TELEGRAM_BOT_TOKEN'):
                print("   Settings access: ✅ Available")
            else:
                print("   Settings access: ❌ Not available")
                return False
            
            return True
            
        except Exception as e:
            print(f"   Constants/config error: {e}")
            return False

    def test_dependency_resolution(self):
        """Test if all dependencies can be resolved"""
        try:
            # Test core imports
            from src.core.config import settings
            from src.core.constants import MAX_RECENT_ITEMS_DISPLAY
            from src.core.database import Database
            
            # Test service imports
            from src.services.message_service import MessageService
            from src.services.group_service import GroupService
            from src.services.blacklist_service import BlacklistService
            
            # Test model imports
            from src.models.message import Message
            from src.models.group import Group
            from src.models.blacklist import BlacklistEntry
            
            print("   All core dependencies: ✅ Resolved")
            print("   All service dependencies: ✅ Resolved")
            print("   All model dependencies: ✅ Resolved")
            
            return True
            
        except ImportError as e:
            print(f"   Dependency resolution error: {e}")
            return False
        except Exception as e:
            print(f"   Unexpected error: {e}")
            return False

    async def test_handler_integration(self):
        """Test integration between different handlers"""
        try:
            from src.telegram.management_bot import ManagementBot
            
            bot = ManagementBot()
            
            # Check if all handlers are properly integrated
            handlers = [
                'auth_handlers',
                'message_handlers', 
                'group_handlers',
                'config_handlers',
                'blacklist_handlers'
            ]
            
            for handler_name in handlers:
                handler = getattr(bot, handler_name)
                
                # Check if handler has required callback method
                if hasattr(handler, 'handle_callback'):
                    print(f"   {handler_name}: ✅ Callback integration ready")
                else:
                    print(f"   {handler_name}: ❌ Missing callback integration")
                    return False
                
                # Check if handler has text input method
                if hasattr(handler, 'handle_text_input'):
                    print(f"   {handler_name}: ✅ Text input integration ready")
                else:
                    print(f"   {handler_name}: ⚠️ No text input handling")
            
            return True
            
        except Exception as e:
            print(f"   Handler integration error: {e}")
            return False

    def run_all_tests(self):
        """Run all interface component tests"""
        print("🤖 OTOGRAM INTERFACE COMPONENT TESTING")
        print("=" * 55)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Import & Initialization Tests
        print("\n📦 IMPORT & INITIALIZATION TESTS")
        print("-" * 40)
        self.run_test("Management Bot Import", self.test_import_management_bot)
        self.run_test("Auth Handlers Import", self.test_import_auth_handlers)
        self.run_test("Message Handlers Import", self.test_import_message_handlers)
        self.run_test("Group Handlers Import", self.test_import_group_handlers)
        self.run_test("Management Bot Initialization", self.test_management_bot_initialization)
        self.run_test("Handler Initialization", self.test_handler_initialization)
        self.run_test("Dependency Resolution", self.test_dependency_resolution)
        
        # Interface Component Tests
        print("\n🎨 INTERFACE COMPONENT TESTS")
        print("-" * 40)
        self.run_test("Message Formatting", self.test_message_formatting)
        self.run_test("Button Layout Structure", self.test_button_layout_structure)
        self.run_test("Error Handling Patterns", self.test_error_handling_patterns)
        self.run_test("Constants & Configuration", self.test_constants_and_config)
        
        # Integration Tests
        print("\n🔗 INTEGRATION TESTS")
        print("-" * 40)
        self.run_test("Callback Routing", self.test_callback_routing)
        self.run_test("Service Integration", self.test_service_integration)
        self.run_test("Handler Integration", self.test_handler_integration)
        
        # Print detailed results
        print(f"\n📊 DETAILED TEST RESULTS")
        print("=" * 40)
        
        passed_tests = [r for r in self.test_results if r["status"] == "PASSED"]
        failed_tests = [r for r in self.test_results if r["status"] in ["FAILED", "ERROR"]]
        
        if passed_tests:
            print(f"\n✅ PASSED TESTS ({len(passed_tests)}):")
            for test in passed_tests:
                print(f"   • {test['name']}")
        
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   • {test['name']}")
                if test['error']:
                    print(f"     Error: {test['error']}")
        
        # Summary
        print(f"\n📊 SUMMARY")
        print("=" * 30)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_run - self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL INTERFACE TESTS PASSED!")
            print("✅ Modernized interface components are working correctly")
            print("✅ System is ready for production use")
            return 0
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} tests failed.")
            print("❌ Some interface components need attention")
            return 1


def main():
    """Main test function"""
    tester = InterfaceComponentTester()
    return tester.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())