#!/usr/bin/env python3
"""
ULTIMATE SIMPLE START - Just run this file
"""
print("🚀 Starting AeroCast with Model Support...")

try:
    import uvicorn
    print("✅ uvicorn found")
except ImportError:
    print("❌ Installing uvicorn...")
    import subprocess
    subprocess.check_call(["pip", "install", "uvicorn", "fastapi"])

try:
    from fastapi import FastAPI
    print("✅ FastAPI found")
except ImportError:
    print("❌ Installing FastAPI...")
    import subprocess
    subprocess.check_call(["pip", "install", "fastapi"])

try:
    import numpy as np
    print("✅ NumPy found")
except ImportError:
    print("❌ Installing NumPy...")
    import subprocess
    subprocess.check_call(["pip", "install", "numpy"])

# Now start the server
import os
from pathlib import Path

os.chdir(Path(__file__).parent)

print("📍 Server will be at: http://localhost:8000")
print("🧠 Model API will be at: http://localhost:8000/api/v1/")
print("⚡ Starting with full model support...")

os.system("python minimal_start.py")