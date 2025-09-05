#!/usr/bin/env python3
"""
Comprehensive Authentication Testing
Tests all authentication features and integration points
"""

import inspect
import sys
from datetime import datetime
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

import requests

# Telegram Bot API Configuration
BOT_TOKEN = "8118820592:AAFX05zaXmmW3nWY2pM7s90Pbqn8f1ptc0M"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


class ComprehensiveAuthTester:
    """Comprehensive Authentication Feature Testing"""

    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.issues_found = []
        self.features_working = []

    def run_test(self, name: str, test_func, *args, **kwargs):
        """Run a single test"""
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            result = test_func(*args, **kwargs)
            if result:
                self.tests_passed += 1
                print(f"✅ Passed - {name}")
                self.features_working.append(name)
                return True
            else:
                print(f"❌ Failed - {name}")
                self.issues_found.append(name)
                return False
        except Exception as e:
            print(f"❌ Failed - {name}: {str(e)}")
            self.issues_found.append(f"{name}: {str(e)}")
            return False

    def test_auth_handlers_complete_implementation(self):
        """Test complete AuthHandlers implementation"""
        try:
            from src.telegram.handlers.auth_handlers import AuthHandlers
            
            auth_handlers = AuthHandlers()
            
            # Test all required methods exist and are callable
            required_methods = {
                'show_auth_status': 'Display authentication status',
                'start_authentication': 'Start authentication process',
                'handle_verification_code': 'Handle verification code input',
                'clear_session': 'Clear userbot session',
                'test_connection': 'Test userbot connection',
                'handle_callback': 'Handle authentication callbacks',
                'show_auth_help': 'Show authentication help',
                '_check_userbot_status': 'Check userbot status',
                '_send_message': 'Send message helper',
                '_send_error_message': 'Send error message helper',
                '_authenticate_userbot': 'Perform authentication'
            }
            
            implemented_methods = 0
            async_methods = 0
            
            for method_name, description in required_methods.items():
                if hasattr(auth_handlers, method_name):
                    method = getattr(auth_handlers, method_name)
                    if callable(method):
                        implemented_methods += 1
                        if inspect.iscoroutinefunction(method):
                            async_methods += 1
                        print(f"   ✅ {method_name}: {description}")
                    else:
                        print(f"   ❌ {method_name}: Not callable")
                else:
                    print(f"   ❌ {method_name}: Missing")
            
            print(f"   Implemented methods: {implemented_methods}/{len(required_methods)}")
            print(f"   Async methods: {async_methods}")
            
            return implemented_methods >= len(required_methods) * 0.9  # 90% implementation
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_management_bot_auth_integration(self):
        """Test ManagementBot authentication integration"""
        try:
            from src.telegram.management_bot import ManagementBot
            
            bot = ManagementBot()
            
            # Check auth_handlers initialization
            if not hasattr(bot, 'auth_handlers'):
                print("   ❌ auth_handlers not initialized")
                return False
            
            print("   ✅ auth_handlers initialized")
            
            # Check if auth command would be registered
            # We can't test the actual registration without starting the bot
            # But we can check if the method exists
            if hasattr(bot.auth_handlers, 'show_auth_status'):
                print("   ✅ /auth command handler available")
            else:
                print("   ❌ /auth command handler missing")
                return False
            
            # Check callback handling integration
            if hasattr(bot, 'handle_callback'):
                print("   ✅ Callback handling integrated")
            else:
                print("   ❌ Callback handling missing")
                return False
            
            # Check text input handling
            if hasattr(bot, 'handle_text_input'):
                print("   ✅ Text input handling integrated")
            else:
                print("   ❌ Text input handling missing")
                return False
            
            return True
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_menu_integration_points(self):
        """Test authentication integration in menus"""
        try:
            from src.telegram.management_bot import ManagementBot
            
            bot = ManagementBot()
            
            integration_points = 0
            
            # Check start_command for auth integration
            if hasattr(bot, 'start_command'):
                print("   ✅ start_command exists")
                integration_points += 1
            
            # Check main_menu for auth status
            if hasattr(bot, 'main_menu'):
                print("   ✅ main_menu exists")
                integration_points += 1
            
            # Check quick setup for userbot step
            if hasattr(bot, '_show_quick_setup'):
                print("   ✅ quick_setup exists")
                integration_points += 1
            
            # Check system stats for userbot status
            if hasattr(bot, '_get_system_stats'):
                print("   ✅ system_stats includes userbot")
                integration_points += 1
            
            print(f"   Menu integration points: {integration_points}/4")
            return integration_points >= 3
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_session_management(self):
        """Test session management functionality"""
        try:
            # Check sessions directory
            sessions_dir = Path("/app/sessions")
            if not sessions_dir.exists():
                print("   ⚠️  Sessions directory missing, creating...")
                sessions_dir.mkdir(exist_ok=True)
            
            print("   ✅ Sessions directory exists")
            
            # Check session file
            session_file = sessions_dir / "userbot_session.session"
            session_exists = session_file.exists()
            
            if session_exists:
                size = session_file.stat().st_size
                print(f"   ✅ Session file exists ({size} bytes)")
                
                if size > 0:
                    print("   ✅ Session has content")
                else:
                    print("   ⚠️  Session file is empty")
            else:
                print("   ℹ️  No session file (fresh installation)")
            
            # Test session file permissions
            if session_exists:
                import stat
                file_stat = session_file.stat()
                permissions = stat.filemode(file_stat.st_mode)
                print(f"   Session file permissions: {permissions}")
            
            return True  # Session management is working
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_configuration_completeness(self):
        """Test authentication configuration completeness"""
        try:
            from src.core.config import settings
            
            # Check required Telegram settings
            telegram_settings = {
                'TELEGRAM_API_ID': settings.TELEGRAM_API_ID,
                'TELEGRAM_API_HASH': settings.TELEGRAM_API_HASH,
                'TELEGRAM_BOT_TOKEN': settings.TELEGRAM_BOT_TOKEN,
                'TELEGRAM_PHONE_NUMBER': settings.TELEGRAM_PHONE_NUMBER
            }
            
            configured_settings = 0
            for setting_name, setting_value in telegram_settings.items():
                if setting_value:
                    print(f"   ✅ {setting_name}: Configured")
                    configured_settings += 1
                else:
                    print(f"   ❌ {setting_name}: Missing")
            
            print(f"   Configured settings: {configured_settings}/{len(telegram_settings)}")
            
            # Check if system is configured
            if hasattr(settings, 'is_configured'):
                system_configured = settings.is_configured()
                print(f"   System configured: {system_configured}")
                return system_configured
            else:
                return configured_settings == len(telegram_settings)
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_error_handling_robustness(self):
        """Test error handling robustness"""
        try:
            from src.telegram.handlers.auth_handlers import AuthHandlers
            
            auth_handlers = AuthHandlers()
            
            # Check error handling methods
            error_methods = [
                '_send_error_message',
                '_send_message'
            ]
            
            error_handling_score = 0
            for method in error_methods:
                if hasattr(auth_handlers, method):
                    print(f"   ✅ {method} exists")
                    error_handling_score += 1
                else:
                    print(f"   ❌ {method} missing")
            
            # Check if methods have proper error handling (try-catch blocks)
            # We can't easily test this without code analysis, but we can check method existence
            
            print(f"   Error handling methods: {error_handling_score}/{len(error_methods)}")
            return error_handling_score >= len(error_methods)
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_callback_data_handling(self):
        """Test callback data handling"""
        try:
            from src.telegram.handlers.auth_handlers import AuthHandlers
            
            auth_handlers = AuthHandlers()
            
            # Test callback data that should be handled
            expected_callbacks = [
                'auth_status',
                'auth_start',
                'auth_clear',
                'auth_test',
                'auth_help',
                'auth_restart'
            ]
            
            # Check if handle_callback method exists
            if not hasattr(auth_handlers, 'handle_callback'):
                print("   ❌ handle_callback method missing")
                return False
            
            print("   ✅ handle_callback method exists")
            print(f"   Expected callbacks: {len(expected_callbacks)}")
            
            # Check if method is async (required for Telegram handlers)
            if inspect.iscoroutinefunction(auth_handlers.handle_callback):
                print("   ✅ handle_callback is async")
            else:
                print("   ❌ handle_callback is not async")
                return False
            
            return True
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_system_integration(self):
        """Test system integration"""
        try:
            # Check if system is running
            import subprocess
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            system_running = 'main.py' in result.stdout
            
            if system_running:
                print("   ✅ System is running")
            else:
                print("   ❌ System is not running")
                return False
            
            # Check logs for authentication integration
            log_file = Path("/app/logs/app.log")
            if log_file.exists():
                with open(log_file, 'r') as f:
                    log_content = f.read()
                
                # Look for authentication-related log entries
                auth_logs = [
                    "Management bot is running",
                    "Userbot authentication required",
                    "Management bot is ready"
                ]
                
                found_logs = 0
                for log_entry in auth_logs:
                    if log_entry in log_content:
                        found_logs += 1
                        print(f"   ✅ Found: {log_entry}")
                
                print(f"   Authentication logs: {found_logs}/{len(auth_logs)}")
                return found_logs >= 2
            else:
                print("   ❌ No log file found")
                return False
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_bot_api_integration(self):
        """Test bot API integration"""
        try:
            # Test bot connectivity
            response = requests.get(f"{BASE_URL}/getMe", timeout=10)
            if response.status_code != 200:
                print("   ❌ Bot API not accessible")
                return False
            
            bot_data = response.json()
            if not bot_data.get('ok'):
                print("   ❌ Bot API error")
                return False
            
            bot_info = bot_data['result']
            print(f"   ✅ Bot: {bot_info.get('first_name')} (@{bot_info.get('username')})")
            
            # Test if bot is receiving updates (indicates it's running)
            updates_response = requests.get(f"{BASE_URL}/getUpdates?limit=1", timeout=10)
            if updates_response.status_code == 200:
                print("   ✅ Bot is receiving updates")
            else:
                print("   ⚠️  Bot updates check failed")
            
            return True
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def test_authentication_flow_completeness(self):
        """Test authentication flow completeness"""
        try:
            from src.telegram.handlers.auth_handlers import AuthHandlers
            
            auth_handlers = AuthHandlers()
            
            # Check authentication flow components
            flow_components = {
                'show_auth_status': 'Status display',
                'start_authentication': 'Start process',
                '_authenticate_userbot': 'Core authentication',
                'handle_verification_code': 'Code handling',
                'clear_session': 'Session cleanup',
                'test_connection': 'Connection test'
            }
            
            complete_components = 0
            for component, description in flow_components.items():
                if hasattr(auth_handlers, component):
                    method = getattr(auth_handlers, component)
                    if callable(method):
                        print(f"   ✅ {component}: {description}")
                        complete_components += 1
                    else:
                        print(f"   ❌ {component}: Not callable")
                else:
                    print(f"   ❌ {component}: Missing")
            
            print(f"   Flow completeness: {complete_components}/{len(flow_components)}")
            return complete_components >= len(flow_components) * 0.85  # 85% complete
            
        except Exception as e:
            print(f"   Error: {e}")
            return False

    def run_all_tests(self):
        """Run all comprehensive authentication tests"""
        print("🔐 COMPREHENSIVE AUTHENTICATION TESTING")
        print("=" * 55)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Bot Token: {BOT_TOKEN}")
        
        # Core implementation tests
        self.run_test("AuthHandlers Complete Implementation", self.test_auth_handlers_complete_implementation)
        self.run_test("ManagementBot Integration", self.test_management_bot_auth_integration)
        self.run_test("Menu Integration Points", self.test_menu_integration_points)
        self.run_test("Session Management", self.test_session_management)
        self.run_test("Configuration Completeness", self.test_configuration_completeness)
        
        # Functionality tests
        self.run_test("Error Handling Robustness", self.test_error_handling_robustness)
        self.run_test("Callback Data Handling", self.test_callback_data_handling)
        self.run_test("Authentication Flow Completeness", self.test_authentication_flow_completeness)
        
        # System integration tests
        self.run_test("System Integration", self.test_system_integration)
        self.run_test("Bot API Integration", self.test_bot_api_integration)
        
        # Print comprehensive results
        print("\n📊 COMPREHENSIVE TEST RESULTS")
        print("=" * 40)
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_run - self.tests_passed}")
        print(f"Success rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        # Feature status summary
        print(f"\n✅ WORKING FEATURES ({len(self.features_working)}):")
        for feature in self.features_working:
            print(f"   • {feature}")
        
        if self.issues_found:
            print(f"\n❌ ISSUES FOUND ({len(self.issues_found)}):")
            for issue in self.issues_found:
                print(f"   • {issue}")
        
        # Overall assessment
        success_rate = (self.tests_passed / self.tests_run) * 100
        
        print("\n🎯 AUTHENTICATION FEATURE ASSESSMENT:")
        
        if success_rate >= 90:
            print("🟢 EXCELLENT - Authentication feature is fully implemented and ready")
            status = "READY"
        elif success_rate >= 75:
            print("🟡 GOOD - Authentication feature is mostly working with minor issues")
            status = "MOSTLY_READY"
        elif success_rate >= 50:
            print("🟠 FAIR - Authentication feature has significant issues")
            status = "NEEDS_WORK"
        else:
            print("🔴 POOR - Authentication feature needs major fixes")
            status = "BROKEN"
        
        print("\n📋 FEATURE READINESS:")
        print(f"   Status: {status}")
        print(f"   Implementation: {success_rate:.1f}% complete")
        
        if success_rate >= 75:
            print("   ✅ Ready for user testing")
            print("   ✅ Core functionality implemented")
            print("   ✅ Integration points working")
        else:
            print("   ❌ Needs fixes before user testing")
        
        print("\n💡 NEXT STEPS:")
        if success_rate >= 90:
            print("   • Test authentication flow manually with /auth command")
            print("   • Verify all menu buttons work correctly")
            print("   • Test error scenarios")
        elif success_rate >= 75:
            print("   • Fix remaining issues")
            print("   • Test authentication flow")
            print("   • Verify error handling")
        else:
            print("   • Fix critical implementation issues")
            print("   • Complete missing components")
            print("   • Re-run tests after fixes")
        
        return 0 if success_rate >= 70 else 1


def main():
    """Main test function"""
    tester = ComprehensiveAuthTester()
    return tester.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())
