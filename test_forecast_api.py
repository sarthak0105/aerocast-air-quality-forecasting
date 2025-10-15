#!/usr/bin/env python3
"""
Test script to verify the forecast API is working
"""
import requests
import json
import sys

def test_model_status():
    """Test model status endpoint"""
    print("🔍 Testing model status...")
    try:
        response = requests.get("http://localhost:8001/api/v1/model-status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model Status: {data['status']}")
            print(f"📊 Model: {data['model_name']} ({data['accuracy']})")
            return True
        else:
            print(f"❌ Model status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model status error: {e}")
        return False

def test_forecast_prediction():
    """Test forecast prediction endpoint"""
    print("\n🔮 Testing forecast prediction...")
    try:
        payload = {
            "latitude": 28.6139,
            "longitude": 77.2090,
            "hours": 24,
            "include_uncertainty": True
        }
        
        response = requests.post(
            "http://localhost:8001/api/v1/predict",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Forecast generated successfully!")
            print(f"📍 Location: {data['metadata']['location']}")
            print(f"⏰ Hours: {data['metadata']['hours']}")
            print(f"🧠 Model: {data['metadata']['model_used']}")
            print(f"🎯 Accuracy: {data['metadata']['accuracy']}")
            
            if data['predictions']:
                first_pred = data['predictions'][0]
                print(f"📊 First prediction:")
                print(f"   NO2: {first_pred['no2']} μg/m³")
                print(f"   O3: {first_pred['o3']} μg/m³")
                print(f"   AQI: {first_pred['aqi']}")
    
          
            return True
        else:
            print(f"❌ Forecast failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Forecast error: {e}")
        return False

def test_current_forecast():
    """Test current forecast endpoint"""
    print("\n🌐 Testing current forecast...")
    try:
        response = requests.get(
            "http://localhost:8001/api/v1/current?lat=28.6139&lon=77.2090&hours=12"
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Current forecast retrieved!")
            print(f"📍 Location: {data['location']}")
            print(f"⏰ Forecast time: {data['forecast_time']}")
            print(f"🔮 Horizon: {data['forecast_horizon']} hours")
            return True
        else:
            print(f"❌ Current forecast failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Current forecast error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing AeroCast Air Quality Forecast API")
    print("=" * 50)
    
    # Test all endpoints
    tests = [
        test_model_status,
        test_forecast_prediction,
        test_current_forecast
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    
    if all(results):
        print("🎉 All tests passed! Backend is working correctly.")
        print("\n🚀 Your forecast API is ready!")
        print("   • Model Status: http://localhost:8001/api/v1/model-status")
        print("   • Predict: POST http://localhost:8001/api/v1/predict")
        print("   • Current: http://localhost:8001/api/v1/current")
        print("   • API Docs: http://localhost:8001/docs")
        return True
    else:
        print("❌ Some tests failed. Check the backend server.")
        failed_count = sum(1 for r in results if not r)
        print(f"   {failed_count}/{len(results)} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)