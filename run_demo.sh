#!/bin/bash

echo "🚀 Starting AI Chatbot Enterprise Demo..."
echo "========================================="
echo ""
echo "📋 Checking dependencies..."

# Check if required packages are installed
python3.11 -c "import streamlit, tensorflow, plotly, pandas" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ All dependencies are installed"
else
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

echo ""
echo "🤖 Checking TensorFlow model..."
if [ -f "tf_model.h5" ]; then
    echo "✅ Model file found: tf_model.h5"
else
    echo "⚠️  Model file not found. Using demo model."
fi

echo ""
echo "🌟 Launching Enterprise Demo Application..."
echo "📱 Access the demo at: http://localhost:8501"
echo ""
echo "🎯 Demo Features:"
echo "   • Real-time AI chat interface"
echo "   • Live performance analytics"
echo "   • Professional dashboard"
echo "   • Model integration showcase"
echo ""
echo "💡 Pro tip: Use the sidebar controls to customize the experience!"
echo ""
echo "🛑 Press Ctrl+C to stop the demo"
echo "========================================="

# Run the demo application
streamlit run demo_app.py --server.port 8501

