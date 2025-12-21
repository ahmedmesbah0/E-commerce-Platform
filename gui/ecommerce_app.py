#!/usr/bin/env python3
"""
E-Commerce Dual-Mode GUI Application
Academic Project - Database Management Systems
Admin Mode + Customer Mode with Login
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

class LoginWindow:
    """Login window for role selection"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("E-Commerce System - Login")
        self.root.geometry("500x400")
        self.root.configure(bg='#2c3e50')
        
        self.selected_role = None
        self.selected_user_id = None
        
        self.create_login_ui()
        
    def create_login_ui(self):
        """Create login interface"""
        # Header
        header = tk.Label(
            self.root,
            text="E-Commerce Management System",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        header.pack(pady=40)
        
        # Login frame
        login_frame = tk.Frame(self.root, bg='white', relief='raised', bd=2)
        login_frame.pack(padx=50, pady=20, fill='both', expand=True)
        
        tk.Label(
            login_frame,
            text="Select Your Role:",
            font=('Arial', 16, 'bold'),
            bg='white'
        ).pack(pady=30)
        
        # Admin button
        tk.Button(
            login_frame,
            text="🔐 Admin Mode",
            command=self.login_as_admin,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 14, 'bold'),
            width=20,
            height=2
        ).pack(pady=15)
        
        tk.Label(
            login_frame,
            text="Manage products, orders, inventory",
            font=('Arial', 10),
            bg='white',
            fg='#7f8c8d'
        ).pack()
        
        # Customer button
        tk.Button(
            login_frame,
            text="🛒 Customer Mode",
            command=self.login_as_customer,
            bg='#27ae60',
            fg='white',
            font=('Arial', 14, 'bold'),
            width=20,
            height=2
        ).pack(pady=15)
        
        tk.Label(
            login_frame,
            text="Browse products, place orders",
            font=('Arial', 10),
            bg='white',
            fg='#7f8c8d'
        ).pack()
        
    def login_as_admin(self):
        """Login as admin"""
        self.selected_role = 'admin'
        self.selected_user_id = None
        self.root.destroy()
        
    def login_as_customer(self):
        """Login as customer - prompt for customer ID"""
        customer_id = tk.simpledialog.askinteger(
            "Customer Login",
            "Enter your Customer ID:\n(Use 2 for demo)",
            parent=self.root,
            minvalue=1
        )
        if customer_id:
            self.selected_role = 'customer'
            self.selected_user_id = customer_id
            self.root.destroy()
        
    def run(self):
        """Run the login window"""
        self.root.mainloop()
        return self.selected_role, self.selected_user_id

# Import the admin GUI class from ecommerce_gui.py
import importlib.util
spec = importlib.util.spec_from_file_location("admin_gui", "ecommerce_gui.py")
admin_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admin_module)
AdminGUI = admin_module.ECommerceGUI

