@echo off
REM ClauseWise 3D Web - Quick Start Script for Windows

echo 🚀 Starting ClauseWise 3D Web Interface...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed
    exit /b 1
)

REM Start backend
echo 📦 Starting Python backend...
cd Claudwise

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo 📚 Installing Python dependencies...
pip install -r requirements.txt -q

REM Start FastAPI server in new window
echo 🔧 Starting FastAPI server on port 8000...
start cmd /k python server.py

cd ..

REM Start frontend in new window
echo ⚡ Starting React frontend on port 5173...
npm install --legacy-peer-deps -q >nul 2>&1
start cmd /k npm run dev

echo.
echo ✅ ClauseWise is running!
echo.
echo 📍 Frontend: http://localhost:5173
echo 📍 Backend:  http://localhost:8000
echo 📍 API Docs: http://localhost:8000/docs
echo.
pause
