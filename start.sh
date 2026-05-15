#!/bin/bash

echo "============================================================"
echo "Starting Crop Disease Detection System"
echo "============================================================"
echo ""

# Activate virtual environment
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

echo "Starting Flask application..."
echo ""
echo "Application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
