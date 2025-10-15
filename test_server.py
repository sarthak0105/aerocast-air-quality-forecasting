#!/usr/bin/env python3
"""
Quick test to verify server can start
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from api.main import app
    print("✅ Server imports successfully!")
    print("✅ FastAPI app created successfully!")
    print("🚀 Ready to start with: python start_server.py")
    print("📍 Will be available at: http://localhost:8000")
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Check if all dependencies are installed")