#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create instance directory if it doesn't exist
mkdir -p instance

# Download ML model (optional - will fallback to API if fails)
python download_model.py || echo "Model download failed, will use API fallback"

# Initialize database
python init_db.py

echo "✓ Build completed successfully!"
