# ClauseWise 3D Web - Quick Start

## 🚀 Get Running in 2 Minutes

### Option 1: Automatic (Recommended)

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

Then open: **http://localhost:5173**

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd Claudwise
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

**Terminal 2 - Frontend:**
```bash
npm install --legacy-peer-deps
npm run dev
```

Then open: **http://localhost:5173**

---

## 📚 What's Included

| Feature | Status |
|---------|--------|
| 3D Animated Background | ✅ |
| Document Upload | ✅ |
| Clause Simplification | ✅ |
| Entity Extraction | ✅ |
| Professional Dark UI | ✅ |
| Responsive Design | ✅ |
| Smooth Animations | ✅ |
| FastAPI Backend | ✅ |

---

## 🎯 Features at a Glance

### 📄 Document Analysis
Upload legal documents and get instant insights:
- Document classification
- Clause extraction
- Entity recognition
- Key obligations

### ✨ Clause Simplifier
Transform complex legal text into plain language:
- Side-by-side comparison
- Professional layout
- One-click simplification

### 🏷️ Entity Extractor
Automatically find important information:
- Parties, dates, money amounts
- Legal terms, locations
- Obligations and responsibilities

### 📊 Analytics Dashboard
Comprehensive insights from your analyses

---

## 🎨 Visual Overview

```
┌────────────────────────────────────────────┐
│  ClauseWise 3D Web Interface               │
│                                            │
│  ┌──────────┬─────────────────────────┐   │
│  │          │                         │   │
│  │  📄 UPLOAD  Animated 3D Scene   │   │
│  │  ✨ SIMPLIFY  (Geometric Shapes) │   │
│  │  🏷️ EXTRACT                     │   │
│  │  📊 ANALYTICS                   │   │
│  │                                 │   │
│  │  Sidebar        Content Area    │   │
│  └──────────┴─────────────────────────┘   │
│                                            │
│  Dark Theme • Smooth Animations            │
│  Interactive 3D • Professional Design      │
└────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

**Frontend:** React + Three.js + Framer Motion
**Backend:** FastAPI + Python
**Build:** Vite (Lightning Fast)
**Styling:** Modern CSS with variables

---

## 📁 Project Structure

```
project/
├── src/                 # React application
│   ├── components/      # React components
│   └── styles/          # CSS styling
├── Claudwise/           # Python backend
│   └── server.py        # FastAPI app
├── package.json         # npm dependencies
├── vite.config.js       # Build config
└── SETUP.md             # Detailed guide
```

---

## 🔧 Commands

| Command | Purpose |
|---------|---------|
| `npm install --legacy-peer-deps` | Install frontend dependencies |
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `python server.py` | Start backend (Claudwise folder) |

---

## 📍 URLs

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🎮 Try It Out

1. Go to **Upload** page
2. Drag and drop a legal document (PDF/DOCX/TXT)
3. See instant analysis results
4. Try **Clause Simplifier** with sample text
5. Use **Entity Extractor** to find legal entities

---

## ⚡ Performance

- **3D Rendering:** 60fps GPU-accelerated
- **Frontend Bundle:** 279KB gzipped
- **Build Time:** ~7 seconds
- **Dev Server:** Hot reload in <100ms

---

## ❓ Troubleshooting

**Backend won't start?**
- Check Python version (3.8+)
- Verify virtual environment activated
- Try: `pip install --upgrade pip`

**Frontend won't load?**
- Clear browser cache (Ctrl+Shift+Delete)
- Check console for errors (F12)
- Verify backend is running

**Port in use?**
- Backend: Change port in `Claudwise/server.py`
- Frontend: Change port in `vite.config.js`

---

## 📖 Documentation

- **Full Guide:** See `SETUP.md`
- **UI Details:** See `WEB_UI_README.md`
- **Implementation:** See `IMPLEMENTATION_SUMMARY.md`
- **Files Created:** See `FILES_CREATED.md`

---

## 🚀 Ready to Deploy?

1. Run: `npm run build`
2. Upload `dist/` folder to any web host
3. Backend can be deployed separately on your server
4. Configure API endpoint in frontend if needed

---

**That's it! You're ready to use ClauseWise 3D Web.**

Questions? Check the documentation files or review the code comments.

Enjoy! 🎉
