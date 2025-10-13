"""
Simple working training script that avoids memory issues
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import argparse

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import settings
from src.training.trainer import ModelTrainer
from src.models.lstm_model import LSTMModel
from src.utils.logger import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def load_single_site_simple(site_id: int = 1, max_rows: int = 5000) -> pd.DataFrame:
    """Load a single site with minimal processing"""
    file_path = f"data/raw/Raw Data/Data_SIH_2025/site_{site_id}_train_data.csv"
    
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # Read limited rows
    df = pd.read_csv(file_path, nrows=max_rows)
    
    # Basic processing
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df = df.sort_values('datetime').reset_index(drop=True)
    
    # Use target values if available
    if 'O3_target' in df.columns and 'NO2_target' in df.columns:
        df['O3_forecast'] = df['O3_target']
        df['NO2_forecast'] = df['NO2_target']
        logger.info("Using target values for training")
    
    # Keep only essential numeric columns
    numeric_cols = ['O3_forecast', 'NO2_forecast', 'T_forecast', 'q_forecast', 
                   'u_forecast', 'v_forecast', 'w_forecast']
    
    # Add datetime features
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    
    # Keep only available columns
    available_cols = ['datetime'] + [col for col in numeric_cols if col in df.columns] + ['hour', 'day_of_week', 'month']
    df = df[available_cols]
    
    # Fill any missing values
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].median())
    
    logger.info(f"Loaded site {site_id} data: {df.shape}")
    logger.info(f"Columns: {list(df.columns)}")
    
    return df


def train_simple_model(site_id: int = 1, max_rows: int = 5000, epochs: int = 20) -> dict:
    """Train a simple model without complex feature engineering"""
    logger.info(f"Training simple model for site {site_id}")
    
    # Load data
    data = load_single_site_simple(site_id, max_rows)
    
    # Initialize trainer
    trainer = ModelTrainer(experiment_name=f"simple_site_{site_id}")
    
    # Prepare data with simple settings
    X_train, y_train, X_val, y_val, X_test, y_test = trainer.prepare_data(
        data,
        sequence_length=12,  # Shorter sequences
        forecast_horizon=1,
        train_ratio=0.7,
        val_ratio=0.2,
        test_ratio=0.1,
        use_simple_features=True  # Use simple feature engineering
    )
    
    logger.info(f"Data shapes - Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    
    # Create simple model
    model = LSTMModel(
        lstm_units=32,  # Smaller model
        num_layers=1,   # Single layer
        dropout_rate=0.2,
        learning_rate=0.001,
        use_bidirectional=False,  # Simpler architecture
        use_attention=False,
        use_cnn_features=False
    )
    
    # Simple training parameters
    training_params = {
        'epochs': epochs,
        'batch_size': 16,  # Small batch size
        'patience': 8
    }
    
    # Train model
    logger.info("Starting simple model training...")
    results = trainer.train_model(
        model, X_train, y_train, X_val, y_val, training_params
    )
    
    # Evaluate
    test_results = trainer.evaluate_models(X_test, y_test)
    
    # Log results
    if test_results:
        for model_name, test_result in test_results.items():
            metrics = test_result.get('metrics', {})
            accuracy_10 = metrics.get('accuracy_within_10_percent', 0)
            accuracy_20 = metrics.get('accuracy_within_20_percent', 0)
            overall_accuracy = metrics.get('overall_accuracy_score', 0)
            
            logger.info(f"Simple Model Results:")
            logger.info(f"  Site: {site_id}")
            logger.info(f"  Data size: {len(data)} rows")
            logger.info(f"  Accuracy within 10%: {accuracy_10:.1f}%")
            logger.info(f"  Accuracy within 20%: {accuracy_20:.1f}%")
            logger.info(f"  Overall Accuracy: {overall_accuracy:.1f}%")
            logger.info(f"  RMSE: {metrics.get('rmse', 0):.3f}")
            logger.info(f"  R²: {metrics.get('r2', 0):.3f}")
    
    return {
        'site_id': site_id,
        'model': model,
        'training_results': results,
        'test_results': test_results,
        'data_size': len(data)
    }


def main():
    parser = argparse.ArgumentParser(description='Simple working air quality model training')
    parser.add_argument('--site-id', type=int, default=1, choices=range(1, 8), 
                       help='Site ID to train on')
    parser.add_argument('--max-rows', type=int, default=5000, 
                       help='Maximum rows to load')
    parser.add_argument('--epochs', type=int, default=20, 
                       help='Number of training epochs')
    
    args = parser.parse_args()
    
    try:
        logger.info("="*60)
        logger.info("🚀 SIMPLE WORKING MODEL TRAINING")
        logger.info("="*60)
        
        result = train_simple_model(
            site_id=args.site_id,
            max_rows=args.max_rows,
            epochs=args.epochs
        )
        
        logger.info("="*60)
        logger.info("✅ TRAINING COMPLETED SUCCESSFULLY!")
        logger.info("="*60)
        
        # Extract final metrics
        if result['test_results']:
            for model_name, test_result in result['test_results'].items():
                metrics = test_result.get('metrics', {})
                accuracy_20 = metrics.get('accuracy_within_20_percent', 0)
                overall_accuracy = metrics.get('overall_accuracy_score', 0)
                
                if overall_accuracy >= 80:
                    logger.info("🎉 EXCELLENT! Model achieved 80%+ accuracy!")
                elif overall_accuracy >= 70:
                    logger.info("✅ GOOD! Model achieved 70%+ accuracy!")
                elif overall_accuracy >= 60:
                    logger.info("👍 DECENT! Model achieved 60%+ accuracy!")
                else:
                    logger.info("📈 Model trained successfully, accuracy can be improved with more data")
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        logger.info("Try reducing --max-rows or using a different site")


if __name__ == "__main__":
    main()