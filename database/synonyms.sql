-- =====================================================
-- SYNONYMS (MySQL Alternative)
-- E-Commerce Platform
-- =====================================================

/*
NOTE: MySQL does not support SYNONYMS like Oracle.
Instead, we create VIEWs that act as synonyms for ease of access.
These views provide simple aliases for commonly used tables.
*/

USE ecommerce_db;

-- =====================================================
-- TABLE SYNONYMS (as Views)
-- =====================================================

-- Synonym for customer table
CREATE OR REPLACE VIEW customers AS
SELECT * FROM customer;

-- Synonym for product table
CREATE OR REPLACE VIEW products AS
SELECT * FROM product;

-- Synonym for order table 
CREATE OR REPLACE VIEW orders AS
SELECT * FROM `order`;

-- Synonym for category table
CREATE OR REPLACE VIEW categories AS
SELECT * FROM category;

-- Synonym for payment table
CREATE OR REPLACE VIEW payments AS
SELECT * FROM payment;

-- Synonym for shipment table
CREATE OR REPLACE VIEW shipments AS
SELECT * FROM shipment;

-- Synonym for inventory table
CREATE OR REPLACE VIEW stock AS
SELECT * FROM inventory;

-- Synonym for review table
CREATE OR REPLACE VIEW reviews AS
SELECT * FROM review;

-- Synonym for cart table
CREATE OR REPLACE VIEW shopping_cart AS
SELECT * FROM cart;

-- Synonym for wishlist table
CREATE OR REPLACE VIEW wishlists AS
SELECT * FROM wishlist;

-- =====================================================
-- SIMPLIFIED ACCESS SYNONYMS
-- =====================================================

-- Active products only
CREATE OR REPLACE VIEW active_products AS
SELECT * FROM product WHERE is_active = TRUE;

-- Active customers only
CREATE OR REPLACE VIEW active_customers AS
SELECT * FROM customer WHERE is_active = TRUE;

-- Recent orders (last 30 days)
CREATE OR REPLACE VIEW recent_orders AS
SELECT * FROM `order` 
WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);

-- Pending shipments
CREATE OR REPLACE VIEW pending_shipments AS
SELECT * FROM shipment 
WHERE status NOT IN ('delivered', 'failed');

-- =====================================================
-- USAGE EXAMPLES
-- =====================================================

/*
Instead of:
    SELECT * FROM customer WHERE is_active = TRUE;

You can use:
    SELECT * FROM customers;
    SELECT * FROM active_customers;

Instead of:
    SELECT * FROM product WHERE is_active = TRUE;

You can use:
    SELECT * FROM products;
    SELECT * FROM active_products;

Instead of:
    SELECT * FROM `order`;

You can use:
    SELECT * FROM orders;
*/

-- =====================================================
-- SYNONYM MAPPING TABLE
-- =====================================================

/*
SYNONYM MAPPINGS:

Original Table      | Synonym/Alias         | Description
--------------------|-----------------------|---------------------------
customer            | customers             | Plural form
                    | active_customers      | Active customers only
product             | products              | Plural form
                    | active_products       | Active products only
`order`             | orders                | Plural form (avoids backticks)
                    | recent_orders         | Last 30 days only
category            | categories            | Plural form
payment             | payments              | Plural form
shipment            | shipments             | Plural form
                    | pending_shipments     | Non-delivered only
inventory           | stock                 | Common business term
review              | reviews               | Plural form
cart                | shopping_cart         | Descriptive name
wishlist            | wishlists             | Plural form

BENEFITS:
1. Easier to remember (plural forms match common usage)
2. Avoids backticks for reserved keywords (order → orders)
3. Pre-filtered views for common queries
4. Consistent naming convention
5. Backward compatibility (can keep using original names)
*/

-- =====================================================
-- END OF SYNONYMS
-- Total Synonym Views Created: 14
-- =====================================================
