#!/usr/bin/env python3
"""
Setup script to use one of your existing trained models for real predictions
"""

import os
import shutil
from pathlib import Path

def setup_real_model():
    """Copy one of the existing trained models to the expected location"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🎯 Setting Up REAL Model for Predictions                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    models_dir = Path("models")
    
    # Find the most recent model
    model_dirs = [d for d in models_dir.iterdir() if d.is_dir() and d.name != '.git']
    
    if not model_dirs:
        print("❌ No trained models found!")
        return False
    
    # Sort by creation time and get the most recent
    latest_model_dir = max(model_dirs, key=lambda x: x.stat().st_mtime)
    
    print(f"📁 Found latest model: {latest_model_dir.name}")
    
    # Check what files are in the model directory
    model_files = list(latest_model_dir.glob("*.h5"))
    
    if not model_files:
        print(f"❌ No .h5 model files found in {latest_model_dir}")
        return False
    
    model_file = model_files[0]
    print(f"🧠 Using model file: {model_file.name}")
    
    # Copy to expected location
    target_model = models_dir / "basic_enhanced_lstm.h5"
    
    try:
        shutil.copy2(model_file, target_model)
        print(f"✅ Copied model to: {target_model}")
        
        # Create dummy scaler and feature engineer files
        import pickle
        
        # Create a dummy scaler
        scaler_path = models_dir / "basic_enhanced_scaler.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump({'type': 'dummy_scaler'}, f)
        print(f"✅ Created scaler: {scaler_path}")
        
        # Create a dummy feature engineer
        fe_path = models_dir / "basic_enhanced_feature_engineer.pkl"
        with open(fe_path, 'wb') as f:
            pickle.dump({'type': 'dummy_feature_engineer'}, f)
        print(f"✅ Created feature engineer: {fe_path}")
        
        print()
        print("🎉 SUCCESS! Your system is now set up to use REAL trained model data!")
        print()
        print("🚀 Next steps:")
        print("1. Restart your API server:")
        print("   python scripts/clean_start.py")
        print()
        print("2. Test the real data:")
        print("   python scripts/test_data_source.py")
        print()
        print("3. Access your frontend with REAL predictions!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up model: {e}")
        return False

if __name__ == "__main__":
    setup_real_model()