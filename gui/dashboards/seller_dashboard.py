"""
Seller Dashboard
Interface for sellers to manage products, inventory, and orders
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QTabWidget,
    QLineEdit, QComboBox, QMessageBox, QFrame, QTextEdit,
    QDoubleSpinBox, QSpinBox, QDialog, QFormLayout, QDialogButtonBox,
    QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
import logging
from backend.database import db
from gui.utils.theme import Theme

logger = logging.getLogger(__name__)


class SellerDashboard(QMainWindow):
    """Seller dashboard main window"""
    
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
        self.setWindowTitle("E-Commerce Platform - Seller Dashboard")
        self.setMinimumSize(1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)
        
        # Tabs
        self.tab_widget = QTabWidget()
        
        # Dashboard/Analytics tab
        self.tab_widget.addTab(self.create_analytics_tab(), "📊 Dashboard")
        
        # Products tab
        self.tab_widget.addTab(self.create_products_tab(), "📦 My Products")
        
        # Orders tab
        self.tab_widget.addTab(self.create_orders_tab(), "🛍️ Orders")
        
        # Inventory tab
        self.tab_widget.addTab(self.create_inventory_tab(), "📦 Inventory")
        
        main_layout.addWidget(self.tab_widget)
    
    def create_top_bar(self):
        """Create top bar"""
        top_bar = QFrame()
        top_bar.setMinimumHeight(70)
        
        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        title = QLabel("🏪 Seller Dashboard")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addStretch()
        
        user_label = QLabel(f"Seller: {self.user_data['first_name']} {self.user_data['last_name']}")
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
    
    def create_analytics_tab(self):
        """Create analytics dashboard"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Sales Analytics")
        title.setFont(QFont('Segoe UI', 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # KPI cards
        kpi_layout = QHBoxLayout()
        
        self.total_products_card = self.create_kpi_card("Total Products", "0")
        kpi_layout.addWidget(self.total_products_card)
        
        self.total_sales_card = self.create_kpi_card("Total Sales", "$0.00")
        kpi_layout.addWidget(self.total_sales_card)
        
        self.pending_orders_card = self.create_kpi_card("Pending Orders", "0")
        kpi_layout.addWidget(self.pending_orders_card)
        
        self.revenue_card = self.create_kpi_card("Revenue (COD)", "$0.00")
        kpi_layout.addWidget(self.revenue_card)
        
        layout.addLayout(kpi_layout)
        
        # Recent activity
        activity_label = QLabel("Recent Orders")
        activity_label.setFont(QFont('Segoe UI', 14, QFont.Weight.Bold))
        layout.addWidget(activity_label)
        
        self.recent_orders_table = QTableWidget()
        self.recent_orders_table.setColumnCount(5)
        self.recent_orders_table.setHorizontalHeaderLabels([
            "Order #", "Product", "Customer", "Amount", "Status"
        ])
        self.recent_orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.recent_orders_table)
        
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
        value_label.setObjectName("kpiValue")
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_label.setFont(value_font)
        frame_layout.addWidget(value_label)
        
        return frame
    
    def create_products_tab(self):
        """Create products management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with add button
        header_layout = QHBoxLayout()
        
        title = QLabel("My Products")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        add_product_btn = QPushButton("➕ Add New Product")
        add_product_btn.setProperty('class', 'success')
        add_product_btn.clicked.connect(self.add_product)
        header_layout.addWidget(add_product_btn)
        
        layout.addLayout(header_layout)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(7)
        self.products_table.setHorizontalHeaderLabels([
            "Product Name", "Category", "Price", "Stock", "Status", "Edit", "Delete"
        ])
        self.products_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.products_table.setAlternatingRowColors(True)
        
        # Make table responsive
        header = self.products_table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Product Name
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Category
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Price
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Stock
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Edit
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Delete
        self.products_table.setColumnWidth(5, 80)
        self.products_table.setColumnWidth(6, 80)
        
        layout.addWidget(self.products_table)
        
        return widget
    
    def create_orders_tab(self):
        """Create orders tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Orders for My Products")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
            "Order #", "Product", "Quantity", "Amount", "Status", "Payment", "Actions"
        ])
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.orders_table)
        
        return widget
    
    def create_inventory_tab(self):
        """Create inventory management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Inventory Management")
        title.setFont(QFont('Segoe UI', 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels([
            "Product", "Warehouse", "Quantity", "Reserved", "Available", "Update Stock"
        ])
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.inventory_table)
        
        return widget
    
    def load_data(self):
        """Load all data"""
        try:
            self.load_analytics()
            self.load_products()
            self.load_orders()
            self.load_inventory()
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def load_analytics(self):
        """Load analytics/KPIs"""
        try:
            # Total products
            query1 = "SELECT COUNT(*) as count FROM products WHERE seller_id = %s"
            result = db.execute_query(query1, (self.user_data['user_id'],), fetch_one=True)
            total_products = result['count'] if result else 0
            
            # Total sales and revenue
            query2 = """
                SELECT COUNT(DISTINCT oi.order_id) as order_count, 
                       SUM(oi.total_price) as revenue
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                WHERE oi.seller_id = %s AND o.order_status NOT IN ('CANCELLED', 'REFUNDED')
            """
            result = db.execute_query(query2, (self.user_data['user_id'],), fetch_one=True)
            total_sales = result['order_count'] if result and result['order_count'] else 0
            revenue = result['revenue'] if result and result['revenue'] else 0
            
            # Pending orders
            query3 = """
                SELECT COUNT(DISTINCT oi.order_id) as count
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                WHERE oi.seller_id = %s AND o.order_status IN ('PENDING', 'CONFIRMED')
            """
            result = db.execute_query(query3, (self.user_data['user_id'],), fetch_one=True)
            pending = result['count'] if result else 0
            
            # Update KPI cards
            self.total_products_card.findChildren(QLabel)[1].setText(str(total_products))
            self.total_sales_card.findChildren(QLabel)[1].setText(str(total_sales))
            self.pending_orders_card.findChildren(QLabel)[1].setText(str(pending))
            self.revenue_card.findChildren(QLabel)[1].setText(f"${revenue:.2f}")
            
            # Load recent orders
            query4 = """
                SELECT o.order_number, p.product_name, 
                       CONCAT(u.first_name, ' ', u.last_name) as customer,
                       oi.total_price, o.order_status
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                JOIN products p ON oi.product_id = p.product_id
                JOIN users u ON o.customer_id = u.user_id
                WHERE oi.seller_id = %s
                ORDER BY o.created_at DESC
                LIMIT 10
            """
            recent = db.execute_query(query4, (self.user_data['user_id'],)) or []
            
            self.recent_orders_table.setRowCount(len(recent))
            for row, order in enumerate(recent):
                self.recent_orders_table.setItem(row, 0, QTableWidgetItem(order['order_number']))
                self.recent_orders_table.setItem(row, 1, QTableWidgetItem(order['product_name']))
                self.recent_orders_table.setItem(row, 2, QTableWidgetItem(order['customer']))
                self.recent_orders_table.setItem(row, 3, QTableWidgetItem(f"${order['total_price']:.2f}"))
                self.recent_orders_table.setItem(row, 4, QTableWidgetItem(order['order_status']))
            
        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
    
    def load_products(self):
        """Load seller's products"""
        try:
            query = """
                SELECT p.product_id, p.product_name, c.category_name, p.final_price,
                       SUM(i.quantity) as stock, p.is_active
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE p.seller_id = %s
                GROUP BY p.product_id, p.product_name, c.category_name, p.final_price, p.is_active
            """
            products = db.execute_query(query, (self.user_data['user_id'],)) or []
            
            self.products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                self.products_table.setItem(row, 0, QTableWidgetItem(product['product_name']))
                self.products_table.setItem(row, 1, QTableWidgetItem(product['category_name'] or ''))
                self.products_table.setItem(row, 2, QTableWidgetItem(f"${product['final_price']:.2f}"))
                self.products_table.setItem(row, 3, QTableWidgetItem(str(product['stock'] or 0)))
                self.products_table.setItem(row, 4, QTableWidgetItem("Active" if product['is_active'] else "Inactive"))
                
                edit_btn = QPushButton("Edit")
                edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
                self.products_table.setCellWidget(row, 5, edit_btn)
                
                delete_btn = QPushButton("Delete")
                delete_btn.setProperty('class', 'danger')
                delete_btn.clicked.connect(lambda checked, p=product: self.delete_product(p))
                self.products_table.setCellWidget(row, 6, delete_btn)
            
        except Exception as e:
            logger.error(f"Error loading products: {e}")
    
    def load_orders(self):
        """Load orders for seller's products"""
        try:
            query = """
                SELECT o.order_number, p.product_name, oi.quantity, oi.total_price,
                       o.order_status, o.payment_status, oi.order_item_id
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.order_id
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.seller_id = %s
                ORDER BY o.created_at DESC
            """
            orders = db.execute_query(query, (self.user_data['user_id'],)) or []
            
            self.orders_table.setRowCount(len(orders))
            
            for row, order in enumerate(orders):
                self.orders_table.setItem(row, 0, QTableWidgetItem(order['order_number']))
                self.orders_table.setItem(row, 1, QTableWidgetItem(order['product_name']))
                self.orders_table.setItem(row, 2, QTableWidgetItem(str(order['quantity'])))
                self.orders_table.setItem(row, 3, QTableWidgetItem(f"${order['total_price']:.2f}"))
                self.orders_table.setItem(row, 4, QTableWidgetItem(order['order_status']))
                self.orders_table.setItem(row, 5, QTableWidgetItem(order['payment_status']))
                
                view_btn = QPushButton("View")
                view_btn.clicked.connect(lambda checked, o=order: self.view_order(o))
                self.orders_table.setCellWidget(row, 6, view_btn)
            
        except Exception as e:
            logger.error(f"Error loading orders: {e}")
    
    def load_inventory(self):
        """Load inventory"""
        try:
            query = """
                SELECT p.product_name, w.warehouse_name, i.quantity, 
                       i.reserved_quantity, i.available_quantity, i.inventory_id
                FROM inventory i
                JOIN products p ON i.product_id = p.product_id
                JOIN warehouses w ON i.warehouse_id = w.warehouse_id
                WHERE p.seller_id = %s
            """
            items = db.execute_query(query, (self.user_data['user_id'],)) or []
            
            self.inventory_table.setRowCount(len(items))
            
            for row, item in enumerate(items):
                self.inventory_table.setItem(row, 0, QTableWidgetItem(item['product_name']))
                self.inventory_table.setItem(row, 1, QTableWidgetItem(item['warehouse_name']))
                self.inventory_table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
                self.inventory_table.setItem(row, 3, QTableWidgetItem(str(item['reserved_quantity'])))
                self.inventory_table.setItem(row, 4, QTableWidgetItem(str(item['available_quantity'])))
                
                update_btn = QPushButton("Update")
                update_btn.clicked.connect(lambda checked, i=item: self.update_inventory(i))
                self.inventory_table.setCellWidget(row, 5, update_btn)
            
        except Exception as e:
            logger.error(f"Error loading inventory: {e}")
    
    def add_product(self):
        """Add new product"""
        QMessageBox.information(
            self,
            "Add Product",
            "Add product dialog would collect:\n"
            "- Product name\n"
            "- Category\n"
            "- Brand\n"
            "- Price\n"
            "- Description\n"
            "- Initial stock\n\n"
            "This is a demonstration of the interface."
        )
    
    def edit_product(self, product):
        """Edit product"""
        QMessageBox.information(self, "Edit Product", f"Editing: {product['product_name']}")
    
    def delete_product(self, product):
        """Delete product"""
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete {product["product_name"]}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                query = "UPDATE products SET is_active = FALSE WHERE product_id = %s"
                db.execute_update(query, (product['product_id'],))
                self.load_products()
                QMessageBox.information(self, "Success", "Product deactivated")
            except Exception as e:
                logger.error(f"Error deleting product: {e}")
                QMessageBox.warning(self, "Error", "Failed to delete product")
    
    def view_order(self, order):
        """View order details"""
        QMessageBox.information(
            self,
            f"Order {order['order_number']}",
            f"Product: {order['product_name']}\n"
            f"Quantity: {order['quantity']}\n"
            f"Amount: ${order['total_price']:.2f}\n"
            f"Status: {order['order_status']}\n"
            f"Payment: {order['payment_status']}"
        )
    
    def update_inventory(self, item):
        """Update inventory"""
        QMessageBox.information(
            self,
            "Update Inventory",
            f"Update stock for {item['product_name']}\n"
            f"Current: {item['quantity']}\n"
            f"Available: {item['available_quantity']}"
        )
    
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
