# ClauseWise 3D Web Interface

Your new interactive 3D web frontend for ClauseWise is complete! This modern, minimal interface replaces the Streamlit UI with a professional React-based application.

## What's New

### Visual Design
- **Dark Theme**: Professional dark interface with gradient accents
- **Interactive 3D Scene**: Animated geometric shapes in the background using Three.js
- **Smooth Animations**: Framer Motion transitions and micro-interactions
- **Minimal & Clean**: No clutter, focus on functionality
- **Responsive**: Works seamlessly on desktop, tablet, and mobile

### Architecture
- **Frontend**: React + Three.js + Vite for lightning-fast development
- **Backend**: FastAPI for efficient Python integration
- **Communication**: RESTful API with CORS support
- **Modern Tech Stack**: Latest libraries and best practices

### Pages & Features

#### 1. Document Upload (📄)
- Drag-and-drop file upload
- Support for PDF, DOCX, TXT
- Real-time file validation
- Comprehensive analysis results
- Visual cards showing:
  - Document classification
  - Clause count
  - Word count
  - Entities found
- Detailed results with clauses and entities

#### 2. Clause Simplifier (✨)
- Transform complex legal text
- Side-by-side comparison view
- Original vs. simplified
- Professional comparison layout

#### 3. Entity Extractor (🏷️)
- Extract legal entities automatically
- Color-coded entity types:
  - Parties (Indigo)
  - Dates (Cyan)
  - Money (Green)
  - Organizations (Amber)
  - Locations (Violet)
  - Legal Terms (Pink)
  - Obligations (Red)
- Entity count badges
- Interactive entity cards

#### 4. Analytics Dashboard (📊)
- Placeholder for comprehensive analytics
- Ready for data visualization integration
- Document statistics and metrics

### Design Details

**Color Palette:**
- Primary: #6366f1 (Indigo)
- Secondary: #818cf8 (Light Indigo)
- Dark Background: #0f1419
- Card Background: #1a1f2e
- Text Primary: #ffffff
- Text Secondary: #a0aec0

**Typography:**
- Inter font for UI (sans-serif)
- Weights: 300, 400, 500, 600, 700, 800
- Playfair Display reserved for future headers

**Components:**
- Modern card-based layout
- Gradient buttons with hover effects
- Glass-morphism effects (backdrop blur)
- Smooth transitions (0.2-0.3s)
- 16px border radius standard

## File Structure

```
project/
├── src/
│   ├── main.jsx                    # React entry point
│   ├── App.jsx                     # Main app component
│   ├── components/
│   │   ├── Scene3D.jsx             # Three.js 3D scene
│   │   ├── Navigation.jsx          # Sidebar navigation
│   │   └── pages/
│   │       ├── DocumentUpload.jsx  # Upload & analysis
│   │       ├── ClauseSimplifier.jsx    # Simplification
│   │       ├── EntityExtractor.jsx     # Entity extraction
│   │       └── Analytics.jsx       # Analytics dashboard
│   └── styles/
│       ├── global.css              # Global styles & variables
│       ├── app.css                 # App layout
│       ├── navigation.css          # Navigation styling
│       └── pages.css               # Page component styles
├── index.html                      # HTML entry
├── package.json                    # Node dependencies
├── vite.config.js                  # Vite config
├── Claudwise/
│   ├── server.py                   # FastAPI backend
│   ├── requirements.txt            # Python dependencies
│   └── [existing analysis code]
└── SETUP.md                        # Setup instructions
```

## Key Technologies

**Frontend:**
- React 18.2 - UI library
- Three.js - 3D graphics
- React Three Fiber - React + Three.js
- Framer Motion - Animations
- Vite - Build tool
- CSS3 - Styling

**Backend:**
- FastAPI - Python web framework
- Uvicorn - ASGI server
- Python 3.8+ - Runtime
- Existing ClauseWise modules

## Getting Started

### Quick Start

```bash
# Terminal 1: Backend
cd Claudwise
source venv/bin/activate  # or venv\Scripts\activate on Windows
python server.py

# Terminal 2: Frontend
npm run dev
```

Visit `http://localhost:5173`

### Production Build

```bash
npm run build
# dist/ folder ready for deployment
```

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Modern mobile browsers

## Performance Optimizations

- GPU-accelerated 3D rendering
- CSS animations (no JavaScript animations)
- Efficient React re-renders
- Lazy component loading ready
- Code splitting support in Vite

## Future Enhancements

- Add more 3D scene elements
- Implement document comparison
- Add chart visualizations in Analytics
- Export analysis results (PDF/Excel)
- Dark/light theme toggle
- User preferences persistence
- Real-time collaboration features

## API Integration

The frontend communicates with the backend through these endpoints:

```
POST /analyze           - Analyze a document
POST /simplify         - Simplify a clause
POST /extract-entities - Extract entities
GET  /health           - Health check
GET  /status           - API status
```

## Customization

### Change Accent Color

Edit `src/styles/global.css`:
```css
--accent: #6366f1;      /* Change this */
--accent-light: #818cf8; /* And this */
```

### Add New Navigation Items

Edit `src/components/Navigation.jsx`:
```jsx
const menuItems = [
  { id: 'upload', label: 'Upload', icon: '📄' },
  { id: 'your-new-page', label: 'New Page', icon: '🆕' },
  // ...
]
```

## Troubleshooting

**Frontend won't load:**
- Clear browser cache (Ctrl+Shift+Delete)
- Check console for errors (F12)
- Verify backend is running

**3D scene not rendering:**
- Check WebGL support in browser
- Update graphics drivers
- Try different browser

**Slow performance:**
- Close other tabs
- Check CPU/GPU usage
- Reduce animation intensity

## Support & Development

For development questions, refer to SETUP.md for detailed instructions.

---

**ClauseWise 3D Web** - Professional. Modern. Minimal.
