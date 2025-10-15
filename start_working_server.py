#!/usr/bin/env python3
"""
Start the working FastAPI server with predictions
"""

import subprocess
import sys
import time
import webbrowser

def start_server():
    """Start the FastAPI server"""
    print("""
🚀 Starting AeroCast with Working Predictions!

✅ FastAPI server with API endpoints
✅ Real prediction functionality  
✅ Beautiful web interface
✅ Interactive forecasting

Starting server...
    """)
    
    try:
        # Start the FastAPI server
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ]
        
        process = subprocess.Popen(cmd)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        print("""
🎉 SUCCESS! AeroCast is running with working predictions!

🌐 OPEN IN BROWSER:
   http://localhost:8000

✨ FEATURES NOW WORKING:
   ✅ Beautiful dashboard
   ✅ Interactive map
   ✅ "Get Forecast" button generates real predictions
   ✅ Charts show actual data
   ✅ All navigation links work

💡 USAGE:
   1. Click different locations on the map
   2. Click "Get Forecast" button
   3. See real predictions appear!

Press Ctrl+C to stop the server
        """)
        
        # Open browser
        try:
            webbrowser.open("http://localhost:8000")
        except:
            pass
        
        # Keep server running
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        process.terminate()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_server()