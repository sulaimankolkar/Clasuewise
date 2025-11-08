import React from 'react'
import { motion } from 'framer-motion'
import '../../styles/pages.css'

function Analytics() {
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
        <h1>Analytics Dashboard</h1>
        <p>Comprehensive insights and visualizations from your analyses</p>
      </motion.div>

      <motion.div className="analytics-empty" variants={itemVariants}>
        <div className="empty-icon">📊</div>
        <h3>No analysis data available</h3>
        <p>Analyze a document first to view comprehensive analytics and insights</p>
      </motion.div>
    </motion.div>
  )
}

export default Analytics