class CustomerGUI:
    """Customer mode GUI for shopping"""
    
    def __init__(self, root, customer_id):
        self.root = root
        self.customer_id = customer_id
        self.root.title(f"E-Commerce - Customer #{customer_id}")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Cart storage
        self.cart = []
        
        # Database connection
        self.conn = None
        self.cursor = None
        self.connect_database()
        
        # Get customer info
        self.load_customer_info()
        
        # Create interface
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
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect:\n{err}")
            sys.exit(1)
            
    def load_customer_info(self):
        """Load customer information"""
        try:
            query = "SELECT name, email FROM customer WHERE customer_id = %s"
            self.cursor.execute(query, (self.customer_id,))
            result = self.cursor.fetchone()
            if result:
                self.customer_name = result['name']
                self.customer_email = result['email']
            else:
                self.customer_name = f"Customer #{self.customer_id}"
                self.customer_email = ""
        except:
            self.customer_name = f"Customer #{self.customer_id}"
            self.customer_email = ""
    
    def create_header(self):
        """Create header with customer info"""
        header_frame = tk.Frame(self.root, bg='#27ae60', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"🛒 Welcome, {self.customer_name}!",
            font=('Arial', 20, 'bold'),
            bg='#27ae60',
            fg='white'
        ).pack(side='left', padx=30, pady=25)
        
        # Store cart button reference so we can update it
        self.cart_button = tk.Button(
            header_frame,
            text=f"🛍️ Cart ({len(self.cart)} items)",
            command=self.view_cart,
            bg='#f39c12',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=15
        )
        self.cart_button.pack(side='right', padx=30, pady=20)
    
    def create_tabs(self):
        """Create customer interface tabs"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tab_products = ttk.Frame(self.notebook)
        self.tab_cart = ttk.Frame(self.notebook)
        self.tab_orders = ttk.Frame(self.notebook)
        self.tab_profile = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_products, text='🛍️ Browse Products')
        self.notebook.add(self.tab_cart, text='🛒 Shopping Cart')
        self.notebook.add(self.tab_orders, text='📦 My Orders')
        self.notebook.add(self.tab_profile, text='👤 My Profile')
        
        self.init_products_tab()
        self.init_cart_tab()
        self.init_orders_tab()
        self.init_profile_tab()
    
    def init_products_tab(self):
        """Product browsing tab"""
        frame = tk.Frame(self.tab_products, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="Browse Products", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Search
        search_frame = tk.Frame(frame, bg='white')
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:", bg='white').pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side='left', padx=5)
        tk.Button(search_frame, text="Search", command=self.search_products,
                 bg='#3498db', fg='white').pack(side='left', padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_products,
                 bg='#16a085', fg='white').pack(side='left', padx=5)
        
        # Products tree
        self.products_tree = ttk.Treeview(frame, columns=('ID', 'Name', 'Price', 'Stock'), show='headings')
        self.products_tree.heading('ID', text='ID')
        self.products_tree.heading('Name', text='Product Name')
        self.products_tree.heading('Price', text='Price (EGP)')
        self.products_tree.heading('Stock', text='In Stock')
        
        self.products_tree.column('ID', width=50)
        self.products_tree.column('Name', width=400)
        self.products_tree.column('Price', width=150)
        self.products_tree.column('Stock', width=100)
        
        self.products_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add to cart button
        button_frame = tk.Frame(frame, bg='white')
        button_frame.pack(pady=10)
        
        tk.Label(button_frame, text="Quantity:", bg='white').pack(side='left', padx=5)
        self.qty_spinbox = tk.Spinbox(button_frame, from_=1, to=10, width=5)
        self.qty_spinbox.pack(side='left', padx=5)
        
        tk.Button(button_frame, text="🛒 Add to Cart", command=self.add_to_cart,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=10)
        
        self.load_products()
    
    def init_cart_tab(self):
        """Shopping cart tab"""
        frame = tk.Frame(self.tab_cart, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="Shopping Cart", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        # Cart tree
        self.cart_tree = ttk.Treeview(frame, columns=('Product', 'Price', 'Qty', 'Subtotal'), show='headings')
        self.cart_tree.heading('Product', text='Product Name')
        self.cart_tree.heading('Price', text='Unit Price')
        self.cart_tree.heading('Qty', text='Quantity')
        self.cart_tree.heading('Subtotal', text='Subtotal')
        
        self.cart_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Total and checkout
        bottom_frame = tk.Frame(frame, bg='white')
        bottom_frame.pack(fill='x', padx=10, pady=20)
        
        self.total_label = tk.Label(bottom_frame, text="Total: EGP 0.00",
                                    font=('Arial', 16, 'bold'), bg='white')
        self.total_label.pack(side='left', padx=20)
        
        tk.Button(bottom_frame, text="🗑️ Clear Cart", command=self.clear_cart,
                 bg='#e74c3c', fg='white', font=('Arial', 12)).pack(side='right', padx=5)
        
        tk.Button(bottom_frame, text="✅ Place Order", command=self.place_order,
                 bg='#27ae60', fg='white', font=('Arial', 14, 'bold')).pack(side='right', padx=5)
    
    def init_orders_tab(self):
        """Order history tab"""
        frame = tk.Frame(self.tab_orders, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="My Order History", font=('Arial', 16, 'bold'), bg='white').pack(pady=10)
        
        button_frame = tk.Frame(frame, bg='white')
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Refresh", command=self.load_customer_orders,
                 bg='#16a085', fg='white').pack(side='left', padx=5)
        
        tk.Button(button_frame, text="📝 Write Review", command=self.show_review_dialog,
                 bg='#f39c12', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Orders tree with more details
        self.orders_tree = ttk.Treeview(frame, columns=('Order ID', 'Date', 'Total', 'Status', 'Items'), show='headings')
        self.orders_tree.heading('Order ID', text='Order #')
        self.orders_tree.heading('Date', text='Order Date')
        self.orders_tree.heading('Total', text='Total Amount')
        self.orders_tree.heading('Status', text='Status')
        self.orders_tree.heading('Items', text='Items Count')
        
        self.orders_tree.column('Order ID', width=80)
        self.orders_tree.column('Date', width=150)
        self.orders_tree.column('Total', width=120)
        self.orders_tree.column('Status', width=100)
        self.orders_tree.column('Items', width=80)
        
        self.orders_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.load_customer_orders()
    
    def init_profile_tab(self):
        """Customer profile tab"""
        frame = tk.Frame(self.tab_profile, bg='white')
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="My Profile", font=('Arial', 16, 'bold'), bg='white').pack(pady=20)
        
        info_frame = tk.Frame(frame, bg='white')
        info_frame.pack(pady=20)
        
        tk.Label(info_frame, text=f"Customer ID: {self.customer_id}",
                font=('Arial', 14), bg='white').pack(pady=10)
        tk.Label(info_frame, text=f"Name: {self.customer_name}",
                font=('Arial', 14), bg='white').pack(pady=10)
        tk.Label(info_frame, text=f"Email: {self.customer_email}",
                font=('Arial', 14), bg='white').pack(pady=10)
    
    # ==== Customer Operations ====
    
    def load_products(self):
        """Load products for browsing"""
        try:
            self.products_tree.delete(*self.products_tree.get_children())
            query = """
                SELECT p.product_id, p.name, p.price, 
                       COALESCE(SUM(i.quantity), 0) as stock
                FROM product p
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.is_active = TRUE
                GROUP BY p.product_id
                ORDER BY p.name
            """
            self.cursor.execute(query)
            
            for row in self.cursor.fetchall():
                self.products_tree.insert('', 'end', values=(
                    row['product_id'],
                    row['name'],
                    f"{row['price']:.2f}",
                    'Yes' if row['stock'] > 0 else 'Out of Stock'
                ))
            self.update_status("Loaded products")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products:\n{e}")
    
    def search_products(self):
        """Search products"""
        search_term = self.search_entry.get()
        if not search_term:
            self.load_products()
            return
            
        try:
            self.products_tree.delete(*self.products_tree.get_children())
            query = """
                SELECT p.product_id, p.name, p.price,
                       COALESCE(SUM(i.quantity), 0) as stock
                FROM product p
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.is_active = TRUE AND p.name LIKE %s
                GROUP BY p.product_id
            """
            self.cursor.execute(query, (f'%{search_term}%',))
            
            for row in self.cursor.fetchall():
                self.products_tree.insert('', 'end', values=(
                    row['product_id'],
                    row['name'],
                    f"{row['price']:.2f}",
                    'Yes' if row['stock'] > 0 else 'Out of Stock'
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Search failed:\n{e}")
    
    def add_to_cart(self):
        """Add selected product to cart"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product!")
            return
            
        item = self.products_tree.item(selection[0])
        values = item['values']
        
        if values[3] == 'Out of Stock':
            messagebox.showwarning("Warning", "Product is out of stock!")
            return
        
        product_id = values[0]
        product_name = values[1]
        price = float(values[2])
        qty = int(self.qty_spinbox.get())
        
        # Add to cart list
        self.cart.append({
            'product_id': product_id,
            'name': product_name,
            'price': price,
            'quantity': qty
        })
        
        messagebox.showinfo("Success", f"Added {qty}x {product_name} to cart!")
        self.update_cart_display()
        self.update_header_cart_count()
    
    def update_cart_display(self):
        """Update cart tree view"""
        self.cart_tree.delete(*self.cart_tree.get_children())
        total = 0
        
        for item in self.cart:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            self.cart_tree.insert('', 'end', values=(
                item['name'],
                f"EGP {item['price']:.2f}",
                item['quantity'],
                f"EGP {subtotal:.2f}"
            ))
        
        self.total_label.config(text=f"Total: EGP {total:.2f}")
    
    def update_header_cart_count(self):
        """Update cart count in header"""
        if hasattr(self, 'cart_button'):
            self.cart_button.config(text=f"🛍️ Cart ({len(self.cart)} items)")
    
    def view_cart(self):
        """Switch to cart tab"""
        self.notebook.select(self.tab_cart)
        self.update_cart_display()
    
    def clear_cart(self):
        """Clear shopping cart"""
        if messagebox.askyesno("Confirm", "Clear entire cart?"):
            self.cart = []
            self.update_cart_display()
            self.update_header_cart_count()
            messagebox.showinfo("Success", "Cart cleared!")

    
    def place_order(self):
        """Place order with cart items"""
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        try:
            # Calculate total
            subtotal = sum(item['price'] * item['quantity'] for item in self.cart)
            tax = subtotal * 0.14  # 14% VAT
            shipping = 50.0
            total = subtotal + tax + shipping
            
            # Insert order (matching actual database schema)
            order_query = """
                INSERT INTO `order` (customer_id, subtotal, tax_amount, shipping_cost, total_amount, shipping_address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(order_query, (
                self.customer_id, subtotal, tax, shipping, total,
                f"Default address for customer {self.customer_id}"
            ))
            order_id = self.cursor.lastrowid
            
            # Insert order items 
            # NOTE: Inventory is automatically reduced by database trigger 'after_order_item_insert'
            for item in self.cart:
                item_query = """
                    INSERT INTO order_item (order_id, product_id, quantity, price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                item_subtotal = item['price'] * item['quantity']
                self.cursor.execute(item_query, (
                    order_id, item['product_id'], item['quantity'],
                    item['price'], item_subtotal
                ))
            
            self.conn.commit()
            
            messagebox.showinfo("Success!", 
                              f"Order #{order_id} placed successfully!\n\n"
                              f"Subtotal: EGP {subtotal:.2f}\n"
                              f"Tax: EGP {tax:.2f}\n"
                              f"Shipping: EGP {shipping:.2f}\n"
                              f"Total: EGP {total:.2f}")
            
            self.cart = []
            self.update_cart_display()
            self.update_header_cart_count()
            self.load_customer_orders()
            self.update_status(f"Order #{order_id} placed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to place order:\n{e}")
            self.conn.rollback()
    
    def load_customer_orders(self):
        """Load customer's order history"""
        try:
            self.orders_tree.delete(*self.orders_tree.get_children())
            query = """
                SELECT o.order_id, o.order_date, o.total_amount, o.status,
                       COUNT(oi.order_item_id) as item_count
                FROM `order` o
                LEFT JOIN order_item oi ON o.order_id = oi.order_id
                WHERE o.customer_id = %s
                GROUP BY o.order_id
                ORDER BY o.order_date DESC
            """
            self.cursor.execute(query, (self.customer_id,))
            
            for row in self.cursor.fetchall():
                self.orders_tree.insert('', 'end', values=(
                    row['order_id'],
                    row['order_date'],
                    f"EGP {row['total_amount']:.2f}",
                    row['status'],
                    row['item_count'] or 0
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders:\n{e}")
    
    def show_review_dialog(self):
        """Show review dialog for delivered orders"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an order first!")
            return
        
        item = self.orders_tree.item(selection[0])
        order_id = item['values'][0]
        order_status = item['values'][3]
        
        if order_status != 'delivered':
            messagebox.showwarning("Review Unavailable", 
                                 "You can only review products from delivered orders!")
            return
        
        # Get products from this order
        self.show_product_selection_for_review(order_id)
    
    def show_product_selection_for_review(self, order_id):
        """Show dialog to select which product to review"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Product to Review")
        dialog.geometry("500x400")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Select a product from Order #{order_id}",
                font=('Arial', 14, 'bold'), bg='white').pack(pady=15)
        
        # Get products from order
        query = """
            SELECT oi.product_id, p.name, 
                   (SELECT COUNT(*) FROM review r 
                    WHERE r.product_id = oi.product_id 
                    AND r.customer_id = %s) as already_reviewed
            FROM order_item oi
            JOIN product p ON oi.product_id = p.product_id
            WHERE oi.order_id = %s
        """
        self.cursor.execute(query, (self.customer_id, order_id))
        products = self.cursor.fetchall()
        
        # Product listbox
        list_frame = tk.Frame(dialog, bg='white')
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        product_listbox = tk.Listbox(list_frame, font=('Arial', 11),
                                     yscrollcommand=scrollbar.set, height=10)
        product_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=product_listbox.yview)
        
        product_map = {}
        for product in products:
            status = "✓ Reviewed" if product['already_reviewed'] > 0 else ""
            display_text = f"{product['name']} {status}"
            product_listbox.insert('end', display_text)
            product_map[product_listbox.size() - 1] = product
        
        def on_select_product():
            sel = product_listbox.curselection()
            if not sel:
                messagebox.showwarning("Warning", "Please select a product!")
                return
            
            product = product_map[sel[0]]
            if product['already_reviewed'] > 0:
                messagebox.showinfo("Already Reviewed", 
                                  "You have already reviewed this product!")
                return
            
            dialog.destroy()
            self.open_review_form(product['product_id'], product['name'])
        
        tk.Button(dialog, text="Write Review", command=on_select_product,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold')).pack(pady=10)
        
        tk.Button(dialog, text="Cancel", command=dialog.destroy,
                 bg='#95a5a6', fg='white').pack(pady=5)
    
    def open_review_form(self, product_id, product_name):
        """Open review submission form"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Write Review")
        dialog.geometry("500x450")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text=f"Write Review for:",
                font=('Arial', 12, 'bold'), bg='white').pack(pady=10)
        tk.Label(dialog, text=product_name,
                font=('Arial', 11), bg='white', fg='#27ae60').pack()
        
        # Rating
        rating_frame = tk.Frame(dialog, bg='white')
        rating_frame.pack(pady=15)
        
        tk.Label(rating_frame, text="Rating:", font=('Arial', 11, 'bold'),
                bg='white').pack(side='left', padx=5)
        
        rating_var = tk.IntVar(value=5)
        for i in range(1, 6):
            tk.Radiobutton(rating_frame, text=f"{'⭐' * i}", variable=rating_var,
                          value=i, bg='white', font=('Arial', 10)).pack(side='left')
        
        # Title
        tk.Label(dialog, text="Review Title (optional):", font=('Arial', 10),
                bg='white').pack(pady=5)
        title_entry = tk.Entry(dialog, width=50, font=('Arial', 10))
        title_entry.pack(pady=5)
        
        # Comment
        tk.Label(dialog, text="Your Review (optional):", font=('Arial', 10),
                bg='white').pack(pady=5)
        comment_text = scrolledtext.ScrolledText(dialog, width=50, height=8,
                                                 font=('Arial', 10))
        comment_text.pack(pady=5)
        
        def submit_review():
            rating = rating_var.get()
            title = title_entry.get().strip()
            comment = comment_text.get("1.0", "end").strip()
            
            try:
                # Insert review
                query = """
                    INSERT INTO review (product_id, customer_id, rating, title, comment, is_verified_purchase)
                    VALUES (%s, %s, %s, %s, %s, TRUE)
                """
                self.cursor.execute(query, (product_id, self.customer_id, rating, 
                                          title if title else None,
                                          comment if comment else None))
                self.conn.commit()
                
                messagebox.showinfo("Success!", 
                                  f"Thank you for your {rating}-star review!\n\n"
                                  "Your review will be visible after admin approval.")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to submit review:\n{e}")
                self.conn.rollback()
        
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Submit Review", command=submit_review,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                 bg='#95a5a6', fg='white').pack(side='left', padx=5)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Label(
            self.root,
            text=f"Customer Mode | {self.customer_name}",
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
        """Handle closing"""
        if messagebox.askokcancel("Quit", "Exit application?"):
            if self.conn:
                self.conn.close()
            self.root.destroy()

def main():
    """Main application entry point"""
    # Show login window
    import tkinter.simpledialog
    login = LoginWindow()
    role, user_id = login.run()
    
    if role is None:
        return
    
    # Create appropriate GUI based on role
    root = tk.Tk()
    
    if role == 'admin':
        app = AdminGUI(root)
    else:  # customer
        app = CustomerGUI(root, user_id)
    
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
