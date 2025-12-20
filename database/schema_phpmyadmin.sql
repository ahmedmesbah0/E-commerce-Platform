-- =====================================================
-- E-COMMERCE DATABASE - phpMyAdmin Compatible Schema
-- Academic Project - Database Management Systems
-- =====================================================
-- Based on: E-Commerce_updated3-dbms.drawio
-- Created for: Academic Submission
-- Compatible with: phpMyAdmin / MySQL 8.0+
-- =====================================================

DROP DATABASE IF EXISTS ecommerce_db;
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ecommerce_db;

-- =====================================================
-- TABLE 1: CUSTOMER
-- Purpose: Store customer account information
-- =====================================================
CREATE TABLE customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    password_hash VARCHAR(255) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    loyalty_points INT DEFAULT 0,
    loyalty_tier ENUM('Bronze', 'Silver', 'Gold', 'Platinum') DEFAULT 'Bronze',
    INDEX idx_customer_email (email),
    INDEX idx_customer_name (name)
) ENGINE=InnoDB COMMENT='Customer account information';

-- =====================================================
-- TABLE 2: CATEGORY
-- Purpose: Product categorization hierarchy
-- =====================================================
CREATE TABLE category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    parent_category_id INT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_category_id) REFERENCES category(category_id) ON DELETE SET NULL,
    INDEX idx_category_name (name)
) ENGINE=InnoDB COMMENT='Product categories with hierarchy support';

-- =====================================================
-- TABLE 3: PRODUCT
-- Purpose: Product catalog
-- =====================================================
CREATE TABLE product (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    category_id INT,
    image_url VARCHAR(255),
    weight DECIMAL(8, 2) COMMENT 'Weight in kg',
    dimensions VARCHAR(50) COMMENT 'Length x Width x Height',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE SET NULL,
    INDEX idx_product_name (name),
    INDEX idx_product_category (category_id),
    INDEX idx_product_price (price)
) ENGINE=InnoDB COMMENT='Product catalog';

-- =====================================================
-- TABLE 4: WAREHOUSE
-- Purpose: Warehouse locations for inventory
-- =====================================================
CREATE TABLE warehouse (
    warehouse_id INT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(200) NOT NULL,
    capacity INT,
    manager_name VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Warehouse locations';

-- =====================================================
-- TABLE 5: INVENTORY
-- Purpose: Track product stock levels by warehouse
-- =====================================================
CREATE TABLE inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    reorder_level INT DEFAULT 10,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id) ON DELETE CASCADE,
    UNIQUE KEY unique_product_warehouse (product_id, warehouse_id),
    INDEX idx_inventory_product (product_id),
    INDEX idx_inventory_warehouse (warehouse_id)
) ENGINE=InnoDB COMMENT='Product inventory by warehouse';

-- =====================================================
-- TABLE 6: SHIPPING_ADDRESS
-- Purpose: Customer shipping addresses
-- =====================================================
CREATE TABLE shipping_address (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    address_label VARCHAR(50) COMMENT 'e.g., Home, Office',
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'Egypt',
    is_default BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    INDEX idx_shipping_customer (customer_id)
) ENGINE=InnoDB COMMENT='Customer shipping addresses';

-- =====================================================
-- TABLE 7: ORDER
-- Purpose: Customer orders
-- =====================================================
CREATE TABLE `order` (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded') DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL CHECK (total_amount >= 0),
    shipping_cost DECIMAL(8, 2) DEFAULT 0,
    tax_amount DECIMAL(8, 2) DEFAULT 0,
    shipping_address_id INT,
    payment_method ENUM('credit_card', 'paypal', 'cash_on_delivery') DEFAULT 'cash_on_delivery',
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (shipping_address_id) REFERENCES shipping_address(address_id) ON DELETE SET NULL,
    INDEX idx_order_customer (customer_id),
    INDEX idx_order_date (order_date),
    INDEX idx_order_status (status)
) ENGINE=InnoDB COMMENT='Customer orders';

-- =====================================================
-- TABLE 8: ORDER_ITEM
-- Purpose: Line items in orders
-- =====================================================
CREATE TABLE order_item (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE RESTRICT,
    INDEX idx_orderitem_order (order_id),
    INDEX idx_orderitem_product (product_id)
) ENGINE=InnoDB COMMENT='Order line items';

-- =====================================================
-- TABLE 9: PAYMENT
-- Purpose: Payment transaction records
-- =====================================================
CREATE TABLE payment (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    payment_method ENUM('credit_card', 'paypal', 'cash_on_delivery') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    transaction_id VARCHAR(100),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE CASCADE,
    INDEX idx_payment_order (order_id),
    INDEX idx_payment_status (payment_status)
) ENGINE=InnoDB COMMENT='Payment transactions';

