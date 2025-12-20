-- Database Views for E-Commerce Platform
-- Simplify complex queries and reporting

-- =============================================
-- CUSTOMER VIEWS
-- =============================================

-- View: Customer order summary with totals
CREATE OR REPLACE VIEW customer_order_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    COUNT(DISTINCT o.order_id) as total_orders,
    COALESCE(SUM(o.total_amount), 0) as total_spent,
    COALESCE(AVG(o.total_amount), 0) as avg_order_value,
    MAX(o.order_date) as last_order_date,
    COALESCE(lp.points, 0) as loyalty_points,
    COALESCE(lp.tier, 'bronze') as loyalty_tier
FROM customer c
LEFT JOIN `order` o ON c.customer_id = o.customer_id
LEFT JOIN loyality_program lp ON c.customer_id = lp.customer_id
GROUP BY c.customer_id, c.name, c.email, lp.points, lp.tier;

-- View: Customer activity dashboard
CREATE OR REPLACE VIEW customer_activity AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    COUNT(DISTINCT o.order_id) as orders_count,
    COUNT(DISTINCT r.review_id) as reviews_count,
    COUNT(DISTINCT st.ticket_id) as support_tickets,
    COUNT(DISTINCT w.wishlist_id) as wishlist_items,
    c.date_created as member_since
FROM customer c
LEFT JOIN `order` o ON c.customer_id = o.customer_id
LEFT JOIN review r ON c.customer_id = r.customer_id
LEFT JOIN support_ticket st ON c.customer_id = st.customer_id
LEFT JOIN wishlist w ON c.customer_id = w.customer_id
GROUP BY c.customer_id, c.name, c.email, c.date_created;

-- =============================================
-- PRODUCT VIEWS
-- =============================================

-- View: Product catalog with inventory and ratings
CREATE OR REPLACE VIEW product_catalog AS
SELECT 
    p.product_id,
    p.name,
    p.description,
    p.price,
    p.sku,
    c.name as category_name,
    b.name as brand_name,
    s.business_name as seller_name,
    COALESCE(SUM(i.quantity), 0) as total_stock,
    COALESCE(AVG(r.rating), 0) as avg_rating,
    COUNT(DISTINCT r.review_id) as review_count,
    p.is_active,
    p.created_at
FROM product p
LEFT JOIN category c ON p.category_id = c.category_id
LEFT JOIN brand b ON p.brand_id = b.brand_id
LEFT JOIN seller s ON p.seller_id = s.seller_id
LEFT JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN review r ON p.product_id = r.product_id AND r.is_approved = TRUE
GROUP BY p.product_id, p.name, p.description, p.price, p.sku, 
         c.name, b.name, s.business_name, p.is_active, p.created_at;

-- View: Low stock products
CREATE OR REPLACE VIEW low_stock_products AS
SELECT 
    p.product_id,
    p.name,
    p.sku,
    w.location as warehouse,
    i.quantity as current_stock,
    i.reorder_level,
    i.reorder_quantity,
    (i.reorder_level - i.quantity) as units_below_threshold
FROM inventory i
JOIN product p ON i.product_id = p.product_id
JOIN warehouse w ON i.warehouse_id = w.warehouse_id
WHERE i.quantity < i.reorder_level AND p.is_active = TRUE
ORDER BY units_below_threshold DESC;

-- View: Product sales performance
CREATE OR REPLACE VIEW product_sales_performance AS
SELECT 
    p.product_id,
    p.name,
    p.price,
    c.name as category,
    COUNT(oi.order_item_id) as times_ordered,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.subtotal) as total_revenue,
    AVG(oi.price) as avg_selling_price
FROM product p
LEFT JOIN order_item oi ON p.product_id = oi.product_id
LEFT JOIN category c ON p.category_id = c.category_id
GROUP BY p.product_id, p.name, p.price, c.name
ORDER BY total_revenue DESC;

-- =============================================
-- ORDER VIEWS
-- =============================================

