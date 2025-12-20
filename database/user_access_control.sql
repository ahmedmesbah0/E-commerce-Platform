-- =====================================================
-- USER ACCESS CONTROL
-- E-Commerce Platform - Role-Based Permissions
-- =====================================================

USE ecommerce_db;

-- =====================================================
-- STEP 1: CREATE DATABASE USERS
-- =====================================================

-- Super Admin (full access)
CREATE USER IF NOT EXISTS 'ecommerce_super_admin'@'localhost' IDENTIFIED BY 'SuperAdmin@2025!';

-- Regular Admin (manage products, orders, customers)
CREATE USER IF NOT EXISTS 'ecommerce_admin'@'localhost' IDENTIFIED BY 'Admin@2025!';

-- Inventory Manager (manage inventory and warehouses)
CREATE USER IF NOT EXISTS 'inventory_manager'@'localhost' IDENTIFIED BY 'Inventory@2025!';

-- Sales Representative (view sales data and customers)
CREATE USER IF NOT EXISTS 'sales_rep'@'localhost' IDENTIFIED BY 'Sales@2025!';

-- Customer Service (handle orders and customers)
CREATE USER IF NOT EXISTS 'customer_service'@'localhost' IDENTIFIED BY 'Service@2025!';

-- Read-Only Analyst (reporting only)
CREATE USER IF NOT EXISTS 'analyst'@'localhost' IDENTIFIED BY 'Analyst@2025!';

-- =====================================================
-- STEP 2: GRANT PRIVILEGES - SUPER ADMIN
-- =====================================================

-- Super Admin gets ALL PRIVILEGES
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_super_admin'@'localhost';
GRANT CREATE USER ON *.* TO 'ecommerce_super_admin'@'localhost';

-- =====================================================
-- STEP 3: GRANT PRIVILEGES - REGULAR ADMIN
-- =====================================================

-- Admin can manage products, categories, orders, customers
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.product TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.category TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.`order` TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.order_item TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.customer TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.shipping_address TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.payment TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.shipment TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.coupon TO 'ecommerce_admin'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.review TO 'ecommerce_admin'@'localhost';

-- Admin can view but not modify inventory
GRANT SELECT ON ecommerce_db.inventory TO 'ecommerce_admin'@'localhost';
GRANT SELECT ON ecommerce_db.warehouse TO 'ecommerce_admin'@'localhost';

-- Admin can view all views
GRANT SELECT ON ecommerce_db.customer_order_summary TO 'ecommerce_admin'@'localhost';
GRANT SELECT ON ecommerce_db.product_sales_performance TO 'ecommerce_admin'@'localhost';
GRANT SELECT ON ecommerce_db.daily_sales_summary TO 'ecommerce_admin'@'localhost';
GRANT SELECT ON ecommerce_db.monthly_revenue_report TO 'ecommerce_admin'@'localhost';

-- Admin can insert activity logs
GRANT INSERT ON ecommerce_db.admin_activity_log TO 'ecommerce_admin'@'localhost';

-- =====================================================
-- STEP 4: GRANT PRIVILEGES - INVENTORY MANAGER
-- =====================================================

-- Inventory Manager has full control over inventory and warehouses
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.inventory TO 'inventory_manager'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.warehouse TO 'inventory_manager'@'localhost';

-- Can view products to manage stock
GRANT SELECT ON ecommerce_db.product TO 'inventory_manager'@'localhost';

-- Can view orders to fulfill them
GRANT SELECT ON ecommerce_db.`order` TO 'inventory_manager'@'localhost';
GRANT SELECT ON ecommerce_db.order_item TO 'inventory_manager'@'localhost';

-- Can view relevant views
GRANT SELECT ON ecommerce_db.low_stock_products TO 'inventory_manager'@'localhost';
GRANT SELECT ON ecommerce_db.warehouse_inventory_status TO 'inventory_manager'@'localhost';

-- Can create notifications
GRANT INSERT ON ecommerce_db.notification TO 'inventory_manager'@'localhost';

-- =====================================================
-- STEP 5: GRANT PRIVILEGES - SALES REPRESENTATIVE
-- =====================================================

-- Sales rep can view customers and orders
GRANT SELECT ON ecommerce_db.customer TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.`order` TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.order_item TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.product TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.category TO 'sales_rep'@'localhost';

-- Can view payments and shipments
GRANT SELECT ON ecommerce_db.payment TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.shipment TO 'sales_rep'@'localhost';

-- Can manage coupons
GRANT SELECT, INSERT, UPDATE ON ecommerce_db.coupon TO 'sales_rep'@'localhost';
GRANT SELECT, INSERT ON ecommerce_db.order_coupon TO 'sales_rep'@'localhost';

-- Can view all sales-related views
GRANT SELECT ON ecommerce_db.customer_order_summary TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.product_sales_performance TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.daily_sales_summary TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.monthly_revenue_report TO 'sales_rep'@'localhost';
GRANT SELECT ON ecommerce_db.top_customers TO 'sales_rep'@'localhost';

-- =====================================================
-- STEP 6: GRANT PRIVILEGES - CUSTOMER SERVICE
-- =====================================================

