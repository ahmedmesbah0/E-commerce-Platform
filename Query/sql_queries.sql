-- ====================================================================
-- E-COMMERCE PLATFORM - COMPLEX SQL QUERIES
-- ====================================================================
-- This file contains comprehensive SQL queries demonstrating:
-- - Data Query Language (DQL)
-- - Data Definition Language (DDL)
-- - Data Manipulation Language (DML)
-- - Aggregate Functions, Joins, Set Operators, Subqueries, etc.
-- ====================================================================

-- ====================================================================
-- SECTION 1: DATA DEFINITION LANGUAGE (DDL)
-- ====================================================================

-- 1.1 CREATE: Create a temporary table for analytics
CREATE TABLE IF NOT EXISTS temp_sales_summary (
    summary_id INT AUTO_INCREMENT PRIMARY KEY,
    summary_date DATE NOT NULL,
    total_orders INT,
    total_revenue DECIMAL(12, 2),
    avg_order_value DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1.2 ALTER: Add index for performance optimization
ALTER TABLE orders 
ADD INDEX idx_customer_created (customer_id, created_at);

-- 1.3 ALTER: Add column for customer segmentation
ALTER TABLE users 
ADD COLUMN customer_segment ENUM('VIP', 'REGULAR', 'NEW') DEFAULT 'NEW';

-- 1.4 CREATE VIEW: Create view for active product inventory
CREATE OR REPLACE VIEW v_active_inventory AS
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    b.brand_name,
    p.final_price,
    SUM(i.available_quantity) as total_available,
    COUNT(DISTINCT i.warehouse_id) as warehouse_count
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN brands b ON p.brand_id = b.brand_id
LEFT JOIN inventory i ON p.product_id = i.product_id
WHERE p.is_active = TRUE
GROUP BY p.product_id, p.product_name, c.category_name, b.brand_name, p.final_price;

-- 1.5 CREATE INDEX: Create composite index for faster queries
CREATE INDEX idx_orders_status_date ON orders(order_status, created_at DESC);


-- ====================================================================
-- SECTION 2: DATA MANIPULATION LANGUAGE (DML)
-- ====================================================================

-- 2.1 INSERT: Add new product
INSERT INTO products (product_name, category_id, brand_id, seller_id, base_price, final_price, description)
VALUES (
    'Premium Wireless Headphones',
    (SELECT category_id FROM categories WHERE category_name = 'Electronics' LIMIT 1),
    (SELECT brand_id FROM brands WHERE brand_name = 'TechPro' LIMIT 1),
    (SELECT user_id FROM users WHERE username = 'seller1' LIMIT 1),
    299.99,
    279.99,
    'High-quality wireless headphones with noise cancellation'
);

-- 2.2 UPDATE: Update product prices with discount
UPDATE products 
SET final_price = base_price * 0.85,
    updated_at = NOW()
WHERE category_id IN (
    SELECT category_id FROM categories WHERE category_name IN ('Electronics', 'Gadgets')
)
AND is_active = TRUE;

-- 2.3 UPDATE: Update customer loyalty tier based on points
UPDATE customer_loyalty cl
SET tier_id = (
    SELECT tier_id FROM loyalty_tiers
    WHERE cl.current_points >= min_points
    ORDER BY min_points DESC
    LIMIT 1
)
WHERE cl.current_points >= 1000;

-- 2.4 DELETE: Remove old audit logs (soft delete equivalent - update)
DELETE FROM audit_log 
WHERE created_at < DATE_SUB(NOW(), INTERVAL 6 MONTH);

-- 2.5 INSERT with SELECT: Copy best-selling products to featured table
INSERT INTO temp_sales_summary (summary_date, total_orders, total_revenue, avg_order_value)
SELECT 
    CURDATE(),
    COUNT(DISTINCT order_id),
    SUM(total_amount),
    AVG(total_amount)
FROM orders
WHERE created_at >= CURDATE();


-- ====================================================================
-- SECTION 3: DATA QUERY LANGUAGE (DQL) - BASIC QUERIES
-- ====================================================================

-- 3.1 SELECT with WHERE clause and ORDER BY
SELECT 
    product_name,
    final_price,
    base_price - final_price AS discount_amount,
    ((base_price - final_price) / base_price) * 100 AS discount_percentage
FROM products
WHERE is_active = TRUE 
    AND final_price < base_price
ORDER BY discount_percentage DESC
LIMIT 10;

-- 3.2 SELECT with DISTINCT and COUNT
SELECT 
    COUNT(DISTINCT customer_id) as unique_customers,
    COUNT(*) as total_orders,
    COUNT(*) / COUNT(DISTINCT customer_id) as avg_orders_per_customer
FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH);

