#!/bin/bash

echo "============================================================"
echo "Crop Disease Detection System - Linux/Mac Setup"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

echo "[1/6] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/6] Activating virtual environment..."
source venv/bin/activate

echo "[3/6] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/6] Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template"
    echo "IMPORTANT: Edit .env and change SECRET_KEY before running!"
else
    echo ".env file already exists"
fi

echo "[5/6] Creating upload directory..."
mkdir -p app/static/uploads

echo "[6/6] Initializing database..."
python init_db.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to initialize database"
    exit 1
fi

echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and change SECRET_KEY"
echo "2. Run: ./start.sh"
echo "3. Visit: http://localhost:5000"
echo ""
echo "Default admin credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "IMPORTANT: Change admin password after first login!"
echo "============================================================"
