#!/usr/bin/env python3
"""
Auto-fix common linting issues for Otogram project
"""

import subprocess
from pathlib import Path


def run_command(cmd: list[str], description: str = "") -> bool:
    """Run a command and return success status"""
    print(f"Running: {' '.join(cmd)}")
    if description:
        print(f"Description: {description}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Success")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed with code {e.returncode}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False


def main():
    """Fix common linting issues"""
    print("🔧 Auto-fixing linting issues for Otogram...")

    # Change to project root
    project_root = Path(__file__).parent.parent
    print(f"Working in: {project_root}")

    # 1. Run ruff with --fix to auto-fix issues
    print("\n1. Running ruff --fix...")
    success = run_command(
        ["ruff", "check", "--fix", "src/", "scripts/", "tests/", "--config", "pyproject.toml"],
        "Auto-fix ruff issues",
    )

    if not success:
        print("⚠️  Some ruff issues could not be auto-fixed")

    # 2. Run ruff format
    print("\n2. Running ruff format...")
    run_command(["ruff", "format", "src/", "scripts/", "tests/"], "Format code with ruff")

    # 3. Show remaining issues
    print("\n3. Checking for remaining issues...")
    result = subprocess.run(
        ["ruff", "check", "src/", "scripts/", "tests/", "--config", "pyproject.toml"],
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✅ All linting issues fixed!")
    else:
        print("⚠️  Some issues remain:")
        print(result.stdout)
        print("\nThese issues need manual review.")

    print("\n🎉 Linting fix complete!")


if __name__ == "__main__":
    main()
