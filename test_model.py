#!/usr/bin/env python3
"""
Test the model API endpoints
"""
import requests
import json

def test_model_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing AeroCast Model API")
    print("=" * 40)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print("❌ Health check: FAILED")
    except Exception as e:
        print(f"❌ Health check: ERROR - {e}")
        return
    
    # Test 2: Model status
    try:
        response = requests.get(f"{base_url}/api/v1/model-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model status: {data['status']}")
            print(f"   Model: {data['model_name']}")
            print(f"   Accuracy: {data['accuracy']}")
        else:
            print(f"❌ Model status: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Model status: ERROR - {e}")
    
    # Test 3: Forecast prediction
    try:
        params = {
            'lat': 28.6139,
            'lon': 77.2090,
            'hours': 24
        }
        response = requests.get(f"{base_url}/api/v1/current", params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Forecast prediction: PASSED")
            print(f"   Location: {data['location']['latitude']}, {data['location']['longitude']}")
            print(f"   Forecasts: {len(data['forecasts'])} pollutants")
            for forecast in data['forecasts']:
                values = forecast['values'][:3]  # First 3 values
                print(f"   {forecast['pollutant']}: {values}... ({len(forecast['values'])} total)")
        else:
            print(f"❌ Forecast prediction: FAILED ({response.status_code})")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Forecast prediction: ERROR - {e}")
    
    print("\n🎯 Test complete!")
    print("If all tests passed, your model is working correctly!")

if __name__ == "__main__":
    test_model_api()