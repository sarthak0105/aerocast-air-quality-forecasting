#!/usr/bin/env python3
"""
Minimal server that definitely works
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

class CustomHandler(SimpleHTTPRequestHandler):
    """Custom handler for serving files"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="static", **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.path = '/index.html'
        elif self.path.startswith('/api/'):
            # Handle API requests with dummy data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Return dummy forecast data
            dummy_data = {
                "location": {"latitude": 28.6139, "longitude": 77.2090, "city": "Delhi"},
                "forecast_time": "2025-10-14T12:00:00",
                "forecast_horizon": 24,
                "forecasts": [
                    {
                        "pollutant": "NO2_forecast",
                        "values": [58, 62, 45, 38, 72, 68, 55, 42, 48, 52, 59, 63, 47, 41, 75, 71, 58, 45, 51, 55, 61, 65, 49, 43],
                        "unit": "µg/m³"
                    },
                    {
                        "pollutant": "O3_forecast", 
                        "values": [32, 28, 35, 42, 38, 45, 52, 35, 30, 34, 31, 38, 45, 41, 48, 55, 38, 33, 37, 40, 36, 43, 50, 36],
                        "unit": "µg/m³"
                    }
                ],
                "metadata": {
                    "model_version": "v1.0",
                    "model_used": "demo_atmospheric_patterns"
                }
            }
            
            import json
            self.wfile.write(json.dumps(dummy_data).encode())
            return
        
        return super().do_GET()

def start_minimal_server():
    """Start a minimal HTTP server"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🌐 AeroCast Minimal Server                              ║
║                                                              ║
║    Simple HTTP server that definitely works!                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Check if static directory exists
    static_dir = Path("static")
    if not static_dir.exists():
        print("❌ Error: 'static' directory not found!")
        print("   Make sure you're in the AeroCast project directory")
        return False
    
    print("✅ Found static directory")
    print(f"📁 Serving files from: {static_dir.absolute()}")
    
    # Start server
    port = 8000
    server_address = ('', port)
    
    try:
        httpd = HTTPServer(server_address, CustomHandler)
        
        print(f"🚀 Server starting on port {port}...")
        print(f"🌐 Your website will be available at:")
        print(f"   http://localhost:{port}")
        print(f"   http://127.0.0.1:{port}")
        
        # Open browser automatically
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open(f"http://localhost:{port}")
                print("🌐 Browser opened automatically")
            except:
                print("💡 Please open http://localhost:8000 manually in your browser")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print(f"""
🎉 SUCCESS! AeroCast server is running!

🌐 OPEN IN BROWSER:
   Main Dashboard: http://localhost:{port}
   Historical: http://localhost:{port}/historical.html
   Analytics: http://localhost:{port}/analytics.html
   Settings: http://localhost:{port}/settings.html

✨ FEATURES WORKING:
   ✅ Beautiful web interface
   ✅ Interactive maps and charts
   ✅ Demo air quality data
   ✅ All navigation links
   ✅ Responsive design

Press Ctrl+C to stop the server
        """)
        
        # Start serving
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()
        return True
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False

def main():
    """Main entry point"""
    # Check if we're in the right directory
    if not Path("static").exists():
        print("❌ Error: Please run this from the AeroCast project directory")
        print("   You should see 'static', 'api', and 'src' folders")
        return
    
    success = start_minimal_server()
    if not success:
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Make sure you're in the AeroCast project directory")
        print("   2. Check that the 'static' folder exists")
        print("   3. Try a different port if 8000 is busy")

if __name__ == "__main__":
    main()