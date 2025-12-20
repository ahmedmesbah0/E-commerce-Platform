-- =====================================================
-- DATABASE VIEWS
-- E-Commerce Platform - Reporting & Analytics
-- =====================================================

USE ecommerce_db;

-- =====================================================
-- VIEW 1: CUSTOMER ORDER SUMMARY
-- Purpose: Aggregate customer purchase statistics
-- =====================================================
CREATE OR REPLACE VIEW customer_order_summary AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.loyalty_tier,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS lifetime_value,
    COALESCE(AVG(o.total_amount), 0) AS avg_order_value,
    MAX(o.order_date) AS last_order_date,
    DATEDIFF(CURDATE(), MAX(o.order_date)) AS days_since_last_order
FROM customer c
LEFT JOIN `order` o ON c.customer_id = o.customer_id
WHERE c.is_active = TRUE
GROUP BY c.customer_id, c.name, c.email, c.loyalty_tier;

-- =====================================================
-- VIEW 2: PRODUCT SALES PERFORMANCE
-- Purpose: Track product sales metrics
-- =====================================================
CREATE OR REPLACE VIEW product_sales_performance AS
SELECT 
    p.product_id,
    p.name AS product_name,
    cat.name AS category_name,
    p.price,
    COALESCE(SUM(oi.quantity), 0) AS units_sold,
    COALESCE(SUM(oi.subtotal), 0) AS total_revenue,
    COALESCE(AVG(r.rating), 0) AS avg_rating,
    COUNT(DISTINCT r.review_id) AS review_count,
    p.is_active
FROM product p
LEFT JOIN category cat ON p.category_id = cat.category_id
LEFT JOIN order_item oi ON p.product_id = oi.product_id
LEFT JOIN review r ON p.product_id = r.product_id
GROUP BY p.product_id, p.name, cat.name, p.price, p.is_active;

-- =====================================================
-- VIEW 3: LOW STOCK ALERT
-- Purpose: Identify products needing reorder
-- =====================================================
CREATE OR REPLACE VIEW low_stock_products AS
SELECT 
    p.product_id,
    p.name AS product_name,
    w.warehouse_id,
    w.location AS warehouse_location,
    i.quantity AS current_stock,
    i.reorder_level,
    (i.reorder_level - i.quantity) AS shortage,
    i.last_updated
FROM inventory i
INNER JOIN product p ON i.product_id = p.product_id
INNER JOIN warehouse w ON i.warehouse_id = w.warehouse_id
WHERE i.quantity <= i.reorder_level
  AND p.is_active = TRUE
ORDER BY shortage DESC;

-- =====================================================
-- VIEW 4: DAILY SALES SUMMARY
-- Purpose: Track daily sales metrics
-- =====================================================
CREATE OR REPLACE VIEW daily_sales_summary AS
SELECT 
    DATE(order_date) AS sale_date,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    SUM(total_amount) AS daily_revenue,
    AVG(total_amount) AS avg_order_value,
    SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
FROM `order`
GROUP BY DATE(order_date)
ORDER BY sale_date DESC;

-- =====================================================
-- VIEW 5: MONTHLY REVENUE SUMMARY
-- Purpose: Monthly financial reporting
-- =====================================================
CREATE OR REPLACE VIEW monthly_revenue_report AS
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    YEAR(order_date) AS year,
    MONTH(order_date) AS month_num,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS gross_revenue,
    SUM(shipping_cost) AS shipping_revenue,
    SUM(tax_amount) AS tax_collected,
    (SUM(total_amount) - SUM(shipping_cost) - SUM(tax_amount)) AS net_revenue
FROM `order`
WHERE status NOT IN ('cancelled', 'refunded')
GROUP BY DATE_FORMAT(order_date, '%Y-%m'), YEAR(order_date), MONTH(order_date)
ORDER BY year DESC, month_num DESC;

-- =====================================================
-- VIEW 6: PENDING ORDERS DASHBOARD
-- Purpose: Track pending and processing orders
-- =====================================================
CREATE OR REPLACE VIEW pending_orders_view AS
SELECT 
    o.order_id,
    o.customer_id,
    c.name AS customer_name,
    c.email AS customer_email,
    o.order_date,
    o.status,
    o.total_amount,
    o.payment_method,
    DATEDIFF(CURDATE(), o.order_date) AS days_pending,
    sa.city AS shipping_city,
    sa.country AS shipping_country
