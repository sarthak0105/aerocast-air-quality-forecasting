#!/usr/bin/env python3
"""
Start frontend with live reload using Node.js live-server
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_node_and_live_server():
    """Check if Node.js and live-server are available"""
    try:
        # Check Node.js
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "Node.js not found"
        
        node_version = result.stdout.strip()
        print(f"✅ Node.js found: {node_version}")
        
        # Check live-server
        result = subprocess.run(["npx", "live-server", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("📦 Installing live-server...")
            install_result = subprocess.run(["npm", "install", "-g", "live-server"], capture_output=True)
            if install_result.returncode != 0:
                return False, "Failed to install live-server"
        
        print("✅ live-server available")
        return True, "Ready"
        
    except FileNotFoundError:
        return False, "Node.js not found"

def start_live_server():
    """Start live-server for frontend development"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🔥 AeroCast Frontend Live Server                         ║
║                                                              ║
║    Hot reload enabled for frontend development              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check prerequisites
    available, message = check_node_and_live_server()
    if not available:
        print(f"❌ {message}")
        print("\n💡 Alternative: Use 'python scripts/start_frontend_only.py'")
        return False
    
    # Change to static directory
    static_dir = Path("static")
    if not static_dir.exists():
        print("❌ Static directory not found!")
        return False
    
    print(f"📁 Serving files from: {static_dir.absolute()}")
    print("🌐 Frontend will be available at: http://localhost:8080")
    print("🔥 Live reload enabled - changes will auto-refresh")
    print("\n⚠️  Note: API calls will fail since backend is not running")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Start live-server
        os.chdir(static_dir)
        subprocess.run([
            "npx", "live-server", 
            "--port=8080",
            "--host=localhost",
            "--open=/index.html"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Live server stopped")
    except Exception as e:
        print(f"❌ Error starting live server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_live_server()