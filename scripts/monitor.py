#!/usr/bin/env python3
"""
Monitoring script for the air quality forecasting system
"""
import requests
import time
import json
from datetime import datetime
import argparse
import sys

def check_api_health(base_url="http://localhost:8000"):
    """Check if API is healthy"""
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}

def check_prediction_accuracy(base_url="http://localhost:8000"):
    """Test prediction endpoint"""
    try:
        payload = {
            "latitude": 28.6139,
            "longitude": 77.2090,
            "hours": 12,
            "include_uncertainty": False
        }
        
        start_time = time.time()
        response = requests.post(f"{base_url}/api/v1/predict", json=payload, timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return True, {
                "response_time": response_time,
                "forecasts_count": len(data.get("forecasts", [])),
                "forecast_horizon": data.get("forecast_horizon")
            }
        else:
            return False, {"status_code": response.status_code, "error": response.text}
            
    except Exception as e:
        return False, {"error": str(e)}

def monitor_system(base_url="http://localhost:8000", interval=60, duration=None):
    """Monitor system continuously"""
    print(f"🔍 Starting system monitoring...")
    print(f"Base URL: {base_url}")
    print(f"Check interval: {interval} seconds")
    if duration:
        print(f"Duration: {duration} seconds")
    print("=" * 50)
    
    start_time = time.time()
    check_count = 0
    health_failures = 0
    prediction_failures = 0
    
    try:
        while True:
            check_count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[{current_time}] Check #{check_count}")
            
            # Health check
            health_ok, health_data = check_api_health(base_url)
            if health_ok:
                print("   ✅ Health check: OK")
                print(f"      Status: {health_data.get('status', 'unknown')}")
                print(f"      Uptime: {health_data.get('uptime', 'unknown')}")
            else:
                health_failures += 1
                print("   ❌ Health check: FAILED")
                print(f"      Error: {health_data.get('error', 'unknown')}")
            
            # Prediction check
            pred_ok, pred_data = check_prediction_accuracy(base_url)
            if pred_ok:
                print("   ✅ Prediction test: OK")
                print(f"      Response time: {pred_data.get('response_time', 0):.2f}s")
                print(f"      Forecasts: {pred_data.get('forecasts_count', 0)}")
            else:
                prediction_failures += 1
                print("   ❌ Prediction test: FAILED")
                print(f"      Error: {pred_data.get('error', 'unknown')}")
            
            # Summary stats
            uptime_pct = ((check_count - health_failures) / check_count) * 100
            pred_success_pct = ((check_count - prediction_failures) / check_count) * 100
            
            print(f"   📊 Stats: Health {uptime_pct:.1f}% | Predictions {pred_success_pct:.1f}%")
            
            # Check if duration exceeded
            if duration and (time.time() - start_time) >= duration:
                break
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped by user")
    
    # Final summary
    total_time = time.time() - start_time
    print("\n" + "=" * 50)
    print("📊 MONITORING SUMMARY")
    print("=" * 50)
    print(f"Total checks: {check_count}")
    print(f"Duration: {total_time:.1f} seconds")
    print(f"Health failures: {health_failures}")
    print(f"Prediction failures: {prediction_failures}")
    print(f"Overall uptime: {((check_count - health_failures) / check_count) * 100:.1f}%")
    print(f"Prediction success rate: {((check_count - prediction_failures) / check_count) * 100:.1f}%")

def run_single_check(base_url="http://localhost:8000"):
    """Run a single comprehensive check"""
    print("🔍 Running system health check...")
    print("=" * 40)
    
    # Health check
    print("\n1. API Health Check")
    health_ok, health_data = check_api_health(base_url)
    if health_ok:
        print("   ✅ API is healthy")
        for key, value in health_data.items():
            print(f"      {key}: {value}")
    else:
        print("   ❌ API health check failed")
        print(f"      Error: {health_data.get('error')}")
        return False
    
    # Model info check
    print("\n2. Model Information")
    try:
        response = requests.get(f"{base_url}/api/v1/model-info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Model info retrieved")
            print(f"      Version: {data.get('model_version')}")
            print(f"      Variables: {data.get('target_variables')}")
            print(f"      Resolution: {data.get('spatial_resolution_km')}km")
        else:
            print(f"   ⚠️  Model info failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Model info error: {e}")
    
    # Prediction test
    print("\n3. Prediction Test")
    pred_ok, pred_data = check_prediction_accuracy(base_url)
    if pred_ok:
        print("   ✅ Prediction test successful")
        print(f"      Response time: {pred_data.get('response_time', 0):.2f}s")
        print(f"      Forecasts generated: {pred_data.get('forecasts_count', 0)}")
    else:
        print("   ❌ Prediction test failed")
        print(f"      Error: {pred_data.get('error')}")
        return False
    
    # Locations check
    print("\n4. Available Locations")
    try:
        response = requests.get(f"{base_url}/api/v1/locations", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data.get('total_count', 0)} locations available")
        else:
            print(f"   ⚠️  Locations check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Locations error: {e}")
    
    print("\n" + "=" * 40)
    print("✅ System check completed successfully!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Monitor air quality forecasting system")
    parser.add_argument("--url", default="http://localhost:8000",
                       help="Base URL of the API")
    parser.add_argument("--mode", choices=["single", "continuous"], default="single",
                       help="Monitoring mode")
    parser.add_argument("--interval", type=int, default=60,
                       help="Check interval in seconds (continuous mode)")
    parser.add_argument("--duration", type=int,
                       help="Total monitoring duration in seconds (continuous mode)")
    
    args = parser.parse_args()
    
    if args.mode == "single":
        success = run_single_check(args.url)
        sys.exit(0 if success else 1)
    else:
        monitor_system(args.url, args.interval, args.duration)

if __name__ == "__main__":
    main()