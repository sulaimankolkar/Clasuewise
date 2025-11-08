#!/bin/bash

# ClauseWise 3D Web - Quick Start Script

echo "🚀 Starting ClauseWise 3D Web Interface..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

# Start backend
echo "📦 Starting Python backend..."
cd Claudwise

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt -q

# Start FastAPI server
echo "🔧 Starting FastAPI server on port 8000..."
python server.py &
BACKEND_PID=$!

# Give backend time to start
sleep 3

cd ..

# Start frontend
echo "⚡ Starting React frontend on port 5173..."
npm install --legacy-peer-deps -q 2>/dev/null || true
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ ClauseWise is running!"
echo ""
echo "📍 Frontend: http://localhost:5173"
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
