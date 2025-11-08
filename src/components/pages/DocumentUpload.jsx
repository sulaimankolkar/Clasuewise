import React, { useState } from 'react'
import { motion } from 'framer-motion'
import '../../styles/pages.css'

function DocumentUpload() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    const files = e.dataTransfer.files
    if (files.length > 0) {
      setFile(files[0])
      setError(null)
    }
  }

  const handleChange = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      setFile(files[0])
      setError(null)
    }
  }

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error('Analysis failed')
      const data = await response.json()
      setResults(data)
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
        <h1>Document Analysis</h1>
        <p>Upload a legal document for comprehensive AI-powered analysis</p>
      </motion.div>

      {!results ? (
        <motion.div className="upload-section" variants={itemVariants}>
          <div
            className="upload-zone"
            onDrop={handleDrop}
            onDragOver={(e) => {
              e.preventDefault()
              e.currentTarget.classList.add('drag-active')
            }}
            onDragLeave={(e) => {
              e.currentTarget.classList.remove('drag-active')
            }}
          >
            <div className="upload-content">
              <motion.div className="upload-icon" whileHover={{ scale: 1.1 }}>
                📄
              </motion.div>
              <h3>Drag and drop your document</h3>
              <p>or</p>
              <label className="upload-button">
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  onChange={handleChange}
                  style={{ display: 'none' }}
                />
                Browse files
              </label>
              <p className="file-hint">Supported: PDF, DOCX, TXT (Max 10MB)</p>
            </div>
          </div>

          {file && (
            <motion.div className="file-info" variants={itemVariants}>
              <div className="file-details">
                <span className="file-name">{file.name}</span>
                <span className="file-size">{(file.size / 1024).toFixed(2)} KB</span>
              </div>
              <motion.button
                className="btn btn-primary"
                onClick={handleAnalyze}
                disabled={loading}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {loading ? 'Analyzing...' : 'Analyze Document'}
              </motion.button>
            </motion.div>
          )}

          {error && (
            <motion.div className="error-message" variants={itemVariants}>
              {error}
            </motion.div>
          )}
        </motion.div>
      ) : (
        <motion.div className="results-section" variants={itemVariants}>
          <ResultsDisplay results={results} onReset={() => setResults(null)} />
        </motion.div>
      )}
    </motion.div>
  )
}

function ResultsDisplay({ results, onReset }) {
  const resultVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.05 } },
  }

  const cardVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 },
  }

  return (
    <motion.div variants={resultVariants} initial="hidden" animate="visible">
      <motion.button
        className="btn btn-secondary"
        onClick={onReset}
        variants={cardVariants}
        whileHover={{ scale: 1.02 }}
      >
        ← Back
      </motion.button>

      <div className="results-grid">
        <motion.div className="result-card" variants={cardVariants}>
          <div className="result-label">Document Type</div>
          <div className="result-value">{results.classification || 'Unknown'}</div>
        </motion.div>

        <motion.div className="result-card" variants={cardVariants}>
          <div className="result-label">Total Clauses</div>
          <div className="result-value">{results.clause_statistics?.total_clauses || 0}</div>
        </motion.div>

        <motion.div className="result-card" variants={cardVariants}>
          <div className="result-label">Word Count</div>
          <div className="result-value">{results.word_count?.toLocaleString() || 0}</div>
        </motion.div>

        <motion.div className="result-card" variants={cardVariants}>
          <div className="result-label">Entities Found</div>
          <div className="result-value">
            {Object.values(results.entities || {}).reduce((sum, arr) => sum + arr.length, 0)}
          </div>
        </motion.div>
      </div>

      {results.summary && (
        <motion.div className="summary-section" variants={cardVariants}>
          <h3>Summary</h3>
          <p>{results.summary}</p>
        </motion.div>
      )}

      {results.obligations && results.obligations.length > 0 && (
        <motion.div className="obligations-section" variants={cardVariants}>
          <h3>Key Obligations</h3>
          <ul>
            {results.obligations.slice(0, 5).map((obligation, idx) => (
              <li key={idx}>{obligation}</li>
            ))}
          </ul>
        </motion.div>
      )}

      {results.clauses && results.clauses.length > 0 && (
        <motion.div className="clauses-section" variants={cardVariants}>
          <h3>Clauses ({results.clauses.length})</h3>
          <div className="clauses-grid">
            {results.clauses.slice(0, 6).map((clause, idx) => (
              <div key={idx} className={`clause-card complexity-${clause.complexity.toLowerCase()}`}>
                <div className="clause-type">{clause.type}</div>
                <div className="clause-complexity">{clause.complexity}</div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {results.entities && Object.keys(results.entities).length > 0 && (
        <motion.div className="entities-section" variants={cardVariants}>
          <h3>Extracted Entities</h3>
          <div className="entities-grid">
            {Object.entries(results.entities).map(([type, entities]) =>
              entities.length > 0 ? (
                <div key={type} className="entity-group">
                  <div className="entity-type">{type.replace(/_/g, ' ')}</div>
                  <div className="entity-list">
                    {entities.slice(0, 3).map((entity, idx) => (
                      <span key={idx} className="entity-tag">{entity}</span>
                    ))}
                  </div>
                </div>
              ) : null
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}

export default DocumentUpload
