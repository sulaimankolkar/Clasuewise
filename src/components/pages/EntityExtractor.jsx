import React, { useState } from 'react'
import { motion } from 'framer-motion'
import '../../styles/pages.css'

function EntityExtractor() {
  const [input, setInput] = useState('')
  const [entities, setEntities] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleExtract = async () => {
    if (!input.trim()) {
      setError('Please enter text to extract entities from')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/extract-entities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input }),
      })

      if (!response.ok) throw new Error('Entity extraction failed')
      const data = await response.json()
      setEntities(data.entities)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, staggerChildren: 0.1 },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 },
  }

  const entityColors = {
    PARTIES: '#6366f1',
    DATES: '#06b6d4',
    MONEY: '#10b981',
    ORGANIZATIONS: '#f59e0b',
    LOCATIONS: '#8b5cf6',
    LEGAL_TERMS: '#ec4899',
    OBLIGATIONS: '#ef4444',
  }

  return (
    <motion.div
      className="page-container"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div className="page-header" variants={itemVariants}>
        <h1>Entity Extractor</h1>
        <p>Automatically identify and extract key legal entities from any text</p>
      </motion.div>

      <motion.div className="extractor-section" variants={itemVariants}>
        <div className="input-group">
          <label>Legal Text</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste your legal text here..."
            disabled={loading}
          />
        </div>

        <motion.button
          className="btn btn-primary"
          onClick={handleExtract}
          disabled={loading}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {loading ? 'Extracting...' : 'Extract Entities'}
        </motion.button>

        {error && (
          <motion.div className="error-message" variants={itemVariants}>
            {error}
          </motion.div>
        )}

        {entities && (
          <motion.div className="entities-results" variants={itemVariants}>
            <div className="entities-grid">
              {Object.entries(entities).map(([type, items]) =>
                items && items.length > 0 ? (
                  <motion.div
                    key={type}
                    className="entity-card"
                    style={{ borderTopColor: entityColors[type] }}
                    variants={itemVariants}
                  >
                    <div className="entity-card-header">
                      <h4>{type.replace(/_/g, ' ')}</h4>
                      <span className="entity-count">{items.length}</span>
                    </div>
                    <div className="entity-items">
                      {items.map((item, idx) => (
                        <span key={idx} className="entity-item">{item}</span>
                      ))}
                    </div>
                  </motion.div>
                ) : null
              )}
            </div>
          </motion.div>
        )}
      </motion.div>
    </motion.div>
  )
}

export default EntityExtractor
