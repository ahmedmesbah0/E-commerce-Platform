# E-Commerce Platform
## Data Dictionary Documentation

**Project Name**: Comprehensive E-Commerce Management System  
**Database**: ecommerce_db  
**DBMS**: MySQL 5.7+  
**Character Set**: utf8mb4  
**Date**: December 2025

---

## Table of Contents

1. [User Management Tables](#user-management-tables)
2. [Product Management Tables](#product-management-tables)
3. [Order Management Tables](#order-management-tables)
4. [Payment Tables](#payment-tables)
5. [Shipping & Delivery Tables](#shipping--delivery-tables)
6. [Support & Communication Tables](#support--communication-tables)
7. [System & Configuration Tables](#system--configuration-tables)

---

## User Management Tables

### 1. CUSTOMER

**Purpose**: Stores customer account information

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| customer_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique customer identifier |
| name | VARCHAR(100) | NOT NULL | Customer full name |
| email | VARCHAR(100) | NOT NULL, UNIQUE | Email address for login |
| password_hash | VARCHAR(255) | NOT NULL | Encrypted password (bcrypt) |
| phone | VARCHAR(20) | NULL | Contact phone number |
| address | TEXT | NULL | Default shipping address |
| date_created | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation date |
| last_login | TIMESTAMP | NULL | Last login timestamp |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |

**Indexes**: email, date_created  
**Relationships**: Referenced by cart, order, wishlist, review

---

### 2. ADMIN

**Purpose**: Administrator accounts for system management

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| admin_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique admin identifier |
| name | VARCHAR(100) | NOT NULL | Administrator name |
| email | VARCHAR(100) | NOT NULL, UNIQUE | Admin email |
| password_hash | VARCHAR(255) | NOT NULL | Encrypted password |
| role | VARCHAR(50) | NOT NULL | Admin role/permissions |
| date_created | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |

**Indexes**: email, role  
**Relationships**: Referenced by system_log

---

### 3. SELLER

**Purpose**: Vendor/seller accounts

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| seller_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique seller identifier |
| name | VARCHAR(100) | NOT NULL | Seller/company name |
| email | VARCHAR(100) | NOT NULL, UNIQUE | Contact email |
| password_hash | VARCHAR(255) | NOT NULL | Encrypted password |
| business_name | VARCHAR(200) | NULL | Registered business name |
| tax_id | VARCHAR(50) | NULL | Tax identification number |
| phone | VARCHAR(20) | NULL | Contact phone |
| address | TEXT | NULL | Business address |
| commission_rate | DECIMAL(5,2) | DEFAULT 10.00 | Platform commission % |
| date_joined | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration date |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |

**Indexes**: email, is_active  
**Relationships**: Referenced by product

---

## Product Management Tables

### 4. CATEGORY

**Purpose**: Product categorization hierarchy

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| category_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique category identifier |
| name | VARCHAR(100) | NOT NULL | Category name |
| description | TEXT | NULL | Category description |
| parent_category_id | INT | NULL, FOREIGN KEY | Parent category for hierarchy |
| image_url | VARCHAR(255) | NULL | Category image |
| display_order | INT | DEFAULT 0 | Sort order for display |
| is_active | BOOLEAN | DEFAULT TRUE | Visibility status |

**Indexes**: parent_category_id, is_active  
**Relationships**: Self-referencing (parent_category_id), Referenced by product

---

### 5. BRAND

**Purpose**: Product brand information

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| brand_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique brand identifier |
| name | VARCHAR(100) | NOT NULL, UNIQUE | Brand name |
| description | TEXT | NULL | Brand description |
| logo_url | VARCHAR(255) | NULL | Brand logo image |
| website | VARCHAR(255) | NULL | Brand website |
| is_active | BOOLEAN | DEFAULT TRUE | Status |

**Indexes**: name, is_active  
**Relationships**: Referenced by product

---

### 6. PRODUCT

**Purpose**: Core product catalog

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| product_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique product identifier |
| name | VARCHAR(200) | NOT NULL | Product name |
| description | TEXT | NULL | Product description |
| sku | VARCHAR(100) | UNIQUE | Stock keeping unit |
| category_id | INT | NULL, FOREIGN KEY | Product category |
| brand_id | INT | NULL, FOREIGN KEY | Product brand |
| seller_id | INT | NULL, FOREIGN KEY | Seller/vendor |
| price | DECIMAL(10,2) | NOT NULL, CHECK >= 0 | Product price |
| cost_price | DECIMAL(10,2) | NULL | Wholesale/cost price |
| weight | DECIMAL(8,2) | NULL | Product weight (kg) |
| dimensions | VARCHAR(100) | NULL | Product dimensions |
| is_featured | BOOLEAN | DEFAULT FALSE | Featured status |
| is_active | BOOLEAN | DEFAULT TRUE | Product availability |
| date_created | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation date |

**Indexes**: sku, category_id, brand_id, seller_id, price, is_active  
**Relationships**: References category, brand, seller; Referenced by inventory, cart_item, order_item, review

---

### 7. INVENTORY

**Purpose**: Track stock levels across warehouses

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| inventory_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique inventory identifier |
| product_id | INT | NOT NULL, FOREIGN KEY | Product reference |
| warehouse_id | INT | NOT NULL, FOREIGN KEY | Warehouse location |
| quantity | INT | NOT NULL, CHECK >= 0 | Available quantity |
| reserved_quantity | INT | DEFAULT 0, CHECK >= 0 | Reserved for orders |
| reorder_level | INT | DEFAULT 10 | Minimum stock threshold |
| reorder_quantity | INT | DEFAULT 50 | Reorder amount |
| last_updated | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Last stock update |

**Indexes**: product_id, warehouse_id, quantity  
**Relationships**: References product, warehouse

---

### 8. WAREHOUSE

**Purpose**: Storage facility information

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| warehouse_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique warehouse identifier |
| name | VARCHAR(100) | NOT NULL | Warehouse name |
| location | VARCHAR(255) | NOT NULL | Physical address |
| phone | VARCHAR(20) | NULL | Contact phone |
| manager_name | VARCHAR(100) | NULL | Manager name |
| capacity | INT | NULL | Storage capacity |
| is_active | BOOLEAN | DEFAULT TRUE | Operational status |

**Indexes**: is_active  
**Relationships**: Referenced by inventory

---

## Order Management Tables

### 9. CART

**Purpose**: Shopping cart for each customer

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| cart_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique cart identifier |
| customer_id | INT | NOT NULL, UNIQUE, FOREIGN KEY | Cart owner |
| date_created | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Cart creation |
| last_updated | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Last modification |

**Indexes**: customer_id  
**Relationships**: References customer; Referenced by cart_item

---

### 10. CART_ITEM

**Purpose**: Items in shopping cart

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| cart_item_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique item identifier |
| cart_id | INT | NOT NULL, FOREIGN KEY | Cart reference |
| product_id | INT | NOT NULL, FOREIGN KEY | Product reference |
| quantity | INT | NOT NULL, CHECK > 0 | Item quantity |
| price | DECIMAL(10,2) | NOT NULL | Price at time of add |
| added_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Add timestamp |

**Indexes**: cart_id, product_id  
**Relationships**: References cart, product  
**Unique Constraint**: (cart_id, product_id)

---

### 11. ORDER

**Purpose**: Customer orders

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| order_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique order identifier |
| customer_id | INT | NOT NULL, FOREIGN KEY | Customer reference |
| order_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Order placement date |
| status | ENUM | 'pending','processing','shipped','delivered','cancelled','refunded' | Order status |
| subtotal | DECIMAL(10,2) | NOT NULL | Items subtotal |
| tax_amount | DECIMAL(10,2) | DEFAULT 0 | Tax amount |
| shipping_cost | DECIMAL(10,2) | DEFAULT 0 | Shipping cost |
| discount_amount | DECIMAL(10,2) | DEFAULT 0 | Discount applied |
| total_amount | DECIMAL(10,2) | NOT NULL | Final total |
| shipping_address | TEXT | NOT NULL | Delivery address |
| billing_address | TEXT | NULL | Billing address |
| coupon_id | INT | NULL, FOREIGN KEY | Applied coupon |
| notes | TEXT | NULL | Order notes |

**Indexes**: customer_id, order_date, status  
**Relationships**: References customer, coupon; Referenced by order_item, payment, shipment

---

### 12. ORDER_ITEM

**Purpose**: Line items in orders

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| order_item_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique item identifier |
| order_id | INT | NOT NULL, FOREIGN KEY | Order reference |
| product_id | INT | NOT NULL, FOREIGN KEY | Product reference |
| quantity | INT | NOT NULL, CHECK > 0 | Ordered quantity |
| price | DECIMAL(10,2) | NOT NULL | Price at order time |
| subtotal | DECIMAL(10,2) | NOT NULL | Line total |

**Indexes**: order_id, product_id  
**Relationships**: References order, product

---

### 13. COUPON

**Purpose**: Discount codes and promotions

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| coupon_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique coupon identifier |
| code | VARCHAR(50) | NOT NULL, UNIQUE | Coupon code |
| discount_type | ENUM | 'percentage', 'fixed' | Discount type |
| discount_value | DECIMAL(10,2) | NOT NULL | Discount amount/% |
| min_purchase_amount | DECIMAL(10,2) | DEFAULT 0 | Minimum order value |
| max_discount | DECIMAL(10,2) | NULL | Maximum discount cap |
| usage_limit | INT | DEFAULT 1 | Total usage limit |
| times_used | INT | DEFAULT 0 | Usage counter |
| expiry_date | DATE | NULL | Expiration date |
| is_active | BOOLEAN | DEFAULT TRUE | Status |

**Indexes**: code, expiry_date, is_active  
**Relationships**: Referenced by order

---

## Payment Tables

### 14. PAYMENT

**Purpose**: Payment transactions

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| payment_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique payment identifier |
| order_id | INT | NOT NULL, FOREIGN KEY | Order reference |
| payment_gateway_id | INT | NOT NULL, FOREIGN KEY | Gateway used |
| payment_method | VARCHAR(50) | NOT NULL | Payment method |
| amount | DECIMAL(10,2) | NOT NULL | Payment amount |
| currency | VARCHAR(3) | DEFAULT 'USD' | Currency code |
| transaction_id | VARCHAR(255) | NULL | Gateway transaction ID |
| status | ENUM | 'pending','completed','failed','refunded' | Payment status |
| payment_date | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Payment timestamp |

**Indexes**: order_id, transaction_id, status  
**Relationships**: References order, payment_gateway

---

### 15. PAYMENT_GATEWAY

**Purpose**: Payment processor configuration

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| payment_gateway_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique gateway identifier |
| name | VARCHAR(100) | NOT NULL | Gateway name |
| api_key | VARCHAR(255) | NULL | API credential |
| secret_key | VARCHAR(255) | NULL | Secret credential |
| is_active | BOOLEAN | DEFAULT TRUE | Status |

**Indexes**: is_active  
**Relationships**: Referenced by payment

---

### 16. TRANSACTION_LOG

**Purpose**: Complete transaction history

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| transaction_log_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique log identifier |
| order_id | INT | NULL, FOREIGN KEY | Related order |
| transaction_type | VARCHAR(50) | NOT NULL | Transaction type |
| amount | DECIMAL(10,2) | NOT NULL | Transaction amount |
| description | TEXT | NULL | Description |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Log timestamp |

**Indexes**: order_id, transaction_type, created_at  
**Relationships**: References order

---

## Shipping & Delivery Tables

### 17. SHIPMENT

**Purpose**: Shipment tracking

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| shipment_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique shipment identifier |
| order_id | INT | NOT NULL, FOREIGN KEY | Order reference |
| delivery_partner_id | INT | NULL, FOREIGN KEY | Delivery company |
| tracking_number | VARCHAR(100) | UNIQUE | Tracking code |
| status | ENUM | 'pending','in_transit','delivered','returned' | Shipment status |
| shipped_date | TIMESTAMP | NULL | Ship date |
| estimated_delivery | DATE | NULL | ETA |
| actual_delivery | TIMESTAMP | NULL | Actual delivery time |
| packaging_id | INT | NULL, FOREIGN KEY | Package type |

**Indexes**: order_id, tracking_number, status  
**Relationships**: References order, delivery_partner, packaging

---

### 18. DELIVERY_PARTNER

**Purpose**: Shipping companies

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| delivery_partner_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique partner identifier |
| name | VARCHAR(100) | NOT NULL | Partner name |
| phone | VARCHAR(20) | NULL | Contact phone |
| email | VARCHAR(100) | NULL | Contact email |
| service_type | VARCHAR(100) | NULL | Service level |
| base_rate | DECIMAL(10,2) | NULL | Base shipping rate |
| is_active | BOOLEAN | DEFAULT TRUE | Status |

**Indexes**: is_active  
**Relationships**: Referenced by shipment

---

## Support & Communication Tables

### 19. SUPPORT_TICKET

**Purpose**: Customer support tickets

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| support_ticket_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique ticket identifier |
| customer_id | INT | NOT NULL, FOREIGN KEY | Customer reference |
| support_rep_id | INT | NULL, FOREIGN KEY | Assigned rep |
| subject | VARCHAR(200) | NOT NULL | Ticket subject |
| description | TEXT | NOT NULL | Issue description |
| priority | ENUM | 'low','medium','high','urgent' | Priority level |
| status | ENUM | 'open','in_progress','resolved','closed' | Ticket status |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |
| resolved_at | TIMESTAMP | NULL | Resolution time |

**Indexes**: customer_id, support_rep_id, status, priority  
**Relationships**: References customer, support_rep

---

### 20. REVIEW

**Purpose**: Product reviews and ratings

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| review_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique review identifier |
| product_id | INT | NOT NULL, FOREIGN KEY | Product reference |
| customer_id | INT | NOT NULL, FOREIGN KEY | Reviewer |
| rating | INT | NOT NULL, CHECK 1-5 | Star rating (1-5) |
| title | VARCHAR(200) | NULL | Review title |
| comment | TEXT | NULL | Review text |
| is_verified_purchase | BOOLEAN | DEFAULT FALSE | Verified buyer |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Review date |
| is_approved | BOOLEAN | DEFAULT TRUE | Moderation status |

**Indexes**: product_id, customer_id, rating  
**Relationships**: References product, customer

---

### 21. NOTIFICATION

**Purpose**: User notifications

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| notification_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique notification ID |
| customer_id | INT | NOT NULL, FOREIGN KEY | Recipient |
| type | VARCHAR(50) | NOT NULL | Notification type |
| title | VARCHAR(200) | NOT NULL | Notification title |
| message | TEXT | NOT NULL | Notification content |
| is_read | BOOLEAN | DEFAULT FALSE | Read status |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation time |

**Indexes**: customer_id, is_read, created_at  
**Relationships**: References customer

---

## System & Configuration Tables

### 22. LOYALTY_PROGRAM

**Purpose**: Customer loyalty and rewards

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| loyalty_program_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique program identifier |
| customer_id | INT | NOT NULL, UNIQUE, FOREIGN KEY | Member |
| points | INT | DEFAULT 0 | Current points |
| tier | ENUM | 'bronze','silver','gold','platinum' | Membership tier |
| points_earned | INT | DEFAULT 0 | Total points earned |
| points_redeemed | INT | DEFAULT 0 | Total points used |
| tier_start_date | DATE | NULL | Current tier start |

**Indexes**: customer_id, tier  
**Relationships**: References customer

---

### 23. SYSTEM_LOG

**Purpose**: System activity audit trail

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|-------------|-------------|
| system_log_id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique log identifier |
| admin_id | INT | NULL, FOREIGN KEY | Admin user |
| action | VARCHAR(100) | NOT NULL | Action performed |
| description | TEXT | NULL | Action details |
| ip_address | VARCHAR(45) | NULL | IP address |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Log timestamp |

**Indexes**: admin_id, action, created_at  
**Relationships**: References admin

---

## Summary Statistics

- **Total Tables**: 39
- **Total Columns**: 300+
- **Primary Keys**: 39
- **Foreign Keys**: 45+
- **Indexes**: 100+
- **Check Constraints**: 20+
- **Unique Constraints**: 15+

---

## Database Normalization

All tables follow **Third Normal Form (3NF)**:
- ✓ No repeating groups (1NF)
- ✓ No partial dependencies (2NF)
- ✓ No transitive dependencies (3NF)

---

**Document Version**: 1.0  
**Last Updated**: December 20, 2025  
**Maintained By**: Database Team
