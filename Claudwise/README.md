# ⚖️ ClauseWise - AI-Powered Legal Document Analyzer

ClauseWise is an advanced AI-powered legal document analyzer designed to simplify, decode, and classify complex legal texts for lawyers, businesses, and laypersons alike. Using cutting-edge generative AI, ClauseWise automates the clause analysis workflow to make legal documents more accessible and understandable.

## 🌟 Features

### 1. **Clause Simplification**
- Automatically rewrites complex legal clauses into simplified, layman-friendly language
- Maintains legal meaning while improving comprehension
- Powered by IBM Granite-3.2-2B Instruct model

### 2. **Named Entity Recognition (NER)**
- Identifies and extracts key legal entities:
  - Parties and organizations
  - Dates and deadlines
  - Monetary values
  - Legal obligations
  - Jurisdictions and legal terms

### 3. **Clause Extraction and Breakdown**
- Detects and segments individual clauses from lengthy legal documents
- Classifies clauses by type (Confidentiality, Termination, Payment, etc.)
- Assesses clause complexity levels (Low, Medium, High)

### 4. **Document Type Classification**
- Accurately classifies legal documents into categories:
  - Non-Disclosure Agreement (NDA)
  - Employment Contract
  - Service Agreement
  - Lease Agreement
  - Purchase Agreement
  - Partnership Agreement
  - License Agreement

### 5. **Multi-Format Document Support**
- Supports PDF, DOCX, and TXT file formats
- Handles documents up to 10MB in size
- Robust text extraction with error handling

### 6. **Interactive Web Interface**
- Modern Streamlit-based user interface
- Multiple analysis modes:
  - 📄 Document Analysis
  - 🔍 Clause Simplifier
  - 🏷️ Entity Extractor
  - 📊 Analytics Dashboard

## 🛠️ Technology Stack

- **Python 3.8+**
- **IBM Granite-3.2-2B Instruct** - Core AI model for text generation and analysis
- **Streamlit** - Web application framework
- **spaCy** - Natural Language Processing and NER
- **HuggingFace Transformers** - Model pipeline management
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX document processing
- **Plotly** - Interactive data visualizations

## 📦 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Claudwise
```

2. **Create a virtual environment:**
```bash
python -m venv clausewise_env
source clausewise_env/bin/activate  # On Windows: clausewise_env\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download spaCy model:**
```bash
python -m spacy download en_core_web_sm
```

## 🚀 Usage

### Running the Application

1. **Start the Streamlit app:**
```bash
streamlit run app.py
```

2. **Open your browser** and navigate to `http://localhost:8501`

### Using ClauseWise

#### Document Analysis
1. Navigate to the "📄 Document Analysis" tab
2. Upload a legal document (PDF, DOCX, or TXT)
3. Wait for the AI analysis to complete
4. Review the comprehensive analysis results:
   - Document classification and summary
   - Clause breakdown and statistics
   - Named entity extraction
   - Key obligations identification

#### Clause Simplification
1. Go to the "🔍 Clause Simplifier" tab
2. Paste a complex legal clause
3. Click "Simplify Clause" to get a layman-friendly version

#### Entity Extraction
1. Visit the "🏷️ Entity Extractor" tab
2. Input any legal text
3. Extract and view categorized legal entities

#### Analytics Dashboard
1. After analyzing a document, visit "📊 Analytics"
2. View detailed insights and visualizations
3. Explore clause distributions and complexity metrics

## 📁 Project Structure

```
Claudwise/
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration settings
├── requirements.txt                 # Python dependencies
├── README.md                       # Project documentation
├── core/
│   ├── __init__.py
│   └── clausewise_analyzer.py      # Main analyzer orchestrator
├── models/
│   ├── __init__.py
│   ├── granite_model.py            # IBM Granite model integration
│   └── ner_model.py               # Named Entity Recognition
└── utils/
    ├── __init__.py
    ├── document_processor.py       # Multi-format document processing
    └── clause_extractor.py         # Clause extraction and segmentation
```

## 🔧 Configuration

Key configuration options in `config.py`:

- **GRANITE_MODEL**: IBM Granite model identifier
- **SUPPORTED_FORMATS**: Allowed file formats
- **MAX_FILE_SIZE**: Maximum upload size (10MB)
- **DOCUMENT_TYPES**: Supported legal document categories
- **LEGAL_ENTITIES**: Entity types for NER

## 🎯 Use Cases

### For Lawyers
- Quick document review and analysis
- Clause complexity assessment
- Entity extraction for due diligence
- Document type verification

### For Businesses
- Contract review and understanding
- Risk assessment through obligation identification
- Simplified explanations for non-legal stakeholders
- Compliance checking

### For Individuals
- Understanding legal documents in plain language
- Identifying key terms and obligations
- Document type recognition
- Educational tool for legal literacy

## 🔮 Future Enhancements

- **Multi-language support** for international legal documents
- **Advanced risk scoring** for contract clauses
- **Comparative analysis** between multiple documents
- **Integration with legal databases** for precedent checking
- **API endpoints** for programmatic access
- **Batch processing** for multiple documents
- **Export functionality** for analysis reports

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **IBM** for the Granite-3.2-2B Instruct model
- **Streamlit** team for the excellent web framework
- **spaCy** for robust NLP capabilities
- **HuggingFace** for transformer model infrastructure

## 📞 Support

For questions, issues, or support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

---

**ClauseWise** - Making legal documents accessible to everyone through AI 🚀
