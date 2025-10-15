#!/usr/bin/env python3
"""
Start frontend only using Python's built-in HTTP server
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def start_frontend_server():
    """Start a simple HTTP server for the frontend"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🎨 AeroCast Frontend Only Server                         ║
║                                                              ║
║    Starting static file server for frontend development     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Change to static directory
    static_dir = Path("static")
    if not static_dir.exists():
        print("❌ Static directory not found!")
        return False
    
    print(f"📁 Serving files from: {static_dir.absolute()}")
    print("🌐 Frontend will be available at: http://localhost:8080")
    print("📄 Files available:")
    for file in static_dir.glob("*.html"):
        print(f"   • http://localhost:8080/{file.name}")
    
    print("\n⚠️  Note: API calls will fail since backend is not running")
    print("   The frontend will show 'System offline' status")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Start Python HTTP server in static directory
        os.chdir(static_dir)
        
        # Try Python 3 first, then Python 2
        try:
            subprocess.run([sys.executable, "-m", "http.server", "8080"])
        except KeyboardInterrupt:
            print("\n🛑 Frontend server stopped")
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start frontend server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_frontend_server()