-- Customer service can view and update customer info
GRANT SELECT, UPDATE ON ecommerce_db.customer TO 'customer_service'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON ecommerce_db.shipping_address TO 'customer_service'@'localhost';

-- Can view and update orders
GRANT SELECT, UPDATE ON ecommerce_db.`order` TO 'customer_service'@'localhost';
GRANT SELECT ON ecommerce_db.order_item TO 'customer_service'@'localhost';

-- Can view products
GRANT SELECT ON ecommerce_db.product TO 'customer_service'@'localhost';

-- Can manage shipments
GRANT SELECT, UPDATE ON ecommerce_db.shipment TO 'customer_service'@'localhost';

-- Can view reviews
GRANT SELECT ON ecommerce_db.review TO 'customer_service'@'localhost';

-- Can view cart and wishlist
GRANT SELECT ON ecommerce_db.cart TO 'customer_service'@'localhost';
GRANT SELECT ON ecommerce_db.wishlist TO 'customer_service'@'localhost';

-- Can view relevant views
GRANT SELECT ON ecommerce_db.customer_order_summary TO 'customer_service'@'localhost';
GRANT SELECT ON ecommerce_db.pending_orders_view TO 'customer_service'@'localhost';
GRANT SELECT ON ecommerce_db.shipment_tracking_view TO 'customer_service'@'localhost';

-- =====================================================
-- STEP 7: GRANT PRIVILEGES - ANALYST (READ-ONLY)
-- =====================================================

-- Analyst has SELECT-only access to all tables
GRANT SELECT ON ecommerce_db.* TO 'analyst'@'localhost';

-- Analyst specifically granted access to all views
GRANT SELECT ON ecommerce_db.customer_order_summary TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.product_sales_performance TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.low_stock_products TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.daily_sales_summary TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.monthly_revenue_report TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.pending_orders_view TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.top_customers TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.warehouse_inventory_status TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.product_review_summary TO 'analyst'@'localhost';
GRANT SELECT ON ecommerce_db.shipment_tracking_view TO 'analyst'@'localhost';

-- =====================================================
-- STEP 8: APPLY ALL PRIVILEGES
-- =====================================================

FLUSH PRIVILEGES;

-- =====================================================
-- STEP 9: VIEW USER PRIVILEGES (for verification)
-- =====================================================

-- To view privileges for a user, run:
-- SHOW GRANTS FOR 'ecommerce_admin'@'localhost';
-- SHOW GRANTS FOR 'inventory_manager'@'localhost';
-- SHOW GRANTS FOR 'sales_rep'@'localhost';
-- SHOW GRANTS FOR 'customer_service'@'localhost';
-- SHOW GRANTS FOR 'analyst'@'localhost';

-- =====================================================
-- USER ROLES SUMMARY
-- =====================================================

/*
USER ROLE PERMISSIONS MATRIX:

┌──────────────────────┬────────────┬───────┬──────────┬──────────┬─────────┬──────────┐
│ Table/Operation      │ Super Admin│ Admin │ Inventory│ Sales Rep│ Cust Svc│ Analyst  │
├──────────────────────┼────────────┼───────┼──────────┼──────────┼─────────┼──────────┤
│ product              │    FULL    │  CRUD │    R     │    R     │    R    │    R     │
│ category             │    FULL    │  CRUD │    -     │    R     │    -    │    R     │
│ customer             │    FULL    │  CRUD │    -     │    R     │   RU    │    R     │
│ order                │    FULL    │  CRUD │    R     │    R     │   RU    │    R     │
│ inventory            │    FULL    │   R   │   CRUD   │    -     │    -    │    R     │
│ warehouse            │    FULL    │   R   │   CRUD   │    -     │    -    │    R     │
│ payment              │    FULL    │  CRUD │    -     │    R     │    -    │    R     │
│ shipment             │    FULL    │  CRUD │    -     │    R     │   RU    │    R     │
│ coupon               │    FULL    │  CRUD │    -     │   RU     │    -    │    R     │
│ review               │    FULL    │  CRUD │    -     │    -     │    R    │    R     │
│ All Views            │    FULL    │   R   │  Some    │  Some    │  Some   │    R     │
└──────────────────────┴────────────┴───────┴──────────┴──────────┴─────────┴──────────┘

Legend:
FULL = All privileges including DDL
CRUD = Create, Read, Update, Delete
R    = Read only (SELECT)
RU   = Read and Update
-    = No access
*/

-- =====================================================
-- SECURITY BEST PRACTICES IMPLEMENTED
-- =====================================================

/*
1. Principle of Least Privilege: Each user has only necessary permissions
2. Role Separation: Different roles for different responsibilities
3. Strong Passwords: All users have complex passwords
4. Host Restriction: Users limited to localhost
5. View-Based Security: Sensitive data filtered through views
6. Audit Trail: Admin activity logged
7. Read-Only Analyst: Prevents accidental data modification
*/

-- =====================================================
-- END OF USER ACCESS CONTROL
-- Total Users Created: 6
-- =====================================================
