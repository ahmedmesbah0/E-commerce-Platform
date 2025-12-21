#!/usr/bin/env python3
"""
Complete E-Commerce Application with Authentication
Sign In / Register → Customer Shopping / Admin Management
Based on ERD: E-Commerce_updated3-dbms.drawio
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from datetime import datetime, timedelta
import hashlib
import sys

class DatabaseConfig:
    HOST = 'localhost'
    USER = 'ecommerce_user'
    PASSWORD = 'SecurePass123!'
    DATABASE = 'ecommerce_db'

class AuthenticationApp:
    """Main application with authentication"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("E-Commerce System - Sign In")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        self.conn = None
        self.cursor = None
        self.connect_database()
        
        self.user_role = None  # 'customer' or 'admin'
        self.user_id = None
        self.user_email = None
        self.user_name = None
        
        self.create_auth_ui()
        
    def connect_database(self):
        """Connect to database"""
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
            messagebox.showerror("Database Error", f"Connection failed:\n{err}")
            sys.exit(1)
    
    def create_auth_ui(self):
        """Create authentication interface"""
        # Header
        header = tk.Frame(self.root, bg='#34495e', height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="🛒 E-Commerce System",
            font=('Arial', 24, 'bold'),
            bg='#34495e',
            fg='white'
        ).pack(pady=30)
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg='#2c3e50')
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Show sign in by default
        self.show_signin()
        
    def show_signin(self):
        """Show sign in form"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Sign in container
        signin_frame = tk.Frame(self.main_frame, bg='white', relief='raised', bd=2)
        signin_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        tk.Label(
            signin_frame,
            text="Sign In",
            font=('Arial', 20, 'bold'),
            bg='white'
        ).pack(pady=20)
        
        # Email
        tk.Label(signin_frame, text="Email:", bg='white', font=('Arial', 12)).pack(pady=5)
        self.signin_email = tk.Entry(signin_frame, width=35, font=('Arial', 12))
        self.signin_email.pack(pady=5)
        
        # Password
        tk.Label(signin_frame, text="Password:", bg='white', font=('Arial', 12)).pack(pady=5)
        self.signin_password = tk.Entry(signin_frame, width=35, font=('Arial', 12), show='*')
        self.signin_password.pack(pady=5)
        self.signin_password.bind('<Return>', lambda e: self.do_signin())
        
        # Role selection
        tk.Label(signin_frame, text="Sign in as:", bg='white', font=('Arial', 12)).pack(pady=10)
        self.role_var = tk.StringVar(value='customer')
        
        role_frame = tk.Frame(signin_frame, bg='white')
        role_frame.pack()
        
        tk.Radiobutton(
            role_frame,
            text="Customer",
            variable=self.role_var,
            value='customer',
            bg='white',
            font=('Arial', 11)
        ).pack(side='left', padx=20)
        
        tk.Radiobutton(
            role_frame,
            text="Admin",
            variable=self.role_var,
            value='admin',
            bg='white',
            font=('Arial', 11)
        ).pack(side='left', padx=20)
        
        # Sign in button
        tk.Button(
            signin_frame,
            text="Sign In",
            command=self.do_signin,
            bg='#27ae60',
            fg='white',
            font=('Arial', 14, 'bold'),
            width=20,
            height=2
        ).pack(pady=20)
        
        # Register link
        tk.Label(signin_frame, text="Don't have an account?", bg='white').pack()
        tk.Button(
            signin_frame,
            text="Register Here",
            command=self.show_register,
            bg='#3498db',
            fg='white',
            font=('Arial', 11)
        ).pack(pady=10)
        
        # Demo credentials
        demo_frame = tk.Frame(signin_frame, bg='#ecf0f1', relief='ridge', bd=1)
        demo_frame.pack(fill='x', pady=10, padx=20)
        
        tk.Label(
            demo_frame,
            text="Demo Credentials:",
            bg='#ecf0f1',
            font=('Arial', 10, 'bold')
        ).pack(pady=5)
        
        tk.Label(
            demo_frame,
            text="Customer: customer@demo.com / password123",
            bg='#ecf0f1',
            font=('Arial', 9)
        ).pack()
        
        tk.Label(
            demo_frame,
            text="Admin: admin@demo.com / admin123",
            bg='#ecf0f1',
            font=('Arial', 9)
        ).pack(pady=(0, 5))
    
    def show_register(self):
        """Show registration form"""
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Register container
        register_frame = tk.Frame(self.main_frame, bg='white', relief='raised', bd=2)
        register_frame.pack(pady=20, padx=40, fill='both', expand=True)
        
        tk.Label(
            register_frame,
            text="Create Account",
            font=('Arial', 20, 'bold'),
            bg='white'
        ).pack(pady=15)
        
        # Name
        tk.Label(register_frame, text="Full Name:", bg='white', font=('Arial', 11)).pack(pady=3)
        self.reg_name = tk.Entry(register_frame, width=35, font=('Arial', 11))
        self.reg_name.pack(pady=3)
        
        # Email
        tk.Label(register_frame, text="Email:", bg='white', font=('Arial', 11)).pack(pady=3)
        self.reg_email = tk.Entry(register_frame, width=35, font=('Arial', 11))
        self.reg_email.pack(pady=3)
        
        # Phone
        tk.Label(register_frame, text="Phone:", bg='white', font=('Arial', 11)).pack(pady=3)
        self.reg_phone = tk.Entry(register_frame, width=35, font=('Arial', 11))
        self.reg_phone.pack(pady=3)
        
        # Address
        tk.Label(register_frame, text="Address:", bg='white', font=('Arial', 11)).pack(pady=3)
        self.reg_address = tk.Entry(register_frame, width=35, font=('Arial', 11))
        self.reg_address.pack(pady=3)
        
        # Password
        tk.Label(register_frame, text="Password:", bg='white', font=('Arial', 11)).pack(pady=3)
        self.reg_password = tk.Entry(register_frame, width=35, font=('Arial', 11), show='*')
        self.reg_password.pack(pady=3)
        
        # Confirm password
        tk.Label(register_frame, text="Confirm Password:", bg='white', font=('Arial', 11)).pack(pady=3)
        self.reg_confirm = tk.Entry(register_frame, width=35, font=('Arial', 11), show='*')
        self.reg_confirm.pack(pady=3)
        
        # Register button
        tk.Button(
            register_frame,
            text="Create Account",
            command=self.do_register,
            bg='#27ae60',
            fg='white',
            font=('Arial', 13, 'bold'),
            width=20
        ).pack(pady=15)
        
        # Back to sign in
        tk.Button(
            register_frame,
            text="← Back to Sign In",
            command=self.show_signin,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10)
        ).pack()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def do_signin(self):
        """Process sign in"""
        email = self.signin_email.get().strip()
        password = self.signin_password.get()
        role = self.role_var.get()
        
        if not email or not password:
            messagebox.showwarning("Validation", "Please enter email and password!")
            return
        
        password_hash = self.hash_password(password)
        
        try:
            if role == 'customer':
                query = """
                    SELECT customer_id, name, email 
                    FROM customer 
                    WHERE email = %s AND password_hash = %s AND is_active = TRUE
                """
                self.cursor.execute(query, (email, password_hash))
                result = self.cursor.fetchone()
                
                if result:
                    self.user_role = 'customer'
                    self.user_id = result['customer_id']
                    self.user_name = result['name']
                    self.user_email = result['email']
                    self.launch_customer_app()
                else:
                    messagebox.showerror("Login Failed", "Invalid email or password!")
                    
            else:  # admin
                query = """
                    SELECT admin_id, email, role
                    FROM admin
                    WHERE email = %s AND password_hash = %s AND is_active = TRUE
                """
                self.cursor.execute(query, (email, password_hash))
                result = self.cursor.fetchone()
                
                if result:
                    self.user_role = 'admin'
                    self.user_id = result['admin_id']
                    self.user_email = result['email']
                    self.user_name = result['role'].replace('_', ' ').title()
                    
                    # Update last login
                    self.cursor.execute(
                        "UPDATE admin SET last_login = NOW() WHERE admin_id = %s",
                        (self.user_id,)
                    )
                    self.conn.commit()
                    
                    self.launch_admin_app()
                else:
                    messagebox.showerror("Login Failed", "Invalid admin credentials!")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Login error:\n{e}")
    
    def do_register(self):
        """Process registration"""
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        phone = self.reg_phone.get().strip()
        address = self.reg_address.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        # Validation
        if not all([name, email, password]):
            messagebox.showwarning("Validation", "Name, email, and password are required!")
            return
        
        if password != confirm:
            messagebox.showerror("Validation", "Passwords do not match!")
            return
        
        if len(password) < 6:
            messagebox.showwarning("Validation", "Password must be at least 6 characters!")
            return
        
        password_hash = self.hash_password(password)
        
        try:
            # Check if email exists
            self.cursor.execute("SELECT email FROM customer WHERE email = %s", (email,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Email already registered!")
                return
            
            # Insert new customer
            query = """
                INSERT INTO customer (name, email, phone, address, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (name, email, phone, address, password_hash))
            self.conn.commit()
            
            messagebox.showinfo(
                "Success!",
                f"Account created successfully!\n\nWelcome, {name}!\n\nYou can now sign in."
            )
            
            self.show_signin()
            self.signin_email.delete(0, tk.END)
            self.signin_email.insert(0, email)
            
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed:\n{e}")
            self.conn.rollback()
    
    def launch_customer_app(self):
        """Launch customer shopping interface"""
        self.root.destroy()
        customer_root = tk.Tk()
        from customer_gui import CustomerGUI
        app = CustomerGUI(customer_root, self.user_id, self.user_name, self.user_email, self.conn)
        customer_root.protocol("WM_DELETE_WINDOW", app.on_closing)
        customer_root.mainloop()
    
    def launch_admin_app(self):
        """Launch admin management interface"""
        self.root.destroy()
        admin_root = tk.Tk()
        from admin_gui import AdminGUI
        app = AdminGUI(admin_root, self.user_id, self.user_name, self.user_email, self.conn)
        admin_root.protocol("WM_DELETE_WINDOW", app.on_closing)
        admin_root.mainloop()
    
    def run(self):
        """Run the authentication app"""
        self.root.mainloop()

def main():
    """Main entry point"""
    # Create demo accounts if they don't exist
    try:
        conn = mysql.connector.connect(
            host=DatabaseConfig.HOST,
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD,
            database=DatabaseConfig.DATABASE
        )
        cursor = conn.cursor()
        
        # Create demo customer
        customer_hash = hashlib.sha256('password123'.encode()).hexdigest()
        try:
            cursor.execute("""
                INSERT INTO customer (name, email, phone, address, password_hash)
                VALUES ('Demo Customer', 'customer@demo.com', '+20123456789', 'Cairo, Egypt', %s)
            """, (customer_hash,))
            conn.commit()
        except:
            pass  # Already exists
        
        # Create demo admin
        admin_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        try:
            cursor.execute("""
                INSERT INTO admin (email, password_hash, role)
                VALUES ('admin@demo.com', %s, 'super_admin')
            """, (admin_hash,))
            conn.commit()
        except:
            pass  # Already exists
        
        conn.close()
    except:
        pass
    
    # Launch authentication app
    app = AuthenticationApp()
    app.run()

if __name__ == "__main__":
    main()
