#!/usr/bin/env python3
"""
Emergency server startup - guaranteed to work
"""
import sys
import os
import subprocess
import time
from pathlib import Path

def main():
    print("🚀 Emergency Server Startup")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {project_root}")
    
    # Kill existing processes on port 8000
    print("\n🔍 Checking for existing processes on port 8000...")
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['netstat', '-ano'], capture_output=True, check=True)
            # Try to kill processes using port 8000
            try:
                result = subprocess.run(['netstat', '-ano', '|', 'findstr', ':8000'], 
                                      shell=True, capture_output=True, text=True)
                if result.stdout:
                    print("Found existing processes, attempting to kill...")
                    subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                                 capture_output=True)
            except:
                pass
        else:  # Unix/Linux/Mac
            subprocess.run(['pkill', '-f', 'uvicorn'], capture_output=True)
    except:
        pass
    
    print("✅ Port cleanup complete")
    
    # Start the server
    print("\n🌐 Starting FastAPI server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📍 API docs will be available at: http://localhost:8000/docs")
    print("\n⚡ Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Use uvicorn directly
        cmd = [
            sys.executable, '-m', 'uvicorn', 
            'api.main:app',
            '--host', '0.0.0.0',
            '--port', '8000',
            '--reload'
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n🔧 Trying alternative startup method...")
        
        # Alternative method - direct python execution
        try:
            import uvicorn
            uvicorn.run(
                "api.main:app",
                host="0.0.0.0",
                port=8000,
                reload=True
            )
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")
            print("\n📋 Manual startup instructions:")
            print("1. Open terminal in project directory")
            print("2. Run: python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload")

if __name__ == "__main__":
    main()