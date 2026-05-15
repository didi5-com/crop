@echo off
echo ============================================================
echo Crop Disease Detection System - Windows Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/6] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
    echo IMPORTANT: Edit .env and change SECRET_KEY before running!
) else (
    echo .env file already exists
)

echo [5/6] Creating upload directory...
if not exist app\static\uploads mkdir app\static\uploads

echo [6/6] Initializing database...
python init_db.py
if errorlevel 1 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Edit .env file and change SECRET_KEY
echo 2. Run: start.bat
echo 3. Visit: http://localhost:5000
echo.
echo Default admin credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo IMPORTANT: Change admin password after first login!
echo ============================================================
pause
