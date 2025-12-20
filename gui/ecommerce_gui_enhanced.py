#!/usr/bin/env python3
"""
E-Commerce Database Management System - Enhanced GUI
Academic Project - Database Management Systems
Python tkinter-based GUI for DML Operations
Enhanced with Categories, Reviews, Coupons, and Shipments
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from datetime import datetime
import sys

class DatabaseConfig:
    """Database connection configuration"""
    HOST = 'localhost'
    USER = 'ecommerce_user'
    PASSWORD = 'SecurePass123!'
    DATABASE = 'ecommerce_db'

class ECommerceGUI:
    """Main GUI Application for E-Commerce Database"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("E-Commerce Database Management System - Enhanced")
        self.root.geometry("1400x850")
        self.root.configure(bg='#f0f0f0')
        
        # Database connection
        self.conn = None
        self.cursor = None
        self.connect_database()
        
        # Create main interface
        self.create_header()
        self.create_status_bar()
        self.create_tabs()
        
    def connect_database(self):
        """Connect to MySQL database"""
        try:
            self.conn = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                database=DatabaseConfig.DATABASE,
                charset='utf8mb4',
                use_unicode=True
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("✓ Database connected successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{err}")
            sys.exit(1)
    
    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="E-Commerce Database Management System - Enhanced",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=25)
        
    def create_tabs(self):
        """Create tabbed interface for different operations"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create all tabs
        self.tab_products = ttk.Frame(self.notebook)
        self.tab_categories = ttk.Frame(self.notebook)
        self.tab_customers = ttk.Frame(self.notebook)
        self.tab_orders = ttk.Frame(self.notebook)
        self.tab_reviews = ttk.Frame(self.notebook)
        self.tab_coupons = ttk.Frame(self.notebook)
        self.tab_inventory = ttk.Frame(self.notebook)
        self.tab_shipments = ttk.Frame(self.notebook)
        self.tab_query = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_products, text='Products (CRUD)')
        self.notebook.add(self.tab_categories, text='Categories (CRUD)')
        self.notebook.add(self.tab_customers, text='Customers (CRUD)')
        self.notebook.add(self.tab_orders, text='Orders (SELECT)')
        self.notebook.add(self.tab_reviews, text='Reviews (I/S)')
        self.notebook.add(self.tab_coupons, text='Coupons (CRUD)')
        self.notebook.add(self.tab_inventory, text='Inventory (UPDATE)')
        self.notebook.add(self.tab_shipments, text='Shipments (S/U)')
        self.notebook.add(self.tab_query, text='Custom Query')
        
        # Initialize each tab
        self.init_products_tab()
        self.init_categories_tab()
        self.init_customers_tab()
        self.init_orders_tab()
        self.init_reviews_tab()
        self.init_coupons_tab()
        self.init_inventory_tab()
        self.init_shipments_tab()
        self.init_query_tab()
    
    # Copy all existing init methods and add new ones...
    # (Due to length, I'll create this as a separate file)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Database:ecommerce_db | Enhanced GUI with 9 tabs",
            bd=1,
            relief='sunken',
            anchor='w',
            bg='#ecf0f1'
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def update_status(self, message):
        """Update status bar"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_bar.config(text=f"{timestamp} | {message}")
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.conn:
                self.conn.close()
            self.root.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ECommerceGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
