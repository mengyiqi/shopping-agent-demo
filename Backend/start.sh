#!/bin/bash

# LangGraph Chatbot API Startup Script

echo "🚀 Starting LangGraph Chatbot API..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env_example.txt .env
    echo "📝 Please edit .env file with your Google API key and other settings."
    echo "   Then run this script again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Validate environment
echo "🔍 Validating environment..."
python -c "
from app.config import settings
try:
    settings.validate()
    print('✅ Environment validation passed')
except Exception as e:
    print(f'❌ Environment validation failed: {e}')
    exit(1)
"

# Start the application
echo "🌟 Starting the API server..."
python main.py 