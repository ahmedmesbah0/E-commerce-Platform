-- ============================================
-- Database Views for Reporting & Analytics
-- ============================================

USE ecommerce_db;

-- View: Product Stock Summary across all warehouses
CREATE OR REPLACE VIEW v_product_stock_summary AS
SELECT 
    p.product_id,
    p.product_name,
    p.sku,
    c.category_name,
    b.brand_name,
    SUM(i.quantity) as total_quantity,
    SUM(i.reserved_quantity) as total_reserved,
    SUM(i.available_quantity) as total_available,
    p.final_price,
    p.is_active,
    COUNT(DISTINCT i.warehouse_id) as warehouse_count
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN brands b ON p.brand_id = b.brand_id
LEFT JOIN inventory i ON p.product_id = i.product_id
GROUP BY p.product_id, p.product_name, p.sku, c.category_name, b.brand_name, p.final_price, p.is_active;

-- View: Complete Order Information
CREATE OR REPLACE VIEW v_order_summary AS
SELECT 
    o.order_id,
    o.order_number,
    o.order_status,
    o.payment_status,
    o.payment_method,
    o.total_amount,
    o.created_at as order_date,
    CONCAT(u.first_name, ' ', u.last_name) as customer_name,
    u.email as customer_email,
    u.phone as customer_phone,
    o.shipping_city,
    o.shipping_country,
    COUNT(oi.order_item_id) as total_items,
    s.tracking_number,
    s.shipment_status,
    dp.user_id as delivery_partner_user_id
FROM orders o
JOIN users u ON o.customer_id = u.user_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN shipments s ON o.order_id = s.order_id
LEFT JOIN delivery_partners dp ON s.partner_id = dp.partner_id
GROUP BY o.order_id, o.order_number, o.order_status, o.payment_status, o.payment_method,
         o.total_amount, o.created_at, u.first_name, u.last_name, u.email, u.phone,
         o.shipping_city, o.shipping_country, s.tracking_number, s.shipment_status, dp.user_id;

-- View: Sales by Category
CREATE OR REPLACE VIEW v_sales_by_category AS
SELECT 
    c.category_id,
    c.category_name,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(oi.unit_price) as avg_unit_price
FROM categories c
JOIN products p ON c.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status NOT IN ('CANCELLED', 'REFUNDED')
GROUP BY c.category_id, c.category_name;

-- View: Sales by Seller
CREATE OR REPLACE VIEW v_sales_by_seller AS
SELECT 
    u.user_id as seller_id,
    CONCAT(u.first_name, ' ', u.last_name) as seller_name,
    u.email as seller_email,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.total_price) as total_revenue,
    COUNT(DISTINCT p.product_id) as total_products
FROM users u
JOIN products p ON u.user_id = p.seller_id
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status NOT IN ('CANCELLED', 'REFUNDED')
GROUP BY u.user_id, u.first_name, u.last_name, u.email;

-- View: Customer Lifetime Value
CREATE OR REPLACE VIEW v_customer_lifetime_value AS
SELECT 
    u.user_id as customer_id,
    CONCAT(u.first_name, ' ', u.last_name) as customer_name,
    u.email,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.created_at) as last_order_date,
    MIN(o.created_at) as first_order_date,
    COALESCE(cl.current_points, 0) as loyalty_points,
    lt.tier_name as loyalty_tier
FROM users u
LEFT JOIN orders o ON u.user_id = o.customer_id AND o.order_status NOT IN ('CANCELLED', 'REFUNDED')
LEFT JOIN customer_loyalty cl ON u.user_id = cl.customer_id
LEFT JOIN loyalty_tiers lt ON cl.tier_id = lt.tier_id
WHERE EXISTS (SELECT 1 FROM user_roles ur JOIN roles r ON ur.role_id = r.role_id 
              WHERE ur.user_id = u.user_id AND r.role_name = 'Customer')
GROUP BY u.user_id, u.first_name, u.last_name, u.email, cl.current_points, lt.tier_name;

-- View: Pending Deliveries
CREATE OR REPLACE VIEW v_pending_deliveries AS
SELECT 
    s.shipment_id,
    s.tracking_number,
    s.shipment_status,
    o.order_number,
    o.order_id,
    CONCAT(u.first_name, ' ', u.last_name) as customer_name,
    o.shipping_address,
    o.shipping_city,
    o.shipping_country,
    o.shipping_phone,
    s.estimated_delivery,
    CONCAT(dp_user.first_name, ' ', dp_user.last_name) as delivery_partner_name,
    dp.partner_id,
    DATEDIFF(NOW(), o.created_at) as days_since_order
FROM shipments s
JOIN orders o ON s.order_id = o.order_id
JOIN users u ON o.customer_id = u.user_id
LEFT JOIN delivery_partners dp ON s.partner_id = dp.partner_id
LEFT JOIN users dp_user ON dp.user_id = dp_user.user_id
WHERE s.shipment_status NOT IN ('DELIVERED', 'RETURNED', 'FAILED')
ORDER BY o.created_at ASC;

