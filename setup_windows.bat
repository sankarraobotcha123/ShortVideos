@echo off
setlocal

echo ========================================
echo Edu Content Platform - Windows Setup
echo ========================================

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.12 and try again.
  exit /b 1
)

if not exist .venv (
  echo Creating virtual environment...
  python -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts\setup_project.py --seed-demo

where npm >nul 2>nul
if errorlevel 1 (
  echo npm was not found. Skipping frontend install. Install Node.js later and run npm run frontend:install.
) else (
  npm run frontend:install
)

echo.
echo Setup completed.
echo Start backend:  .venv\Scripts\activate ^&^& uvicorn app.main:app --reload
echo Start frontend: npm run frontend:dev
echo.
endlocal