-- View: Order details with customer info
CREATE OR REPLACE VIEW order_details_view AS
SELECT 
    o.order_id,
    o.order_date,
    o.status,
    c.customer_id,
    c.name as customer_name,
    c.email as customer_email,
    o.subtotal,
    o.tax_amount,
    o.shipping_cost,
    o.discount_amount,
    o.total_amount,
    p.payment_method,
    p.status as payment_status,
    s.tracking_number,
    s.status as shipping_status,
    s.estimated_delivery
FROM `order` o
JOIN customer c ON o.customer_id = c.customer_id
LEFT JOIN payment p ON o.order_id = p.order_id
LEFT JOIN shipment s ON o.order_id = s.order_id;

-- View: Order items details
CREATE OR REPLACE VIEW order_items_detail AS
SELECT 
    oi.order_item_id,
    oi.order_id,
    o.order_date,
    o.status as order_status,
    p.product_id,
    p.name as product_name,
    p.sku,
    oi.quantity,
    oi.price,
    oi.subtotal
FROM order_item oi
JOIN `order` o ON oi.order_id = o.order_id
JOIN product p ON oi.product_id = p.product_id;

-- View: Pending orders requiring action
CREATE OR REPLACE VIEW pending_orders AS
SELECT 
    o.order_id,
    o.order_date,
    c.name as customer_name,
    o.total_amount,
    p.status as payment_status,
    o.status as order_status,
    DATEDIFF(NOW(), o.order_date) as days_pending
FROM `order` o
JOIN customer c ON o.customer_id = c.customer_id
LEFT JOIN payment p ON o.order_id = p.order_id
WHERE o.status IN ('pending', 'processing')
ORDER BY o.order_date ASC;

-- =============================================
-- FINANCIAL VIEWS
-- =============================================

-- View: Daily sales summary
CREATE OR REPLACE VIEW daily_sales_summary AS
SELECT 
    DATE(order_date) as sale_date,
    COUNT(DISTINCT order_id) as total_orders,
    SUM(subtotal) as gross_sales,
    SUM(tax_amount) as total_tax,
    SUM(shipping_cost) as total_shipping,
    SUM(discount_amount) as total_discounts,
    SUM(total_amount) as net_sales
FROM `order`
WHERE status NOT IN ('cancelled', 'refunded')
GROUP BY DATE(order_date)
ORDER BY sale_date DESC;

-- View: Revenue by category
CREATE OR REPLACE VIEW revenue_by_category AS
SELECT 
    c.category_id,
    c.name as category_name,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.quantity) as units_sold,
    SUM(oi.subtotal) as total_revenue
FROM category c
JOIN product p ON c.category_id = p.category_id
JOIN order_item oi ON p.product_id = oi.product_id
JOIN `order` o ON oi.order_id = o.order_id
WHERE o.status NOT IN ('cancelled', 'refunded')
GROUP BY c.category_id, c.name
ORDER BY total_revenue DESC;

-- View: Seller performance
CREATE OR REPLACE VIEW seller_performance AS
SELECT 
    s.seller_id,
    s.business_name,
    COUNT(DISTINCT p.product_id) as products_listed,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.quantity) as units_sold,
    SUM(oi.subtotal) as gross_revenue,
    SUM(oi.subtotal * s.commission_rate / 100) as commission_due
FROM seller s
LEFT JOIN product p ON s.seller_id = p.seller_id
LEFT JOIN order_item oi ON p.product_id = oi.product_id
LEFT JOIN `order` o ON oi.order_id = o.order_id AND o.status = 'delivered'
GROUP BY s.seller_id, s.business_name, s.commission_rate
ORDER BY gross_revenue DESC;

-- View: Payment summary
CREATE OR REPLACE VIEW payment_summary AS
SELECT 
    payment_method,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) as completed_amount,
    SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) as pending_amount,
    SUM(CASE WHEN status = 'failed' THEN amount ELSE 0 END) as failed_amount,
    SUM(CASE WHEN status = 'refunded' THEN amount ELSE 0 END) as refunded_amount
FROM payment
GROUP BY payment_method;

-- =============================================
-- INVENTORY VIEWS
-- =============================================