FROM `order` o
INNER JOIN customer c ON o.customer_id = c.customer_id
LEFT JOIN shipping_address sa ON o.shipping_address_id = sa.address_id
WHERE o.status IN ('pending', 'processing')
ORDER BY o.order_date ASC;

-- =====================================================
-- VIEW 7: TOP CUSTOMERS
-- Purpose: Identify high-value customers
-- =====================================================
CREATE OR REPLACE VIEW top_customers AS
SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.loyalty_tier,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value,
    MAX(o.order_date) AS last_purchase_date
FROM customer c
INNER JOIN `order` o ON c.customer_id = o.customer_id
WHERE o.status NOT IN ('cancelled', 'refunded')
  AND c.is_active = TRUE
GROUP BY c.customer_id, c.name, c.email, c.loyalty_tier
HAVING total_spent > 0
ORDER BY total_spent DESC
LIMIT 100;

-- =====================================================
-- VIEW 8: INVENTORY STATUS BY WAREHOUSE
-- Purpose: Warehouse inventory overview
-- =====================================================
CREATE OR REPLACE VIEW warehouse_inventory_status AS
SELECT 
    w.warehouse_id,
    w.location,
    w.manager_name,
    COUNT(DISTINCT i.product_id) AS products_stored,
    SUM(i.quantity) AS total_units,
    SUM(CASE WHEN i.quantity <= i.reorder_level THEN 1 ELSE 0 END) AS low_stock_products,
    SUM(p.price * i.quantity) AS inventory_value
FROM warehouse w
LEFT JOIN inventory i ON w.warehouse_id = i.warehouse_id
LEFT JOIN product p ON i.product_id = p.product_id
GROUP BY w.warehouse_id, w.location, w.manager_name;

-- =====================================================
-- VIEW 9: PRODUCT REVIEW SUMMARY
-- Purpose: Aggregate product review metrics
-- =====================================================
CREATE OR REPLACE VIEW product_review_summary AS
SELECT 
    p.product_id,
    p.name AS product_name,
    COUNT(r.review_id) AS total_reviews,
    AVG(r.rating) AS avg_rating,
    SUM(CASE WHEN r.rating = 5 THEN 1 ELSE 0 END) AS five_star_count,
    SUM(CASE WHEN r.rating = 4 THEN 1 ELSE 0 END) AS four_star_count,
    SUM(CASE WHEN r.rating = 3 THEN 1 ELSE 0 END) AS three_star_count,
    SUM(CASE WHEN r.rating = 2 THEN 1 ELSE 0 END) AS two_star_count,
    SUM(CASE WHEN r.rating = 1 THEN 1 ELSE 0 END) AS one_star_count,
    SUM(CASE WHEN r.is_verified_purchase = TRUE THEN 1 ELSE 0 END) AS verified_reviews
FROM product p
LEFT JOIN review r ON p.product_id = r.product_id
GROUP BY p.product_id, p.name;

-- =====================================================
-- VIEW 10: SHIPMENT TRACKING STATUS
-- Purpose: Track delivery status
-- =====================================================
CREATE OR REPLACE VIEW shipment_tracking_view AS
SELECT 
    s.shipment_id,
    s.order_id,
    o.customer_id,
    c.name AS customer_name,
    c.email AS customer_email,
    sp.name AS shipping_provider,
    s.tracking_number,
    s.status AS shipment_status,
    s.shipped_date,
    s.estimated_delivery,
    s.actual_delivery,
    DATEDIFF(s.estimated_delivery, CURDATE()) AS days_until_delivery
FROM shipment s
INNER JOIN `order` o ON s.order_id = o.order_id
INNER JOIN customer c ON o.customer_id = c.customer_id
LEFT JOIN shipping_provider sp ON s.provider_id = sp.provider_id
WHERE s.status NOT IN ('delivered', 'failed');

-- =====================================================
-- END OF VIEWS
-- Total Views Created: 10
-- =====================================================
