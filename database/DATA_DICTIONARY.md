# E-COMMERCE DATABASE - DATA DICTIONARY

**Project:** E-Commerce Platform Database  
**Course:** Database Management Systems  
**Database Name:** ecommerce_db  
**Total Tables:** 20  
**Date:** December 2025

---

## TABLE 1: CUSTOMER

**Purpose:** Store customer account information and profile data

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| customer_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique customer identifier |
| name | VARCHAR | 100 | NO | - | - | NOT NULL | Customer full name |
| email | VARCHAR | 100 | NO | UNI, IDX | - | NOT NULL, UNIQUE | Customer email address for login |
| phone | VARCHAR | 20 | YES | - | NULL | - | Contact phone number |
| address | TEXT | - | YES | - | NULL | - | Customer primary address |
| password_hash | VARCHAR | 255 | NO | - | - | NOT NULL | Encrypted password (bcrypt) |
| date_created | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Account creation timestamp |
| is_active | BOOLEAN | - | YES | - | TRUE | DEFAULT | Account status flag |
| loyalty_points | INT | - | YES | - | 0 | DEFAULT | Accumulated loyalty points |
| loyalty_tier | ENUM | - | YES | - | 'Bronze' | VALUES: Bronze, Silver, Gold, Platinum | Customer loyalty tier level |

**Indexes:**
- idx_customer_email (email)
- idx_customer_name (name)

**Sample Data:**
```
customer_id: 1
name: "Ahmed Mohamed"
email: "ahmed@email.com"
phone: "+20123456789"
loyalty_tier: "Silver"
```

---

## TABLE 2: CATEGORY

**Purpose:** Organize products into hierarchical categories

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| category_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique category identifier |
| name | VARCHAR | 100 | NO | UNI, IDX | - | NOT NULL, UNIQUE | Category name |
| parent_category_id | INT | - | YES | FOR | NULL | FK to category(category_ id) | Parent category for hierarchy |
| description | TEXT | - | YES | - | NULL | - | Category description |
| created_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Creation timestamp |

**Relationships:**
- Self-referencing FK: parent_category_id → category(category_id)

**Business Rules:**
- Categories can have subcategories (parent-child relationship)
- Root categories have parent_category_id = NULL

**Sample Data:**
```
category_id: 1, name: "Electronics", parent_category_id: NULL
category_id: 5, name: "Laptops", parent_category_id: 1
```

---

## TABLE 3: PRODUCT

**Purpose:** Store product catalog information

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| product_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique product identifier |
| name | VARCHAR | 200 | NO | IDX | - | NOT NULL | Product name |
| description | TEXT | - | YES | - | NULL | - | Detailed product description |
| price | DECIMAL | 10,2 | NO | IDX | - | NOT NULL, CHECK >= 0 | Product price |
| category_id | INT | - | YES | FOR, IDX | NULL | FK to category(category_id) | Product category |
| image_url | VARCHAR | 255 | YES | - | NULL | - | Product image path |
| weight | DECIMAL | 8,2 | YES | - | NULL | - | Product weight in kg |
| dimensions | VARCHAR | 50 | YES | - | NULL | - | Product dimensions (L x W x H) |
| is_active | BOOLEAN | - | YES | - | TRUE | DEFAULT | Product availability flag |
| created_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Product creation date |
| updated_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | ON UPDATE | Last modification timestamp |

**Indexes:**
- idx_product_name (name)
- idx_product_category (category_id)
- idx_product_price (price)

**Sample Data:**
```
product_id: 101
name: "Dell Laptop XPS 15"
price: 15999.99
category_id: 5
weight: 2.5
```

---

## TABLE 4: WAREHOUSE

**Purpose:** Store warehouse location information

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| warehouse_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique warehouse identifier |
| location | VARCHAR | 200 | NO | - | - | NOT NULL | Warehouse address/location |
| capacity | INT | - | YES | - | NULL | - | Maximum storage capacity |
| manager_name | VARCHAR | 100 | YES | - | NULL | - | Warehouse manager name |
| phone | VARCHAR | 20 | YES | - | NULL | - | Contact phone number |
| created_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Creation timestamp |

**Sample Data:**
```
warehouse_id: 1
location: "Cairo Distribution Center"
capacity: 10000
manager_name: "Mohamed Ali"
```

---

## TABLE 5: INVENTORY

