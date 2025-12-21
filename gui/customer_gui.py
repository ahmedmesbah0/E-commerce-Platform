#!/usr/bin/env python3
"""
Customer GUI Module - Shopping Interface
Wrapper to integrate with authentication system
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.insert(0, '.')

# Import the CustomerGUI from ecommerce_app.py and adapt it
from ecommerce_app import CustomerGUI as BaseCustomerGUI

class CustomerGUI:
    """Wrapper for CustomerGUI to match authentication parameters"""
    
    def __init__(self, root, user_id, user_name, user_email, conn):
        """Initialize with authentication parameters"""
        # The base CustomerGUI only takes (root, customer_id)
        # So we just pass what it needs
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        
        # Create the base customer GUI
        self.app = BaseCustomerGUI(root, user_id)
        
        # Override connection to reuse the existing one
        self.app.conn = conn
        self.app.cursor = conn.cursor(dictionary=True)
        
        # Update customer info
        self.app.customer_name = user_name
        self.app.customer_email = user_email
        
        # Update window title
        root.title(f"E-Commerce - {user_name}")
    
    def on_closing(self):
        """Handle closing"""
        self.app.on_closing()
