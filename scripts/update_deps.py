#!/usr/bin/env python3
"""
Dependency Update Checker
Checks for outdated dependencies and suggests updates
"""

import subprocess
import sys
from pathlib import Path


def check_outdated_packages() -> bool:
    """Check for outdated packages"""
    print("🔍 Checking for outdated packages...")

    try:
        result = subprocess.run(
            ["pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True,
            check=True,
        )

        import json

        outdated = json.loads(result.stdout)

        if not outdated:
            print("✅ All packages are up to date!")
            return True

        print(f"📦 Found {len(outdated)} outdated packages:")
        print("\nPackage                Current    Latest")
        print("-" * 45)

        for pkg in outdated:
            name = pkg["name"]
            current = pkg["version"]
            latest = pkg["latest_version"]
            print(f"{name:<20} {current:<10} {latest}")

        return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking packages: {e}")
        return False
    except json.JSONDecodeError:
        print("❌ Error parsing pip output")
        return False


def check_security_vulnerabilities() -> bool:
    """Check for security vulnerabilities in dependencies"""
    print("\n🔒 Checking for security vulnerabilities...")

    try:
        # Try safety check
        result = subprocess.run(
            ["safety", "check", "--json"], check=False, capture_output=True, text=True
        )

        if result.returncode == 0:
            print("✅ No known security vulnerabilities found!")
            return True
        else:
            print("⚠️ Security vulnerabilities detected:")
            print(result.stdout)
            return False

    except FileNotFoundError:
        print("⚠️ Safety not installed. Install with: pip install safety")
        return True  # Don't fail if safety not available
    except Exception as e:
        print(f"❌ Error running security check: {e}")
        return True


def suggest_updates():
    """Suggest dependency updates"""
    print("\n💡 Dependency Update Suggestions:")
    print("=" * 50)

    suggestions = [
        "1. Review outdated packages above",
        "2. Check changelogs for breaking changes",
        "3. Test updates in development environment first",
        "4. Update pyproject.toml with new versions",
        "5. Run tests after updating",
        "6. Commit updates with clear message",
    ]

    for suggestion in suggestions:
        print(f"   {suggestion}")

    print("\n🚨 Important Notes:")
    print("   • Always test updates thoroughly")
    print("   • Pin specific versions in pyproject.toml")
    print("   • Monitor for compatibility issues")
    print("   • Keep security updates prioritized")


def main():
    """Main dependency update checker"""
    print("🔄 DEPENDENCY UPDATE CHECKER")
    print("=" * 40)

    # Check current directory
    if not Path("pyproject.toml").exists():
        print("❌ pyproject.toml not found. Run from project root.")
        sys.exit(1)

    # Check outdated packages
    packages_ok = check_outdated_packages()

    # Check security
    security_ok = check_security_vulnerabilities()

    # Show suggestions
    if not packages_ok:
        suggest_updates()

    # Summary
    print("\n📊 Summary:")
    print(f"   Packages up to date: {'✅' if packages_ok else '❌'}")
    print(f"   Security status: {'✅' if security_ok else '⚠️'}")

    if packages_ok and security_ok:
        print("\n🎉 All dependencies are up to date and secure!")
        return 0
    else:
        print("\n⚠️ Consider updating dependencies")
        return 1


if __name__ == "__main__":
    sys.exit(main())
