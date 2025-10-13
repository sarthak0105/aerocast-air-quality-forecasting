#!/usr/bin/env python3
"""
Test script for the air quality forecasting API
"""
import requests
import json
import time
from datetime import datetime

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Air Quality Forecasting API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/api")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Model info
    print("\n3. Testing model info endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/model-info")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Model Version: {data.get('model_version')}")
        print(f"   Target Variables: {data.get('target_variables')}")
        print(f"   Coverage Area: {data.get('coverage_area', {}).get('region')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Available locations
    print("\n4. Testing available locations...")
    try:
        response = requests.get(f"{base_url}/api/v1/locations")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Total locations: {data.get('total_count')}")
        for loc in data.get('locations', [])[:3]:
            print(f"   - {loc['name']}: ({loc['latitude']}, {loc['longitude']})")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Current forecast (GET)
    print("\n5. Testing current forecast (GET)...")
    try:
        params = {
            "lat": 28.6139,
            "lon": 77.2090,
            "hours": 12
        }
        response = requests.get(f"{base_url}/api/v1/current", params=params)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Location: {data.get('location')}")
        print(f"   Forecast horizon: {data.get('forecast_horizon')} hours")
        print(f"   Pollutants forecasted: {len(data.get('forecasts', []))}")
        
        for forecast in data.get('forecasts', []):
            values = forecast.get('values', [])
            avg_value = sum(values) / len(values) if values else 0
            print(f"   - {forecast.get('pollutant')}: avg {avg_value:.1f} {forecast.get('unit')}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Prediction (POST)
    print("\n6. Testing prediction endpoint (POST)...")
    try:
        payload = {
            "latitude": 28.6315,
            "longitude": 77.2167,
            "hours": 24,
            "include_uncertainty": True
        }
        response = requests.post(f"{base_url}/api/v1/predict", json=payload)
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Location: {data.get('location')}")
        print(f"   Forecast time: {data.get('forecast_time')}")
        
        for forecast in data.get('forecasts', []):
            has_uncertainty = forecast.get('uncertainty') is not None
            print(f"   - {forecast.get('pollutant')}: {len(forecast.get('values', []))} values, uncertainty: {has_uncertainty}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 7: Invalid location (should fail)
    print("\n7. Testing invalid location (should fail)...")
    try:
        params = {
            "lat": 40.7128,  # New York latitude (outside Delhi)
            "lon": -74.0060,  # New York longitude
            "hours": 12
        }
        response = requests.get(f"{base_url}/api/v1/current", params=params)
        print(f"   Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Error (expected): {response.json().get('detail')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")

def performance_test():
    """Test API performance"""
    print("\n🚀 Performance Testing")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    # Test multiple requests
    locations = [
        (28.6139, 77.2090),  # Delhi Center
        (28.6315, 77.2167),  # Connaught Place
        (28.6129, 77.2295),  # India Gate
        (28.5921, 77.0460),  # Dwarka
        (28.4595, 77.0266),  # Gurgaon
    ]
    
    total_time = 0
    successful_requests = 0
    
    for i, (lat, lon) in enumerate(locations):
        print(f"\nRequest {i+1}: ({lat}, {lon})")
        
        start_time = time.time()
        try:
            response = requests.get(f"{base_url}/api/v1/current", 
                                  params={"lat": lat, "lon": lon, "hours": 24})
            end_time = time.time()
            
            request_time = end_time - start_time
            total_time += request_time
            
            if response.status_code == 200:
                successful_requests += 1
                print(f"   ✅ Success in {request_time:.2f}s")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            end_time = time.time()
            print(f"   ❌ Error: {e}")
    
    if successful_requests > 0:
        avg_time = total_time / successful_requests
        print(f"\n📊 Performance Summary:")
        print(f"   Successful requests: {successful_requests}/{len(locations)}")
        print(f"   Average response time: {avg_time:.2f}s")
        print(f"   Total time: {total_time:.2f}s")

if __name__ == "__main__":
    print("Starting API tests...")
    print("Make sure the API server is running on http://localhost:8000")
    
    try:
        test_api_endpoints()
        performance_test()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")