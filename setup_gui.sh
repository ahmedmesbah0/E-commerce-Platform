#!/bin/bash

# E-Commerce GUI Setup Script
# Installs dependencies and sets up the Python GUI

echo "========================================="
echo "E-Commerce GUI Setup"
echo "========================================="
echo ""

# Install mysql-connector-python
echo "Installing Python MySQL connector..."
pip3 install mysql-connector-python --break-system-packages

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To run the GUI:"
echo "  cd gui"
echo "  python3 ecommerce_gui.py"
echo ""
echo "Make sure your database is set up first:"
echo "  mysql -u root -p < database/schema_phpmyadmin.sql"
echo ""