-- View: Low Stock Alerts
CREATE OR REPLACE VIEW v_low_stock_alerts AS
SELECT 
    p.product_id,
    p.product_name,
    p.sku,
    w.warehouse_id,
    w.warehouse_name,
    i.quantity,
    i.available_quantity,
    i.reserved_quantity,
    i.reorder_level,
    (i.reorder_level - i.available_quantity) as units_needed
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
WHERE i.available_quantity <= i.reorder_level
  AND p.is_active = TRUE
ORDER BY (i.reorder_level - i.available_quantity) DESC;

-- View: Best Selling Products
CREATE OR REPLACE VIEW v_best_selling_products AS
SELECT 
    p.product_id,
    p.product_name,
    p.sku,
    c.category_name,
    b.brand_name,
    p.final_price,
    COUNT(DISTINCT oi.order_id) as times_ordered,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(r.rating) as avg_rating,
    COUNT(DISTINCT r.review_id) as review_count
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN brands b ON p.brand_id = b.brand_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.order_status NOT IN ('CANCELLED', 'REFUNDED')
LEFT JOIN reviews r ON p.product_id = r.product_id AND r.is_approved = TRUE
GROUP BY p.product_id, p.product_name, p.sku, c.category_name, b.brand_name, p.final_price
HAVING total_units_sold > 0
ORDER BY total_units_sold DESC;

-- View: Support Ticket SLA Status
CREATE OR REPLACE VIEW v_ticket_sla_status AS
SELECT 
    t.ticket_id,
    t.ticket_number,
    t.subject,
    t.priority,
    t.status,
    CONCAT(customer.first_name, ' ', customer.last_name) as customer_name,
    CONCAT(agent.first_name, ' ', agent.last_name) as assigned_agent,
    t.created_at,
    t.resolved_at,
    TIMESTAMPDIFF(HOUR, t.created_at, COALESCE(t.resolved_at, NOW())) as hours_open,
    CASE 
        WHEN t.priority = 'URGENT' THEN 4
        WHEN t.priority = 'HIGH' THEN 8
        WHEN t.priority = 'MEDIUM' THEN 24
        WHEN t.priority = 'LOW' THEN 48
    END as sla_hours,
    CASE 
        WHEN t.status IN ('RESOLVED', 'CLOSED') THEN 'COMPLETED'
        WHEN TIMESTAMPDIFF(HOUR, t.created_at, NOW()) > (
            CASE 
                WHEN t.priority = 'URGENT' THEN 4
                WHEN t.priority = 'HIGH' THEN 8
                WHEN t.priority = 'MEDIUM' THEN 24
                WHEN t.priority = 'LOW' THEN 48
            END
        ) THEN 'BREACHED'
        ELSE 'WITHIN_SLA'
    END as sla_status
FROM tickets t
JOIN users customer ON t.customer_id = customer.user_id
LEFT JOIN users agent ON t.assigned_to = agent.user_id;

-- View: Marketing Commission Summary
CREATE OR REPLACE VIEW v_marketing_commission_summary AS
SELECT 
    u.user_id as agent_id,
    CONCAT(u.first_name, ' ', u.last_name) as agent_name,
    u.email as agent_email,
    COUNT(mc.commission_id) as total_commissions,
    SUM(CASE WHEN mc.status = 'PENDING' THEN mc.commission_amount ELSE 0 END) as pending_amount,
    SUM(CASE WHEN mc.status = 'APPROVED' THEN mc.commission_amount ELSE 0 END) as approved_amount,
    SUM(CASE WHEN mc.status = 'PAID' THEN mc.commission_amount ELSE 0 END) as paid_amount,
    SUM(mc.commission_amount) as total_amount
FROM users u
JOIN marketing_commissions mc ON u.user_id = mc.agent_id
GROUP BY u.user_id, u.first_name, u.last_name, u.email;

-- View: Daily Sales Report
CREATE OR REPLACE VIEW v_daily_sales_report AS
SELECT 
    DATE(o.created_at) as sale_date,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.subtotal) as subtotal,
    SUM(o.discount_amount) as total_discounts,
    SUM(o.tax_amount) as total_tax,
    SUM(o.shipping_fee) as total_shipping,
    SUM(o.total_amount) as total_revenue,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    AVG(o.total_amount) as avg_order_value
FROM orders o
WHERE o.order_status NOT IN ('CANCELLED', 'REFUNDED')
GROUP BY DATE(o.created_at)
ORDER BY sale_date DESC;

-- View: Inventory Valuation
CREATE OR REPLACE VIEW v_inventory_valuation AS
SELECT 
    w.warehouse_id,
    w.warehouse_name,
    p.product_id,
    p.product_name,
    i.quantity,
    i.available_quantity,
    p.final_price,
    (i.quantity * p.final_price) as total_value,
    (i.available_quantity * p.final_price) as available_value
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
WHERE p.is_active = TRUE;
