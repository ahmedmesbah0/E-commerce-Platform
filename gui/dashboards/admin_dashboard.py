"""
Admin Dashboard
Full system administration interface
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QTabWidget,
    QLineEdit, QComboBox, QMessageBox, QFrame, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import logging
from backend.database import db
from gui.utils.theme import Theme

logger = logging.getLogger(__name__)


class AdminDashboard(QMainWindow):
    """Admin dashboard for system management"""
    
    logout_requested = pyqtSignal()
    
    def __init__(self, user_data, token, theme='dark'):
        super().__init__()
        self.user_data = user_data
        self.token = token
        self.current_theme = theme
        
        self.init_ui()
        self.apply_theme()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("E-Commerce Platform - Admin Dashboard")
        self.setMinimumSize(1400, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)
        
        # Tabs
        self.tab_widget = QTabWidget()
        
        self.tab_widget.addTab(self.create_overview_tab(), "📊 Overview")
        self.tab_widget.addTab(self.create_users_tab(), "👥 Users")
        self.tab_widget.addTab(self.create_products_tab(), "📦 Products")
        self.tab_widget.addTab(self.create_orders_tab(), "🛍️ Orders")
        self.tab_widget.addTab(self.create_categories_tab(), "🏷️ Categories")
        self.tab_widget.addTab(self.create_coupons_tab(), "🎟️ Coupons")
        self.tab_widget.addTab(self.create_logs_tab(), "📋 Audit Logs")
        
        main_layout.addWidget(self.tab_widget)
    
    def create_top_bar(self):
        """Create top bar"""
        top_bar = QFrame()
        top_bar.setMinimumHeight(70)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        title = QLabel("⚙️ Admin Dashboard")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addStretch()
        
        user_label = QLabel(f"Admin: {self.user_data['first_name']} {self.user_data['last_name']}")
        layout.addWidget(user_label)
        
        self.theme_btn = QPushButton("☀️" if self.current_theme == 'dark' else "🌙")
        self.theme_btn.setProperty('class', 'secondary')
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setProperty('class', 'danger')
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return top_bar
    
    def create_overview_tab(self):
        """Create system overview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("System Overview")
        title.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # KPI cards
        kpi_layout = QHBoxLayout()
        
        self.total_users_card = self.create_kpi_card("Total Users", "0")
        kpi_layout.addWidget(self.total_users_card)
        
        self.total_products_card = self.create_kpi_card("Total Products", "0")
        kpi_layout.addWidget(self.total_products_card)
        
        self.total_orders_card = self.create_kpi_card("Total Orders", "0")
        kpi_layout.addWidget(self.total_orders_card)
        
        self.total_revenue_card = self.create_kpi_card("Total Revenue", "$0.00")
        kpi_layout.addWidget(self.total_revenue_card)
        
        layout.addLayout(kpi_layout)
        
        # System stats
        stats_label = QLabel("System Statistics")
        stats_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        layout.addWidget(stats_label)
        
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.stats_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.stats_table)
        
        return widget
    
    def create_kpi_card(self, title, value):
        """Create KPI card"""
        frame = QFrame()
        frame.setMinimumHeight(100)
        frame_layout = QVBoxLayout(frame)
        
        title_label = QLabel(title)
        title_label.setFont(QFont('Segoe UI', 11))
        frame_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_label.setFont(value_font)
        frame_layout.addWidget(value_label)
        
        return frame
    
    def create_users_tab(self):
        """Create user management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("User Management")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_user_btn = QPushButton("➕ Add User")
        add_user_btn.setProperty('class', 'success')
        add_user_btn.clicked.connect(self.add_user)
        header_layout.addWidget(add_user_btn)
        
        layout.addLayout(header_layout)
        
        # Search
        search_layout = QHBoxLayout()
        self.user_search = QLineEdit()
        self.user_search.setPlaceholderText("Search users...")
        self.user_search.textChanged.connect(self.filter_users)
        search_layout.addWidget(self.user_search)
        
        role_filter = QComboBox()
        role_filter.addItems(["All Roles", "Customer", "Seller", "Admin", "Support Representative", 
                              "Manager", "Investor", "Supplier", "Delivery Partner", "Marketing Agent"])
        role_filter.currentTextChanged.connect(self.filter_users)
        search_layout.addWidget(role_filter)
        
        layout.addLayout(search_layout)
        
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(7)
        self.users_table.setHorizontalHeaderLabels([
            "Username", "Name", "Email", "Roles", "Status", "Edit", "Deactivate"
        ])
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Make table responsive
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Username
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Email
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Roles
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Edit
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Deactivate
        self.users_table.setColumnWidth(5, 80)
        self.users_table.setColumnWidth(6, 100)
        
        layout.addWidget(self.users_table)
        
        return widget
    
    def create_products_tab(self):
        """Create all products management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("All Products")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.admin_products_table = QTableWidget()
        self.admin_products_table.setColumnCount(7)
        self.admin_products_table.setHorizontalHeaderLabels([
            "Product", "Seller", "Category", "Price", "Stock", "Status", "Actions"
        ])
        self.admin_products_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.admin_products_table)
        
        return widget
    
    def create_orders_tab(self):
        """Create all orders tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("All Orders")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.admin_orders_table = QTableWidget()
        self.admin_orders_table.setColumnCount(7)
        self.admin_orders_table.setHorizontalHeaderLabels([
            "Order #", "Customer", "Date", "Total", "Status", "Payment", "Actions"
        ])
        self.admin_orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.admin_orders_table)
        
        return widget
    
    def create_categories_tab(self):
        """Create categories management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("Categories & Brands")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_category_btn = QPushButton("➕ Add Category")
        add_category_btn.clicked.connect(self.add_category)
        header_layout.addWidget(add_category_btn)
        
        add_brand_btn = QPushButton("➕ Add Brand")
        add_brand_btn.clicked.connect(self.add_brand)
        header_layout.addWidget(add_brand_btn)
        
        layout.addLayout(header_layout)
        
        # Split layout for categories and brands
        split_layout = QHBoxLayout()
        
        # Categories
        cat_widget = QWidget()
        cat_layout = QVBoxLayout(cat_widget)
        cat_label = QLabel("Categories")
        cat_label.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        cat_layout.addWidget(cat_label)
        
        self.categories_table = QTableWidget()
        self.categories_table.setColumnCount(4)
        self.categories_table.setHorizontalHeaderLabels(["Name", "Parent", "Active", "Actions"])
        self.categories_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        cat_layout.addWidget(self.categories_table)
        
        split_layout.addWidget(cat_widget)
        
        # Brands
        brand_widget = QWidget()
        brand_layout = QVBoxLayout(brand_widget)
        brand_label = QLabel("Brands")
        brand_label.setFont(QFont('Segoe UI', 12, QFont.Weight.Bold))
        brand_layout.addWidget(brand_label)
        
        self.brands_table = QTableWidget()
        self.brands_table.setColumnCount(3)
        self.brands_table.setHorizontalHeaderLabels(["Name", "Active", "Actions"])
        self.brands_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        brand_layout.addWidget(self.brands_table)
        
        split_layout.addWidget(brand_widget)
        
        layout.addLayout(split_layout)
        
        return widget
    
    def create_coupons_tab(self):
        """Create coupons management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("Coupon Management")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_coupon_btn = QPushButton("➕ Create Coupon")
        add_coupon_btn.setProperty('class', 'success')
        add_coupon_btn.clicked.connect(self.create_coupon)
        header_layout.addWidget(add_coupon_btn)
        
        layout.addLayout(header_layout)
        
        self.coupons_table = QTableWidget()
        self.coupons_table.setColumnCount(7)
        self.coupons_table.setHorizontalHeaderLabels([
            "Code", "Type", "Value", "Min Purchase", "Expires", "Active", "Actions"
        ])
        self.coupons_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.coupons_table)
        
        return widget
    
    def create_logs_tab(self):
        """Create audit logs tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Audit Logs")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(5)
        self.logs_table.setHorizontalHeaderLabels([
            "Timestamp", "User", "Action", "Resource", "Details"
        ])
        self.logs_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.logs_table)
        
        return widget
    
    def load_data(self):
        """Load all data"""
        try:
            self.load_overview()
            self.load_users()
            self.load_products()
            self.load_orders()
            self.load_categories()
            self.load_coupons()
            self.load_logs()
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def load_overview(self):
        """Load overview KPIs"""
        try:
            # Total users
            result = db.execute_query("SELECT COUNT(*) as count FROM users", fetch_one=True)
            total_users = result['count'] if result else 0
            
            # Total products
            result = db.execute_query("SELECT COUNT(*) as count FROM products WHERE is_active = TRUE", fetch_one=True)
            total_products = result['count'] if result else 0
            
            # Total orders
            result = db.execute_query("SELECT COUNT(*) as count FROM orders", fetch_one=True)
            total_orders = result['count'] if result else 0
            
            # Total revenue
            result = db.execute_query(
                "SELECT SUM(total_amount) as revenue FROM orders WHERE order_status = 'DELIVERED'",
                fetch_one=True
            )
            total_revenue = result['revenue'] if result and result['revenue'] else 0
            
            self.total_users_card.findChildren(QLabel)[1].setText(str(total_users))
            self.total_products_card.findChildren(QLabel)[1].setText(str(total_products))
            self.total_orders_card.findChildren(QLabel)[1].setText(str(total_orders))
            self.total_revenue_card.findChildren(QLabel)[1].setText(f"${total_revenue:.2f}")
            
            # System stats
            stats = [
                ("Active Customers", db.execute_query(
                    "SELECT COUNT(DISTINCT ur.user_id) as count FROM user_roles ur JOIN roles r ON ur.role_id = r.role_id WHERE r.role_name = 'Customer'",
                    fetch_one=True)['count']),
                ("Active Sellers", db.execute_query(
                    "SELECT COUNT(DISTINCT ur.user_id) as count FROM user_roles ur JOIN roles r ON ur.role_id = r.role_id WHERE r.role_name = 'Seller'",
                    fetch_one=True)['count']),
                ("Pending Orders", db.execute_query(
                    "SELECT COUNT(*) as count FROM orders WHERE order_status IN ('PENDING', 'CONFIRMED')",
                    fetch_one=True)['count']),
                ("Shipped Orders", db.execute_query(
                    "SELECT COUNT(*) as count FROM orders WHERE order_status = 'SHIPPED'",
                    fetch_one=True)['count']),
            ]
            
            self.stats_table.setRowCount(len(stats))
            for row, (metric, value) in enumerate(stats):
                self.stats_table.setItem(row, 0, QTableWidgetItem(metric))
                self.stats_table.setItem(row, 1, QTableWidgetItem(str(value)))
            
        except Exception as e:
            logger.error(f"Error loading overview: {e}")
    
    def load_users(self):
        """Load all users"""
        try:
            query = """
                SELECT u.user_id, u.username, CONCAT(u.first_name, ' ', u.last_name) as name,
                       u.email, u.is_active,
                       GROUP_CONCAT(r.role_name SEPARATOR ', ') as roles
                FROM users u
                LEFT JOIN user_roles ur ON u.user_id = ur.user_id
                LEFT JOIN roles r ON ur.role_id = r.role_id
                GROUP BY u.user_id, u.username, u.first_name, u.last_name, u.email, u.is_active
            """
            users = db.execute_query(query) or []
            
            self.users_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                self.users_table.setItem(row, 0, QTableWidgetItem(user['username']))
                self.users_table.setItem(row, 1, QTableWidgetItem(user['name']))
                self.users_table.setItem(row, 2, QTableWidgetItem(user['email']))
                self.users_table.setItem(row, 3, QTableWidgetItem(user['roles'] or ''))
                self.users_table.setItem(row, 4, QTableWidgetItem("Active" if user['is_active'] else "Inactive"))
                
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, u=user: self.edit_user(u))
                self.users_table.setCellWidget(row, 5, edit_btn)
                
                toggle_btn = QPushButton("Deactivate" if user['is_active'] else "Activate")
                toggle_btn.clicked.connect(lambda checked, u=user: self.toggle_user_status(u))
                self.users_table.setCellWidget(row, 6, toggle_btn)
            
        except Exception as e:
            logger.error(f"Error loading users: {e}")
    
    def load_products(self):
        """Load all products"""
        try:
            query = """
                SELECT p.product_id, p.product_name, CONCAT(u.first_name, ' ', u.last_name) as seller,
                       c.category_name, p.final_price, SUM(i.quantity) as stock, p.is_active
                FROM products p
                LEFT JOIN users u ON p.seller_id = u.user_id
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                GROUP BY p.product_id, p.product_name, u.first_name, u.last_name, c.category_name, p.final_price, p.is_active
                LIMIT 100
            """
            products = db.execute_query(query) or []
            
            self.admin_products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                self.admin_products_table.setItem(row, 0, QTableWidgetItem(product['product_name']))
                self.admin_products_table.setItem(row, 1, QTableWidgetItem(product['seller'] or ''))
                self.admin_products_table.setItem(row, 2, QTableWidgetItem(product['category_name'] or ''))
                self.admin_products_table.setItem(row, 3, QTableWidgetItem(f"${product['final_price']:.2f}"))
                self.admin_products_table.setItem(row, 4, QTableWidgetItem(str(product['stock'] or 0)))
                self.admin_products_table.setItem(row, 5, QTableWidgetItem("Active" if product['is_active'] else "Inactive"))
                
                view_btn = QPushButton("View")
                view_btn.clicked.connect(lambda checked, p=product: self.view_product(p))
                self.admin_products_table.setCellWidget(row, 6, view_btn)
            
        except Exception as e:
            logger.error(f"Error loading products: {e}")
    
    def load_orders(self):
        """Load all orders"""
        try:
            query = """
                SELECT o.order_number, CONCAT(u.first_name, ' ', u.last_name) as customer,
                       o.created_at, o.total_amount, o.order_status, o.payment_status
                FROM orders o
                JOIN users u ON o.customer_id = u.user_id
                ORDER BY o.created_at DESC
                LIMIT 100
            """
            orders = db.execute_query(query) or []
            
            self.admin_orders_table.setRowCount(len(orders))
            
            for row, order in enumerate(orders):
                self.admin_orders_table.setItem(row, 0, QTableWidgetItem(order['order_number']))
                self.admin_orders_table.setItem(row, 1, QTableWidgetItem(order['customer']))
                self.admin_orders_table.setItem(row, 2, QTableWidgetItem(str(order['created_at'])[:10]))
                self.admin_orders_table.setItem(row, 3, QTableWidgetItem(f"${order['total_amount']:.2f}"))
                self.admin_orders_table.setItem(row, 4, QTableWidgetItem(order['order_status']))
                self.admin_orders_table.setItem(row, 5, QTableWidgetItem(order['payment_status']))
                
                view_btn = QPushButton("View")
                view_btn.clicked.connect(lambda checked, o=order: self.view_order(o))
                self.admin_orders_table.setCellWidget(row, 6, view_btn)
            
        except Exception as e:
            logger.error(f"Error loading orders: {e}")
    
    def load_categories(self):
        """Load categories and brands"""
        try:
            # Categories
            cat_query = """
                SELECT c1.category_id, c1.category_name, c2.category_name as parent, c1.is_active
                FROM categories c1
                LEFT JOIN categories c2 ON c1.parent_category_id = c2.category_id
            """
            categories = db.execute_query(cat_query) or []
            
            self.categories_table.setRowCount(len(categories))
            for row, cat in enumerate(categories):
                self.categories_table.setItem(row, 0, QTableWidgetItem(cat['category_name']))
                self.categories_table.setItem(row, 1, QTableWidgetItem(cat['parent'] or 'Root'))
                self.categories_table.setItem(row, 2, QTableWidgetItem("Yes" if cat['is_active'] else "No"))
                
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, c=cat: self.edit_category(c))
                self.categories_table.setCellWidget(row, 3, edit_btn)
            
            # Brands
            brands = db.execute_query("SELECT * FROM brands") or []
            
            self.brands_table.setRowCount(len(brands))
            for row, brand in enumerate(brands):
                self.brands_table.setItem(row, 0, QTableWidgetItem(brand['brand_name']))
                self.brands_table.setItem(row, 1, QTableWidgetItem("Yes" if brand['is_active'] else "No"))
                
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, b=brand: self.edit_brand(b))
                self.brands_table.setCellWidget(row, 2, edit_btn)
            
        except Exception as e:
            logger.error(f"Error loading categories: {e}")
    
    def load_coupons(self):
        """Load coupons"""
        try:
            query =  "SELECT * FROM coupons ORDER BY created_at DESC"
            coupons = db.execute_query(query) or []
            
            self.coupons_table.setRowCount(len(coupons))
            
            for row, coupon in enumerate(coupons):
                self.coupons_table.setItem(row, 0, QTableWidgetItem(coupon['coupon_code']))
                self.coupons_table.setItem(row, 1, QTableWidgetItem(coupon['discount_type']))
                self.coupons_table.setItem(row, 2, QTableWidgetItem(str(coupon['discount_value'])))
                self.coupons_table.setItem(row, 3, QTableWidgetItem(f"${coupon['min_purchase_amount']:.2f}"))
                self.coupons_table.setItem(row, 4, QTableWidgetItem(str(coupon['valid_until'])[:10] if coupon['valid_until'] else 'N/A'))
                self.coupons_table.setItem(row, 5, QTableWidgetItem("Yes" if coupon['is_active'] else "No"))
                
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, c=coupon: self.edit_coupon(c))
                self.coupons_table.setCellWidget(row, 6, edit_btn)
            
        except Exception as e:
            logger.error(f"Error loading coupons: {e}")
    
    def load_logs(self):
        """Load audit logs"""
        try:
            query = """
                SELECT al.created_at, CONCAT(u.first_name, ' ', u.last_name) as user,
                       al.action, al.resource_type, al.resource_id
                FROM audit_log al
                LEFT JOIN users u ON al.user_id = u.user_id
                ORDER BY al.created_at DESC
                LIMIT 100
            """
            logs = db.execute_query(query) or []
            
            self.logs_table.setRowCount(len(logs))
            
            for row, log in enumerate(logs):
                self.logs_table.setItem(row, 0, QTableWidgetItem(str(log['created_at'])))
                self.logs_table.setItem(row, 1, QTableWidgetItem(log['user'] or 'System'))
                self.logs_table.setItem(row, 2, QTableWidgetItem(log['action']))
                self.logs_table.setItem(row, 3, QTableWidgetItem(log['resource_type']))
                self.logs_table.setItem(row, 4, QTableWidgetItem(f"ID: {log['resource_id']}" if log['resource_id'] else ''))
            
        except Exception as e:
            logger.error(f"Error loading logs: {e}")
    
    def filter_users(self):
        """Filter users table"""
        # Placeholder for search functionality
        pass
    
    def add_user(self):
        """Add new user"""
        QMessageBox.information(self, "Add User", "User creation dialog would appear here")
    
    def edit_user(self, user):
        """Edit user"""
        QMessageBox.information(self, "Edit User", f"Editing user: {user['username']}")
    
    def toggle_user_status(self, user):
        """Toggle user active status"""
        try:
            new_status = not user['is_active']
            query = "UPDATE users SET is_active = %s WHERE user_id = %s"
            db.execute_update(query, (new_status, user['user_id']))
            self.load_users()
        except Exception as e:
            logger.error(f"Error toggling user status: {e}")
    
    def view_product(self, product):
        """View product details"""
        QMessageBox.information(self, "Product Details", f"Product: {product['product_name']}")
    
    def view_order(self, order):
        """View order details"""
        QMessageBox.information(self, "Order Details", f"Order: {order['order_number']}")
    
    def add_category(self):
        """Add category"""
        QMessageBox.information(self, "Add Category", "Category creation dialog")
    
    def add_brand(self):
        """Add brand"""
        QMessageBox.information(self, "Add Brand", "Brand creation dialog")
    
    def edit_category(self, category):
        """Edit category"""
        QMessageBox.information(self, "Edit Category", f"Editing: {category['category_name']}")
    
    def edit_brand(self, brand):
        """Edit brand"""
        QMessageBox.information(self, "Edit Brand", f"Editing: {brand['brand_name']}")
    
    def create_coupon(self):
        """Create coupon"""
        QMessageBox.information(self, "Create Coupon", "Coupon creation dialog")
    
    def edit_coupon(self, coupon):
        """Edit coupon"""
        QMessageBox.information(self, "Edit Coupon", f"Editing: {coupon['coupon_code']}")
    
    def toggle_theme(self):
        """Toggle theme"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme_btn.setText("🌙" if self.current_theme == 'light' else "☀️")
        self.apply_theme()
    
    def apply_theme(self):
        """Apply theme"""
        if self.current_theme == 'dark':
            self.setStyleSheet(Theme.get_dark_stylesheet())
        else:
            self.setStyleSheet(Theme.get_light_stylesheet())
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self, 'Confirm Logout',
            'Are you sure you want to logout?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from backend.services.auth_service import AuthService
            AuthService.logout(self.token)
            self.logout_requested.emit()
            self.close()
