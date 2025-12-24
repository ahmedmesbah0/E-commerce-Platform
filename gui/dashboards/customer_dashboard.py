"""
Customer Dashboard
Main interface for customer role with product browsing, cart, orders
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QTabWidget,
    QLineEdit, QComboBox, QMessageBox, QScrollArea, QGridLayout,
    QFrame, QSpinBox, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import logging
from backend.database import db
from backend.utils.security import SecurityUtils
from gui.utils.theme import Theme

logger = logging.getLogger(__name__)


class CustomerDashboard(QMainWindow):
    """Customer dashboard main window"""
    
    logout_requested = pyqtSignal()
    
    def __init__(self, user_data, token, theme='dark'):
        super().__init__()
        self.user_data = user_data
        self.token = token
        self.current_theme = theme
        self.cart_items = []
        
        self.init_ui()
        self.apply_theme()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle(f"E-Commerce Platform - Customer Dashboard")
        self.setMinimumSize(1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)
        
        # Main content area with tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Products tab
        products_tab = self.create_products_tab()
        self.tab_widget.addTab(products_tab, "🛍️ Browse Products")
        
        # Cart tab
        cart_tab = self.create_cart_tab()
        self.tab_widget.addTab(cart_tab, f"🛒 Cart ({len(self.cart_items)})")
        
        # Orders tab
        orders_tab = self.create_orders_tab()
        self.tab_widget.addTab(orders_tab, "📦 My Orders")
        
        # Wishlist tab
        wishlist_tab = self.create_wishlist_tab()
        self.tab_widget.addTab(wishlist_tab, "❤️ Wishlist")
        
        # Profile tab
        profile_tab = self.create_profile_tab()
        self.tab_widget.addTab(profile_tab, "👤 Profile")
        
        main_layout.addWidget(self.tab_widget)
    
    def create_top_bar(self):
        """Create top navigation bar"""
        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar.setMinimumHeight(70)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Logo/Title
        title_label = QLabel("🛍️ E-Commerce Platform")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # User info
        user_label = QLabel(f"Welcome, {self.user_data['first_name']} {self.user_data['last_name']}")
        user_font = QFont()
        user_font.setPointSize(11)
        user_label.setFont(user_font)
        layout.addWidget(user_label)
        
        # Loyalty points (load from DB)
        self.points_label = QLabel("Points: Loading...")
        layout.addWidget(self.points_label)
        
        # Theme toggle
        self.theme_btn = QPushButton("☀️" if self.current_theme == 'dark' else "🌙")
        self.theme_btn.setProperty('class', 'secondary')
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setProperty('class', 'danger')
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        return top_bar
    
    def create_products_tab(self):
        """Create products browsing tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Search and filter bar
        filter_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search products...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.filter_products)
        filter_layout.addWidget(self.search_input)
        
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.setMinimumWidth(150)
        self.category_filter.currentTextChanged.connect(self.filter_products)
        filter_layout.addWidget(self.category_filter)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Price: Low to High", "Price: High to Low", "Name A-Z", "Newest"])
        self.sort_combo.currentTextChanged.connect(self.filter_products)
        filter_layout.addWidget(self.sort_combo)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(7)
        self.products_table.setHorizontalHeaderLabels([
            "Product Name", "Category", "Brand", "Price", "Stock", "Actions", "Wishlist"
        ])
        self.products_table.horizontalHeader().setStretchLastSection(False)
        self.products_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.products_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.products_table.setAlternatingRowColors(True)
        
        # Set column stretch to make responsive
        header = self.products_table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)  # Product Name
        header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)  # Category
        header.setSectionResizeMode(2, header.ResizeMode.ResizeToContents)  # Brand
        header.setSectionResizeMode(3, header.ResizeMode.ResizeToContents)  # Price
        header.setSectionResizeMode(4, header.ResizeMode.ResizeToContents)  # Stock
        header.setSectionResizeMode(5, header.ResizeMode.Fixed)  # Actions
        header.setSectionResizeMode(6, header.ResizeMode.Fixed)  # Wishlist
        self.products_table.setColumnWidth(5, 120)
        self.products_table.setColumnWidth(6, 80)
        
        layout.addWidget(self.products_table)
        
        return widget
    
    def create_cart_tab(self):
        """Create shopping cart tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Cart table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(6)
        self.cart_table.setHorizontalHeaderLabels([
            "Product", "Price", "Quantity", "Subtotal", "Remove", "Details"
        ])
        self.cart_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.cart_table)
        
        # Cart summary
        summary_layout = QHBoxLayout()
        summary_layout.addStretch()
        
        summary_frame = QFrame()
        summary_frame.setMinimumWidth(300)
        summary_vlayout = QVBoxLayout(summary_frame)
        
        self.subtotal_label = QLabel("Subtotal: $0.00")
        self.subtotal_label.setFont(QFont('Segoe UI', 12))
        summary_vlayout.addWidget(self.subtotal_label)
        
        self.tax_label = QLabel("Tax (10%): $0.00")
        summary_vlayout.addWidget(self.tax_label)
        
        self.shipping_label = QLabel("Shipping: $5.00")
        summary_vlayout.addWidget(self.shipping_label)
        
        self.total_label = QLabel("Total: $0.00")
        total_font = QFont('Segoe UI', 14, QFont.Weight.Bold)
        self.total_label.setFont(total_font)
        summary_vlayout.addWidget(self.total_label)
        
        checkout_btn = QPushButton("Proceed to Checkout (COD)")
        checkout_btn.setProperty('class', 'success')
        checkout_btn.setMinimumHeight(45)
        checkout_btn.clicked.connect(self.checkout)
        summary_vlayout.addWidget(checkout_btn)
        
        summary_layout.addWidget(summary_frame)
        layout.addLayout(summary_layout)
        
        return widget
    
    def create_orders_tab(self):
        """Create orders history tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Order History")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Orders table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
            "Order #", "Date", "Items", "Total", "Status", "Payment", "Actions"
        ])
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.orders_table.setAlternatingRowColors(True)
        layout.addWidget(self.orders_table)
        
        return widget
    
    def create_wishlist_tab(self):
        """Create wishlist tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("My Wishlist")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.wishlist_table = QTableWidget()
        self.wishlist_table.setColumnCount(5)
        self.wishlist_table.setHorizontalHeaderLabels([
            "Product", "Price", "Stock", "Add to Cart", "Remove"
        ])
        self.wishlist_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.wishlist_table)
        
        return widget
    
    def create_profile_tab(self):
        """Create profile/account tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Profile info
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        
        title = QLabel("Account Information")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        info_layout.addWidget(title)
        
        info_layout.addWidget(QLabel(f"Name: {self.user_data['first_name']} {self.user_data['last_name']}"))
        info_layout.addWidget(QLabel(f"Email: {self.user_data['email']}"))
        info_layout.addWidget(QLabel(f"Username: {self.user_data['username']}"))
        
        self.loyalty_info_label = QLabel("Loyalty Tier: Loading...")
        info_layout.addWidget(self.loyalty_info_label)
        
        info_layout.addStretch()
        layout.addWidget(info_frame)
        
        return widget
    
    def load_data(self):
        """Load all necessary data from database"""
        try:
            # Load products
            self.load_products()
            
            # Load categories for filter
            self.load_categories()
            
            # Load loyalty points
            self.load_loyalty_points()
            
            # Load orders
            self.load_orders()
            
            # Load wishlist
            self.load_wishlist()
            
            # Load cart from database
            self.load_cart()
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            QMessageBox.warning(self, "Error", "Failed to load some data from database")
    
    def load_products(self):
        """Load products from database"""
        try:
            query = """
                SELECT p.product_id, p.product_name, c.category_name, b.brand_name,
                       p.final_price, SUM(i.available_quantity) as stock
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN brands b ON p.brand_id = b.brand_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.is_active = TRUE
                GROUP BY p.product_id, p.product_name, c.category_name, b.brand_name, p.final_price
                ORDER BY p.product_name
            """
            self.all_products = db.execute_query(query) or []
            self.display_products(self.all_products)
            
        except Exception as e:
            logger.error(f"Error loading products: {e}")
    
    def display_products(self, products):
        """Display products in table"""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(product['product_name']))
            self.products_table.setItem(row, 1, QTableWidgetItem(product['category_name'] or ''))
            self.products_table.setItem(row, 2, QTableWidgetItem(product['brand_name'] or ''))
            self.products_table.setItem(row, 3, QTableWidgetItem(f"${product['final_price']:.2f}"))
            
            stock = product['stock'] or 0
            stock_item = QTableWidgetItem(f"{stock}" if stock > 0 else "Out of Stock")
            self.products_table.setItem(row, 4, stock_item)
            
            # Add to cart button
            add_btn = QPushButton("Add to Cart")
            add_btn.setProperty('class', 'success')
            add_btn.setEnabled(stock > 0)
            add_btn.clicked.connect(lambda checked, p=product: self.add_to_cart(p))
            self.products_table.setCellWidget(row, 5, add_btn)
            
            # Add to wishlist button
            wish_btn = QPushButton("♥")
            wish_btn.setFixedWidth(60)
            wish_btn.clicked.connect(lambda checked, p=product: self.add_to_wishlist(p))
            self.products_table.setCellWidget(row, 6, wish_btn)
    
    def load_categories(self):
        """Load categories for filter"""
        try:
            query = "SELECT category_name FROM categories WHERE is_active = TRUE ORDER BY category_name"
            categories = db.execute_query(query) or []
            
            for cat in categories:
                self.category_filter.addItem(cat['category_name'])
                
        except Exception as e:
            logger.error(f"Error loading categories: {e}")
    
    def load_loyalty_points(self):
        """Load customer loyalty points"""
        try:
            query = """
                SELECT cl.current_points, cl.lifetime_points, lt.tier_name
                FROM customer_loyalty cl
                LEFT JOIN loyalty_tiers lt ON cl.tier_id = lt.tier_id
                WHERE cl.customer_id = %s
            """
            result = db.execute_query(query, (self.user_data['user_id'],), fetch_one=True)
            
            if result:
                self.points_label.setText(f"💎 {result['current_points']} Points")
                self.loyalty_info_label.setText(
                    f"Loyalty Tier: {result['tier_name']}\n"
                    f"Current Points: {result['current_points']}\n"
                    f"Lifetime Points: {result['lifetime_points']}"
                )
            else:
                self.points_label.setText("💎 0 Points")
                
        except Exception as e:
            logger.error(f"Error loading loyalty points: {e}")
    
    def load_orders(self):
        """Load customer orders"""
        try:
            query = """
                SELECT o.order_id, o.order_number, o.created_at, o.total_amount,
                       o.order_status, o.payment_status,
                       COUNT(oi.order_item_id) as item_count
                FROM orders o
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.customer_id = %s
                GROUP BY o.order_id, o.order_number, o.created_at, o.total_amount,
                         o.order_status, o.payment_status
                ORDER BY o.created_at DESC
            """
            orders = db.execute_query(query, (self.user_data['user_id'],)) or []
            
            self.orders_table.setRowCount(len(orders))
            
            for row, order in enumerate(orders):
                self.orders_table.setItem(row, 0, QTableWidgetItem(order['order_number']))
                self.orders_table.setItem(row, 1, QTableWidgetItem(str(order['created_at'])[:10]))
                self.orders_table.setItem(row, 2, QTableWidgetItem(str(order['item_count'])))
                self.orders_table.setItem(row, 3, QTableWidgetItem(f"${order['total_amount']:.2f}"))
                self.orders_table.setItem(row, 4, QTableWidgetItem(order['order_status']))
                self.orders_table.setItem(row, 5, QTableWidgetItem(order['payment_status']))
                
                view_btn = QPushButton("View Details")
                view_btn.clicked.connect(lambda checked, o=order: self.view_order_details(o))
                self.orders_table.setCellWidget(row, 6, view_btn)
                
        except Exception as e:
            logger.error(f"Error loading orders: {e}")
    
    def load_wishlist(self):
        """Load wishlist items"""
        try:
            query = """
                SELECT p.product_id, p.product_name, p.final_price,
                       SUM(i.available_quantity) as stock
                FROM wishlists w
                JOIN products p ON w.product_id = p.product_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE w.customer_id = %s AND p.is_active = TRUE
                GROUP BY p.product_id, p.product_name, p.final_price
            """
            items = db.execute_query(query, (self.user_data['user_id'],)) or []
            
            self.wishlist_table.setRowCount(len(items))
            
            for row, item in enumerate(items):
                self.wishlist_table.setItem(row, 0, QTableWidgetItem(item['product_name']))
                self.wishlist_table.setItem(row, 1, QTableWidgetItem(f"${item['final_price']:.2f}"))
                
                stock = item['stock'] or 0
                self.wishlist_table.setItem(row, 2, QTableWidgetItem(f"{stock}" if stock > 0 else "Out of Stock"))
                
                add_btn = QPushButton("Add to Cart")
                add_btn.setEnabled(stock > 0)
                add_btn.clicked.connect(lambda checked, i=item: self.add_to_cart(i))
                self.wishlist_table.setCellWidget(row, 3, add_btn)
                
                remove_btn = QPushButton("Remove")
                remove_btn.setProperty('class', 'danger')
                remove_btn.clicked.connect(lambda checked, i=item: self.remove_from_wishlist(i))
                self.wishlist_table.setCellWidget(row, 4, remove_btn)
                
        except Exception as e:
            logger.error(f"Error loading wishlist: {e}")
    
    def load_cart(self):
        """Load cart from database"""
        try:
            query = """
                SELECT sc.cart_id, sc.product_id, p.product_name, p.final_price, sc.quantity
                FROM shopping_cart sc
                JOIN products p ON sc.product_id = p.product_id
                WHERE sc.customer_id = %s
            """
            self.cart_items = db.execute_query(query, (self.user_data['user_id'],)) or []
            self.update_cart_display()
            
        except Exception as e:
            logger.error(f"Error loading cart: {e}")
    
    def filter_products(self):
        """Filter products based on search and category"""
        search_text = self.search_input.text().lower()
        category = self.category_filter.currentText()
        
        filtered = [p for p in self.all_products
                   if (search_text in p['product_name'].lower()) and
                      (category == "All Categories" or p['category_name'] == category)]
        
        self.display_products(filtered)
    
    def add_to_cart(self, product):
        """Add product to cart"""
        try:
            query = """
                INSERT INTO shopping_cart (customer_id, product_id, quantity)
                VALUES (%s, %s, 1)
                ON DUPLICATE KEY UPDATE quantity = quantity + 1
            """
            db.execute_update(query, (self.user_data['user_id'], product['product_id']))
            
            QMessageBox.information(self, "Success", f"Added {product['product_name']} to cart")
            self.load_cart()
            
        except Exception as e:
            logger.error(f"Error adding to cart: {e}")
            QMessageBox.warning(self, "Error", "Failed to add item to cart")
    
    def add_to_wishlist(self, product):
        """Add product to wishlist"""
        try:
            query = """
                INSERT IGNORE INTO wishlists (customer_id, product_id)
                VALUES (%s, %s)
            """
            db.execute_update(query, (self.user_data['user_id'], product['product_id']))
            
            QMessageBox.information(self, "Success", "Added to wishlist")
            self.load_wishlist()
            
        except Exception as e:
            logger.error(f"Error adding to wishlist: {e}")
    
    def remove_from_wishlist(self, item):
        """Remove item from wishlist"""
        try:
            query = "DELETE FROM wishlists WHERE customer_id = %s AND product_id = %s"
            db.execute_update(query, (self.user_data['user_id'], item['product_id']))
            
            self.load_wishlist()
            
        except Exception as e:
            logger.error(f"Error removing from wishlist: {e}")
    
    def update_cart_display(self):
        """Update cart table and summary"""
        self.cart_table.setRowCount(len(self.cart_items))
        
        subtotal = 0.0  # Use float for calculations
        
        for row, item in enumerate(self.cart_items):
            self.cart_table.setItem(row, 0, QTableWidgetItem(item['product_name']))
            self.cart_table.setItem(row, 1, QTableWidgetItem(f"${float(item['final_price']):.2f}"))
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
            
            # Convert Decimal to float for calculation
            item_total = float(item['final_price']) * int(item['quantity'])
            subtotal += item_total
            self.cart_table.setItem(row, 3, QTableWidgetItem(f"${item_total:.2f}"))
            
            remove_btn = QPushButton("Remove")
            remove_btn.setProperty('class', 'danger')
            remove_btn.clicked.connect(lambda checked, i=item: self.remove_from_cart(i))
            self.cart_table.setCellWidget(row, 4, remove_btn)
            
            details_btn = QPushButton("Details")
            details_btn.clicked.connect(lambda checked, i=item: self.show_product_details(i))
            self.cart_table.setCellWidget(row, 5, details_btn)
        
        # Update summary
        tax = subtotal * 0.10
        shipping = 5.00
        total = subtotal + tax + shipping
        
        self.subtotal_label.setText(f"Subtotal: ${subtotal:.2f}")
        self.tax_label.setText(f"Tax (10%): ${tax:.2f}")
        self.total_label.setText(f"Total: ${total:.2f}")
        
        # Update cart tab badge
        self.tab_widget.setTabText(1, f"🛒 Cart ({len(self.cart_items)})")
    
    def remove_from_cart(self, item):
        """Remove item from cart"""
        try:
            query = "DELETE FROM shopping_cart WHERE cart_id = %s"
            db.execute_update(query, (item['cart_id'],))
            
            self.load_cart()
            
        except Exception as e:
            logger.error(f"Error removing from cart: {e}")
    
    def checkout(self):
        """Process checkout"""
        if not self.cart_items:
            QMessageBox.warning(self, "Empty Cart", "Your cart is empty")
            return
        
        QMessageBox.information(
            self,
            "Checkout",
            "⚠️ Checkout functionality requires complete order service implementation.\n\n"
            "This would normally:\n"
            "1. Collect shipping address\n"
            "2. Apply coupons\n"
            "3. Create order with COD payment\n"
            "4. Reserve inventory\n"
            "5. Generate tracking number\n\n"
            "For this demo, orders can be viewed in the Orders tab."
        )
    
    def view_order_details(self, order):
        """View order details"""
        QMessageBox.information(
            self,
            f"Order {order['order_number']}",
            f"Order ID: {order['order_number']}\n"
            f"Date: {order['created_at']}\n"
            f"Items: {order['item_count']}\n"
            f"Total: ${order['total_amount']:.2f}\n"
            f"Status: {order['order_status']}\n"
            f"Payment: {order['payment_status']}"
        )
    
    def show_product_details(self, product):
        """Show product details"""
        QMessageBox.information(
            self,
            product['product_name'],
            f"Product: {product['product_name']}\n"
            f"Price: ${product['final_price']:.2f}\n"
            f"Quantity: {product['quantity']}"
        )
    
    def toggle_theme(self):
        """Toggle theme"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme_btn.setText("🌙" if self.current_theme == 'light' else "☀️")
        self.apply_theme()
    
    def apply_theme(self):
        """Apply current theme"""
        if self.current_theme == 'dark':
            self.setStyleSheet(Theme.get_dark_stylesheet())
        else:
            self.setStyleSheet(Theme.get_light_stylesheet())
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            'Confirm Logout',
            'Are you sure you want to logout?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            from backend.services.auth_service import AuthService
            AuthService.logout(self.token)
            self.logout_requested.emit()
            self.close()
