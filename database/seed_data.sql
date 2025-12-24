-- ============================================
-- Seed Data for All 9 User Roles & Demo Data
-- ============================================

USE ecommerce_db;

-- ============================================
-- 1. ROLES & PERMISSIONS
-- ============================================

INSERT INTO roles (role_name, description) VALUES
('Customer', 'End users who browse and purchase products'),
('Seller', 'Product vendors who manage inventory and fulfill orders'),
('Admin', 'System administrators with full access'),
('Support Representative', 'Customer support agents handling tickets'),
('Manager', 'Business managers overseeing operations'),
('Investor', 'Investors viewing financial reports and analytics'),
('Supplier', 'Suppliers providing products to warehouses'),
('Delivery Partner', 'Delivery personnel handling shipments'),
('Marketing Agent', 'Marketing professionals managing campaigns and referrals');

-- Permissions for Customers
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('view_products', 'product', 'read', 'View product catalog'),
('manage_cart', 'cart', 'write', 'Add/remove items from shopping cart'),
('place_order', 'order', 'create', 'Place new orders'),
('view_own_orders', 'order', 'read', 'View own order history'),
('write_reviews', 'review', 'create', 'Write product reviews'),
('create_tickets', 'ticket', 'create', 'Create support tickets'),
('view_wishlist', 'wishlist', 'read', 'View and manage wishlist');

-- Permissions for Sellers
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('manage_products', 'product', 'write', 'Create, update, delete own products'),
('manage_inventory', 'inventory', 'write', 'Update inventory levels'),
('view_seller_orders', 'order', 'read', 'View orders for own products'),
('update_order_status', 'order', 'update', 'Update order fulfillment status'),
('view_seller_analytics', 'analytics', 'read', 'View sales analytics');

-- Permissions for Admin
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('manage_users', 'user', 'write', 'Full user management'),
('manage_roles', 'role', 'write', 'Manage roles and permissions'),
('manage_categories', 'category', 'write', 'Manage product categories'),
('manage_coupons', 'coupon', 'write', 'Create and manage coupons'),
('view_all_orders', 'order', 'read', 'View all system orders'),
('view_audit_logs', 'audit', 'read', 'View system audit logs'),
('system_config', 'system', 'write', 'Modify system configuration');

-- Permissions for Support
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('view_all_tickets', 'ticket', 'read', 'View all support tickets'),
('manage_tickets', 'ticket', 'write', 'Respond to and manage tickets'),
('view_customer_orders', 'order', 'read', 'View customer order details for support');

-- Permissions for Manager
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('view_reports', 'report', 'read', 'View business reports'),
('view_analytics', 'analytics', 'read', 'View comprehensive analytics'),
('manage_employees', 'user', 'write', 'Manage employee accounts');

-- Permissions for Investor
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('view_financial_reports', 'report', 'read', 'View financial data and reports');

-- Permissions for Supplier
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('view_po', 'purchase_order', 'read', 'View purchase orders'),
('update_po_status', 'purchase_order', 'update', 'Update PO delivery status'),
('manage_supply_inventory', 'inventory', 'write', 'Update supplied inventory');

-- Permissions for Delivery Partner
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('view_assigned_shipments', 'shipment', 'read', 'View assigned shipments'),
('update_shipment_status', 'shipment', 'update', 'Update delivery status'),
('confirm_delivery', 'shipment', 'update', 'Confirm order delivery');

-- Permissions for Marketing Agent
INSERT INTO permissions (permission_name, resource, action, description) VALUES
('view_campaigns', 'campaign', 'read', 'View marketing campaigns'),
('manage_referrals', 'referral', 'write', 'Manage referral programs'),
('view_commissions', 'commission', 'read', 'View commission reports');

-- Assign permissions to roles
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM roles r
CROSS JOIN permissions p
WHERE 
    (r.role_name = 'Customer' AND p.resource IN ('product', 'cart', 'order', 'review', 'ticket', 'wishlist'))
    OR (r.role_name = 'Seller' AND p.resource IN ('product', 'inventory', 'order', 'analytics') AND p.permission_name LIKE '%seller%' OR p.permission_name = 'manage_products' OR p.permission_name = 'manage_inventory')
    OR (r.role_name = 'Admin' AND (p.permission_name LIKE '%manage%' OR p.permission_name LIKE 'view_all%' OR p.permission_name LIKE 'system%' OR p.permission_name = 'view_audit_logs'))
    OR (r.role_name = 'Support Representative' AND (p.permission_name LIKE '%ticket%' OR p.permission_name = 'view_customer_orders'))
    OR (r.role_name = 'Manager' AND p.permission_name IN ('view_reports', 'view_analytics', 'manage_employees'))
    OR (r.role_name = 'Investor' AND p.permission_name = 'view_financial_reports')
    OR (r.role_name = 'Supplier' AND p.resource = 'purchase_order' OR p.permission_name = 'manage_supply_inventory')
    OR (r.role_name = 'Delivery Partner' AND p.resource = 'shipment')
    OR (r.role_name = 'Marketing Agent' AND p.resource IN ('campaign', 'referral', 'commission'));

