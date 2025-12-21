#!/usr/bin/env python3
# Admin GUI Module - imports from ecommerce_gui.py
import sys, tkinter as tk
sys.path.insert(0, '.')

# Wrapper for ECommerceGUI to match admin interface
class AdminGUI:
    def __init__(self, root, admin_id, admin_name, admin_email, conn):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.admin_email = admin_email
        
        # Import and use existing GUI
        from ecommerce_gui import ECommerceGUI
        self.app = ECommerceGUI(root)
        self.app.conn = conn
        self.app.cursor = conn.cursor(dictionary=True)
        
        # Update title
        root.title(f"E-Commerce Admin - {admin_name}")
        
    def on_closing(self):
        self.app.on_closing()
