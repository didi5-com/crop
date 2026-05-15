@echo off
echo ============================================================
echo Starting Crop Disease Detection System
echo ============================================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Starting Flask application...
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python run.py
