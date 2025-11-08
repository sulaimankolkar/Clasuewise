import React, { useState } from 'react'
import { motion } from 'framer-motion'
import '../../styles/pages.css'

function ClauseSimplifier() {
  const [input, setInput] = useState('')
  const [simplified, setSimplified] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSimplify = async () => {
    if (!input.trim()) {
      setError('Please enter a clause to simplify')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/simplify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clause: input }),
      })

      if (!response.ok) throw new Error('Simplification failed')
      const data = await response.json()
      setSimplified(data.simplified)
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

  return (
    <motion.div
      className="page-container"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.div className="page-header" variants={itemVariants}>
        <h1>Clause Simplifier</h1>
        <p>Transform complex legal language into clear, understandable text</p>
      </motion.div>

      <motion.div className="simplifier-section" variants={itemVariants}>
        <div className="input-group">
          <label>Original Clause</label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Paste your legal clause here..."
            disabled={loading}
          />
        </div>

        <motion.button
          className="btn btn-primary"
          onClick={handleSimplify}
          disabled={loading}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          {loading ? 'Simplifying...' : 'Simplify Clause'}
        </motion.button>

        {error && (
          <motion.div className="error-message" variants={itemVariants}>
            {error}
          </motion.div>
        )}

        {simplified && (
          <motion.div className="comparison" variants={itemVariants}>
            <div className="comparison-column">
              <h3>Original</h3>
              <div className="comparison-text original">
                {input}
              </div>
            </div>

            <div className="comparison-divider">→</div>

            <div className="comparison-column">
              <h3>Simplified</h3>
              <div className="comparison-text simplified">
                {simplified}
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>

      <motion.div className="tips-section" variants={itemVariants}>
        <h3>Tips for best results:</h3>
        <ul>
          <li>Paste a complete clause for better context</li>
          <li>Use single clauses rather than entire documents</li>
          <li>Include surrounding context if needed</li>
        </ul>
      </motion.div>
    </motion.div>
  )
}

export default ClauseSimplifier
