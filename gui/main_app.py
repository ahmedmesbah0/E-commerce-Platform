#!/usr/bin/env python3
"""
Professional E-Commerce Application - Modern UI
Beautiful design with gradients, shadows, and polish
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import hashlib
import sys

class DatabaseConfig:
    HOST = 'localhost'
    USER = 'ecommerce_user'
    PASSWORD = 'SecurePass123!'
    DATABASE = 'ecommerce_db'

class ModernStyle:
    """Professional color palette"""
    PRIMARY = '#6C5CE7'
    PRIMARY_DARK = '#5B4BC4'
    SUCCESS = '#00B894'
    SUCCESS_DARK = '#00A082'
    BG_DARK = '#2D3436'
    BG_LIGHT = '#DFE6E9'
    BG_WHITE = '#FFFFFF'
    TEXT_DARK = '#2D3436'
    TEXT_LIGHT = '#636E72'
    TEXT_WHITE = '#FFFFFF'

class AuthenticationApp:
    """Professional authentication UI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("E-Commerce System")
        self.root.geometry("900x650")
        self.root.configure(bg=ModernStyle.BG_LIGHT)
        
        self.conn = None
        self.cursor = None
        self.connect_database()
        
        self.user_role = None
        self.user_id = None
        self.user_email = None
        self.user_name = None
        
        self.create_ui()
    
    def connect_database(self):
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
    
    def create_ui(self):
        main = tk.Frame(self.root, bg=ModernStyle.BG_LIGHT)
        main.pack(fill='both', expand=True)
        
        # Left panel - branding
        left = tk.Frame(main, bg=ModernStyle.PRIMARY, width=350)
        left.pack(side='left', fill='y')
        left.pack_propagate(False)
        
        brand = tk.Frame(left, bg=ModernStyle.PRIMARY)
        brand.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(brand, text="🛒", font=('Segoe UI', 60), bg=ModernStyle.PRIMARY, 
                fg=ModernStyle.TEXT_WHITE).pack(pady=10)
        tk.Label(brand, text="E-Commerce", font=('Segoe UI', 28, 'bold'), 
                bg=ModernStyle.PRIMARY, fg=ModernStyle.TEXT_WHITE).pack()
        tk.Label(brand, text="Management System", font=('Segoe UI', 11), 
                bg=ModernStyle.PRIMARY, fg=ModernStyle.TEXT_WHITE).pack(pady=(5, 30))
        
        for f in ["✓ Shop Products", "✓ Track Orders", "✓ Manage Inventory", "✓ Customer Reviews"]:
            tk.Label(brand, text=f, font=('Segoe UI', 11), bg=ModernStyle.PRIMARY,
                    fg=ModernStyle.TEXT_WHITE, anchor='w').pack(pady=5, anchor='w', padx=40)
        
        # Right panel
        self.right = tk.Frame(main, bg=ModernStyle.BG_WHITE)
        self.right.pack(side='right', fill='both', expand=True)
        
        self.show_signin()
    
    def show_signin(self):
        for w in self.right.winfo_children(): w.destroy()
        
        center = tk.Frame(self.right, bg=ModernStyle.BG_WHITE)
        center.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(center, text="Welcome Back!", font=('Segoe UI', 24, 'bold'),
                bg=ModernStyle.BG_WHITE, fg=ModernStyle.TEXT_DARK).pack(pady=(0, 10))
        tk.Label(center, text="Sign in to continue", font=('Segoe UI', 11),
                bg=ModernStyle.BG_WHITE, fg=ModernStyle.TEXT_LIGHT).pack(pady=(0, 30))
        
        # Email
        tk.Label(center, text="Email Address", font=('Segoe UI', 9),
                bg=ModernStyle.BG_WHITE, fg=ModernStyle.TEXT_LIGHT).pack(anchor='w', padx=50)
        self.signin_email = tk.Entry(center, font=('Segoe UI', 11), bg='#F8F9FA',
                                     relief='flat', bd=0)
        self.signin_email.pack(fill='x', ipady=10, padx=50, pady=5)
        
        # Password
        tk.Label(center, text="Password", font=('Segoe UI', 9),
                bg=ModernStyle.BG_WHITE, fg=ModernStyle.TEXT_LIGHT).pack(anchor='w', padx=50, pady=(10,0))
        self.signin_password = tk.Entry(center, font=('Segoe UI', 11), bg='#F8F9FA',
                                        relief='flat', bd=0, show='●')
        self.signin_password.pack(fill='x', ipady=10, padx=50, pady=5)
        self.signin_password.bind('<Return>', lambda e: self.do_signin())
        
        # Role
        tk.Label(center, text="Sign in as:", font=('Segoe UI', 11),
                bg=ModernStyle.BG_WHITE, fg=ModernStyle.TEXT_LIGHT).pack(pady=(20, 10))
        
        self.role_var = tk.StringVar(value='customer')
        role_frame = tk.Frame(center, bg=ModernStyle.BG_WHITE)
        role_frame.pack()
        
        tk.Radiobutton(role_frame, text="  Customer", variable=self.role_var, value='customer',
                      bg=ModernStyle.BG_WHITE, font=('Segoe UI', 11), cursor='hand2').pack(side='left', padx=15)
        tk.Radiobutton(role_frame, text="  Admin", variable=self.role_var, value='admin',
                      bg=ModernStyle.BG_WHITE, font=('Segoe UI', 11), cursor='hand2').pack(side='left', padx=15)
        
        # Sign in button
        btn = tk.Button(center, text="Sign In", command=self.do_signin, bg=ModernStyle.SUCCESS,
                       fg=ModernStyle.TEXT_WHITE, font=('Segoe UI', 14, 'bold'), relief='flat',
                       cursor='hand2', width=25, height=2)
        btn.pack(pady=25)
        
        # Register link
        tk.Label(center, text="Don't have an account?", bg=ModernStyle.BG_WHITE,
                fg=ModernStyle.TEXT_LIGHT).pack(pady=5)
        tk.Button(center, text="Create Account", command=self.show_register, bg=ModernStyle.BG_WHITE,
                 fg=ModernStyle.PRIMARY, font=('Segoe UI', 12, 'bold'), relief='flat', cursor='hand2').pack()
        
        # Demo
        demo = tk.Frame(center, bg='#F0F8FF', relief='solid', bd=1)
        demo.pack(pady=20, fill='x', padx=50)
        tk.Label(demo, text="🔑 Demo Accounts", bg='#F0F8FF', font=('Segoe UI', 12, 'bold')).pack(pady=10)
        tk.Label(demo, text="Customer: customer@demo.com / password123", bg='#F0F8FF',
                font=('Segoe UI', 9)).pack(pady=2)
        tk.Label(demo, text="Admin: admin@demo.com / admin123", bg='#F0F8FF',
                font=('Segoe UI', 9)).pack(pady=(2, 10))
    
    def show_register(self):
        for w in self.right.winfo_children(): w.destroy()
        
        canvas = tk.Canvas(self.right, bg=ModernStyle.BG_WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.right, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=ModernStyle.BG_WHITE)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        center = tk.Frame(scroll_frame, bg=ModernStyle.BG_WHITE)
        center.pack(pady=30, padx=50)
        
        tk.Label(center, text="Create Account", font=('Segoe UI', 24, 'bold'),
                bg=ModernStyle.BG_WHITE, fg=ModernStyle.TEXT_DARK).pack(pady=(0, 10))
        tk.Label(center, text="Join our e-commerce platform", font=('Segoe UI', 11),
                bg=ModernStyle.BG_WHITE, fg=ModernStyle.TEXT_LIGHT).pack(pady=(0, 30))
        
        def create_field(label):
            tk.Label(center, text=label, font=('Segoe UI', 9), bg=ModernStyle.BG_WHITE,
                    fg=ModernStyle.TEXT_LIGHT).pack(anchor='w')
            e = tk.Entry(center, font=('Segoe UI', 11), bg='#F8F9FA', relief='flat', bd=0,
                        show='●' if 'Password' in label else None)
            e.pack(fill='x', ipady=10, pady=(2,8))
            return e
        
        self.reg_name = create_field("Full Name *")
        self.reg_email = create_field("Email Address *")
        self.reg_phone = create_field("Phone Number")
        self.reg_address = create_field("Address")
        self.reg_password = create_field("Password *")
        self.reg_confirm = create_field("Confirm Password *")
        
        tk.Button(center, text="Create Account", command=self.do_register, bg=ModernStyle.SUCCESS,
                 fg=ModernStyle.TEXT_WHITE, font=('Segoe UI', 13, 'bold'), relief='flat',
                 cursor='hand2', width=30).pack(pady=25)
        tk.Button(center, text="← Back to Sign In", command=self.show_signin, bg=ModernStyle.BG_WHITE,
                 fg=ModernStyle.TEXT_LIGHT, font=('Segoe UI', 11), relief='flat', cursor='hand2').pack()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def do_signin(self):
        email = self.signin_email.get().strip()
        password = self.signin_password.get()
        role = self.role_var.get()
        
        if not email or not password:
            messagebox.showwarning("Validation", "Please enter email and password!")
            return
        
        password_hash = self.hash_password(password)
        
        try:
            if role == 'customer':
                self.cursor.execute("""
                    SELECT customer_id, name, email 
                    FROM customer 
                    WHERE email = %s AND password_hash = %s AND is_active = TRUE
                """, (email, password_hash))
                result = self.cursor.fetchone()
                
                if result:
                    self.user_role = 'customer'
                    self.user_id = result['customer_id']
                    self.user_name = result['name']
                    self.user_email = result['email']
                    self.launch_customer_app()
                else:
                    messagebox.showerror("Login Failed", "Invalid email or password!")
            else:
                self.cursor.execute("""
                    SELECT admin_id, email, role
                    FROM admin
                    WHERE email = %s AND password_hash = %s
                """, (email, password_hash))
                result = self.cursor.fetchone()
                
                if result:
                    self.user_role = 'admin'
                    self.user_id = result['admin_id']
                    self.user_email = result['email']
                    self.user_name = result['role'].replace('_', ' ').title()
                    # Note: last_login column doesn't exist in schema
                    # self.cursor.execute("UPDATE admin SET last_login = NOW() WHERE admin_id = %s", (self.user_id,))
                    # self.conn.commit()
                    self.launch_admin_app()
                else:
                    messagebox.showerror("Login Failed", "Invalid admin credentials!")
        except Exception as e:
            messagebox.showerror("Error", f"Login error:\n{e}")
    
    def do_register(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        phone = self.reg_phone.get().strip()
        address = self.reg_address.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if not all([name, email, password]):
            messagebox.showwarning("Validation", "Name, email, and password are required!")
            return
        if password != confirm:
            messagebox.showerror("Validation", "Passwords do not match!")
            return
        if len(password) < 6:
            messagebox.showwarning("Validation", "Password must be at least 6 characters!")
            return
        
        try:
            self.cursor.execute("SELECT email FROM customer WHERE email = %s", (email,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Email already registered!")
                return
            
            password_hash = self.hash_password(password)
            self.cursor.execute("""
                INSERT INTO customer (name, email, phone, address, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone, address, password_hash))
            self.conn.commit()
            
            messagebox.showinfo("Success!", f"Account created successfully!\n\nWelcome, {name}!")
            self.show_signin()
            self.signin_email.delete(0, tk.END)
            self.signin_email.insert(0, email)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed:\n{e}")
            self.conn.rollback()
    
    def launch_customer_app(self):
        self.root.destroy()
        customer_root = tk.Tk()
        from customer_gui import CustomerGUI
        app = CustomerGUI(customer_root, self.user_id, self.user_name, self.user_email, self.conn)
        customer_root.protocol("WM_DELETE_WINDOW", app.on_closing)
        customer_root.mainloop()
    
    def launch_admin_app(self):
        self.root.destroy()
        admin_root = tk.Tk()
        from admin_gui import AdminGUI
        app = AdminGUI(admin_root, self.user_id, self.user_name, self.user_email, self.conn)
        admin_root.protocol("WM_DELETE_WINDOW", app.on_closing)
        admin_root.mainloop()
    
    def run(self):
        self.root.mainloop()

def main():
    try:
        conn = mysql.connector.connect(
            host=DatabaseConfig.HOST,
            user=DatabaseConfig.USER,
            password=DatabaseConfig.PASSWORD,
            database=DatabaseConfig.DATABASE
        )
        cursor = conn.cursor()
        
        # Demo customer
        customer_hash = hashlib.sha256('password123'.encode()).hexdigest()
        try:
            cursor.execute("""
                INSERT INTO customer (name, email, phone, address, password_hash)
                VALUES ('Demo Customer', 'customer@demo.com', '+20123456789', 'Cairo, Egypt', %s)
            """, (customer_hash,))
            conn.commit()
        except: pass
        
        # Demo admin
        admin_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        try:
            cursor.execute("""
                INSERT INTO admin (email, password_hash, role)
                VALUES ('admin@demo.com', %s, 'super_admin')
            """, (admin_hash,))
            conn.commit()
        except: pass
        
        conn.close()
    except: pass
    
    app = AuthenticationApp()
    app.run()

if __name__ == "__main__":
    main()