-- 3.3 SELECT with LIKE and wildcards
SELECT 
    product_name,
    final_price,
    description
FROM products
WHERE product_name LIKE '%Pro%'
    OR description LIKE '%premium%'
    OR description LIKE '%professional%'
ORDER BY final_price DESC;


-- ====================================================================
-- SECTION 4: AGGREGATE FUNCTIONS
-- ====================================================================

-- 4.1 Multiple aggregate functions with GROUP BY
SELECT 
    c.category_name,
    COUNT(p.product_id) as product_count,
    AVG(p.final_price) as avg_price,
    MIN(p.final_price) as min_price,
    MAX(p.final_price) as max_price,
    SUM(i.quantity) as total_inventory
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
LEFT JOIN inventory i ON p.product_id = i.product_id
WHERE c.is_active = TRUE
GROUP BY c.category_id, c.category_name
HAVING product_count > 0
ORDER BY total_inventory DESC;

-- 4.2 Aggregate with HAVING clause
SELECT 
    seller_id,
    CONCAT(u.first_name, ' ', u.last_name) as seller_name,
    COUNT(DISTINCT p.product_id) as products_listed,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.total_price) as total_revenue
FROM products p
JOIN users u ON p.seller_id = u.user_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY seller_id, seller_name
HAVING total_revenue > 1000
ORDER BY total_revenue DESC;

-- 4.3 GROUP BY with ROLLUP (hierarchical aggregation)
SELECT 
    YEAR(created_at) as year,
    MONTH(created_at) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as revenue
FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 YEAR)
GROUP BY year, month WITH ROLLUP;


-- ====================================================================
-- SECTION 5: JOINS
-- ====================================================================

-- 5.1 INNER JOIN: Get orders with customer and product details
SELECT 
    o.order_number,
    CONCAT(u.first_name, ' ', u.last_name) as customer_name,
    u.email,
    o.total_amount,
    o.order_status,
    o.payment_status,
    COUNT(oi.order_item_id) as items_count
FROM orders o
INNER JOIN users u ON o.customer_id = u.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.created_at >= DATE_SUB(NOW(), INTERVAL 1 WEEK)
GROUP BY o.order_id, o.order_number, customer_name, u.email, o.total_amount, o.order_status, o.payment_status
ORDER BY o.created_at DESC;

-- 5.2 LEFT JOIN: All products with or without inventory
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    COALESCE(SUM(i.available_quantity), 0) as available_stock,
    COALESCE(SUM(i.reserved_quantity), 0) as reserved_stock,
    CASE 
        WHEN COALESCE(SUM(i.available_quantity), 0) = 0 THEN 'OUT OF STOCK'
        WHEN COALESCE(SUM(i.available_quantity), 0) < 10 THEN 'LOW STOCK'
        ELSE 'IN STOCK'
    END as stock_status
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN inventory i ON p.product_id = i.product_id
WHERE p.is_active = TRUE
GROUP BY p.product_id, p.product_name, c.category_name
ORDER BY available_stock ASC;

-- 5.3 RIGHT JOIN: All warehouses with or without inventory
SELECT 
    w.warehouse_name,
    w.city,
    w.state,
    COUNT(DISTINCT i.product_id) as unique_products,
    SUM(i.quantity) as total_units,
    SUM(i.quantity * p.final_price) as inventory_value
FROM inventory i
RIGHT JOIN warehouses w ON i.warehouse_id = w.warehouse_id
LEFT JOIN products p ON i.product_id = p.product_id
WHERE w.is_active = TRUE
GROUP BY w.warehouse_id, w.warehouse_name, w.city, w.state
ORDER BY inventory_value DESC;

-- 5.4 SELF JOIN: Find products in same category with similar prices
SELECT 
    p1.product_name as product1,
    p1.final_price as price1,
    p2.product_name as product2,
    p2.final_price as price2,
    ABS(p1.final_price - p2.final_price) as price_difference
FROM products p1
INNER JOIN products p2 ON p1.category_id = p2.category_id
WHERE p1.product_id < p2.product_id
    AND ABS(p1.final_price - p2.final_price) < 50
    AND p1.is_active = TRUE
    AND p2.is_active = TRUE
