#!/usr/bin/env python3
"""
E-Commerce Database Management System - GUI Application
Academic Project - Database Management Systems
Python tkinter-based GUI for DML Operations
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
        self.root.title("E-Commerce Database Management System")
        self.root.geometry("1400x850")
        self.root.configure(bg='#f0f0f0')
        
        # Database connection
        self.conn = None
        self.cursor = None
        self.connect_database()
        
        # Create main interface
        self.create_header()
        self.create_status_bar()  # Create status bar BEFORE tabs
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
            text="E-Commerce Database Management System",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=25)
        
    def create_tabs(self):
        """Create tabbed interface for different operations"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
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
    
    def init_products_tab(self):
        """Initialize Products tab with CRUD operations"""
        # Left panel for form
        left_panel = tk.Frame(self.tab_products, bg='white', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', padx=10, pady=10)
        
        tk.Label(left_panel, text="Product Management", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Form fields
        tk.Label(left_panel, text="Product ID:", bg='white').pack(anchor='w', padx=20)
        self.product_id_entry = tk.Entry(left_panel, width=30)
        self.product_id_entry.pack(padx=20, pady=5)
        
        tk.Label(left_panel, text="Product Name:", bg='white').pack(anchor='w', padx=20)
        self.product_name_entry = tk.Entry(left_panel, width=30)
        self.product_name_entry.pack(padx=20, pady=5)
        
        tk.Label(left_panel, text="Description:", bg='white').pack(anchor='w', padx=20)
        self.product_desc_entry = tk.Entry(left_panel, width=30)
        self.product_desc_entry.pack(padx=20, pady=5)
        
        tk.Label(left_panel, text="Price:", bg='white').pack(anchor='w', padx=20)
        self.product_price_entry = tk.Entry(left_panel, width=30)
        self.product_price_entry.pack(padx=20, pady=5)
        
        tk.Label(left_panel, text="Category ID:", bg='white').pack(anchor='w', padx=20)
        self.product_category_entry = tk.Entry(left_panel, width=30)
        self.product_category_entry.pack(padx=20, pady=5)
        
        # Buttons
        button_frame = tk.Frame(left_panel, bg='white')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="INSERT", command=self.insert_product, 
                 bg='#27ae60', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="UPDATE", command=self.update_product, 
                 bg='#3498db', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="DELETE", command=self.delete_product, 
                 bg='#e74c3c', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="CLEAR", command=self.clear_product_form, 
                 bg='#95a5a6', fg='white', width=10).pack(side='left', padx=5)
        
        # Right panel for data display
        right_panel = tk.Frame(self.tab_products, bg='white', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(right_panel, text="Products List (SELECT)", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        tk.Button(right_panel, text="Refresh List", command=self.load_products, 
                 bg='#16a085', fg='white').pack(pady=5)
        
        # Treeview for products
        self.products_tree = ttk.Treeview(right_panel, columns=('ID', 'Name', 'Price', 'Category'), show='headings')
        self.products_tree.heading('ID', text='ID')
        self.products_tree.heading('Name', text='Name')
        self.products_tree.heading('Price', text='Price')
        self.products_tree.heading('Category', text='Category ID')
        
        self.products_tree.column('ID', width=50)
        self.products_tree.column('Name', width=200)
        self.products_tree.column('Price', width=100)
        self.products_tree.column('Category', width=100)
        
        self.products_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.products_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Load initial data
        self.load_products()
    
    def init_customers_tab(self):
        """Initialize Customers tab with CRUD operations"""
        # Left panel for form
        left_panel = tk.Frame(self.tab_customers, bg='white', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', padx=10, pady=10)
        
        tk.Label(left_panel, text="Customer Management", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Form fields
        tk.Label(left_panel, text="Customer ID:", bg='white').pack(anchor='w', padx=20)
        self.customer_id_entry = tk.Entry(left_panel, width=30)
        self.customer_id_entry.pack(padx=20, pady=5)
        
        tk.Label(left_panel, text="Name:", bg='white').pack(anchor='w', padx=20)
        self.customer_name_entry = tk.Entry(left_panel, width=30)
        self.customer_name_entry.pack(padx=20, pady=5)
        
        tk.Label(left_panel, text="Email:", bg='white').pack(anchor='w', padx=20)
        self.customer_email_entry = tk.Entry(left_panel, width=30)
        self.customer_email_entry.pack(padx=20, pady=5)
        
        tk.Label(left_panel, text="Phone:", bg='white').pack(anchor='w', padx=20)
        self.customer_phone_entry = tk.Entry(left_panel, width=30)
        self.customer_phone_entry.pack(padx=20, pady=5)
        
        tk.Label(left_panel, text="Address:", bg='white').pack(anchor='w', padx=20)
        self.customer_address_entry = tk.Entry(left_panel, width=30)
        self.customer_address_entry.pack(padx=20, pady=5)
        
        # Buttons
        button_frame = tk.Frame(left_panel, bg='white')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="INSERT", command=self.insert_customer, 
                 bg='#27ae60', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="UPDATE", command=self.update_customer, 
                 bg='#3498db', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="DELETE", command=self.delete_customer, 
                 bg='#e74c3c', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="CLEAR", command=self.clear_customer_form, 
                 bg='#95a5a6', fg='white', width=10).pack(side='left', padx=5)
        
        # Right panel for data display
        right_panel = tk.Frame(self.tab_customers, bg='white', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(right_panel, text="Customers List (SELECT)", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        tk.Button(right_panel, text="Refresh List", command=self.load_customers, 
                 bg='#16a085', fg='white').pack(pady=5)
        
        # Treeview for customers
        self.customers_tree = ttk.Treeview(right_panel, columns=('ID', 'Name', 'Email', 'Phone'), show='headings')
        self.customers_tree.heading('ID', text='ID')
        self.customers_tree.heading('Name', text='Name')
        self.customers_tree.heading('Email', text='Email')
        self.customers_tree.heading('Phone', text='Phone')
        
        self.customers_tree.column('ID', width=50)
        self.customers_tree.column('Name', width=150)
        self.customers_tree.column('Email', width=200)
        self.customers_tree.column('Phone', width=120)
        
        self.customers_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.customers_tree.bind('<<TreeviewSelect>>', self.on_customer_select)
        
        # Load initial data
        self.load_customers()
    
    def init_orders_tab(self):
        """Initialize Orders tab (SELECT only)"""
        frame = tk.Frame(self.tab_orders, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="Orders View (SELECT Operation)", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        tk.Button(frame, text="Refresh Orders", command=self.load_orders, 
                 bg='#16a085', fg='white').pack(pady=5)
        
        # Treeview for orders
        self.orders_tree = ttk.Treeview(frame, columns=('Order ID', 'Customer', 'Date', 'Total', 'Status'), show='headings')
        self.orders_tree.heading('Order ID', text='Order ID')
        self.orders_tree.heading('Customer', text='Customer Name')
        self.orders_tree.heading('Date', text='Order Date')
        self.orders_tree.heading('Total', text='Total Amount')
        self.orders_tree.heading('Status', text='Status')
        
        self.orders_tree.column('Order ID', width=80)
        self.orders_tree.column('Customer', width=200)
        self.orders_tree.column('Date', width=150)
        self.orders_tree.column('Total', width=120)
        self.orders_tree.column('Status', width=120)
        
        self.orders_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load initial data
        self.load_orders()
    
    def init_inventory_tab(self):
        """Initialize Inventory tab (UPDATE operations)"""
        frame = tk.Frame(self.tab_inventory, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="Inventory Management (UPDATE Operation)", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Update form
        form_frame = tk.Frame(frame, bg='white')
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Inventory ID:", bg='white').grid(row=0, column=0, padx=5, pady=5)
        self.inv_id_entry = tk.Entry(form_frame, width=20)
        self.inv_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="New Quantity:", bg='white').grid(row=1, column=0, padx=5, pady=5)
        self.inv_quantity_entry = tk.Entry(form_frame, width=20)
        self.inv_quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(form_frame, text="UPDATE Quantity", command=self.update_inventory, 
                 bg='#3498db', fg='white', width=15).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(form_frame, text="Refresh List", command=self.load_inventory, 
                 bg='#16a085', fg='white', width=15).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Treeview for inventory
        self.inventory_tree = ttk.Treeview(frame, columns=('ID', 'Product', 'Warehouse', 'Quantity', 'Reorder'), show='headings')
        self.inventory_tree.heading('ID', text='Inv ID')
        self.inventory_tree.heading('Product', text='Product ID')
        self.inventory_tree.heading('Warehouse', text='Warehouse ID')
        self.inventory_tree.heading('Quantity', text='Quantity')
        self.inventory_tree.heading('Reorder', text='Reorder Level')
        
        self.inventory_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.inventory_tree.bind('<<TreeviewSelect>>', self.on_inventory_select)
        
        # Load initial data
        self.load_inventory()
    
    def init_query_tab(self):
        """Initialize Custom Query tab"""
        frame = tk.Frame(self.tab_query, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="Custom SQL Query Executor", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        tk.Label(frame, text="Enter SQL Query:", bg='white').pack(anchor='w', padx=10)
        
        self.query_text = scrolledtext.ScrolledText(frame, height=6, width=80)
        self.query_text.pack(padx=10, pady=5)
        
        tk.Button(frame, text="Execute Query", command=self.execute_custom_query, 
                 bg='#9b59b6', fg='white', width=15).pack(pady=5)
        
        tk.Label(frame, text="Query Results:", bg='white').pack(anchor='w', padx=10, pady=(10,0))
        
        self.query_result_text = scrolledtext.ScrolledText(frame, height=20, width=80)
        self.query_result_text.pack(padx=10, pady=5, fill='both', expand=True)
    
    # ==================== DML OPERATIONS ====================
    
    def insert_product(self):
        """INSERT operation for products"""
        try:
            name = self.product_name_entry.get()
            desc = self.product_desc_entry.get()
            price = float(self.product_price_entry.get())
            category_id = int(self.product_category_entry.get()) if self.product_category_entry.get() else None
            
            if not name or not price:
                messagebox.showwarning("Validation Error", "Name and Price are required!")
                return
            
            query = """
                INSERT INTO product (name, description, price, category_id, is_active)
                VALUES (%s, %s, %s, %s, TRUE)
            """
            self.cursor.execute(query, (name, desc, price, category_id))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Product inserted successfully!")
            self.update_status(f"INSERT: Added product '{name}'")
            self.clear_product_form()
            self.load_products()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert product:\n{e}")
            self.conn.rollback()
    
    def update_product(self):
        """UPDATE operation for products"""
        try:
            product_id = int(self.product_id_entry.get())
            name = self.product_name_entry.get()
            desc = self.product_desc_entry.get()
            price = float(self.product_price_entry.get())
            category_id = int(self.product_category_entry.get()) if self.product_category_entry.get() else None
            
            query = """
                UPDATE product 
                SET name = %s, description = %s, price = %s, category_id = %s
                WHERE product_id = %s
            """
            self.cursor.execute(query, (name, desc, price, category_id, product_id))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", "Product updated successfully!")
                self.update_status(f"UPDATE: Modified product ID {product_id}")
                self.clear_product_form()
                self.load_products()
            else:
                messagebox.showwarning("Warning", "No product found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product:\n{e}")
            self.conn.rollback()
    
    def delete_product(self):
        """DELETE operation for products"""
        try:
            product_id = int(self.product_id_entry.get())
            
            if messagebox.askyesno("Confirm Delete", f"Delete product ID {product_id}?"):
                query = "DELETE FROM product WHERE product_id = %s"
                self.cursor.execute(query, (product_id,))
                self.conn.commit()
                
                if self.cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    self.update_status(f"DELETE: Removed product ID {product_id}")
                    self.clear_product_form()
                    self.load_products()
                else:
                    messagebox.showwarning("Warning", "No product found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product:\n{e}")
            self.conn.rollback()
    
    def insert_customer(self):
        """INSERT operation for customers"""
        try:
            name = self.customer_name_entry.get()
            email = self.customer_email_entry.get()
            phone = self.customer_phone_entry.get()
            address = self.customer_address_entry.get()
            
            if not name or not email:
                messagebox.showwarning("Validation Error", "Name and Email are required!")
                return
            
            # Generate a random password hash for demo
            password_hash = "$2y$10$demo hash for academic project"
            
            query = """
                INSERT INTO customer (name, email, phone, address, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email, phone, address, password_hash))
            self.conn.commit()
            
            messagebox.showinfo("Success", "Customer inserted successfully!")
            self.update_status(f"INSERT: Added customer '{name}'")
            self.clear_customer_form()
            self.load_customers()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert customer:\n{e}")
            self.conn.rollback()
    
    def update_customer(self):
        """UPDATE operation for customers"""
        try:
            customer_id = int(self.customer_id_entry.get())
            name = self.customer_name_entry.get()
            email = self.customer_email_entry.get()
            phone = self.customer_phone_entry.get()
            address = self.customer_address_entry.get()
            
            query = """
                UPDATE customer 
                SET name = %s, email = %s, phone = %s, address = %s
                WHERE customer_id = %s
            """
            self.cursor.execute(query, (name, email, phone, address, customer_id))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", "Customer updated successfully!")
                self.update_status(f"UPDATE: Modified customer ID {customer_id}")
                self.clear_customer_form()
                self.load_customers()
            else:
                messagebox.showwarning("Warning", "No customer found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update customer:\n{e}")
            self.conn.rollback()
    
    def delete_customer(self):
        """DELETE operation for customers"""
        try:
            customer_id = int(self.customer_id_entry.get())
            
            if messagebox.askyesno("Confirm Delete", f"Delete customer ID {customer_id}?"):
                query = "DELETE FROM customer WHERE customer_id = %s"
                self.cursor.execute(query, (customer_id,))
                self.conn.commit()
                
                if self.cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Customer deleted successfully!")
                    self.update_status(f"DELETE: Removed customer ID {customer_id}")
                    self.clear_customer_form()
                    self.load_customers()
                else:
                    messagebox.showwarning("Warning", "No customer found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete customer:\n{e}")
            self.conn.rollback()
    
    def update_inventory(self):
        """UPDATE operation for inventory"""
        try:
            inv_id = int(self.inv_id_entry.get())
            quantity = int(self.inv_quantity_entry.get())
            
            query = "UPDATE inventory SET quantity = %s WHERE inventory_id = %s"
            self.cursor.execute(query, (quantity, inv_id))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", "Inventory updated successfully!")
                self.update_status(f"UPDATE: Modified inventory ID {inv_id}, new quantity: {quantity}")
                self.load_inventory()
            else:
                messagebox.showwarning("Warning", "No inventory record found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update inventory:\n{e}")
            self.conn.rollback()
    
    # ==================== SELECT OPERATIONS ====================
    
    def load_products(self):
        """SELECT operation to load products"""
        try:
            self.products_tree.delete(*self.products_tree.get_children())
            query = "SELECT product_id, name, price, category_id FROM product ORDER BY product_id DESC LIMIT 100"
            self.cursor.execute(query)
            
            for row in self.cursor.fetchall():
                self.products_tree.insert('', 'end', values=(
                    row['product_id'],
                    row['name'],
                    f"${row['price']:.2f}",
                    row['category_id'] or 'N/A'
                ))
            self.update_status("SELECT: Loaded products")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products:\n{e}")
    
    def load_customers(self):
        """SELECT operation to load customers"""
        try:
            self.customers_tree.delete(*self.customers_tree.get_children())
            query = "SELECT customer_id, name, email, phone FROM customer ORDER BY customer_id DESC LIMIT 100"
            self.cursor.execute(query)
            
            for row in self.cursor.fetchall():
                self.customers_tree.insert('', 'end', values=(
                    row['customer_id'],
                    row['name'],
                    row['email'],
                    row['phone'] or 'N/A'
                ))
            self.update_status("SELECT: Loaded customers")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load customers:\n{e}")
    
    def load_orders(self):
        """SELECT operation to load orders with JOIN"""
        try:
            self.orders_tree.delete(*self.orders_tree.get_children())
            query = """
                SELECT o.order_id, c.name, o.order_date, o.total_amount, o.status
                FROM `order` o
                INNER JOIN customer c ON o.customer_id = c.customer_id
                ORDER BY o.order_date DESC
                LIMIT 100
            """
            self.cursor.execute(query)
            
            for row in self.cursor.fetchall():
                self.orders_tree.insert('', 'end', values=(
                    row['order_id'],
                    row['name'],
                    row['order_date'],
                    f"${row['total_amount']:.2f}",
                    row['status']
                ))
            self.update_status("SELECT: Loaded orders with JOIN")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders:\n{e}")
    
    def load_inventory(self):
        """SELECT operation to load inventory"""
        try:
            self.inventory_tree.delete(*self.inventory_tree.get_children())
            query = "SELECT inventory_id, product_id, warehouse_id, quantity, reorder_level FROM inventory LIMIT 100"
            self.cursor.execute(query)
            
            for row in self.cursor.fetchall():
                self.inventory_tree.insert('', 'end', values=(
                    row['inventory_id'],
                    row['product_id'],
                    row['warehouse_id'],
                    row['quantity'],
                    row['reorder_level']
                ))
            self.update_status("SELECT: Loaded inventory")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load inventory:\n{e}")
    
    def execute_custom_query(self):
        """Execute custom SQL query"""
        try:
            query = self.query_text.get('1.0', 'end-1c')
            if not query.strip():
                messagebox.showwarning("Warning", "Please enter a query")
                return
            
            self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = self.cursor.fetchall()
                self.query_result_text.delete('1.0', tk.END)
                self.query_result_text.insert('1.0', f"Query returned {len(results)} rows:\n\n")
                
                for row in results:
                    self.query_result_text.insert(tk.END, f"{row}\n")
            else:
                self.conn.commit()
                self.query_result_text.delete('1.0', tk.END)
                self.query_result_text.insert('1.0', f"Query executed successfully!\nRows affected: {self.cursor.rowcount}")
            
            self.update_status(f"Custom query executed")
        except Exception as e:
            self.query_result_text.delete('1.0', tk.END)
            self.query_result_text.insert('1.0', f"Error:\n{e}")
            self.conn.rollback()
    
    # ==================== EVENT HANDLERS ====================
    
    def on_product_select(self, event):
        """Handle product selection"""
        selection = self.products_tree.selection()
        if selection:
            item = self.products_tree.item(selection[0])
            values = item['values']
            
            self.product_id_entry.delete(0, tk.END)
            self.product_id_entry.insert(0, values[0])
            
            self.product_name_entry.delete(0, tk.END)
            self.product_name_entry.insert(0, values[1])
            
            self.product_price_entry.delete(0, tk.END)
            self.product_price_entry.insert(0, values[2].replace('$', ''))
            
            if values[3] != 'N/A':
                self.product_category_entry.delete(0, tk.END)
                self.product_category_entry.insert(0, values[3])
    
    def on_customer_select(self, event):
        """Handle customer selection"""
        selection = self.customers_tree.selection()
        if selection:
            item = self.customers_tree.item(selection[0])
            values = item['values']
            
            self.customer_id_entry.delete(0, tk.END)
            self.customer_id_entry.insert(0, values[0])
            
            self.customer_name_entry.delete(0, tk.END)
            self.customer_name_entry.insert(0, values[1])
            
            self.customer_email_entry.delete(0, tk.END)
            self.customer_email_entry.insert(0, values[2])
            
            if values[3] != 'N/A':
                self.customer_phone_entry.delete(0, tk.END)
                self.customer_phone_entry.insert(0, values[3])
    
    def on_inventory_select(self, event):
        """Handle inventory selection"""
        selection = self.inventory_tree.selection()
        if selection:
            item = self.inventory_tree.item(selection[0])
            values = item['values']
            
            self.inv_id_entry.delete(0, tk.END)
            self.inv_id_entry.insert(0, values[0])
            
            self.inv_quantity_entry.delete(0, tk.END)
            self.inv_quantity_entry.insert(0, values[3])
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def clear_product_form(self):
        """Clear product form"""
        self.product_id_entry.delete(0, tk.END)
        self.product_name_entry.delete(0, tk.END)
        self.product_desc_entry.delete(0, tk.END)
        self.product_price_entry.delete(0, tk.END)
        self.product_category_entry.delete(0, tk.END)
    
    def clear_customer_form(self):
        """Clear customer form"""
        self.customer_id_entry.delete(0, tk.END)
        self.customer_name_entry.delete(0, tk.END)
        self.customer_email_entry.delete(0, tk.END)
        self.customer_phone_entry.delete(0, tk.END)
        self.customer_address_entry.delete(0, tk.END)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready | Database: ecommerce_db | User: ecommerce_user",
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
    
    # ==================== NEW TABS IMPLEMENTATIONS ====================
    def init_reviews_tab(self):
        """Initialize Reviews tab - STUB"""
        tk.Label(self.tab_reviews, text="Reviews Tab - Coming Soon", 
                font=('Arial', 16)).pack(expand=True)
    
    def init_coupons_tab(self):
        """Initialize Coupons tab - STUB"""
        tk.Label(self.tab_coupons, text="Coupons Tab - Coming Soon", 
                font=('Arial', 16)).pack(expand=True)
    
    def init_shipments_tab(self):
        """Initialize Shipments tab - STUB"""
        tk.Label(self.tab_shipments, text="Shipments Tab - Coming Soon", 
                font=('Arial', 16)).pack(expand=True)



    def init_categories_tab(self):
        """Initialize Categories tab with CRUD operations"""
        # Left panel for form
        left_panel = tk.Frame(self.tab_categories, bg='white', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', padx=10, pady=10)
    
        tk.Label(left_panel, text="Category Management", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
    
        # Form fields
        tk.Label(left_panel, text="Category ID:", bg='white').pack(anchor='w', padx=20)
        self.cat_id_entry = tk.Entry(left_panel, width=30)
        self.cat_id_entry.pack(padx=20, pady=5)
    
        tk.Label(left_panel, text="Category Name:", bg='white').pack(anchor='w', padx=20)
        self.cat_name_entry = tk.Entry(left_panel, width=30)
        self.cat_name_entry.pack(padx=20, pady=5)
    
        tk.Label(left_panel, text="Description:", bg='white').pack(anchor='w', padx=20)
        self.cat_desc_entry = tk.Entry(left_panel, width=30)
        self.cat_desc_entry.pack(padx=20, pady=5)
    
        # Buttons
        button_frame = tk.Frame(left_panel, bg='white')
        button_frame.pack(pady=20)
    
        tk.Button(button_frame, text="INSERT", command=self.insert_category, 
                 bg='#27ae60', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="UPDATE", command=self.update_category, 
                 bg='#3498db', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="DELETE", command=self.delete_category, 
                 bg='#e74c3c', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="CLEAR", command=self.clear_category_form, 
                 bg='#95a5a6', fg='white', width=10).pack(side='left', padx=5)
    
        # Right panel for data display
        right_panel = tk.Frame(self.tab_categories, bg='white', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
    
        tk.Label(right_panel, text="Categories List (SELECT)", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
    
        tk.Button(right_panel, text="Refresh List", command=self.load_categories, 
                 bg='#16a085', fg='white').pack(pady=5)
    
        # Treeview for categories
        self.categories_tree = ttk.Treeview(right_panel, columns=('ID', 'Name', 'Description'), show='headings')
        self.categories_tree.heading('ID', text='ID')
        self.categories_tree.heading('Name', text='Name')
        self.categories_tree.heading('Description', text='Description')
    
        self.categories_tree.column('ID', width=50)
        self.categories_tree.column('Name', width=200)
        self.categories_tree.column('Description', width=300)
    
        self.categories_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.categories_tree.bind('<<TreeviewSelect>>', self.on_category_select)
    
        # Load initial data
        self.load_categories()

    def init_reviews_tab(self):
        """Initialize Reviews tab (INSERT and SELECT)"""
        # Top panel for form
        top_panel = tk.Frame(self.tab_reviews, bg='white', relief='raised', bd=2)
        top_panel.pack(side='top', fill='x', padx=10, pady=10)
    
        tk.Label(top_panel, text="Add Product Review (INSERT)", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
    
        form_frame = tk.Frame(top_panel, bg='white')
        form_frame.pack(pady=10)
    
        tk.Label(form_frame, text="Product ID:", bg='white').grid(row=0, column=0, padx=5, pady=5)
        self.review_product_entry = tk.Entry(form_frame, width=20)
        self.review_product_entry.grid(row=0, column=1, padx=5, pady=5)
    
        tk.Label(form_frame, text="Customer ID:", bg='white').grid(row=0, column=2, padx=5, pady=5)
        self.review_customer_entry = tk.Entry(form_frame, width=20)
        self.review_customer_entry.grid(row=0, column=3, padx=5, pady=5)
    
        tk.Label(form_frame, text="Rating (1-5):", bg='white').grid(row=1, column=0, padx=5, pady=5)
        self.review_rating_entry = tk.Entry(form_frame, width=20)
        self.review_rating_entry.grid(row=1, column=1, padx=5, pady=5)
    
        tk.Label(form_frame, text="Title:", bg='white').grid(row=1, column=2, padx=5, pady=5)
        self.review_title_entry = tk.Entry(form_frame, width=20)
        self.review_title_entry.grid(row=1, column=3, padx=5, pady=5)
    
        tk.Label(form_frame, text="Comment:", bg='white').grid(row=2, column=0, padx=5, pady=5)
        self.review_comment_entry = tk.Entry(form_frame, width=65)
        self.review_comment_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
    
        tk.Button(form_frame, text="INSERT Review", command=self.insert_review, 
                 bg='#27ae60', fg='white', width=15).grid(row=3, column=0, columnspan=4, pady=10)
    
        # Bottom panel for data display
        bottom_panel = tk.Frame(self.tab_reviews, bg='white', relief='raised', bd=2)
        bottom_panel.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)
    
        tk.Label(bottom_panel, text="Reviews List (SELECT)", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
    
        tk.Button(bottom_panel, text="Refresh List", command=self.load_reviews, 
                 bg='#16a085', fg='white').pack(pady=5)
    
        # Treeview for reviews
        self.reviews_tree = ttk.Treeview(bottom_panel, columns=('ID', 'Product', 'Customer', 'Rating', 'Title'), show='headings')
        self.reviews_tree.heading('ID', text='Review ID')
        self.reviews_tree.heading('Product', text='Product ID')
        self.reviews_tree.heading('Customer', text='Customer ID')
        self.reviews_tree.heading('Rating', text='Rating')
        self.reviews_tree.heading('Title', text='Title')
    
        self.reviews_tree.pack(fill='both', expand=True, padx=10, pady=10)
    
        # Load initial data
        self.load_reviews()

    def init_coupons_tab(self):
        """Initialize Coupons tab with CRUD operations"""
        # Left panel for form
        left_panel = tk.Frame(self.tab_coupons, bg='white', relief='raised', bd=2)
        left_panel.pack(side='left', fill='both', padx=10, pady=10)
    
        tk.Label(left_panel, text="Coupon Management", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
    
        # Form fields
        tk.Label(left_panel, text="Coupon ID:", bg='white').pack(anchor='w', padx=20)
        self.coupon_id_entry = tk.Entry(left_panel, width=30)
        self.coupon_id_entry.pack(padx=20, pady=5)
    
        tk.Label(left_panel, text="Code:", bg='white').pack(anchor='w', padx=20)
        self.coupon_code_entry = tk.Entry(left_panel, width=30)
        self.coupon_code_entry.pack(padx=20, pady=5)
    
        tk.Label(left_panel, text="Discount Value:", bg='white').pack(anchor='w', padx=20)
        self.coupon_value_entry = tk.Entry(left_panel, width=30)
        self.coupon_value_entry.pack(padx=20, pady=5)
    
        tk.Label(left_panel, text="Type (percentage/fixed):", bg='white').pack(anchor='w', padx=20)
        self.coupon_type_entry = tk.Entry(left_panel, width=30)
        self.coupon_type_entry.pack(padx=20, pady=5)
    
        # Buttons
        button_frame = tk.Frame(left_panel, bg='white')
        button_frame.pack(pady=20)
    
        tk.Button(button_frame, text="INSERT", command=self.insert_coupon, 
                 bg='#27ae60', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="UPDATE", command=self.update_coupon, 
                 bg='#3498db', fg='white', width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="DELETE", command=self.delete_coupon, 
                 bg='#e74c3c', fg='white', width=10).pack(side='left', padx=5)
    
        # Right panel for data display
        right_panel = tk.Frame(self.tab_coupons, bg='white', relief='raised', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
    
        tk.Label(right_panel, text="Coupons List (SELECT)", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
    
        tk.Button(right_panel, text="Refresh List", command=self.load_coupons, 
                 bg='#16a085', fg='white').pack(pady=5)
    
        # Treeview for coupons
        self.coupons_tree = ttk.Treeview(right_panel, columns=('ID', 'Code', 'Value', 'Type', 'Active'), show='headings')
        self.coupons_tree.heading('ID', text='ID')
        self.coupons_tree.heading('Code', text='Code')
        self.coupons_tree.heading('Value', text='Value')
        self.coupons_tree.heading('Type', text='Type')
        self.coupons_tree.heading('Active', text='Active')
    
        self.coupons_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.coupons_tree.bind('<<TreeviewSelect>>', self.on_coupon_select)
    
        # Load initial data
        self.load_coupons()

    def init_shipments_tab(self):
        """Initialize Shipments tab (SELECT and UPDATE status)"""
        frame = tk.Frame(self.tab_shipments, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
    
        tk.Label(frame, text="Shipment Tracking (SELECT & UPDATE)", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
    
        # Update form
        form_frame = tk.Frame(frame, bg='white')
        form_frame.pack(pady=10)
    
        tk.Label(form_frame, text="Shipment ID:", bg='white').grid(row=0, column=0, padx=5, pady=5)
        self.ship_id_entry = tk.Entry(form_frame, width=20)
        self.ship_id_entry.grid(row=0, column=1, padx=5, pady=5)
    
        tk.Label(form_frame, text="New Status:", bg='white').grid(row=0, column=2, padx=5, pady=5)
        self.ship_status_var = tk.StringVar()
        status_combo = ttk.Combobox(form_frame, textvariable=self.ship_status_var, width=18,
                                    values=['pending', 'in_transit', 'out_for_delivery', 'delivered', 'returned'])
        status_combo.grid(row=0, column=3, padx=5, pady=5)
    
        tk.Button(form_frame, text="UPDATE Status", command=self.update_shipment, 
                 bg='#3498db', fg='white', width=15).grid(row=1, column=0, columnspan=4, pady=10)
        tk.Button(form_frame, text="Refresh List", command=self.load_shipments, 
                 bg='#16a085', fg='white', width=15).grid(row=2, column=0, columnspan=4, pady=5)
    
        # Treeview for shipments
        self.shipments_tree = ttk.Treeview(frame, columns=('ID', 'Order', 'Tracking', 'Status', 'Est. Delivery'), show='headings')
        self.shipments_tree.heading('ID', text='Shipment ID')
        self.shipments_tree.heading('Order', text='Order ID')
        self.shipments_tree.heading('Tracking', text='Tracking#')
        self.shipments_tree.heading('Status', text='Status')
        self.shipments_tree.heading('Est. Delivery', text='Est. Delivery')
    
        self.shipments_tree.pack(fill='both', expand=True, padx=10, pady=10)
        self.shipments_tree.bind('<<TreeviewSelect>>', self.on_shipment_select)
    
        # Load initial data
        self.load_shipments()

    # DML Operations for new tabs

    def insert_category(self):
        """INSERT operation for categories"""
        try:
            name = self.cat_name_entry.get()
            desc = self.cat_desc_entry.get()
        
            if not name:
                messagebox.showwarning("Validation Error", "Category name is required!")
                return
        
            query = "INSERT INTO category (name, description) VALUES (%s, %s)"
            self.cursor.execute(query, (name, desc))
            self.conn.commit()
        
            messagebox.showinfo("Success", "Category inserted successfully!")
            self.update_status(f"INSERT: Added category '{name}'")
            self.clear_category_form()
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert category:\n{e}")
            self.conn.rollback()

    def update_category(self):
        """UPDATE operation for categories"""
        try:
            cat_id = int(self.cat_id_entry.get())
            name = self.cat_name_entry.get()
            desc = self.cat_desc_entry.get()
        
            query = "UPDATE category SET name = %s, description = %s WHERE category_id = %s"
            self.cursor.execute(query, (name, desc, cat_id))
            self.conn.commit()
        
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", "Category updated successfully!")
                self.update_status(f"UPDATE: Modified category ID {cat_id}")
                self.clear_category_form()
                self.load_categories()
            else:
                messagebox.showwarning("Warning", "No category found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update category:\n{e}")
            self.conn.rollback()

    def delete_category(self):
        """DELETE operation for categories"""
        try:
            cat_id = int(self.cat_id_entry.get())
        
            if messagebox.askyesno("Confirm Delete", f"Delete category ID {cat_id}?"):
                query = "DELETE FROM category WHERE category_id = %s"
                self.cursor.execute(query, (cat_id,))
                self.conn.commit()
            
                if self.cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Category deleted successfully!")
                    self.update_status(f"DELETE: Removed category ID {cat_id}")
                    self.clear_category_form()
                    self.load_categories()
                else:
                    messagebox.showwarning("Warning", "No category found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete category:\n{e}")
            self.conn.rollback()

    def insert_review(self):
        """INSERT operation for reviews"""
        try:
            product_id = int(self.review_product_entry.get())
            customer_id = int(self.review_customer_entry.get())
            rating = int(self.review_rating_entry.get())
            title = self.review_title_entry.get()
            comment = self.review_comment_entry.get()
        
            if rating < 1 or rating > 5:
                messagebox.showwarning("Validation Error", "Rating must be between 1 and 5!")
                return
        
            query = """
                INSERT INTO review (product_id, customer_id, rating, title, comment)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (product_id, customer_id, rating, title, comment))
            self.conn.commit()
        
            messagebox.showinfo("Success", "Review inserted successfully!")
            self.update_status(f"INSERT: Added review for product {product_id}")
            self.load_reviews()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert review:\n{e}")
            self.conn.rollback()

    def insert_coupon(self):
        """INSERT operation for coupons"""
        try:
            code = self.coupon_code_entry.get()
            value = float(self.coupon_value_entry.get())
            disc_type = self.coupon_type_entry.get()
        
            if not code or disc_type not in ['percentage', 'fixed']:
                messagebox.showwarning("Validation Error", "Valid code and type required!")
                return
        
            query = """
                INSERT INTO coupon (code, discount_value, discount_type, is_active)
                VALUES (%s, %s, %s, TRUE)
            """
            self.cursor.execute(query, (code, value, disc_type))
            self.conn.commit()
        
            messagebox.showinfo("Success", "Coupon inserted successfully!")
            self.update_status(f"INSERT: Added coupon '{code}'")
            self.load_coupons()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert coupon:\n{e}")
            self.conn.rollback()

    def update_coupon(self):
        """UPDATE operation for coupons"""
        try:
            coupon_id = int(self.coupon_id_entry.get())
            code = self.coupon_code_entry.get()
            value = float(self.coupon_value_entry.get())
            disc_type = self.coupon_type_entry.get()
        
            query = """
                UPDATE coupon 
                SET code = %s, discount_value = %s, discount_type = %s
                WHERE coupon_id = %s
            """
            self.cursor.execute(query, (code, value, disc_type, coupon_id))
            self.conn.commit()
        
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", "Coupon updated successfully!")
                self.update_status(f"UPDATE: Modified coupon ID {coupon_id}")
                self.load_coupons()
            else:
                messagebox.showwarning("Warning", "No coupon found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update coupon:\n{e}")
            self.conn.rollback()

    def delete_coupon(self):
        """DELETE operation for coupons"""
        try:
            coupon_id = int(self.coupon_id_entry.get())
        
            if messagebox.askyesno("Confirm Delete", f"Delete coupon ID {coupon_id}?"):
                query = "DELETE FROM coupon WHERE coupon_id = %s"
                self.cursor.execute(query, (coupon_id,))
                self.conn.commit()
            
                if self.cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Coupon deleted successfully!")
                    self.update_status(f"DELETE: Removed coupon ID {coupon_id}")
                    self.load_coupons()
                else:
                    messagebox.showwarning("Warning", "No coupon found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete coupon:\n{e}")
            self.conn.rollback()

    def update_shipment(self):
        """UPDATE operation for shipment status"""
        try:
            ship_id = int(self.ship_id_entry.get())
            status = self.ship_status_var.get()
        
            query = "UPDATE shipment SET status = %s WHERE shipment_id = %s"
            self.cursor.execute(query, (status, ship_id))
            self.conn.commit()
        
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", "Shipment status updated!")
                self.update_status(f"UPDATE: Shipment {ship_id} status = {status}")
                self.load_shipments()
            else:
                messagebox.showwarning("Warning", "No shipment found with that ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update shipment:\n{e}")
            self.conn.rollback()

    # SELECT operations for new tabs

    def load_categories(self):
        """SELECT operation to load categories"""
        try:
            self.categories_tree.delete(*self.categories_tree.get_children())
            query = "SELECT category_id, name, description FROM category ORDER BY category_id"
            self.cursor.execute(query)
        
            for row in self.cursor.fetchall():
                self.categories_tree.insert('', 'end', values=(
                    row['category_id'],
                    row['name'],
                    row['description'] or 'N/A'
                ))
            self.update_status("SELECT: Loaded categories")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories:\n{e}")

    def load_reviews(self):
        """SELECT operation to load reviews"""
        try:
            self.reviews_tree.delete(*self.reviews_tree.get_children())
            query = "SELECT review_id, product_id, customer_id, rating, title FROM review ORDER BY review_id DESC LIMIT 50"
            self.cursor.execute(query)
        
            for row in self.cursor.fetchall():
                self.reviews_tree.insert('', 'end', values=(
                    row['review_id'],
                    row['product_id'],
                    row['customer_id'],
                    row['rating'],
                    row['title'] or 'No title'
                ))
            self.update_status("SELECT: Loaded reviews")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reviews:\n{e}")

    def load_coupons(self):
        """SELECT operation to load coupons"""
        try:
            self.coupons_tree.delete(*self.coupons_tree.get_children())
            query = "SELECT coupon_id, code, discount_value, discount_type, is_active FROM coupon LIMIT 50"
            self.cursor.execute(query)
        
            for row in self.cursor.fetchall():
                self.coupons_tree.insert('', 'end', values=(
                    row['coupon_id'],
                    row['code'],
                    row['discount_value'],
                    row['discount_type'],
                    'Yes' if row['is_active'] else 'No'
                ))
            self.update_status("SELECT: Loaded coupons")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load coupons:\n{e}")

    def load_shipments(self):
        """SELECT operation to load shipments"""
        try:
            self.shipments_tree.delete(*self.shipments_tree.get_children())
            query = """
                SELECT shipment_id, order_id, tracking_number, status, estimated_delivery
                FROM shipment
                ORDER BY shipment_id DESC
                LIMIT 50
            """
            self.cursor.execute(query)
        
            for row in self.cursor.fetchall():
                self.shipments_tree.insert('', 'end', values=(
                    row['shipment_id'],
                    row['order_id'],
                    row['tracking_number'] or 'N/A',
                    row['status'],
                    row['estimated_delivery'] or 'N/A'
                ))
            self.update_status("SELECT: Loaded shipments")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load shipments:\n{e}")

    # Event handlers

    def on_category_select(self, event):
        """Handle category selection"""
        selection = self.categories_tree.selection()
        if selection:
            item = self.categories_tree.item(selection[0])
            values = item['values']
        
            self.cat_id_entry.delete(0, tk.END)
            self.cat_id_entry.insert(0, values[0])
        
            self.cat_name_entry.delete(0, tk.END)
            self.cat_name_entry.insert(0, values[1])
        
            if values[2] != 'N/A':
                self.cat_desc_entry.delete(0, tk.END)
                self.cat_desc_entry.insert(0, values[2])

    def on_coupon_select(self, event):
        """Handle coupon selection"""
        selection = self.coupons_tree.selection()
        if selection:
            item = self.coupons_tree.item(selection[0])
            values = item['values']
        
            self.coupon_id_entry.delete(0, tk.END)
            self.coupon_id_entry.insert(0, values[0])
        
            self.coupon_code_entry.delete(0, tk.END)
            self.coupon_code_entry.insert(0, values[1])
        
            self.coupon_value_entry.delete(0, tk.END)
            self.coupon_value_entry.insert(0, values[2])
        
            self.coupon_type_entry.delete(0, tk.END)
            self.coupon_type_entry.insert(0, values[3])

    def on_shipment_select(self, event):
        """Handle shipment selection"""
        selection = self.shipments_tree.selection()
        if selection:
            item = self.shipments_tree.item(selection[0])
            values = item['values']
        
            self.ship_id_entry.delete(0, tk.END)
            self.ship_id_entry.insert(0, values[0])
        
            self.ship_status_var.set(values[3])

    def clear_category_form(self):
        """Clear category form"""
        self.cat_id_entry.delete(0, tk.END)
        self.cat_name_entry.delete(0, tk.END)
        self.cat_desc_entry.delete(0, tk.END)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ECommerceGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
    
    # ==================== STUB METHODS FOR NEW TABS ====================
