#!/bin/bash
# Quick setup script for E-commerce Platform
# Run with: source setup_venv.sh

echo "🚀 E-Commerce Platform - Quick Setup Script"
echo "============================================"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip -q

# Install model dependencies
echo "📚 Installing model dependencies..."
pip install -r models/requirements.txt -q

# Install GUI dependencies
echo "🖥️  Installing GUI dependencies..."
pip install -r gui/requirements.txt -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Available commands:"
echo "  - Run Admin GUI:     cd gui && python3 ecommerce_gui.py"
echo "  - Run Dual App:      cd gui && python3 main_app.py"
echo "  - Test Models:       python3 models/verify.py"
echo "  - Run Examples:      python3 models/examples.py"
echo ""
echo "💡 Virtual environment is activated!"
echo "   Deactivate with: deactivate"
echo ""
