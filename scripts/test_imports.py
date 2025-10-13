"""
Test script to verify all imports work correctly
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

def test_imports():
    """Test all critical imports"""
    print("Testing imports...")
    
    try:
        # Test basic imports
        import numpy as np
        import pandas as pd
        print("✅ NumPy and Pandas imported successfully")
        
        # Test TensorFlow
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} imported successfully")
        
        # Test sklearn
        from sklearn.preprocessing import StandardScaler
        from sklearn.impute import KNNImputer
        print("✅ Scikit-learn imported successfully")
        
        # Test config
        from config.settings import settings
        print("✅ Settings imported successfully")
        
        # Test utils
        from src.utils.logger import get_logger
        from src.utils.helpers import create_time_features
        print("✅ Utils imported successfully")
        
        # Test models
        from src.models.base_model import BaseModel
        print("✅ Base model imported successfully")
        
        from src.models.lstm_model import LSTMModel
        print("✅ LSTM model imported successfully")
        
        # Test preprocessing
        from src.preprocessing.feature_engineering import FeatureEngineer
        print("✅ Feature engineering imported successfully")
        
        from src.preprocessing.data_quality import DataQualityEnhancer
        print("✅ Data quality enhancer imported successfully")
        
        # Test ensemble model
        from src.models.ensemble_model import EnsembleModel
        print("✅ Ensemble model imported successfully")
        
        # Test training
        from src.training.trainer import ModelTrainer
        print("✅ Model trainer imported successfully")
        
        # Test evaluation
        from src.evaluation.metrics import ModelEvaluator
        print("✅ Model evaluator imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\nTesting basic functionality...")
    
    try:
        # Test logger
        from src.utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Logger test successful")
        print("✅ Logger working")
        
        # Test settings
        from config.settings import settings
        print(f"✅ Settings loaded: {settings.APP_NAME}")
        
        # Test feature engineering with dummy data
        from src.preprocessing.feature_engineering import FeatureEngineer
        import pandas as pd
        import numpy as np
        
        # Create dummy data
        df = pd.DataFrame({
            'year': [2023] * 10,
            'month': [1] * 10,
            'day': list(range(1, 11)),
            'hour': [12] * 10,
            'T_forecast': np.random.normal(20, 5, 10),
            'q_forecast': np.random.normal(0.01, 0.002, 10),
            'u_forecast': np.random.normal(2, 1, 10),
            'v_forecast': np.random.normal(1, 1, 10),
            'w_forecast': np.random.normal(0, 0.1, 10),
            'NO2_satellite': np.random.normal(30, 10, 10),
            'HCHO_satellite': np.random.normal(15, 5, 10),
            'ratio_satellite': np.random.normal(2, 0.5, 10),
            'O3_forecast': np.random.normal(50, 15, 10),
            'NO2_forecast': np.random.normal(40, 12, 10)
        })
        
        fe = FeatureEngineer()
        processed_df = fe.fit_transform(df)
        print(f"✅ Feature engineering working: {df.shape} -> {processed_df.shape}")
        
        # Test LSTM model creation
        from src.models.lstm_model import LSTMModel
        model = LSTMModel(lstm_units=32, num_layers=1)
        print("✅ LSTM model creation working")
        
        print("\n🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧪 Running import and functionality tests...\n")
    
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    
    if imports_ok and functionality_ok:
        print("\n✅ All tests passed! The system is ready to use.")
        exit(0)
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        exit(1)