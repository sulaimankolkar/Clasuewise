import React, { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import Scene3D from './components/Scene3D'
import Navigation from './components/Navigation'
import DocumentUpload from './components/pages/DocumentUpload'
import ClauseSimplifier from './components/pages/ClauseSimplifier'
import EntityExtractor from './components/pages/EntityExtractor'
import Analytics from './components/pages/Analytics'
import './styles/app.css'

function App() {
  const [currentPage, setCurrentPage] = useState('upload')

  const renderPage = () => {
    switch (currentPage) {
      case 'upload':
        return <DocumentUpload />
      case 'simplifier':
        return <ClauseSimplifier />
      case 'extractor':
        return <EntityExtractor />
      case 'analytics':
        return <Analytics />
      default:
        return <DocumentUpload />
    }
  }

  return (
    <div className="app">
      <div className="canvas-container">
        <Canvas>
          <Scene3D />
        </Canvas>
      </div>

      <Navigation currentPage={currentPage} setCurrentPage={setCurrentPage} />

      <div className="content">
        {renderPage()}
      </div>
    </div>
  )
}

export default App
