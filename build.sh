#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create instance directory if it doesn't exist
mkdir -p instance

echo "✓ Build completed successfully!"
echo "Database tables will be created automatically on first run."