**Purpose:** Track product stock levels across warehouses

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| inventory_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique inventory record ID |
| product_id | INT | - | NO | FOR, IDX, UNI | - | NOT NULL, FK to product | Product reference |
| warehouse_id | INT | - | NO | FOR, IDX, UNI | - | NOT NULL, FK to warehouse | Warehouse reference |
| quantity | INT | - | NO | - | 0 | NOT NULL, CHECK >= 0, DEFAULT | Current stock quantity |
| reorder_level | INT | - | YES | - | 10 | DEFAULT | Minimum stock before reorder |
| last_updated | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | ON UPDATE | Last stock update time |

**Unique Constraint:**
- unique_product_warehouse (product_id, warehouse_id) - One record per product-warehouse combination

**Indexes:**
- idx_inventory_product (product_id)
- idx_inventory_warehouse (warehouse_id)

**Sample Data:**
```
inventory_id: 1, product_id: 101, warehouse_id: 1, quantity: 50, reorder_level: 10
```

---

## TABLE 6: SHIPPING_ADDRESS

**Purpose:** Store customer shipping addresses

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| address_id | INT | - | NO | PRI | AUTO_INCREMENT | PK | Unique address ID |
| customer_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to customer | Customer reference |
| address_label | VARCHAR | 50 | YES | - | NULL | - | Address nickname (Home, Office) |
| street_address | VARCHAR | 255 | NO | - | - | NOT NULL | Street address |
| city | VARCHAR | 100 | NO | - | - | NOT NULL | City name |
| state | VARCHAR | 100 | YES | - | NULL | - | State/Province |
| postal_code | VARCHAR | 20 | NO | - | - | NOT NULL | ZIP/Postal code |
| country | VARCHAR | 100 | NO | - | 'Egypt' | NOT NULL, DEFAULT | Country |
| is_default | BOOLEAN | - | YES | - | FALSE | DEFAULT | Default address flag |

**Sample Data:**
```
address_id: 1
customer_id: 1
address_label: "Home"
street_address: "123 Tahrir Street"
city: "Cairo"
postal_code: "11511"
country: "Egypt"
is_default: TRUE
```

---

## TABLE 7: ORDER

**Purpose:** Customer purchase orders

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| order_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique order identifier |
| customer_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to customer | Customer who placed order |
| order_date | TIMESTAMP | - | YES | IDX | CURRENT_TIMESTAMP | DEFAULT | Order placement date/time |
| status | ENUM | - | YES | IDX | 'pending' | VALUES: pending, processing, shipped, delivered, cancelled, refunded | Order status |
| total_amount | DECIMAL | 10,2 | NO | - | - | NOT NULL, CHECK >= 0 | Final order total |
| shipping_cost | DECIMAL | 8,2 | YES | - | 0 | DEFAULT | Shipping charges |
| tax_amount | DECIMAL | 8,2 | YES | - | 0 | DEFAULT | Tax amount |
| shipping_address_id | INT | - | YES | FOR | NULL | FK to shipping_address | Delivery address |
| payment_method | ENUM | - | YES | - | 'cash_on_delivery' | VALUES: credit_card, paypal, cash_on_delivery | Payment method used |
| notes | TEXT | - | YES | - | NULL | - | Special instructions |

**Indexes:**
- idx_order_customer (customer_id)
- idx_order_date (order_date)
- idx_order_status (status)

**Sample Data:**
```
order_id: 1001
customer_id: 1
status: "delivered"
total_amount: 15999.99
payment_method: "credit_card"
```

---

## TABLE 8: ORDER_ITEM

**Purpose:** Line items/products in each order

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| order_item_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique order item ID |
| order_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to order | Order reference |
| product_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to product | Product ordered |
| quantity | INT | - | NO | - | - | NOT NULL, CHECK > 0 | Quantity ordered |
| unit_price | DECIMAL | 10,2 | NO | - | - | NOT NULL | Price per unit at time of order |
| subtotal | DECIMAL | 10,2 | NO | - | - | NOT NULL | quantity × unit_price |

**Indexes:**
- idx_orderitem_order (order_id)
- idx_orderitem_product (product_id)

**Business Rules:**
- subtotal = quantity × unit_price
- Cannot be modified after order is delivered

**Sample Data:**
```
order_item_id: 1, order_id: 1001, product_id: 101, quantity: 1, unit_price: 15999.99, subtotal: 15999.99
```

