"""
Additional Tab Implementations for E-Commerce GUI
To be integrated into ecommerce_gui.py
"""

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
    self.shipments_tree = ttv.Treeview(frame, columns=('ID', 'Order', 'Tracking', 'Status', 'Est. Delivery'), show='headings')
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