-- =====================================================
-- TABLE 10: SHIPPING_PROVIDER
-- Purpose: Delivery companies
-- =====================================================
CREATE TABLE shipping_provider (
    provider_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(20),
    contact_email VARCHAR(100),
    tracking_url_template VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB COMMENT='Shipping/delivery companies';

-- =====================================================
-- TABLE 11: SHIPMENT
-- Purpose: Track order deliveries
-- =====================================================
CREATE TABLE shipment (
    shipment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    provider_id INT,
    tracking_number VARCHAR(100),
    shipped_date TIMESTAMP NULL,
    estimated_delivery TIMESTAMP NULL,
    actual_delivery TIMESTAMP NULL,
    status ENUM('preparing', 'shipped', 'in_transit', 'out_for_delivery', 'delivered', 'failed') DEFAULT 'preparing',
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES shipping_provider(provider_id) ON DELETE SET NULL,
    INDEX idx_shipment_order (order_id),
    INDEX idx_shipment_tracking (tracking_number)
) ENGINE=InnoDB COMMENT='Shipment tracking';

-- =====================================================
-- TABLE 12: CART
-- Purpose: Shopping cart items
-- =====================================================
CREATE TABLE cart (
    cart_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100) COMMENT 'For guest users',
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
    INDEX idx_cart_customer (customer_id),
    INDEX idx_cart_session (session_id)
) ENGINE=InnoDB COMMENT='Shopping cart items';

-- =====================================================
-- TABLE 13: WISHLIST
-- Purpose: Customer wishlists
-- =====================================================
CREATE TABLE wishlist (
    wishlist_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
    UNIQUE KEY unique_customer_product (customer_id, product_id),
    INDEX idx_wishlist_customer (customer_id)
) ENGINE=InnoDB COMMENT='Customer wishlists';

-- =====================================================
-- TABLE 14: REVIEW
-- Purpose: Product reviews and ratings
-- =====================================================
CREATE TABLE review (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title VARCHAR(200),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (product_id) REFERENCES product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    INDEX idx_review_product (product_id),
    INDEX idx_review_customer (customer_id),
    INDEX idx_review_rating (rating)
) ENGINE=InnoDB COMMENT='Product reviews';

-- =====================================================
-- TABLE 15: COUPON
-- Purpose: Discount coupons
-- =====================================================
CREATE TABLE coupon (
    coupon_id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    discount_type ENUM('percentage', 'fixed_amount') NOT NULL,
    discount_value DECIMAL(10, 2) NOT NULL,
    min_order_amount DECIMAL(10, 2) DEFAULT 0,
    max_discount_amount DECIMAL(10, 2),
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP NULL,
    usage_limit INT,
    times_used INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_coupon_code (code)
) ENGINE=InnoDB COMMENT='Discount coupons';

-- =====================================================
-- TABLE 16: ORDER_COUPON
-- Purpose: Track coupon usage in orders
-- =====================================================
CREATE TABLE order_coupon (
    order_coupon_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    coupon_id INT NOT NULL,
    discount_applied DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE CASCADE,
    FOREIGN KEY (coupon_id) REFERENCES coupon(coupon_id) ON DELETE RESTRICT,
    INDEX idx_ordercoupon_order (order_id)
) ENGINE=InnoDB COMMENT='Coupons applied to orders';

-- =====================================================
-- TABLE 17: ADMIN
-- Purpose: Administrator accounts
-- =====================================================
CREATE TABLE admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('super_admin', 'admin', 'inventory_manager', 'sales_rep') DEFAULT 'admin',
    permissions JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_admin_email (email)
) ENGINE=InnoDB COMMENT='Administrator accounts';

-- =====================================================
-- TABLE 18: ADMIN_ACTIVITY_LOG
-- Purpose: Track admin actions
-- =====================================================
CREATE TABLE admin_activity_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    table_affected VARCHAR(50),
    record_id INT,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE CASCADE,
    INDEX idx_log_admin (admin_id),
    INDEX idx_log_date (created_at)
) ENGINE=InnoDB COMMENT='Admin activity audit log';

-- =====================================================
-- TABLE 19: NOTIFICATION
-- Purpose: System notifications
-- =====================================================
CREATE TABLE notification (
    notification_id INT PRIMARY KEY AUTO_INCREMENT,
    type ENUM('LOW_STOCK', 'ORDER_PLACED', 'SHIPMENT_UPDATE', 'PAYMENT_RECEIVED', 'SYSTEM') NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_notification_type (type),
    INDEX idx_notification_read (is_read)
) ENGINE=InnoDB COMMENT='System notifications';

-- =====================================================
-- TABLE 20: LOYALTY_TRANSACTION
-- Purpose: Track loyalty points transactions
-- =====================================================
CREATE TABLE loyalty_transaction (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    points INT NOT NULL,
    transaction_type ENUM('earned', 'redeemed', 'expired') NOT NULL,
    order_id INT,
    description VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES `order`(order_id) ON DELETE SET NULL,
    INDEX idx_loyalty_customer (customer_id)
) ENGINE=InnoDB COMMENT='Loyalty points history';

-- =====================================================
-- END OF SCHEMA
-- Total Tables: 20
-- =====================================================