ORDER BY p1.category_id, price_difference;

-- 5.5 Multiple JOINS: Complete order information
SELECT 
    o.order_number,
    o.created_at as order_date,
    CONCAT(u.first_name, ' ', u.last_name) as customer,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.total_price,
    s.shipment_status,
    s.tracking_number,
    CONCAT(dp.first_name, ' ', dp.last_name) as delivery_partner
FROM orders o
JOIN users u ON o.customer_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN shipments s ON o.order_id = s.order_id
LEFT JOIN delivery_partners dpt ON s.delivery_partner_id = dpt.delivery_partner_id
LEFT JOIN users dp ON dpt.user_id = dp.user_id
WHERE o.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY o.created_at DESC, o.order_id, oi.order_item_id;


-- ====================================================================
-- SECTION 6: SUBQUERIES
-- ====================================================================

-- 6.1 Subquery in WHERE clause: Products above average price
SELECT 
    product_name,
    final_price,
    (SELECT AVG(final_price) FROM products WHERE is_active = TRUE) as avg_price,
    final_price - (SELECT AVG(final_price) FROM products WHERE is_active = TRUE) as price_difference
FROM products
WHERE final_price > (SELECT AVG(final_price) FROM products WHERE is_active = TRUE)
    AND is_active = TRUE
ORDER BY price_difference DESC;

-- 6.2 Correlated subquery: Customers with above-average orders
SELECT 
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) as customer_name,
    u.email,
    (SELECT COUNT(*) FROM orders WHERE customer_id = u.user_id) as order_count,
    (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE customer_id = u.user_id) as total_spent
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = u.user_id
    GROUP BY o.customer_id
    HAVING COUNT(*) > (SELECT AVG(order_count) FROM (
        SELECT COUNT(*) as order_count FROM orders GROUP BY customer_id
    ) as avg_orders)
)
ORDER BY total_spent DESC;

-- 6.3 Subquery in FROM clause (derived table)
SELECT 
    category_name,
    product_count,
    avg_price,
    RANK() OVER (ORDER BY product_count DESC) as category_rank
FROM (
    SELECT 
        c.category_name,
        COUNT(p.product_id) as product_count,
        AVG(p.final_price) as avg_price
    FROM categories c
    LEFT JOIN products p ON c.category_id = p.category_id
    WHERE c.is_active = TRUE AND (p.is_active = TRUE OR p.is_active IS NULL)
    GROUP BY c.category_id, c.category_name
) as category_stats
ORDER BY category_rank;

-- 6.4 Subquery with IN operator
SELECT 
    product_name,
    final_price,
    c.category_name
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.product_id IN (
    SELECT product_id 
    FROM order_items 
    GROUP BY product_id 
    HAVING COUNT(*) >= 5
)
ORDER BY final_price DESC;

-- 6.5 Subquery with NOT EXISTS
SELECT 
    p.product_id,
    p.product_name,
    p.final_price,
    p.created_at
FROM products p
WHERE NOT EXISTS (
    SELECT 1 FROM order_items oi WHERE oi.product_id = p.product_id
)
AND p.is_active = TRUE
ORDER BY p.created_at DESC;


-- ====================================================================
-- SECTION 7: SET OPERATORS
-- ====================================================================

-- 7.1 UNION: Combine all users who are either customers or sellers
SELECT 
    u.user_id,
    u.username,
    u.email,
    'Customer' as user_type,
    COUNT(o.order_id) as interaction_count
FROM users u
JOIN user_roles ur ON u.user_id = ur.user_id
JOIN roles r ON ur.role_id = r.role_id
LEFT JOIN orders o ON u.user_id = o.customer_id
WHERE r.role_name = 'Customer'
GROUP BY u.user_id, u.username, u.email

UNION

SELECT 
    u.user_id,
    u.username,
    u.email,
    'Seller' as user_type,
    COUNT(p.product_id) as interaction_count
FROM users u
JOIN user_roles ur ON u.user_id = ur.user_id
JOIN roles r ON ur.role_id = r.role_id
LEFT JOIN products p ON u.user_id = p.seller_id
WHERE r.role_name = 'Seller'
GROUP BY u.user_id, u.username, u.email

ORDER BY user_type, interaction_count DESC;

-- 7.2 UNION ALL: Get all product price changes (including duplicates)
SELECT 
    product_id,
    product_name,
    base_price as price,
    'Base Price' as price_type,
    created_at as date