---

## TABLE 9: PAYMENT

**Purpose:** Payment transaction records

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| payment_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique payment ID |
| order_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to order | Order being paid for |
| payment_method | ENUM | - | NO | - | - | NOT NULL, VALUES: credit_card, paypal, cash_on_delivery | Payment method |
| amount | DECIMAL | 10,2 | NO | - | - | NOT NULL | Payment amount |
| payment_status | ENUM | - | YES | IDX | 'pending' | VALUES: pending, completed, failed, refunded | Transaction status |
| transaction_id | VARCHAR | 100 | YES | - | NULL | - | External transaction reference |
| payment_date | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Payment timestamp |

**Sample Data:**
```
payment_id: 1
order_id: 1001
payment_method: "credit_card"
amount: 15999.99
payment_status: "completed"
transaction_id: "TXN123456789"
```

---

## TABLE 10: SHIPPING_PROVIDER

**Purpose:** Delivery/courier companies

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| provider_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique provider ID |
| name | VARCHAR | 100 | NO | - | - | NOT NULL | Company name |
| contact_phone | VARCHAR | 20 | YES | - | NULL | - | Contact number |
| contact_email | VARCHAR | 100 | YES | - | NULL | - | Contact email |
| tracking_url_template | VARCHAR | 255 | YES | - | NULL | - | URL pattern for tracking |
| is_active | BOOLEAN | - | YES | - | TRUE | DEFAULT | Active status |

**Sample Data:**
```
provider_id: 1
name: "Aramex Egypt"
contact_phone: "+201234567890"
tracking_url_template: "https://aramex.com/track/{tracking_number}"
```

---

## TABLE 11: SHIPMENT

**Purpose:** Track order deliveries

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
| ------------|-----------|------|------|-----|---------|-------------|-------------|
| shipment_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique shipment ID |
| order_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to order | Order being shipped |
| provider_id | INT | - | YES | FOR | NULL | FK to shipping_provider | Courier company |
| tracking_number | VARCHAR | 100 | YES | IDX | NULL | - | Tracking number |
| shipped_date | TIMESTAMP | - | YES | - | NULL | - | Shipment dispatch date |
| estimated_delivery | TIMESTAMP | - | YES | - | NULL | - | Expected delivery date |
| actual_delivery | TIMESTAMP | - | YES | - | NULL | - | Actual delivery timestamp |
| status | ENUM | - | YES | - | 'preparing' | VALUES: preparing, shipped, in_transit, out_for_delivery, delivered, failed | Delivery status |

**Sample Data:**
```
shipment_id: 1, order_id: 1001, tracking_number: "ARM123456", status: "delivered"
```

---

## TABLE 12: CART

**Purpose:** Shopping cart items for customers

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| cart_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique cart item ID |
| customer_id | INT | - | YES | FOR, IDX | NULL | FK to customer | Customer (NULL for guests) |
| product_id | INT | - | NO | FOR | - | NOT NULL, FK to product | Product in cart |
| quantity | INT | - | NO | - | 1 | NOT NULL, DEFAULT, CHECK > 0 | Quantity |
| added_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | When item was added |
| session_id | VARCHAR | 100 | YES | IDX | NULL | - | For guest users |

**Sample Data:**
```
cart_id: 1, customer_id: 1, product_id: 101, quantity: 1
```

---

## TABLE 13: WISHLIST

**Purpose:** Customer product wishlists

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| wishlist_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique wishlist entry ID |
| customer_id | INT | - | NO | FOR, IDX, UNI | - | NOT NULL, FK to customer | Customer |
| product_id | INT | - | NO | FOR, UNI | - | NOT NULL, FK to product | Desired product |
| added_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Addition timestamp |

**Unique Constraint:**
- unique_customer_product (customer_id, product_id)

**Sample Data:**
```
wishlist_id: 1, customer_id: 1, product_id: 105, added_at: "2025-12-20 10:30:00"
```

---

## TABLE 14: REVIEW

**Purpose:** Product reviews and ratings

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| review_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique review ID |
| product_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to product | Product reviewed |
| customer_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to customer | Reviewer |
| rating | INT | - | NO | IDX | - | NOT NULL, CHECK 1-5 | Star rating (1-5) |
| title | VARCHAR | 200 | YES | - | NULL | - | Review title |
| comment | TEXT | - | YES | - | NULL | - | Review text |
| review_date | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Review submission date |
| is_verified_purchase | BOOLEAN | - | YES | - | FALSE | DEFAULT | Verified buyer flag |

