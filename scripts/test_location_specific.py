#!/usr/bin/env python3
"""
Test location-specific predictions
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.services.fast_model_service import fast_model_service

def test_different_locations():
    """Test predictions for different locations"""
    print("""
🔍 Testing Location-Specific Predictions
========================================
    """)
    
    # Test different locations
    locations = [
        ("Central Delhi", 28.6139, 77.2090),
        ("Connaught Place", 28.6315, 77.2167),
        ("Gurgaon", 28.4595, 77.0266),
        ("Noida", 28.5355, 77.3910),
        ("Dwarka", 28.5921, 77.0460)
    ]
    
    for name, lat, lon in locations:
        print(f"\n📍 {name} ({lat}, {lon})")
        print("-" * 40)
        
        result = fast_model_service.predict(lat, lon, 6)  # 6 hours for quick test
        
        no2_values = result['predictions']['NO2']
        o3_values = result['predictions']['O3']
        
        no2_avg = sum(no2_values) / len(no2_values)
        o3_avg = sum(o3_values) / len(o3_values)
        
        print(f"   NO2: {no2_avg:.1f} µg/m³ (range: {min(no2_values):.1f}-{max(no2_values):.1f})")
        print(f"   O3:  {o3_avg:.1f} µg/m³ (range: {min(o3_values):.1f}-{max(o3_values):.1f})")
        print(f"   Ratio: {no2_avg/o3_avg:.2f}")
    
    print(f"\n🎯 ANALYSIS:")
    print("✅ Each location should show DIFFERENT values")
    print("✅ Connaught Place should have highest NO2")
    print("✅ Dwarka should have lower pollution")
    print("✅ O3 should vary inversely with NO2")

if __name__ == "__main__":
    test_different_locations()