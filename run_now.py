#!/usr/bin/env python3
"""
Direct server startup - guaranteed to work
"""
import os
import sys
from pathlib import Path

# Change to project directory
os.chdir(Path(__file__).parent)

print("🚀 Starting AeroCast Server...")
print("📍 Will be available at: http://localhost:8000")
print("⚡ Starting now...")

# Direct uvicorn command
os.system("python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload")