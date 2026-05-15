@echo off
echo ============================================================
echo Starting Crop Disease Detection System
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist venv\Scripts\activate.bat (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
)

REM Check if database exists, if not initialize it
if not exist instance\crop_disease.db (
    echo Initializing database...
    python init_db.py
)

echo.
echo ============================================================
echo Application starting...
echo ============================================================
echo.
echo Access the application at: http://localhost:5000
echo.
echo Default credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Run the application
python run.py
