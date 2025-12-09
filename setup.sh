#!/bin/bash

echo "⚖️  LegalEagle Setup Script"
echo "============================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🔑 Checking for .env file..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f "env_template.txt" ]; then
        cp env_template.txt .env
        echo "✅ .env file created from template"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env and add your GROQ_API_KEY"
        echo "   You can get a FREE API key from: https://console.groq.com/"
    else
        echo "❌ env_template.txt not found. Creating basic .env file..."
        echo "GROQ_API_KEY=your_groq_api_key_here" > .env
        echo "VECTOR_STORE_TYPE=faiss" >> .env
        echo "LLM_MODEL=llama-3.3-70b-versatile" >> .env
        echo "EMBEDDING_MODEL=all-MiniLM-L6-v2" >> .env
        echo "✅ Basic .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env and add your GROQ_API_KEY"
        echo "   Get your FREE key from: https://console.groq.com/"
    fi
else
    echo "✅ .env file exists"
fi

echo ""
echo "============================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your GROQ_API_KEY (free from https://console.groq.com/)"
echo "2. Run: source venv/bin/activate"
echo "3. Run: streamlit run app.py"
echo ""
echo "Or use: ./run.sh"

