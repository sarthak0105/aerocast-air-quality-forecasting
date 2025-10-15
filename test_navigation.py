#!/usr/bin/env python3
"""
Test all navigation links
"""
import requests

def test_navigation():
    base_url = "http://localhost:8000"
    
    pages = [
        ("/", "Dashboard"),
        ("/historical", "Historical Data"),
        ("/analytics", "Analytics"),
        ("/settings", "Settings"),
        ("/docs", "API Documentation"),
        ("/health", "Health Check")
    ]
    
    print("🧪 Testing Navigation Links")
    print("=" * 40)
    
    for path, name in pages:
        try:
            response = requests.get(f"{base_url}{path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: WORKING")
            else:
                print(f"❌ {name}: FAILED ({response.status_code})")
        except Exception as e:
            print(f"❌ {name}: ERROR - {e}")
    
    print("\n🎯 Navigation test complete!")

if __name__ == "__main__":
    test_navigation()