-- View: Inventory by warehouse
CREATE OR REPLACE VIEW inventory_by_warehouse AS
SELECT 
    w.warehouse_id,
    w.location,
    COUNT(DISTINCT i.product_id) as product_count,
    SUM(i.quantity) as total_units,
    SUM(i.quantity * p.price) as inventory_value
FROM warehouse w
LEFT JOIN inventory i ON w.warehouse_id = i.warehouse_id
LEFT JOIN product p ON i.product_id = p.product_id
GROUP BY w.warehouse_id, w.location;

-- View: Products needing reorder
CREATE OR REPLACE VIEW reorder_alerts AS
SELECT 
    p.product_id,
    p.name,
    p.sku,
    sup.company_name as supplier,
    SUM(i.quantity) as total_stock,
    MAX(i.reorder_level) as reorder_level,
    MAX(i.reorder_quantity) as reorder_quantity,
    (MAX(i.reorder_level) - SUM(i.quantity)) as shortage
FROM product p
JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN supplier sup ON p.supplier_id = sup.supplier_id
WHERE p.is_active = TRUE
GROUP BY p.product_id, p.name, p.sku, sup.company_name
HAVING SUM(i.quantity) < MAX(i.reorder_level)
ORDER BY shortage DESC;

-- =============================================
-- SUPPORT VIEWS
-- =============================================

-- View: Active support tickets
CREATE OR REPLACE VIEW active_support_tickets AS
SELECT 
    st.ticket_id,
    st.created_at,
    st.status,
    st.priority,
    st.subject,
    c.name as customer_name,
    c.email as customer_email,
    sr.name as assigned_to,
    DATEDIFF(NOW(), st.created_at) as days_open
FROM support_ticket st
JOIN customer c ON st.customer_id = c.customer_id
LEFT JOIN support_rep sr ON st.support_id = sr.support_id
WHERE st.status IN ('open', 'in_progress')
ORDER BY st.priority DESC, st.created_at ASC;

-- =============================================
-- SHIPPING VIEWS
-- =============================================

-- View: Shipment tracking
CREATE OR REPLACE VIEW shipment_tracking_view AS
SELECT 
    s.shipment_id,
    s.tracking_number,
    s.status as shipment_status,
    o.order_id,
    c.name as customer_name,
    c.email as customer_email,
    dp.name as courier_name,
    s.shipped_date,
    s.estimated_delivery,
    s.actual_delivery,
    DATEDIFF(s.estimated_delivery, NOW()) as days_until_delivery
FROM shipment s
JOIN `order` o ON s.order_id = o.order_id
JOIN customer c ON o.customer_id = c.customer_id
LEFT JOIN delivery_partner dp ON s.courier_id = dp.courier_id
ORDER BY s.shipped_date DESC;

-- View: Deliveries in progress
CREATE OR REPLACE VIEW deliveries_in_progress AS
SELECT 
    s.tracking_number,
    o.order_id,
    c.name as customer_name,
    dp.name as courier,
    s.status,
    s.estimated_delivery,
    o.shipping_address
FROM shipment s
JOIN `order` o ON s.order_id = o.order_id
JOIN customer c ON o.customer_id = c.customer_id
JOIN delivery_partner dp ON s.courier_id = dp.courier_id
WHERE s.status IN ('in_transit', 'out_for_delivery')
ORDER BY s.estimated_delivery ASC;

-- =============================================
-- ANALYTICS VIEWS
-- =============================================

-- View: Top customers by revenue
CREATE OR REPLACE VIEW top_customers AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.order_date) as last_purchase_date,
    DATEDIFF(NOW(), MAX(o.order_date)) as days_since_last_order
FROM customer c
JOIN `order` o ON c.customer_id = o.customer_id
WHERE o.status NOT IN ('cancelled', 'refunded')
GROUP BY c.customer_id, c.name, c.email
ORDER BY lifetime_value DESC
LIMIT 100;

-- View: Monthly revenue trend
CREATE OR REPLACE VIEW monthly_revenue AS
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') as month,
    COUNT(DISTINCT order_id) as total_orders,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(total_amount) as revenue,
    AVG(total_amount) as avg_order_value
FROM `order`
WHERE status NOT IN ('cancelled', 'refunded')
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month DESC;