**Sample Data:**
```
review_id: 1, product_id: 101, customer_id: 1, rating: 5, title: "Excellent laptop!", comment: "Great performance..."
```

---

## TABLE 15: COUPON

**Purpose:** Discount coupons/promo codes

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| coupon_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique coupon ID |
| code | VARCHAR | 50 | NO | UNI, IDX | - | NOT NULL, UNIQUE | Coupon code |
| description | VARCHAR | 200 | YES | - | NULL | - | Coupon description |
| discount_type | ENUM | - | NO | - | - | NOT NULL, VALUES: percentage, fixed_amount | Discount type |
| discount_value | DECIMAL | 10,2 | NO | - | - | NOT NULL | Discount value |
| min_order_amount | DECIMAL | 10,2 | YES | - | 0 | DEFAULT | Minimum order for coupon |
| max_discount_amount | DECIMAL | 10,2 | YES | - | NULL | - | Maximum discount cap |
| valid_from | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Coupon start date |
| valid_until | TIMESTAMP | - | YES | - | NULL | - | Expiration date |
| usage_limit | INT | - | YES | - | NULL | - | Max number of uses |
| times_used | INT | - | YES | - | 0 | DEFAULT | Times coupon used |
| is_active | BOOLEAN | - | YES | - | TRUE | DEFAULT | Active status |

**Sample Data:**
```
coupon_id: 1, code: "SUMMER2025", discount_type: "percentage", discount_value: 20.00, min_order_amount: 500.00
```

---

## TABLE 16: ORDER_COUPON

**Purpose:** Track coupon usage in orders

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| order_coupon_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique record ID |
| order_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to order | Order where coupon used |
| coupon_id | INT | - | NO | FOR | - | NOT NULL, FK to coupon | Coupon applied |
| discount_applied | DECIMAL | 10,2 | NO | - | - | NOT NULL | Actual discount amount |

**Sample Data:**
```
order_coupon_id: 1, order_id: 1001, coupon_id: 1, discount_applied: 500.00
```

---

## TABLE 17: ADMIN

**Purpose:** Administrator accounts

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| admin_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique admin ID |
| email | VARCHAR | 100 | NO | UNI, IDX | - | NOT NULL, UNIQUE | Admin email/login |
| password_hash | VARCHAR | 255 | NO | - | - | NOT NULL | Encrypted password |
| role | ENUM | - | YES | - | 'admin' | VALUES: super_admin, admin, inventory_manager, sales_rep | Admin role |
| permissions | JSON | - | YES | - | NULL | - | Permission settings |
| created_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Account creation date |
| last_login | TIMESTAMP | - | YES | - | NULL | - | Last login timestamp |
| is_active | BOOLEAN | - | YES | - | TRUE | DEFAULT | Account status |

**Sample Data:**
```
admin_id: 1, email: "admin@ecommerce.com", role: "super_admin", is_active: TRUE
```

---

## TABLE 18: ADMIN_ACTIVITY_LOG

**Purpose:** Audit trail for admin actions

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| log_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique log entry ID |
| admin_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to admin | Admin who performed action |
| action | VARCHAR | 100 | NO | - | - | NOT NULL | Action performed |
| table_affected | VARCHAR | 50 | YES | - | NULL | - | Database table modified |
| record_id | INT | - | YES | - | NULL | - | Record ID affected |
| details | TEXT | - | YES | - | NULL | - | Additional details |
| ip_address | VARCHAR | 45 | YES | - | NULL | - | IP address of admin |
| created_at | TIMESTAMP | - | YES | IDX | CURRENT_TIMESTAMP | DEFAULT | Action timestamp |

**Sample Data:**
```
log_id: 1, admin_id: 1, action: "UPDATE_PRODUCT", table_affected: "product", record_id: 101
```

---

## TABLE 19: NOTIFICATION

**Purpose:** System notifications

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| notification_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique notification ID |
| type | ENUM | - | NO | IDX | - | NOT NULL, VALUES: LOW_STOCK, ORDER_PLACED, SHIPMENT_UPDATE, PAYMENT_RECEIVED, SYSTEM | Notification type |
| message | TEXT | - | NO | - | - | NOT NULL | Notification message |
| is_read | BOOLEAN | - | YES | IDX | FALSE | DEFAULT | Read status |
| created_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Creation timestamp |

