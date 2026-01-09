#!/bin/bash

echo "================================================"
echo "   Stock Recommendation Tool"
echo "================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo "   Please edit .env with your email credentials"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Stock Recommendation Tool..."
echo "   Access at: http://localhost:5000"
echo ""

# Start the application
python app.py