FROM products
WHERE is_active = TRUE

UNION ALL

SELECT 
    product_id,
    product_name,
    final_price as price,
    'Final Price' as price_type,
    updated_at as date
FROM products
WHERE is_active = TRUE AND final_price < base_price

ORDER BY product_id, date;

-- 7.3 INTERSECT (simulated with JOIN): Products that are both in cart and wishlist
SELECT DISTINCT
    p.product_id,
    p.product_name,
    p.final_price,
    'In Both Cart and Wishlist' as status
FROM products p
WHERE p.product_id IN (SELECT product_id FROM shopping_cart)
    AND p.product_id IN (SELECT product_id FROM wishlists);


-- ====================================================================
-- SECTION 8: WINDOW FUNCTIONS
-- ====================================================================

-- 8.1 ROW_NUMBER: Rank products by price within each category
SELECT 
    category_name,
    product_name,
    final_price,
    ROW_NUMBER() OVER (PARTITION BY c.category_id ORDER BY p.final_price DESC) as price_rank,
    DENSE_RANK() OVER (PARTITION BY c.category_id ORDER BY p.final_price DESC) as dense_rank
FROM products p
JOIN categories c ON p.category_id = c.category_id
WHERE p.is_active = TRUE
ORDER BY c.category_name, price_rank;

-- 8.2 Running total: Cumulative revenue by date
SELECT 
    DATE(created_at) as order_date,
    COUNT(*) as orders_count,
    SUM(total_amount) as daily_revenue,
    SUM(SUM(total_amount)) OVER (ORDER BY DATE(created_at)) as cumulative_revenue
FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY order_date;

-- 8.3 LAG and LEAD: Compare with previous and next values
SELECT 
    DATE(created_at) as order_date,
    COUNT(*) as orders_today,
    LAG(COUNT(*), 1) OVER (ORDER BY DATE(created_at)) as orders_yesterday,
    LEAD(COUNT(*), 1) OVER (ORDER BY DATE(created_at)) as orders_tomorrow,
    COUNT(*) - LAG(COUNT(*), 1) OVER (ORDER BY DATE(created_at)) as vs_yesterday
FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(created_at)
ORDER BY order_date;


-- ====================================================================
-- SECTION 9: COMPLEX QUERIES WITH MULTIPLE CONCEPTS
-- ====================================================================

-- 9.1 Customer Lifetime Value Analysis (Aggregation + Join + Window Function)
SELECT 
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) as customer_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(o.total_amount) as lifetime_value,
    AVG(o.total_amount) as avg_order_value,
    MAX(o.total_amount) as max_order_value,
    DATEDIFF(MAX(o.created_at), MIN(o.created_at)) as customer_lifespan_days,
    cl.current_points,
    lt.tier_name,
    NTILE(4) OVER (ORDER BY SUM(o.total_amount) DESC) as value_quartile
FROM users u
JOIN orders o ON u.user_id = o.customer_id
LEFT JOIN customer_loyalty cl ON u.user_id = cl.customer_id
LEFT JOIN loyalty_tiers lt ON cl.tier_id = lt.tier_id
WHERE o.order_status NOT IN ('CANCELLED', 'REFUNDED')
GROUP BY u.user_id, customer_name, cl.current_points, lt.tier_name
HAVING total_orders >= 2
ORDER BY lifetime_value DESC;

-- 9.2 Product Performance Report (Multiple Joins + Subqueries + Aggregation)
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    b.brand_name,
    p.final_price,
    COALESCE(sales.units_sold, 0) as units_sold,
    COALESCE(sales.revenue, 0) as revenue,
    COALESCE(reviews.avg_rating, 0) as avg_rating,
    COALESCE(reviews.review_count, 0) as review_count,
    COALESCE(inventory.stock_level, 0) as current_stock,
    CASE 
        WHEN COALESCE(sales.units_sold, 0) >= 50 THEN 'Best Seller'
        WHEN COALESCE(sales.units_sold, 0) >= 20 THEN 'Popular'
        WHEN COALESCE(sales.units_sold, 0) >= 5 THEN 'Moderate'
        ELSE 'Slow Moving'
    END as sales_category
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN brands b ON p.brand_id = b.brand_id
LEFT JOIN (
    SELECT 
        product_id,
        SUM(quantity) as units_sold,
        SUM(total_price) as revenue
    FROM order_items
    GROUP BY product_id
) sales ON p.product_id = sales.product_id
LEFT JOIN (
    SELECT 
        product_id,
        AVG(rating) as avg_rating,
        COUNT(*) as review_count
   FROM reviews
    WHERE is_approved = TRUE
    GROUP BY product_id
) reviews ON p.product_id = reviews.product_id
LEFT JOIN (
    SELECT 
        product_id,
        SUM(available_quantity) as stock_level
    FROM inventory
    GROUP BY product_id
) inventory ON p.product_id = inventory.product_id
WHERE p.is_active = TRUE
ORDER BY revenue DESC, units_sold DESC;

