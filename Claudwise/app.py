"""
ClauseWise - AI-Powered Legal Document Analyzer
Main Streamlit Application with Secure Authentication
"""
# Force reload

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
from typing import Dict, Any, List
import logging

# Import our modules
from core.clausewise_analyzer import ClauseWiseAnalyzer
from auth.auth_ui import require_authentication, render_user_menu, render_change_password_modal
from auth.admin_panel import render_admin_panel
from auth.authenticator import SecureAuthenticator
from config import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Premium Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0 3rem 0;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    .premium-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }
    
    .entity-tag {
        background: linear-gradient(135deg, #ddd6fe, #e0e7ff);
        color: #5b21b6;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
        display: inline-block;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .complexity-high { border-left: 4px solid #ef4444; }
    .complexity-medium { border-left: 4px solid #f59e0b; }
    .complexity-low { border-left: 4px solid #10b981; }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            margin: 1rem 0 2rem 0;
        }
        .premium-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .metric-card {
            padding: 1rem;
        }
    }
    
    /* Enhanced Streamlit Components */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 0.75rem 1rem;
    }
    
    .stFileUploader > div {
        background: linear-gradient(135deg, #f8fafc, #ffffff);
        border: 2px dashed #cbd5e1;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #6366f1;
        background: linear-gradient(135deg, #f1f5f9, #f8fafc);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
    }
    
    /* Metrics Enhancement */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_analyzer():
    """Load and cache the ClauseWise analyzer"""
    with st.spinner("🔄 Loading AI models... This may take 2-3 minutes on first run."):
        try:
            return ClauseWiseAnalyzer()
        except Exception as e:
            st.error(f"Failed to load analyzer: {str(e)}")
            st.info("💡 Try refreshing the page or check your internet connection.")
            return None

def main():
    """Main application function with authentication"""
    
    # Check authentication first
    if not require_authentication():
        return
    
    # Render change password modal if requested
    if st.session_state.get('show_change_password', False):
        render_change_password_modal()
        return
    
    # Premium Header
    st.markdown('<h1 class="main-header">⚖️ ClauseWise</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <p style="font-size: 1.25rem; color: #64748b; font-weight: 400; margin: 0;">
            Premium AI-Powered Legal Document Analysis Platform
        </p>
        <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <span style="color: #10b981; font-size: 0.875rem; font-weight: 500;">✓ Enterprise Security</span>
            <span style="color: #10b981; font-size: 0.875rem; font-weight: 500;">✓ AI-Powered Analysis</span>
            <span style="color: #10b981; font-size: 0.875rem; font-weight: 500;">✓ Real-time Processing</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render user menu in sidebar
    render_user_menu()
    
    # Check if user is admin to show admin panel
    authenticator = SecureAuthenticator()
    current_user = authenticator.get_current_user()
    is_admin = authenticator.is_admin(current_user) if current_user else False
    
    # Navigation menu (with admin panel for admins)
    menu_options = ["📄 Document Analysis", "🔍 Clause Simplifier", "🏷️ Entity Extractor", "📊 Analytics"]
    menu_icons = ["file-earmark-text", "search", "tags", "graph-up"]
    
    if is_admin:
        menu_options.append("🔧 Admin Panel")
        menu_icons.append("gear")
    
    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
    
    # Initialize analyzer
    analyzer = load_analyzer()
    if analyzer is None:
        st.error("❌ Failed to initialize ClauseWise analyzer")
        st.info("🔄 Please refresh the page to try again")
        st.stop()
    
    # Show model status
    if hasattr(analyzer, 'model_type'):
        if analyzer.model_type == "granite":
            st.success("🚀 Using IBM Granite-3.2-2B model for advanced AI analysis")
        elif analyzer.model_type == "simple":
            st.info("⚡ Using rule-based analysis for instant results")
            st.caption("📋 Provides document classification, clause extraction, and basic simplification")
    
    if selected == "📄 Document Analysis":
        document_analysis_page(analyzer)
    elif selected == "🔍 Clause Simplifier":
        clause_simplifier_page(analyzer)
    elif selected == "🏷️ Entity Extractor":
        entity_extractor_page(analyzer)
    elif selected == "📊 Analytics":
        analytics_page()
    elif selected == "🔧 Admin Panel" and is_admin:
        render_admin_panel()

def document_analysis_page(analyzer):
    """Document analysis page"""
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #1e293b; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            📄 Document Analysis
        </h2>
        <p style="color: #64748b; margin: 0; font-size: 1rem;">
            Upload your legal document for comprehensive AI-powered analysis with clause extraction, entity recognition, and complexity assessment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a legal document",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT (Max size: 10MB)"
    )
    
    if uploaded_file is not None:
        # Validate file size
        if len(uploaded_file.getvalue()) > MAX_FILE_SIZE:
            st.error(f"File size exceeds {MAX_FILE_SIZE / (1024*1024):.1f}MB limit")
            return
        
        # Process document
        with st.spinner("🔄 Analyzing document... This may take a few minutes."):
            try:
                results = analyzer.analyze_document(uploaded_file.getvalue(), uploaded_file.name)
                
                # Store results in session state
                st.session_state['analysis_results'] = results
                
                display_analysis_results(results)
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                logger.error(f"Document analysis error: {e}")

def display_analysis_results(results: Dict[str, Any]):
    """Display comprehensive analysis results"""
    
    # Document Overview
    st.markdown("""
    <div class="premium-card">
        <h3 style="color: #1e293b; font-weight: 600; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;">
            📋 Document Overview
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Document Type", results.get('classification', 'Unknown'))
    
    with col2:
        st.metric("Total Clauses", results.get('clause_statistics', {}).get('total_clauses', 0))
    
    with col3:
        st.metric("Word Count", f"{results.get('word_count', 0):,}")
    
    with col4:
        entities = results.get('entities', {})
        total_entities = sum(len(entity_list) for entity_list in entities.values())
        st.metric("Entities Found", total_entities)
    
    # Document Summary
    st.subheader("📝 Document Summary")
    st.markdown(f"**Summary:** {results.get('summary', 'No summary available')}")
    
    # Key Obligations
    obligations = results.get('obligations', [])
    if obligations:
        st.subheader("⚖️ Key Obligations")
        for i, obligation in enumerate(obligations[:5], 1):  # Show top 5
            st.markdown(f"**{i}.** {obligation}")
    
    # Clause Analysis
    st.subheader("📑 Clause Analysis")
    
    clauses = results.get('clauses', [])
    if clauses:
        # Clause statistics visualization
        clause_stats = results.get('clause_statistics', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Clause types pie chart
            clause_types = clause_stats.get('clause_types', {})
            if clause_types:
                fig_types = px.pie(
                    values=list(clause_types.values()),
                    names=list(clause_types.keys()),
                    title="Clause Types Distribution"
                )
                st.plotly_chart(fig_types, use_container_width=True)
        
        with col2:
            # Complexity distribution
            complexity_dist = clause_stats.get('complexity_distribution', {})
            if complexity_dist:
                fig_complexity = px.bar(
                    x=list(complexity_dist.keys()),
                    y=list(complexity_dist.values()),
                    title="Clause Complexity Distribution",
                    color=list(complexity_dist.keys()),
                    color_discrete_map={'Low': '#388e3c', 'Medium': '#f57c00', 'High': '#d32f2f'}
                )
                st.plotly_chart(fig_complexity, use_container_width=True)
        
        # Display individual clauses
        st.subheader("📄 Individual Clauses")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            clause_types_filter = st.multiselect(
                "Filter by Type",
                options=list(set(clause['type'] for clause in clauses)),
                default=list(set(clause['type'] for clause in clauses))
            )
        
        with col2:
            complexity_filter = st.multiselect(
                "Filter by Complexity",
                options=['Low', 'Medium', 'High'],
                default=['Low', 'Medium', 'High']
            )
        
        with col3:
            show_simplified = st.checkbox("Show Simplified Version", value=False)
        
        # Filter clauses
        filtered_clauses = [
            clause for clause in clauses
            if clause['type'] in clause_types_filter and clause['complexity'] in complexity_filter
        ]
        
        # Display filtered clauses
        for clause in filtered_clauses[:10]:  # Limit to 10 clauses for performance
            complexity_class = f"complexity-{clause['complexity'].lower()}"
            
            with st.container():
                st.markdown(f"""
                <div class="clause-card {complexity_class}">
                    <h4>Clause {clause['id']} - {clause['type']}</h4>
                    <p><strong>Complexity:</strong> {clause['complexity']} | <strong>Length:</strong> {clause['length']} words</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Original:** {clause['text']}")
                
                if show_simplified:
                    with st.spinner(f"Simplifying clause {clause['id']}..."):
                        simplified = analyzer.simplify_clause(clause['text'])
                        st.markdown(f"**Simplified:** {simplified}")
                
                st.markdown("---")
    
    # Named Entity Recognition
    st.subheader("🏷️ Named Entity Recognition")
    
    entities = results.get('entities', {})
    if entities:
        for entity_type, entity_list in entities.items():
            if entity_list:
                st.markdown(f"**{entity_type.replace('_', ' ').title()}:**")
                entity_html = " ".join([f'<span class="entity-tag">{entity}</span>' for entity in entity_list[:10]])
                st.markdown(entity_html, unsafe_allow_html=True)
                st.markdown("")

def clause_simplifier_page(analyzer):
    """Clause simplification page"""
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #1e293b; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            🔍 Clause Simplifier
        </h2>
        <p style="color: #64748b; margin: 0; font-size: 1rem;">
            Transform complex legal language into clear, understandable text that anyone can comprehend.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input
    clause_text = st.text_area(
        "Enter legal clause:",
        height=200,
        placeholder="Paste your legal clause here..."
    )
    
    if st.button("Simplify Clause", type="primary"):
        if clause_text.strip():
            with st.spinner("🔄 Simplifying clause..."):
                try:
                    simplified = analyzer.simplify_clause(clause_text)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📄 Original Clause")
                        st.markdown(clause_text)
                    
                    with col2:
                        st.subheader("✨ Simplified Version")
                        st.markdown(simplified)
                        
                except Exception as e:
                    st.error(f"Simplification failed: {str(e)}")
        else:
            st.warning("Please enter a clause to simplify")

def entity_extractor_page(analyzer):
    """Entity extraction page"""
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #1e293b; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            🏷️ Entity Extractor
        </h2>
        <p style="color: #64748b; margin: 0; font-size: 1rem;">
            Automatically identify and extract key legal entities including parties, dates, obligations, and terms.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input
    text_input = st.text_area(
        "Enter text:",
        height=200,
        placeholder="Paste your legal text here..."
    )
    
    if st.button("Extract Entities", type="primary"):
        if text_input.strip():
            with st.spinner("🔄 Extracting entities..."):
                try:
                    entities = analyzer.extract_entities_from_text(text_input)
                    
                    if entities:
                        st.subheader("🏷️ Extracted Entities")
                        
                        for entity_type, entity_list in entities.items():
                            if entity_list:
                                st.markdown(f"**{entity_type.replace('_', ' ').title()}:**")
                                entity_html = " ".join([f'<span class="entity-tag">{entity}</span>' for entity in entity_list])
                                st.markdown(entity_html, unsafe_allow_html=True)
                                st.markdown("")
                    else:
                        st.info("No entities found in the text")
                        
                except Exception as e:
                    st.error(f"Entity extraction failed: {str(e)}")
        else:
            st.warning("Please enter text to analyze")

def analytics_page():
    """Analytics and insights page"""
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #1e293b; font-weight: 600; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            📊 Analytics Dashboard
        </h2>
        <p style="color: #64748b; margin: 0; font-size: 1rem;">
            Comprehensive insights and visualizations from your document analysis results.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'analysis_results' not in st.session_state:
        st.markdown("""
        <div class="premium-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
            <h3 style="color: #64748b; font-weight: 500; margin-bottom: 1rem;">No Analysis Data Available</h3>
            <p style="color: #94a3b8; margin: 0;">Please analyze a document first to view comprehensive analytics and insights.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    results = st.session_state['analysis_results']
    
    # Key metrics
    st.subheader("📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Document Type", results.get('classification', 'Unknown'))
    
    with col2:
        clause_stats = results.get('clause_statistics', {})
        st.metric("Total Clauses", clause_stats.get('total_clauses', 0))
    
    with col3:
        complexity_dist = clause_stats.get('complexity_distribution', {})
        high_complexity = complexity_dist.get('High', 0)
        st.metric("High Complexity Clauses", high_complexity)
    
    with col4:
        st.metric("Total Obligations", len(results.get('obligations', [])))
    
    # Detailed analytics
    st.subheader("📊 Detailed Analysis")
    
    # Create tabs for different analytics
    tab1, tab2, tab3 = st.tabs(["Clause Analysis", "Entity Distribution", "Document Insights"])
    
    with tab1:
        clauses = results.get('clauses', [])
        if clauses:
            # Clause length distribution
            clause_lengths = [clause['length'] for clause in clauses]
            fig_lengths = px.histogram(
                x=clause_lengths,
                nbins=20,
                title="Clause Length Distribution",
                labels={'x': 'Word Count', 'y': 'Number of Clauses'}
            )
            st.plotly_chart(fig_lengths, use_container_width=True)
            
            # Clause complexity by type
            clause_df = pd.DataFrame(clauses)
            complexity_by_type = clause_df.groupby(['type', 'complexity']).size().reset_index(name='count')
            
            fig_complexity_type = px.bar(
                complexity_by_type,
                x='type',
                y='count',
                color='complexity',
                title="Clause Complexity by Type",
                color_discrete_map={'Low': '#388e3c', 'Medium': '#f57c00', 'High': '#d32f2f'}
            )
            st.plotly_chart(fig_complexity_type, use_container_width=True)
    
    with tab2:
        entities = results.get('entities', {})
        if entities:
            # Entity count by type
            entity_counts = {k: len(v) for k, v in entities.items() if v}
            
            if entity_counts:
                fig_entities = px.bar(
                    x=list(entity_counts.keys()),
                    y=list(entity_counts.values()),
                    title="Entity Distribution",
                    labels={'x': 'Entity Type', 'y': 'Count'}
                )
                st.plotly_chart(fig_entities, use_container_width=True)
    
    with tab3:
        # Document statistics
        st.markdown("### 📋 Document Statistics")
        
        doc_info = results.get('document_info', {})
        
        stats_data = {
            'Metric': ['File Size (MB)', 'Word Count', 'Character Count', 'Average Words per Clause'],
            'Value': [
                doc_info.get('size_mb', 0),
                results.get('word_count', 0),
                results.get('text_length', 0),
                clause_stats.get('average_words_per_clause', 0)
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)

if __name__ == "__main__":
    main()
