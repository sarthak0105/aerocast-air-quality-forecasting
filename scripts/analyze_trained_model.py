#!/usr/bin/env python3
"""
Analyze the existing trained model to understand its structure
"""

import sys
import pickle
import json
from pathlib import Path
import tensorflow as tf
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def analyze_model(model_path):
    """Analyze a trained model file"""
    print(f"🔍 Analyzing model: {model_path}")
    print("=" * 60)
    
    try:
        # Load the model
        model = tf.keras.models.load_model(model_path)
        
        print("✅ Model loaded successfully!")
        print()
        
        # Model summary
        print("📊 MODEL ARCHITECTURE:")
        model.summary()
        print()
        
        # Input shape
        print("📥 INPUT REQUIREMENTS:")
        for i, layer in enumerate(model.layers):
            if hasattr(layer, 'input_shape'):
                print(f"   Layer {i} ({layer.name}): {layer.input_shape}")
        
        print(f"   Expected input shape: {model.input_shape}")
        print()
        
        # Output shape
        print("📤 OUTPUT SHAPE:")
        print(f"   Output shape: {model.output_shape}")
        print()
        
        # Model configuration
        print("⚙️ MODEL CONFIG:")
        config = model.get_config()
        print(f"   Model type: {config.get('name', 'Unknown')}")
        print(f"   Number of layers: {len(model.layers)}")
        
        # Try to get layer details
        for i, layer in enumerate(model.layers):
            if 'lstm' in layer.name.lower():
                print(f"   LSTM Layer {i}: {layer.name}")
                if hasattr(layer, 'units'):
                    print(f"     Units: {layer.units}")
                if hasattr(layer, 'return_sequences'):
                    print(f"     Return sequences: {layer.return_sequences}")
        
        return model
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def analyze_metadata(metadata_path):
    """Analyze model metadata if available"""
    if not metadata_path.exists():
        print("⚠️  No metadata file found")
        return None
    
    try:
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        print("📋 MODEL METADATA:")
        print(f"   Keys: {list(metadata.keys())}")
        
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                print(f"   {key}: {value}")
            elif isinstance(value, (list, tuple)) and len(value) < 10:
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: {type(value)} (length: {len(value) if hasattr(value, '__len__') else 'N/A'})")
        
        return metadata
        
    except Exception as e:
        print(f"❌ Error loading metadata: {e}")
        return None

def analyze_training_history(history_path):
    """Analyze training history if available"""
    if not history_path.exists():
        print("⚠️  No training history found")
        return None
    
    try:
        with open(history_path, 'r') as f:
            history = json.load(f)
        
        print("📈 TRAINING HISTORY:")
        print(f"   Keys: {list(history.keys())}")
        
        if 'loss' in history:
            final_loss = history['loss'][-1] if history['loss'] else 'N/A'
            print(f"   Final training loss: {final_loss}")
        
        if 'val_loss' in history:
            final_val_loss = history['val_loss'][-1] if history['val_loss'] else 'N/A'
            print(f"   Final validation loss: {final_val_loss}")
        
        if 'accuracy' in history:
            final_acc = history['accuracy'][-1] if history['accuracy'] else 'N/A'
            print(f"   Final accuracy: {final_acc}")
        
        return history
        
    except Exception as e:
        print(f"❌ Error loading training history: {e}")
        return None

def main():
    """Main analysis function"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🔍 Trained Model Analysis                                ║
║                                                              ║
║    Understanding your existing models                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    models_dir = Path("models")
    
    # Find all model directories
    model_dirs = [d for d in models_dir.iterdir() if d.is_dir() and d.name != '.git']
    
    if not model_dirs:
        print("❌ No model directories found!")
        return
    
    print(f"📁 Found {len(model_dirs)} model directories:")
    for i, model_dir in enumerate(model_dirs):
        print(f"   {i+1}. {model_dir.name}")
    
    print()
    
    # Analyze the most recent model
    latest_model_dir = max(model_dirs, key=lambda x: x.stat().st_mtime)
    print(f"🎯 Analyzing latest model: {latest_model_dir.name}")
    print()
    
    # Look for model files
    model_file = latest_model_dir / "lstm_model.h5"
    metadata_file = latest_model_dir / "metadata.pkl"
    history_file = latest_model_dir / "training_history.json"
    
    # Analyze model
    model = analyze_model(model_file)
    print()
    
    # Analyze metadata
    metadata = analyze_metadata(metadata_file)
    print()
    
    # Analyze training history
    history = analyze_training_history(history_file)
    print()
    
    # Provide recommendations
    print("🎯 RECOMMENDATIONS:")
    print("=" * 60)
    
    if model:
        input_shape = model.input_shape
        print(f"✅ Your model expects input shape: {input_shape}")
        
        if len(input_shape) == 3:  # (batch, timesteps, features)
            timesteps = input_shape[1]
            features = input_shape[2]
            print(f"   Timesteps: {timesteps}")
            print(f"   Features: {features}")
            print()
            print("🔧 To fix compatibility:")
            print(f"   1. Modify feature engineering to produce {features} features")
            print(f"   2. Use {timesteps} timesteps for input sequences")
            print("   3. Update model service to match this architecture")
        
        output_shape = model.output_shape
        if len(output_shape) == 2:  # (batch, outputs)
            outputs = output_shape[1]
            print(f"   Model outputs: {outputs} values")
            if outputs == 2:
                print("   ✅ Perfect! Model predicts both NO2 and O3")
            elif outputs == 1:
                print("   ⚠️  Model predicts single value - may need adjustment")
    
    print()
    print("🚀 Next steps:")
    print("   1. I'll create a compatible model service")
    print("   2. Update feature engineering to match your model")
    print("   3. Test with real predictions")

if __name__ == "__main__":
    main()