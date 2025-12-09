#!/bin/bash

echo "⚖️  Starting LegalEagle..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=gsk-" .env 2>/dev/null; then
    echo "⚠️  WARNING: GROQ_API_KEY not set in .env file"
    echo "   The app may not work without it."
    echo "   Edit .env and add: GROQ_API_KEY=gsk-your-key-here"
    echo "   Get your FREE key from: https://console.groq.com/"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🚀 Launching Streamlit app..."
echo ""
streamlit run app.py

