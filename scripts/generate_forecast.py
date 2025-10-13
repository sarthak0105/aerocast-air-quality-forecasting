#!/usr/bin/env python3
"""
Batch forecast generation script
"""
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.services.model_service import model_service
from src.utils.logger import setup_logging, get_logger
from config.settings import settings

setup_logging()
logger = get_logger(__name__)

def generate_grid_forecast(output_file: str = None, hours: int = 24):
    """Generate forecast for a grid of locations in Delhi NCR"""
    
    # Define grid bounds for Delhi NCR
    lat_min, lat_max = settings.DELHI_BBOX_MIN_LAT, settings.DELHI_BBOX_MAX_LAT
    lon_min, lon_max = settings.DELHI_BBOX_MIN_LON, settings.DELHI_BBOX_MAX_LON
    
    # Create grid (0.01 degree resolution ~ 1km)
    resolution = 0.01
    lats = np.arange(lat_min, lat_max + resolution, resolution)
    lons = np.arange(lon_min, lon_max + resolution, resolution)
    
    logger.info(f"Generating forecast for {len(lats)}x{len(lons)} grid ({len(lats)*len(lons)} points)")
    
    forecasts = []
    total_points = len(lats) * len(lons)
    
    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            point_idx = i * len(lons) + j + 1
            
            if point_idx % 100 == 0:
                logger.info(f"Processing point {point_idx}/{total_points}")
            
            try:
                # Get prediction for this location
                result = model_service.predict(lat, lon, hours, include_uncertainty=False)
                
                forecast_data = {
                    'latitude': lat,
                    'longitude': lon,
                    'forecast_time': datetime.utcnow().isoformat(),
                    'forecast_horizon_hours': hours,
                    'model_used': result.get('model_used', 'unknown'),
                    'predictions': result['predictions']
                }
                
                forecasts.append(forecast_data)
                
            except Exception as e:
                logger.error(f"Error generating forecast for ({lat}, {lon}): {e}")
                continue
    
    # Save results
    if output_file is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_file = f"forecasts/grid_forecast_{timestamp}.json"
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(forecasts, f, indent=2)
    
    logger.info(f"Saved {len(forecasts)} forecasts to {output_path}")
    return output_path

def generate_location_forecast(locations: list, output_file: str = None, hours: int = 24):
    """Generate forecast for specific locations"""
    
    forecasts = []
    
    for location in locations:
        lat = location['latitude']
        lon = location['longitude']
        name = location.get('name', f"Location_{lat}_{lon}")
        
        logger.info(f"Generating forecast for {name} ({lat}, {lon})")
        
        try:
            result = model_service.predict(lat, lon, hours, include_uncertainty=True)
            
            forecast_data = {
                'name': name,
                'latitude': lat,
                'longitude': lon,
                'forecast_time': datetime.utcnow().isoformat(),
                'forecast_horizon_hours': hours,
                'model_used': result.get('model_used', 'unknown'),
                'predictions': result['predictions'],
                'uncertainties': result.get('uncertainties', {})
            }
            
            forecasts.append(forecast_data)
            
        except Exception as e:
            logger.error(f"Error generating forecast for {name}: {e}")
            continue
    
    # Save results
    if output_file is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_file = f"forecasts/location_forecast_{timestamp}.json"
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(forecasts, f, indent=2)
    
    logger.info(f"Saved {len(forecasts)} forecasts to {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Generate air quality forecasts")
    parser.add_argument("--mode", choices=["grid", "locations"], default="locations",
                       help="Forecast generation mode")
    parser.add_argument("--hours", type=int, default=24,
                       help="Forecast horizon in hours")
    parser.add_argument("--output", type=str,
                       help="Output file path")
    parser.add_argument("--locations-file", type=str,
                       help="JSON file with locations to forecast")
    
    args = parser.parse_args()
    
    logger.info(f"Starting forecast generation in {args.mode} mode")
    
    if args.mode == "grid":
        output_path = generate_grid_forecast(args.output, args.hours)
        
    elif args.mode == "locations":
        # Default locations if no file provided
        if args.locations_file:
            with open(args.locations_file, 'r') as f:
                locations = json.load(f)
        else:
            locations = [
                {"name": "Connaught Place", "latitude": 28.6315, "longitude": 77.2167},
                {"name": "India Gate", "latitude": 28.6129, "longitude": 77.2295},
                {"name": "Dwarka", "latitude": 28.5921, "longitude": 77.0460},
                {"name": "Gurgaon", "latitude": 28.4595, "longitude": 77.0266},
                {"name": "Noida", "latitude": 28.5355, "longitude": 77.3910},
                {"name": "Rohini", "latitude": 28.7041, "longitude": 77.1025},
                {"name": "Lajpat Nagar", "latitude": 28.5677, "longitude": 77.2431},
                {"name": "Karol Bagh", "latitude": 28.6519, "longitude": 77.1909}
            ]
        
        output_path = generate_location_forecast(locations, args.output, args.hours)
    
    logger.info(f"Forecast generation completed. Output saved to: {output_path}")

if __name__ == "__main__":
    main()