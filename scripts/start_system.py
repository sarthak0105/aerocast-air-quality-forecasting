#!/usr/bin/env python3
"""
Simple system startup script for Delhi Air Quality Forecasting System
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def print_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🌬️  Delhi Air Quality Forecasting System                ║
║                                                              ║
║    🚀 Starting Enhanced Visual Interface                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting server...")
    
    try:
        # Start server
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ]
        
        process = subprocess.Popen(
            cmd, 
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(15):  # Wait up to 15 seconds
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Server is running!")
                    break
            except:
                time.sleep(1)
                print(f"   Starting... {i+1}/15")
        else:
            print("⚠️  Server may still be starting...")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def print_access_info():
    """Print access information"""
    info = """
🌐 ACCESS YOUR ENHANCED SYSTEM:

   📊 Main Dashboard (Beautiful UI):
   → http://localhost:8000
   
   📈 Historical Analysis:
   → http://localhost:8000/static/historical.html
   
   📊 Analytics Dashboard:
   → http://localhost:8000/static/analytics.html
   
   ⚙️  Settings Page:
   → http://localhost:8000/static/settings.html
   
   📚 API Documentation:
   → http://localhost:8000/docs

✨ FEATURES:
   • Enhanced visual interface with animations
   • Real-time air quality predictions
   • Interactive maps and charts
   • Fast atmospheric science predictions
   • Professional gradient design
   • Mobile-responsive layout

🎯 READY TO USE:
   1. Click on locations on the map
   2. Generate forecasts instantly
   3. Explore beautiful visualizations
   4. Navigate between pages seamlessly

Press Ctrl+C to stop the server.
    """
    print(info)

def main():
    """Main entry point"""
    print_banner()
    
    # Start server
    server_process = start_server()
    if not server_process:
        print("❌ Failed to start server")
        sys.exit(1)
    
    # Show access info
    print_access_info()
    
    try:
        # Keep server running
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        server_process.terminate()
        print("✅ Server stopped successfully")

if __name__ == "__main__":
    main()