**Sample Data:**
```
notification_id: 1, type: "LOW_STOCK", message: "Product ID 101 stock below reorder level", is_read: FALSE
```

---

## TABLE 20: LOYALTY_TRANSACTION

**Purpose:** Track loyalty points history

| Column Name | Data Type | Size | Null | Key | Default | Constraints | Description |
|-------------|-----------|------|------|-----|---------|-------------|-------------|
| transaction_id | INT | - | NO | PRI | AUTO_INCREMENT | PRIMARY KEY | Unique transaction ID |
| customer_id | INT | - | NO | FOR, IDX | - | NOT NULL, FK to customer | Customer account |
| points | INT | - | NO | - | - | NOT NULL | Points amount (+ or -) |
| transaction_type | ENUM | - | NO | - | - | NOT NULL, VALUES: earned, redeemed, expired | Transaction type |
| order_id | INT | - | YES | FOR | NULL | FK to order | Related order (if applicable) |
| description | VARCHAR | 200 | YES | - | NULL | - | Transaction description |
| created_at | TIMESTAMP | - | YES | - | CURRENT_TIMESTAMP | DEFAULT | Transaction timestamp |

**Sample Data:**
```
transaction_id: 1, customer_id: 1, points: 159, transaction_type: "earned", order_id: 1001, description: "Earned from order #1001"
```

---

## DATABASE RELATIONSHIPS SUMMARY

**One-to-Many Relationships:**
1. customer (1) → order (M)
2. customer (1) → cart (M)
3. customer (1) → wishlist (M)
4. customer (1) → review (M)
5. customer (1) → shipping_address (M)
6. customer (1) → loyalty_transaction (M)
7. product (1) → order_item (M)
8. product (1) → inventory (M)
9. product (1) → cart (M)
10. product (1) → wishlist (M)
11. product (1) → review (M)
12. order (1) → order_item (M)
13. order (1) → payment (M)
14. order (1) → shipment (M)
15. order (1) → order_coupon (M)
16. category (1) → category (M) [Self-referencing]
17. category (1) → product (M)
18. warehouse (1) → inventory (M)
19. shipping_provider (1) → shipment (M)
20. admin (1) → admin_activity_log (M)

**Many-to-Many Relationships (via junction tables):**
- customer ↔ product (via cart)
- customer ↔ product (via wishlist)
- customer ↔ product (via review)
- order ↔ product (via order_item)
- order ↔ coupon (via order_coupon)
- product ↔ warehouse (via inventory)

---

## INDEXING STRATEGY

**Primary Indexes (on all tables):**
- All tables have a PRIMARY KEY (auto-increment INT)

**Foreign Key Indexes:**
- All foreign keys automatically indexed for join performance

**Search/Query Indexes:**
- Customer: email, name
- Product: name, price, category_id
- Order: customer_id, order_date, status
- Inventory: product_id, warehouse_id
- Review: product_id, rating
- Payment: order_id, payment_status
- Cart: customer_id, session_id
- Coupon: code

**Purpose:** Optimize common queries (customer lookup, product search, order history, inventory checks)

---

## DATA INTEGRITY CONSTRAINTS

**Foreign Keys:** ON DELETE behaviors
- CASCADE: Child records deleted when parent deleted
- RESTRICT: Prevent parent deletion if children exist
- SET NULL: Set foreign key to NULL when parent deleted

**Check Constraints:**
- price >= 0
- quantity > 0
- rating BETWEEN 1 AND 5

**Unique Constraints:**
- Email addresses (customer, admin)
- Coupon codes
- Product-warehouse pairs (inventory)
- Customer-product pairs (wishlist)

---

## SECURITY CONSIDERATIONS

1. **Password Storage:** All passwords stored as bcrypt hashes (VARCHAR(255))
2. **Email Validation:** Email fields marked as UNIQUE to prevent duplicates
3. **Data Sanitization:** All TEXT fields should be sanitized before storage
4. **Access Control:** Admin table with role-based permissions (JSON)
5. **Audit Trail:** admin_activity_log tracks all admin actions

---

**END OF DATA DICTIONARY**
**Total Tables Documented:** 20  
**Total Columns:** 188  
**Total Relationships:** 20+ 
**Last Updated:** December 2025
