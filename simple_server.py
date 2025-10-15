#!/usr/bin/env python3
"""
Simple direct server startup - bypasses complex imports
"""
import uvicorn
import os
from pathlib import Path

def main():
    # Change to project directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("🚀 Starting AeroCast Server (Simple Mode)")
    print("📁 Working directory:", project_root)
    print("📍 Server will be available at: http://localhost:8000")
    print("⚡ Starting now...")
    
    try:
        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for stability
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try running: pip install fastapi uvicorn")

if __name__ == "__main__":
    main()