"""
Setup script for ClauseWise installation and initialization
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def download_spacy_model():
    """Download spaCy English model"""
    print("🔽 Downloading spaCy English model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading spaCy model: {e}")
        return False
    return True

def create_sample_data():
    """Create sample data directory"""
    sample_dir = "sample_documents"
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
        print(f"📁 Created {sample_dir} directory")
    
    # Create a sample legal clause file
    sample_clause = """
CONFIDENTIALITY CLAUSE

The Receiving Party acknowledges that the Confidential Information is proprietary to the Disclosing Party, has been developed and obtained through great efforts by the Disclosing Party, and that the Disclosing Party regards the same as trade secrets. The Receiving Party agrees to hold and maintain the Confidential Information in strict confidence for the sole and exclusive benefit of the Disclosing Party. The Receiving Party further agrees not to, without the prior written approval of the Disclosing Party, publish, copy, or otherwise disclose to others, or use for any purpose other than the evaluation of potential business relationships between the parties, any Confidential Information. The Receiving Party shall take the same security precautions to protect the Confidential Information that the Receiving Party takes with its own similar confidential information, but in no event less than reasonable care.
"""
    
    sample_file_path = os.path.join(sample_dir, "sample_nda_clause.txt")
    with open(sample_file_path, "w", encoding="utf-8") as f:
        f.write(sample_clause)
    
    print(f"📄 Created sample document: {sample_file_path}")

def main():
    """Main setup function"""
    print("🚀 Setting up ClauseWise...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during requirements installation")
        return
    
    # Download spaCy model
    if not download_spacy_model():
        print("❌ Setup failed during spaCy model download")
        return
    
    # Create sample data
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 ClauseWise setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run: streamlit run app.py")
    print("2. Open your browser to http://localhost:8501")
    print("3. Upload a legal document or try the sample clause")
    print("\n⚖️ Happy analyzing!")

if __name__ == "__main__":
    main()
