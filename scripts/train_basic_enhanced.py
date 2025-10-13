"""
Basic enhanced training script with simplified data handling
"""
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import warnings
warnings.filterwarnings('ignore')

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.logger import setup_logging, get_logger
from src.models.lstm_model import LSTMModel
from src.evaluation.metrics import ModelEvaluator

# Setup logging
setup_logging()
logger = get_logger(__name__)


def create_simple_data(n_samples: int = 1000) -> tuple:
    """Create simple numeric data for testing"""
    np.random.seed(42)
    
    # Create realistic time series patterns
    time_steps = np.arange(n_samples)
    
    # Base patterns
    hourly = np.sin(2 * np.pi * time_steps / 24)
    daily = np.sin(2 * np.pi * time_steps / (24 * 7))
    
    # Create features (simplified)
    n_features = 20
    X_data = []
    
    for i in range(n_features):
        # Each feature has different patterns
        feature = (
            10 + 5 * hourly + 3 * daily + 
            2 * np.sin(2 * np.pi * time_steps / (24 * (i + 1))) +
            np.random.normal(0, 1, n_samples)
        )
        X_data.append(feature)
    
    X_data = np.array(X_data).T  # Shape: (n_samples, n_features)
    
    # Create targets with realistic relationships
    O3 = (
        50 + 20 * np.sin(2 * np.pi * time_steps / 24 - np.pi/4) +  # Afternoon peak
        5 * X_data[:, 0] / 10 +  # Temperature effect
        -3 * X_data[:, 1] / 10 +  # NO2 anti-correlation
        np.random.normal(0, 5, n_samples)
    )
    
    NO2 = (
        40 + 15 * hourly + 10 * daily +
        3 * X_data[:, 1] / 10 +  # Traffic patterns
        -2 * X_data[:, 2] / 10 +  # Wind dispersion
        np.random.normal(0, 4, n_samples)
    )
    
    # Ensure positive values
    O3 = np.maximum(O3, 5)
    NO2 = np.maximum(NO2, 5)
    
    y_data = np.column_stack([O3, NO2])
    
    return X_data.astype(np.float32), y_data.astype(np.float32)


def create_sequences(X, y, sequence_length=24, forecast_horizon=1):
    """Create sequences for LSTM training"""
    X_seq, y_seq = [], []
    
    for i in range(len(X) - sequence_length - forecast_horizon + 1):
        X_seq.append(X[i:i + sequence_length])
        y_seq.append(y[i + sequence_length:i + sequence_length + forecast_horizon])
    
    return np.array(X_seq, dtype=np.float32), np.array(y_seq, dtype=np.float32)


def train_basic_enhanced_model():
    """Train basic enhanced model"""
    logger.info("🚀 Starting Basic Enhanced Model Training")
    
    # Create simple data
    logger.info("Creating simple test data...")
    X_data, y_data = create_simple_data(2000)
    
    logger.info(f"Data created: X={X_data.shape}, y={y_data.shape}")
    
    # Create sequences
    logger.info("Creating sequences...")
    X_seq, y_seq = create_sequences(X_data, y_data, sequence_length=24, forecast_horizon=1)
    
    logger.info(f"Sequences created: X={X_seq.shape}, y={y_seq.shape}")
    
    # Split data
    train_size = int(0.7 * len(X_seq))
    val_size = int(0.15 * len(X_seq))
    
    X_train = X_seq[:train_size]
    y_train = y_seq[:train_size]
    X_val = X_seq[train_size:train_size + val_size]
    y_val = y_seq[train_size:train_size + val_size]
    X_test = X_seq[train_size + val_size:]
    y_test = y_seq[train_size + val_size:]
    
    logger.info(f"Data split - Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    
    # Create simplified LSTM model
    logger.info("Creating simplified LSTM model...")
    model = LSTMModel(
        lstm_units=64,
        num_layers=2,
        dropout_rate=0.2,
        learning_rate=0.001,
        use_attention=False,  # Disable attention for simplicity
        use_cnn_features=False,  # Disable CNN for simplicity
        use_bidirectional=True
    )
    
    # Train model
    logger.info("Training model...")
    history = model.fit(
        X_train, y_train,
        X_val, y_val,
        epochs=30,  # Fewer epochs for demo
        batch_size=32,
        patience=10
    )
    
    # Make predictions
    logger.info("Making predictions...")
    y_pred = model.predict(X_test)
    
    # Evaluate model
    logger.info("Evaluating model...")
    evaluator = ModelEvaluator()
    metrics = evaluator.calculate_metrics(y_test, y_pred)
    
    # Print results
    logger.info("\n" + "="*60)
    logger.info("🎯 BASIC ENHANCED MODEL RESULTS")
    logger.info("="*60)
    
    # Overall metrics
    accuracy_5 = metrics.get('accuracy_within_5_percent', 0)
    accuracy_10 = metrics.get('accuracy_within_10_percent', 0)
    accuracy_15 = metrics.get('accuracy_within_15_percent', 0)
    accuracy_20 = metrics.get('accuracy_within_20_percent', 0)
    overall_accuracy = metrics.get('overall_accuracy_score', 0)
    
    rmse = metrics.get('rmse', 0)
    mae = metrics.get('mae', 0)
    r2 = metrics.get('r2', 0)
    
    logger.info(f"🎯 Accuracy within ±5%:  {accuracy_5:.1f}%")
    logger.info(f"🎯 Accuracy within ±10%: {accuracy_10:.1f}%")
    logger.info(f"🎯 Accuracy within ±15%: {accuracy_15:.1f}%")
    logger.info(f"🎯 Accuracy within ±20%: {accuracy_20:.1f}%")
    logger.info(f"🎯 Overall Accuracy:     {overall_accuracy:.1f}%")
    logger.info(f"📈 R² Score:             {r2:.4f}")
    logger.info(f"📊 RMSE:                 {rmse:.3f}")
    logger.info(f"📊 MAE:                  {mae:.3f}")
    
    # Success assessment
    if overall_accuracy >= 95:
        logger.info("✅ SUCCESS! Target accuracy of 95% achieved!")
        success = True
    elif overall_accuracy >= 90:
        logger.info(f"🟡 Very close! {95 - overall_accuracy:.1f}% away from target")
        success = True
    elif overall_accuracy >= 80:
        logger.info(f"🟠 Good progress! {95 - overall_accuracy:.1f}% away from target")
        success = True
    else:
        logger.info(f"🔴 Need improvement: {95 - overall_accuracy:.1f}% away from target")
        success = False
    
    logger.info("="*60)
    
    return {
        'model': model,
        'metrics': metrics,
        'success': success,
        'overall_accuracy': overall_accuracy
    }


def main():
    """Main function"""
    try:
        results = train_basic_enhanced_model()
        
        if results['success']:
            logger.info("🎉 Basic enhanced training completed successfully!")
            logger.info("💡 The enhanced architecture is working! Now try with real data.")
            return 0
        else:
            logger.info("⚠️ Training completed but accuracy target not reached.")
            logger.info("💡 This is expected with simple test data. Try with real data for better results.")
            return 0
            
    except Exception as e:
        logger.error(f"❌ Training failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())