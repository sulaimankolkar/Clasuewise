# ClauseWise 3D Web - Setup Guide

## Overview

ClauseWise now features a modern, interactive 3D web interface built with React, Three.js, and Vite, with a Python FastAPI backend for AI-powered legal document analysis.

## Project Structure

```
project/
├── Claudwise/              # Python backend
│   ├── server.py          # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── core/              # Core analysis logic
│   ├── models/            # AI models
│   └── utils/             # Document processing utilities
├── src/                   # React frontend
│   ├── components/        # React components
│   ├── styles/            # CSS styling
│   └── main.jsx          # Entry point
├── package.json          # Node dependencies
├── vite.config.js        # Vite configuration
└── index.html            # HTML entry point
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Installation

### 1. Backend Setup

```bash
cd Claudwise

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
# Return to project root
cd ..

# Install Node dependencies
npm install
```

## Running the Application

### Terminal 1: Start Python Backend

```bash
cd Claudwise

# Activate virtual environment (if not already active)
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start FastAPI server
python server.py
```

The backend will be available at `http://localhost:8000`

### Terminal 2: Start React Frontend

```bash
# From project root
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Features

### 📄 Document Analysis
- Upload legal documents (PDF, DOCX, TXT)
- Get comprehensive AI-powered analysis
- View clause extraction and classification
- Extract named entities

### ✨ Clause Simplifier
- Transform complex legal language into plain English
- Maintain legal meaning while improving comprehension
- Side-by-side comparison view

### 🏷️ Entity Extractor
- Automatically identify legal entities
- Extract parties, dates, money, obligations
- Categorized results with color coding

### 📊 Analytics Dashboard
- View analysis results and statistics
- Visualize document insights
- Track document metrics

## API Endpoints

- `GET /health` - Health check
- `GET /status` - API status and component information
- `POST /analyze` - Analyze a document
- `POST /simplify` - Simplify a legal clause
- `POST /extract-entities` - Extract entities from text

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Performance Notes

- First load may take 2-3 minutes as models are initialized
- 3D scene runs at 60fps with GPU acceleration
- Optimized for files up to 10MB

## Troubleshooting

### Models not loading
- Check Python environment is activated
- Ensure all requirements are installed: `pip install -r Claudwise/requirements.txt`

### Frontend not connecting to backend
- Verify backend is running on localhost:8000
- Check browser console for CORS errors
- Ensure vite.config.js proxy is correct

### Port conflicts
- Change backend port in `Claudwise/server.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`
- Change frontend port in `vite.config.js`: `port: 5174`

## Development

### Adding New Pages

1. Create component in `src/components/pages/`
2. Add route in `src/App.jsx`
3. Add navigation item in `src/components/Navigation.jsx`

### Styling

- Use CSS variables from `src/styles/global.css`
- Follow existing component patterns in `src/styles/pages.css`
- Maintain responsive design with provided media queries

### Backend Extensions

- Add new endpoints in `Claudwise/server.py`
- Use existing analyzer methods or create new ones in `core/clausewise_analyzer.py`
- Follow FastAPI patterns for request/response handling

## License

MIT
