import React from 'react'
import { motion } from 'framer-motion'
import '../styles/navigation.css'

function Navigation({ currentPage, setCurrentPage }) {
  const menuItems = [
    { id: 'upload', label: 'Upload', icon: '📄' },
    { id: 'simplifier', label: 'Simplify', icon: '✨' },
    { id: 'extractor', label: 'Extract', icon: '🏷️' },
    { id: 'analytics', label: 'Analytics', icon: '📊' },
  ]

  return (
    <nav className="navigation">
      <div className="nav-header">
        <div className="logo">
          <span className="logo-icon">⚖️</span>
          <span className="logo-text">ClauseWise</span>
        </div>
      </div>

      <div className="nav-menu">
        {menuItems.map((item) => (
          <motion.button
            key={item.id}
            className={`nav-item ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => setCurrentPage(item.id)}
            whileHover={{ x: 4 }}
            whileTap={{ scale: 0.98 }}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
            {currentPage === item.id && <motion.div className="nav-indicator" layoutId="indicator" />}
          </motion.button>
        ))}
      </div>

      <div className="nav-footer">
        <div className="nav-badge">
          <span>v1.0</span>
        </div>
      </div>
    </nav>
  )
}

export default Navigation
