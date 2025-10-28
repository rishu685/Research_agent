#!/bin/bash

echo "🔒 AI Research Agent - Secure Setup"
echo "=================================="

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install Python 3 and pip."
    exit 1
fi

echo "📦 Installing required dependencies..."
pip3 install -r requirements.txt

echo ""
echo "🔑 API Key Setup"
echo "---------------"
echo "You need a Gemini API key to use this agent."
echo ""
echo "1. Get a free API key from: https://makersuite.google.com/app/apikey"
echo "2. Choose one setup method:"
echo ""
echo "   Method A - Environment Variable (Recommended):"
echo "   export GEMINI_API_KEY='your_api_key_here'"
echo ""
echo "   Method B - .env File:"
echo "   cp .env.example .env"
echo "   # Then edit .env and add your API key"
echo ""

read -p "Do you want to set up .env file now? (y/n): " setup_env

if [[ $setup_env =~ ^[Yy]$ ]]; then
    if [[ ! -f .env.example ]]; then
        echo "❌ .env.example not found"
        exit 1
    fi
    
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "📝 Please edit .env file and add your Gemini API key:"
    echo "   GEMINI_API_KEY=your_actual_api_key_here"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

echo ""
echo "🚀 Setup complete! You can now run:"
echo "   python3 interview_prep_agent.py    # Interactive mode"
echo "   python3 demo.py                    # Quick demo"
echo ""
echo "🔒 Security reminder: Never commit your API key to version control!"