-- ============================================
-- 2. DEMO USERS (All passwords are 'Password123')
-- ============================================
-- Password hash for 'Password123' using bcrypt
-- $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i

INSERT INTO users (username, email, password_hash, first_name, last_name, phone, is_active) VALUES
('customer1', 'customer1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'John', 'Smith', '+1234567890', TRUE),
('customer2', 'customer2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Jane', 'Doe', '+1234567891', TRUE),
('seller1', 'seller1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Mike', 'Johnson', '+1234567892', TRUE),
('seller2', 'seller2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Sarah', 'Williams', '+1234567893', TRUE),
('admin1', 'admin1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Admin', 'User', '+1234567894', TRUE),
('support1', 'support1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Emily', 'Brown', '+1234567895', TRUE),
('manager1', 'manager1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'David', 'Miller', '+1234567896', TRUE),
('investor1', 'investor1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Robert', 'Davis', '+1234567897', TRUE),
('supplier1', 'supplier1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Lisa', 'Wilson', '+1234567898', TRUE),
('delivery1', 'delivery1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Tom', 'Anderson', '+1234567899', TRUE),
('delivery2', 'delivery2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Chris', 'Taylor', '+1234567800', TRUE),
('marketing1', 'marketing1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ztJkcYWPfF6i', 'Amanda', 'Martinez', '+1234567801', TRUE);

-- Assign roles to users
INSERT INTO user_roles (user_id, role_id)
SELECT u.user_id, r.role_id
FROM users u
CROSS JOIN roles r
WHERE 
    (u.username IN ('customer1', 'customer2') AND r.role_name = 'Customer')
    OR (u.username IN ('seller1', 'seller2') AND r.role_name = 'Seller')
    OR (u.username = 'admin1' AND r.role_name = 'Admin')
    OR (u.username = 'support1' AND r.role_name = 'Support Representative')
    OR (u.username = 'manager1' AND r.role_name = 'Manager')
    OR (u.username = 'investor1' AND r.role_name = 'Investor')
    OR (u.username = 'supplier1' AND r.role_name = 'Supplier')
    OR (u.username IN ('delivery1', 'delivery2') AND r.role_name = 'Delivery Partner')
    OR (u.username = 'marketing1' AND r.role_name = 'Marketing Agent');

-- ============================================
-- 3. CATEGORIES & BRANDS
-- ============================================

INSERT INTO categories (category_name, parent_category_id, description, is_active) VALUES
('Electronics', NULL, 'Electronic devices and gadgets', TRUE),
('Computers', 1, 'Laptops, desktops, and accessories', TRUE),
('Smartphones', 1, 'Mobile phones and accessories', TRUE),
('Home & Kitchen', NULL, 'Home appliances and kitchen items', TRUE),
('Clothing', NULL, 'Apparel and fashion', TRUE),
('Men Fashion', 5, 'Men clothing and accessories', TRUE),
('Women Fashion', 5, 'Women clothing and accessories', TRUE),
('Books', NULL, 'Physical and ebooks', TRUE),
('Sports', NULL, 'Sports equipment and gear', TRUE),
('Toys', NULL, 'Toys and games for children', TRUE);

INSERT INTO brands (brand_name, description, website, is_active) VALUES
('TechPro', 'Premium electronics brand', 'https://techpro.example.com', TRUE),
('SmartTech', 'Smartphone manufacturer', 'https://smarttech.example.com', TRUE),
('HomeComfort', 'Home appliance brand', 'https://homecomfort.example.com', TRUE),
('FashionHub', 'Trendy clothing brand', 'https://fashionhub.example.com', TRUE),
('BookWorld', 'Book publisher', 'https://bookworld.example.com', TRUE),
('SportGear', 'Sports equipment brand', 'https://sportgear.example.com', TRUE),
('ToyLand', 'Children toy manufacturer', 'https://toyland.example.com', TRUE),
('GenericBrand', 'Generic products', NULL, TRUE);

-- ============================================
-- 4. WAREHOUSES
-- ============================================

INSERT INTO warehouses (warehouse_name, address, city, state, country, postal_code, phone, is_active) VALUES
('Main Warehouse North', '123 Industrial Blvd', 'New York', 'NY', 'USA', '10001', '+1-212-555-0001', TRUE),
('Warehouse South', '456 Commerce St', 'Miami', 'FL', 'USA', '33101', '+1-305-555-0002', TRUE),
('Warehouse West', '789 Logistics Ave', 'Los Angeles', 'CA', 'USA', '90001', '+1-213-555-0003', TRUE);

-- ============================================
-- 5. PRODUCTS (50+ products)
-- ============================================

INSERT INTO products (seller_id, category_id, brand_id, product_name, description, base_price, discount_percentage, sku, is_active) VALUES
-- Electronics - Computers
((SELECT user_id FROM users WHERE username = 'seller1'), 2, 1, 'TechPro Laptop 15"', 'High-performance laptop with 16GB RAM', 1299.99, 10.00, 'TP-LP-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 2, 1, 'TechPro Desktop Pro', 'Gaming desktop with RGB', 1899.99, 5.00, 'TP-DT-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 2, 1, 'Wireless Mouse', 'Ergonomic wireless mouse', 29.99, 0.00, 'TP-MS-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 2, 1, 'Mechanical Keyboard', 'RGB mechanical keyboard', 99.99, 15.00, 'TP-KB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 2, 1, 'USB-C Hub', '7-in-1 USB-C adapter', 49.99, 0.00, 'TP-HB-001', TRUE),

-- Electronics - Smartphones
((SELECT user_id FROM users WHERE username = 'seller1'), 3, 2, 'SmartTech Pro X', 'Flagship smartphone 256GB', 999.99, 8.00, 'ST-PX-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 3, 2, 'SmartTech Lite', 'Budget-friendly smartphone', 399.99, 12.00, 'ST-LT-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 3, 2, 'Phone Case Premium', 'Protective phone case', 19.99, 0.00, 'ST-CS-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 3, 2, 'Screen Protector', 'Tempered glass screen protector', 9.99, 0.00, 'ST-SP-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 3, 2, 'Wireless Earbuds', 'Bluetooth earbuds with charging case', 79.99, 20.00, 'ST-WE-001', TRUE),

-- Home & Kitchen
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Coffee Maker Deluxe', 'Programmable coffee maker', 89.99, 10.00, 'HC-CM-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Blender Pro 2000', 'High-speed blender', 129.99, 15.00, 'HC-BL-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Air Fryer XL', 'Large capacity air fryer', 119.99, 5.00, 'HC-AF-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Cookware Set', '10-piece non-stick cookware', 199.99, 25.00, 'HC-CW-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Microwave Oven', '1000W microwave', 149.99, 0.00, 'HC-MW-001', TRUE),

-- Men Fashion
((SELECT user_id FROM users WHERE username = 'seller2'), 6, 4, 'Men Classic T-Shirt', '100% cotton t-shirt', 24.99, 0.00, 'FH-MT-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 6, 4, 'Men Jeans Slim Fit', 'Comfortable denim jeans', 59.99, 10.00, 'FH-MJ-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 6, 4, 'Men Casual Shirt', 'Long sleeve casual shirt', 39.99, 15.00, 'FH-MS-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 6, 4, 'Men Leather Belt', 'Genuine leather belt', 29.99, 0.00, 'FH-MB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 6, 4, 'Men Sneakers', 'Comfortable running sneakers', 79.99, 20.00, 'FH-MSN-001', TRUE),

-- Women Fashion
((SELECT user_id FROM users WHERE username = 'seller2'), 7, 4, 'Women Summer Dress', 'Floral print dress', 49.99, 10.00, 'FH-WD-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 7, 4, 'Women Blouse', 'Elegant office blouse', 34.99, 0.00, 'FH-WB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 7, 4, 'Women Jeans', 'High-waist skinny jeans', 54.99, 15.00, 'FH-WJ-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 7, 4, 'Women Handbag', 'Stylish leather handbag', 89.99, 20.00, 'FH-WHB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 7, 4, 'Women Heels', 'Comfortable high heels', 69.99, 10.00, 'FH-WH-001', TRUE),

-- Books
((SELECT user_id FROM users WHERE username = 'seller1'), 8, 5, 'Python Programming Guide', 'Comprehensive Python book', 39.99, 0.00, 'BW-PP-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 8, 5, 'Database Design Essentials', 'Database fundamentals', 44.99, 10.00, 'BW-DB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 8, 5, 'Web Development Mastery', 'Full-stack development guide', 49.99, 0.00, 'BW-WD-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 8, 5, 'Fiction Bestseller', 'Award-winning novel', 19.99, 5.00, 'BW-FB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 8, 5, 'Cookbook Delights', 'International recipes', 29.99, 0.00, 'BW-CB-001', TRUE),

-- Sports
((SELECT user_id FROM users WHERE username = 'seller2'), 9, 6, 'Yoga Mat Premium', 'Extra thick yoga mat', 34.99, 0.00, 'SG-YM-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 9, 6, 'Dumbbell Set', 'Adjustable dumbbells 20kg', 89.99, 10.00, 'SG-DB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 9, 6, 'Resistance Bands', 'Set of 5 resistance bands', 24.99, 15.00, 'SG-RB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 9, 6, 'Running Shoes Pro', 'Professional running shoes', 119.99, 20.00, 'SG-RS-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 9, 6, 'Water Bottle', 'Insulated sports bottle', 19.99, 0.00, 'SG-WB-001', TRUE),

-- Toys
((SELECT user_id FROM users WHERE username = 'seller1'), 10, 7, 'Building Blocks Set', '500-piece building set', 44.99, 10.00, 'TL-BB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 10, 7, 'Remote Control Car', 'High-speed RC car', 59.99, 15.00, 'TL-RC-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 10, 7, 'Puzzle 1000 Pieces', 'Landscape puzzle', 24.99, 0.00, 'TL-PZ-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 10, 7, 'Board Game Family', 'Fun family board game', 32.99, 5.00, 'TL-BG-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 10, 7, 'Plush Teddy Bear', 'Soft cuddly teddy bear', 19.99, 0.00, 'TL-TB-001', TRUE),

-- Additional Electronics
((SELECT user_id FROM users WHERE username = 'seller1'), 1, 1, 'Tablet 10 inch', '128GB Android tablet', 299.99, 12.00, 'TP-TB-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 1, 1, 'Smart Watch', 'Fitness tracking smartwatch', 199.99, 18.00, 'TP-SW-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 1, 1, 'Bluetooth Speaker', 'Portable waterproof speaker', 59.99, 10.00, 'TP-BS-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 1, 1, 'Webcam HD', '1080p webcam with mic', 79.99, 0.00, 'TP-WC-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller1'), 1, 1, 'Hard Drive 1TB', 'External USB hard drive', 89.99, 8.00, 'TP-HD-001', TRUE),

-- More Home & Kitchen
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Vacuum Cleaner', 'Cordless stick vacuum', 249.99, 20.00, 'HC-VC-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Toaster 4-Slice', 'Stainless steel toaster', 49.99, 0.00, 'HC-TS-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Electric Kettle', 'Fast boil kettle 1.7L', 39.99, 10.00, 'HC-EK-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Food Processor', 'Multi-function food processor', 139.99, 15.00, 'HC-FP-001', TRUE),
((SELECT user_id FROM users WHERE username = 'seller2'), 4, 3, 'Rice Cooker', 'Digital rice cooker 10 cups', 79.99, 5.00, 'HC-RC-001', TRUE);

-- ============================================
-- 6. PRODUCT IMAGES (Sample URLs)
-- ============================================

INSERT INTO product_images (product_id, image_url, is_primary, display_order)
SELECT product_id, 
       CONCAT('https://placehold.co/600x400/png?text=', REPLACE(product_name, ' ', '+')),
       TRUE,
       0
FROM products;

-- ============================================
-- 7. INVENTORY
-- ============================================

INSERT INTO inventory (product_id, warehouse_id, quantity, reserved_quantity, reorder_level)
SELECT p.product_id, w.warehouse_id, 
       FLOOR(RAND() * 200) + 50 as quantity,  -- Random quantity 50-250
       0 as reserved_quantity,
       20 as reorder_level
FROM products p
CROSS JOIN (SELECT warehouse_id FROM warehouses LIMIT 1) w;

-- ============================================
-- 8. LOYALTY TIERS
-- ============================================

INSERT INTO loyalty_tiers (tier_name, min_points, max_points, discount_percentage, benefits) VALUES
('Bronze', 0, 999, 0.00, 'Welcome tier - Start earning points'),
('Silver', 1000, 4999, 5.00, '5% discount on all purchases'),
('Gold', 5000, 9999, 10.00, '10% discount + Priority support'),
('Platinum', 10000, NULL, 15.00, '15% discount + Free shipping + VIP support');

-- ============================================
-- 9. COUPONS
-- ============================================

INSERT INTO coupons (coupon_code, description, discount_type, discount_value, min_purchase_amount, max_discount_amount, usage_limit, valid_from, valid_until, is_active, created_by) VALUES
('WELCOME10', 'Welcome discount for new customers', 'PERCENTAGE', 10.00, 50.00, 20.00, 1000, NOW(), DATE_ADD(NOW(), INTERVAL 30 DAY), TRUE, (SELECT user_id FROM users WHERE username = 'admin1')),
('SAVE20', 'Save $20 on orders above $100', 'FIXED_AMOUNT', 20.00, 100.00, 20.00, 500, NOW(), DATE_ADD(NOW(), INTERVAL 60 DAY), TRUE, (SELECT user_id FROM users WHERE username = 'admin1')),
('FLASH50', 'Flash sale - 50% off', 'PERCENTAGE', 50.00, 200.00, 100.00, 100, NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY), TRUE, (SELECT user_id FROM users WHERE username = 'admin1')),
('FREESHIP', '$10 off for free shipping simulation', 'FIXED_AMOUNT', 10.00, 0.00, 10.00, 5000, NOW(), DATE_ADD(NOW(), INTERVAL 90 DAY), TRUE, (SELECT user_id FROM users WHERE username = 'admin1'));

-- ============================================
-- 10. REGIONS & DELIVERY PARTNERS
-- ============================================

INSERT INTO regions (region_name, country, state, cities, is_active) VALUES
('Northeast Region', 'USA', 'NY', 'New York,Buffalo,Rochester', TRUE),
('Southeast Region', 'USA', 'FL', 'Miami,Orlando,Tampa', TRUE),
('West Region', 'USA', 'CA', 'Los Angeles,San Francisco,San Diego', TRUE);

INSERT INTO delivery_partners (user_id, vehicle_type, license_number, region_id, is_active, rating) VALUES
((SELECT user_id FROM users WHERE username = 'delivery1'), 'Van', 'DL-1234', 1, TRUE, 4.8),
((SELECT user_id FROM users WHERE username = 'delivery2'), 'Motorcycle', 'MC-5678', 2, TRUE, 4.9);

-- ============================================
-- 11. SUPPLIERS
-- ============================================

INSERT INTO suppliers (user_id, company_name, contact_person, address, city, country, phone, email, is_active) VALUES
((SELECT user_id FROM users WHERE username = 'supplier1'), 'Global Tech Supplies Inc', 'Lisa Wilson', '500 Supply Chain Blvd', 'Chicago', 'USA', '+1234567898', 'supplier1@example.com', TRUE);

-- ============================================
-- 12. SAMPLE ORDERS (for demonstration)
-- ============================================

-- Sample order 1 (Delivered - Payment Completed)
INSERT INTO orders (customer_id, order_number, order_status, payment_status, payment_method, subtotal, discount_amount, tax_amount, shipping_fee, total_amount, shipping_address, shipping_city, shipping_country, shipping_postal_code, shipping_phone, created_at) 
VALUES (
    (SELECT user_id FROM users WHERE username = 'customer1'),
    'ORD-20231201-123456',
    'DELIVERED',
    'PAID',
    'CASH_ON_DELIVERY',
    259.98,
    25.99,
    23.40,
    5.00,
    262.39,
    '123 Main Street, Apt 4B',
    'New York',
    'USA',
    '10001',
    '+1234567890',
    DATE_SUB(NOW(), INTERVAL 10 DAY)
);

SET @order1_id = LAST_INSERT_ID();

INSERT INTO order_items (order_id, product_id, seller_id, quantity, unit_price, total_price)
SELECT @order1_id, p.product_id, p.seller_id, 2, p.final_price, p.final_price * 2
FROM products p
WHERE p.sku = 'TP-MS-001' LIMIT 1;

INSERT INTO payments (order_id, payment_method, amount, payment_status, payment_date)
VALUES (@order1_id, 'CASH_ON_DELIVERY', 262.39, 'COMPLETED', DATE_SUB(NOW(), INTERVAL 3 DAY));

INSERT INTO shipments (order_id, tracking_number, shipment_status, partner_id, estimated_delivery, actual_delivery)
VALUES (@order1_id, 'TRK-DELIVERED-001', 'DELIVERED', 
        (SELECT partner_id FROM delivery_partners WHERE user_id = (SELECT user_id FROM users WHERE username = 'delivery1')),
        DATE_SUB(NOW(), INTERVAL 5 DAY),
        DATE_SUB(NOW(), INTERVAL 3 DAY));

-- Initialize loyalty for customer
INSERT INTO customer_loyalty (customer_id, current_points, lifetime_points, tier_id)
VALUES (
    (SELECT user_id FROM users WHERE username = 'customer1'),
    262,
    262,
    (SELECT tier_id FROM loyalty_tiers WHERE tier_name = 'Bronze')
);
