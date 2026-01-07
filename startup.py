#!/usr/bin/env python3
"""
Startup script for Documentation Download Agent
Handles initialization and provides seamless startup experience
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path


def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "aiohttp",
        "beautifulsoup4",
        "lxml",
        "aiofiles",
        "typing_extensions",
    ]

    missing_packages = []
    for package in required_packages:
        spec = importlib.util.find_spec(package.replace("-", "_"))
        if spec is None:
            missing_packages.append(package)

    if missing_packages:
        print("[*] Installing missing dependencies...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + missing_packages
        )
        print("[+] All dependencies installed successfully")


def create_directories():
    """Create necessary directories"""
    directories = ["static", "templates", "downloads", "downloads/archives"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def main():
    """Main startup function"""
    print("[*] Initializing Documentation Download Agent...")

    check_dependencies()
    create_directories()

    print("[+] Starting server on http://localhost:8001")
    print("[*] Press Ctrl+C to stop the server")
    print("=" * 50)

    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n[*] Server stopped by user")
    except Exception as e:
        print(f"[!] Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
