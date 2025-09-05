#!/usr/bin/env python3
"""
Otogram System Monitor
Real-time monitoring script for Otogram system
"""

import asyncio
import subprocess
import time
from datetime import datetime

import requests

from src.core.config import settings
from src.core.database import database


class OtogramMonitor:
    """System monitor for Otogram"""

    def __init__(self):
        self.start_time = datetime.now()

    def check_process(self) -> bool:
        """Check if main process is running"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "python main.py"], capture_output=True, text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def check_bot_api(self) -> dict:
        """Check bot API connectivity"""
        try:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getMe"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data.get("ok"):
                bot_info = data["result"]
                return {
                    "status": "✅ ONLINE",
                    "name": bot_info["first_name"],
                    "username": f"@{bot_info['username']}",
                    "id": bot_info["id"],
                }
            else:
                return {"status": "❌ ERROR", "error": data}
        except Exception as e:
            return {"status": "❌ FAILED", "error": str(e)}

    async def check_database(self) -> dict:
        """Check database connectivity"""
        try:
            await database.connect()
            ping_ok = await database.ping()

            if ping_ok:
                collections = await database.list_collections()
                stats = {
                    "messages": await database.get_collection_size("messages"),
                    "groups": await database.get_collection_size("groups"),
                    "blacklists": await database.get_collection_size("blacklists"),
                }
                await database.disconnect()

                return {
                    "status": "✅ CONNECTED",
                    "collections": len(collections),
                    "stats": stats,
                }
            else:
                return {"status": "❌ PING FAILED"}

        except Exception as e:
            return {"status": "❌ ERROR", "error": str(e)}

    def get_system_uptime(self) -> str:
        """Get system uptime"""
        uptime = datetime.now() - self.start_time
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        return f"{hours}h {minutes}m"

    def get_recent_logs(self, lines: int = 5) -> list:
        """Get recent log entries"""
        try:
            with open("server.log", "r") as f:
                log_lines = f.readlines()
                return [line.strip() for line in log_lines[-lines:]]
        except Exception:
            return ["No logs available"]

    async def full_system_check(self) -> dict:
        """Comprehensive system check"""
        print("🔍 OTOGRAM SYSTEM MONITOR")
        print("=" * 50)
        print(f"📅 Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  Monitor Uptime: {self.get_system_uptime()}")
        print()

        # Process check
        process_running = self.check_process()
        print(f"🔄 Main Process: {'✅ RUNNING' if process_running else '❌ STOPPED'}")

        # Bot API check
        print("🤖 Bot API Check:")
        bot_status = self.check_bot_api()
        if bot_status["status"] == "✅ ONLINE":
            print(f"   Name: {bot_status['name']}")
            print(f"   Username: {bot_status['username']}")
            print(f"   Status: {bot_status['status']}")
        else:
            print(f"   Status: {bot_status['status']}")
            if "error" in bot_status:
                print(f"   Error: {bot_status['error']}")

        # Database check
        print("🗄️  Database Check:")
        db_status = await self.check_database()
        if db_status["status"] == "✅ CONNECTED":
            print(f"   Status: {db_status['status']}")
            print(f"   Collections: {db_status['collections']}")
            print("   Data:")
            for collection, count in db_status["stats"].items():
                print(f"     {collection}: {count} documents")
        else:
            print(f"   Status: {db_status['status']}")
            if "error" in db_status:
                print(f"   Error: {db_status['error']}")

        # Recent logs
        print("\n📋 Recent Logs:")
        recent_logs = self.get_recent_logs(3)
        for log in recent_logs:
            print(f"   {log}")

        # System recommendations
        print("\n💡 System Status:")
        if process_running and bot_status["status"] == "✅ ONLINE":
            if db_status["status"] == "✅ CONNECTED":
                print("   🟢 EXCELLENT: All systems operational")
                print("   📱 Ready for authentication: Send /auth to @otogrambot")
            else:
                print("   🟠 WARNING: Database issues detected")
        else:
            print("   🔴 CRITICAL: Core services not running")

        return {
            "process": process_running,
            "bot": bot_status,
            "database": db_status,
            "uptime": self.get_system_uptime(),
        }

    async def continuous_monitor(self, interval: int = 30):
        """Continuous monitoring mode"""
        print("🔄 Starting continuous monitoring...")
        print(f"📊 Checking every {interval} seconds (Ctrl+C to stop)")
        print("=" * 50)

        try:
            while True:
                await self.full_system_check()
                print(f"\n⏳ Next check in {interval} seconds...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")


async def main():
    """Main monitoring function"""
    monitor = OtogramMonitor()

    # Single check
    await monitor.full_system_check()

    # Ask for continuous monitoring
    response = input("\n🔄 Start continuous monitoring? (y/N): ")
    if response.lower() in ["y", "yes"]:
        interval = input("📊 Check interval in seconds (default 30): ")
        try:
            interval = int(interval) if interval else 30
        except ValueError:
            interval = 30
        await monitor.continuous_monitor(interval)


if __name__ == "__main__":
    asyncio.run(main())