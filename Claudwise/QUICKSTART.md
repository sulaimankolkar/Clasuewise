# 🚀 ClauseWise Quick Start Guide

Get up and running with ClauseWise in just a few minutes!

## ⚡ Quick Setup

### 1. Prerequisites
- Python 3.8 or higher
- At least 4GB RAM (8GB recommended)
- Internet connection for model downloads

### 2. Installation

```bash
# Navigate to the ClauseWise directory
cd Claudwise

# Run the setup script (recommended)
python setup.py

# OR install manually:
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Launch the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📋 First Steps

### Upload and Analyze a Document

1. **Go to "📄 Document Analysis"**
2. **Click "Choose a legal document"**
3. **Upload a PDF, DOCX, or TXT file** (max 10MB)
4. **Wait for analysis** (may take 2-3 minutes for first run)
5. **Review the results:**
   - Document classification
   - Clause breakdown
   - Entity extraction
   - Key obligations

### Try Clause Simplification

1. **Navigate to "🔍 Clause Simplifier"**
2. **Paste a complex legal clause** like:
   ```
   The Party of the First Part hereby covenants and agrees that it shall indemnify, defend, and hold harmless the Party of the Second Part from and against any and all claims, demands, losses, costs, expenses, obligations, liabilities, damages, recoveries, and deficiencies, including interest, penalties, and reasonable attorney fees, that the Party of the Second Part may incur or suffer.
   ```
3. **Click "Simplify Clause"**
4. **Compare original vs. simplified versions**

### Extract Entities from Text

1. **Go to "🏷️ Entity Extractor"**
2. **Paste any legal text**
3. **Click "Extract Entities"**
4. **View categorized legal entities:**
   - Parties and organizations
   - Dates and monetary values
   - Legal terms and obligations

## 🎯 Sample Use Cases

### For Contract Review
- Upload employment contracts to identify key obligations
- Extract payment terms and deadlines
- Simplify complex clauses for stakeholder review

### For Legal Education
- Analyze different document types to understand structures
- Practice entity recognition on legal texts
- Learn to identify clause complexity levels

### For Business Analysis
- Review vendor agreements for risk assessment
- Extract key parties and financial terms
- Understand legal obligations in plain language

## 🔧 Troubleshooting

### Common Issues

**Model Loading Errors:**
- Ensure stable internet connection for first-time model download
- Check available disk space (models require ~2GB)
- Restart the application if models fail to load

**File Upload Issues:**
- Verify file format (PDF, DOCX, TXT only)
- Check file size (max 10MB)
- Ensure file is not corrupted or password-protected

**Performance Issues:**
- Close other resource-intensive applications
- Use smaller documents for faster processing
- Consider upgrading RAM for better performance

### Getting Help

1. **Check the logs** in the terminal/command prompt
2. **Review error messages** in the Streamlit interface
3. **Restart the application** if issues persist
4. **Check system requirements** and available resources

## 📊 Understanding Results

### Document Classification
ClauseWise identifies document types:
- **NDA**: Non-Disclosure Agreements
- **Employment**: Employment contracts
- **Service**: Service agreements
- **Lease**: Rental/lease agreements
- **Other**: Miscellaneous legal documents

### Clause Complexity
- **Low**: Simple, straightforward clauses
- **Medium**: Moderate complexity with some legal terms
- **High**: Complex clauses with advanced legal language

### Entity Types
- **PARTIES**: People and organizations involved
- **DATES**: Important dates and deadlines
- **MONEY**: Financial amounts and terms
- **OBLIGATIONS**: Key duties and responsibilities
- **LEGAL_TERMS**: Important legal concepts

## 🎉 Next Steps

Once you're comfortable with the basics:

1. **Explore the Analytics Dashboard** for detailed insights
2. **Try different document types** to see classification accuracy
3. **Experiment with clause simplification** on various complexity levels
4. **Use entity extraction** for due diligence workflows
5. **Integrate insights** into your legal review processes

## 💡 Tips for Best Results

- **Use clear, well-formatted documents** for better text extraction
- **Try different document types** to explore all features
- **Compare simplified clauses** with originals to verify accuracy
- **Use analytics** to identify document patterns and risks
- **Save important results** by copying text or taking screenshots

---

**Ready to analyze your first legal document? Let's get started! 🚀**