-- 9.3 Seller Performance Dashboard (Complex Aggregation + Multiple Joins)
SELECT 
    u.user_id as seller_id,
    CONCAT(u.first_name, ' ', u.last_name) as seller_name,
    u.email,
    COUNT(DISTINCT p.product_id) as products_count,
    COUNT(DISTINCT oi.order_id) as orders_fulfilled,
    SUM(oi.quantity) as total_units_sold,
    SUM(oi.total_price) as total_revenue,
    AVG(oi.unit_price) as avg_selling_price,
    AVG(r.rating) as avg_product_rating,
    COUNT(DISTINCT r.review_id) as total_reviews,
    p_stats.avg_stock_level
FROM users u
JOIN products p ON u.user_id = p.seller_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN reviews r ON p.product_id = r.product_id
LEFT JOIN (
    SELECT 
        p.seller_id,
        AVG(i.available_quantity) as avg_stock_level
    FROM products p
    LEFT JOIN inventory i ON p.product_id = i.product_id
    GROUP BY p.seller_id
) p_stats ON u.user_id = p_stats.seller_id
WHERE p.is_active = TRUE
GROUP BY u.user_id, seller_name, u.email, p_stats.avg_stock_level
HAVING total_revenue IS NOT NULL
ORDER BY total_revenue DESC;


-- ====================================================================
-- SECTION 10: ADVANCED CONDITIONAL LOGIC
-- ====================================================================

-- 10.1 CASE statement for customer segmentation
SELECT 
    u.user_id,
    CONCAT(u.first_name, ' ', u.last_name) as customer_name,
    order_stats.order_count,
    order_stats.total_spent,
    CASE 
        WHEN order_stats.total_spent >= 5000 THEN 'VIP'
        WHEN order_stats.total_spent >= 2000 THEN 'Premium'
        WHEN order_stats.total_spent >= 500 THEN 'Regular'
        WHEN order_stats.order_count > 0 THEN 'New Customer'
        ELSE 'Prospect'
    END as customer_segment,
    CASE 
        WHEN DATEDIFF(NOW(), order_stats.last_order_date) > 180 THEN 'At Risk'
        WHEN DATEDIFF(NOW(), order_stats.last_order_date) > 90 THEN 'Needs Attention'
        WHEN DATEDIFF(NOW(), order_stats.last_order_date) > 30 THEN 'Active'
        ELSE 'Very Active'
    END as engagement_status
FROM users u
LEFT JOIN (
    SELECT 
        customer_id,
        COUNT(*) as order_count,
        SUM(total_amount) as total_spent,
        MAX(created_at) as last_order_date
    FROM orders
    WHERE order_status NOT IN ('CANCELLED', 'REFUNDED')
    GROUP BY customer_id
) order_stats ON u.user_id = order_stats.customer_id
WHERE EXISTS (
    SELECT 1 FROM user_roles ur 
    JOIN roles r ON ur.role_id = r.role_id 
    WHERE ur.user_id = u.user_id AND r.role_name = 'Customer'
)
ORDER BY total_spent DESC;

-- 10.2 IF and COALESCE for data completeness
SELECT 
    product_id,
    product_name,
    COALESCE(description, 'No description available') as description,
    COALESCE(base_price, 0) as base_price,
    COALESCE(final_price, base_price, 0) as final_price,
    IF(final_price < base_price, 'On Sale', 'Regular Price') as price_status,
    IF(stock.total_stock > 0, 'Available', 'Out of Stock') as availability
FROM products p
LEFT JOIN (
    SELECT product_id, SUM(available_quantity) as total_stock
    FROM inventory
    GROUP BY product_id
) stock ON p.product_id = stock.product_id
WHERE p.is_active = TRUE
LIMIT 20;


-- ====================================================================
-- END OF SQL QUERIES FILE
-- ====================================================================
