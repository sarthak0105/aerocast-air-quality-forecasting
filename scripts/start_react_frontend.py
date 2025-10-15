#!/usr/bin/env python3
"""
Start the React/TypeScript frontend (Next.js)
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_node_and_dependencies():
    """Check if Node.js is available and dependencies are installed"""
    try:
        # Check Node.js
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            return False, "Node.js not found"
        
        node_version = result.stdout.strip()
        print(f"✅ Node.js found: {node_version}")
        
        # Check if we're in the frontend directory
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            return False, "Frontend directory not found"
        
        # Check if package.json exists
        package_json = frontend_dir / "package.json"
        if not package_json.exists():
            return False, "package.json not found in frontend directory"
        
        # Check if node_modules exists
        node_modules = frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Installing dependencies...")
            install_result = subprocess.run(
                ["npm", "install"], 
                cwd=frontend_dir, 
                capture_output=True
            )
            if install_result.returncode != 0:
                return False, "Failed to install dependencies"
            print("✅ Dependencies installed")
        else:
            print("✅ Dependencies already installed")
        
        return True, "Ready"
        
    except FileNotFoundError:
        return False, "Node.js not found"

def start_frontend_dev_server():
    """Start the Next.js development server"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ⚛️  AeroCast React/TypeScript Frontend                   ║
║                                                              ║
║    🚀 Next.js 15 + React 19 + TypeScript                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check prerequisites
    available, message = check_node_and_dependencies()
    if not available:
        print(f"❌ {message}")
        print("\n💡 Please install Node.js from https://nodejs.org/")
        return False
    
    frontend_dir = Path("frontend")
    print(f"📁 Starting from: {frontend_dir.absolute()}")
    print("🌐 Frontend will be available at: http://localhost:3000")
    print("🔥 Hot reload enabled - changes will auto-refresh")
    print("🔗 Make sure backend API is running on http://localhost:8000")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Start Next.js dev server
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)
        
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend server: {e}")
        return False
    
    return True

def main():
    """Main entry point"""
    success = start_frontend_dev_server()
    if not success:
        print("\n❌ Failed to start React frontend")
        print("\n🔄 Alternative options:")
        print("   • Install Node.js from https://nodejs.org/")
        print("   • Use the vanilla HTML frontend: python scripts/start_frontend_only.py")
        sys.exit(1)

if __name__ == "__main__":
    main()