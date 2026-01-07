#!/bin/bash

# Documentation Download Agent - Startup Script

echo "🚀 Documentation Download Agent"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python3 -c "import aiohttp, beautifulsoup4, fastapi, uvicorn" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "📥 Installing dependencies..."
    pip3 install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please check your Python environment."
        exit 1
    fi
    
    echo "✅ Dependencies installed successfully"
else
    echo "✅ All dependencies are already installed"
fi

# Create necessary directories
echo "📁 Setting up directories..."
mkdir -p static css js templates downloads/archives

# Start the application
echo ""
echo "🚀 Starting Documentation Download Agent..."
echo "🌐 Open your browser and navigate to: http://localhost:8001"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python3 main.py