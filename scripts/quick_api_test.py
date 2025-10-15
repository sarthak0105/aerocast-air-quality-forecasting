#!/usr/bin/env python3
"""
Quick test to verify the API is using the real model
"""

import requests
import json

def test_api():
    """Test the API with real model"""
    print("🔮 Testing API with real model...")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/current?lat=28.6139&lon=77.2090&hours=24",
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response successful!")
            
            # Check metadata for model info
            if 'metadata' in data:
                print(f"📋 Metadata: {data['metadata']}")
            
            # Show predictions
            if 'forecasts' in data:
                print("📊 Predictions:")
                for forecast in data['forecasts']:
                    values = forecast['values']
                    avg_val = sum(values) / len(values)
                    print(f"   {forecast['pollutant']}: {avg_val:.1f} µg/m³")
                    print(f"     Range: {min(values):.1f} - {max(values):.1f}")
                    print(f"     Sample: {[round(v, 1) for v in values[:5]]}")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n✅ API is working with predictions!")
    else:
        print("\n❌ API test failed - make sure server is running")
        print("Start with: python scripts/start_with_real_model.py")