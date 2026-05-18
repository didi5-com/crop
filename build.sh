#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Try to install TensorFlow (optional - will fail on Python 3.14+)
echo "Attempting to install TensorFlow..."
pip install -r requirements-ml.txt || echo "⚠️  TensorFlow installation failed - ML model will not be available. System will use API fallback."

# Create instance directory if it doesn't exist
mkdir -p instance

# Download ML model (optional - only if TensorFlow installed)
python download_model.py || echo "Model download skipped - will use API fallback"

# Initialize database
python init_db.py

echo "✓ Build completed successfully!"
