# Air Quality Forecasting System

AI/ML-based system for short-term forecasting (24-48 hours) of surface O3 and NO2 concentrations in Delhi using satellite data and meteorological reanalysis.

## Features

- **Multi-source Data Integration**: Satellite observations, meteorological reanalysis, and ground-based measurements
- **Advanced ML Models**: LSTM, Transformer, and ensemble approaches for accurate predictions
- **Real-time Forecasting**: Automated 24-48 hour predictions at hourly intervals
- **High Resolution**: 1km x 1km spatial resolution for Delhi NCR
- **REST API**: Easy integration with external applications
- **Interactive Dashboard**: Web-based visualization of forecasts and historical data

## Quick Start

### Option 1: Automated Deployment (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd air-quality-forecasting

# Deploy locally (installs dependencies and starts server)
python scripts/deploy.py --mode local

# Or deploy with Docker
python scripts/deploy.py --mode docker
```

### Option 2: Manual Setup

**Prerequisites:**
- Python 3.9+
- Docker and Docker Compose (optional)
- Git

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Train Models** (Optional - API works with dummy data)
```bash
# Quick training
python scripts/train_simple.py

# High accuracy training  
python scripts/train_high_accuracy.py
```

3. **Start the API Server**
```bash
# Local development
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Or with Docker
docker-compose up -d
```

4. **Access the Application**
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs  
- **Health Check**: http://localhost:8000/health

### Testing the API
```bash
# Run comprehensive tests
python scripts/test_api.py

# Generate batch forecasts
python scripts/generate_forecast.py --mode locations --hours 24
```

### API Usage Examples

**Get current forecast:**
```bash
curl "http://localhost:8000/api/v1/current?lat=28.6139&lon=77.2090&hours=24"
```

**Post prediction request:**
```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 28.6315, "longitude": 77.2167, "hours": 24, "include_uncertainty": true}'
```

## Data Sources

- **TROPOMI NO2**: Daily satellite observations
- **ERA5 Reanalysis**: Hourly meteorological data
- **CPCB Stations**: Ground-based air quality measurements
- **MODIS AOD**: Aerosol optical depth data

## Model Architecture

The system uses an ensemble approach combining:
- **LSTM Networks**: For temporal pattern recognition
- **Transformer Models**: For attention-based feature learning
- **XGBoost**: For non-linear meteorological relationships

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/ api/ scripts/
isort src/ api/ scripts/
```

### Training Models
```bash
python scripts/train_model.py --config config/model_config.yaml
```

## Monitoring

- **MLflow**: Model experiment tracking at `http://localhost:5000`
- **Airflow**: Workflow monitoring at `http://localhost:8080`
- **API Docs**: Interactive API documentation at `http://localhost:8000/docs`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.