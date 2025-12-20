# E-COMMERCE DATABASE MANAGEMENT SYSTEM
## Academic Project Documentation

**Course:** Database Management Systems  
**Semester:** Fall 2025/2026  
**Submission Date:** December 2025

---

## PROJECT TEAM

| Role | Name | Student ID | Email |
|------|------|------------|-------|
| **Team Leader** | [Your Name] | [Your ID] | [your.email@university.edu] |
| Member 1 | [Member 1 Name] | [ID] | [email] |
| Member 2 | [Member 2 Name] | [ID] | [email] |
| Member 3 | [Member 3 Name] | [ID] | [email] |
| Member 4 | [Member 4 Name] | [ID] | [email] |

**Instructor:** Dr. [Instructor Name]  
**Department:** Computer Science  
**University:** [University Name]

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)
2. [Business Requirements (R#1)](#2-business-requirements)
3. [Entity-Relationship Diagram (R#2)](#3-entity-relationship-diagram)
4. [Database Schema & Data Dictionary (R#3)](#4-database-schema--data-dictionary)
5. [Query Reports & Relational Algebra (R#4)](#5-query-reports--relational-algebra)
6. [Advanced Features (Bonus)](#6-advanced-features-bonus)
7. [GUI Implementation (Bonus)](#7-gui-implementation-bonus)
8. [Testing & Validation](#8-testing--validation)
9. [Conclusion](#9-conclusion)
10. [Appendices](#10-appendices)

---

## 1. INTRODUCTION

### 1.1 Project Overview
The E-Commerce Platform is a comprehensive database management system designed to handle all aspects of online retail operations. The system manages products, customers, orders, payments, inventory, shipping, and administrative functions.

### 1.2 Objectives
- Design and implement a normalized relational database
- Create efficient data structures for e-commerce operations
- Implement business logic through triggers and stored procedures
- Develop reporting views for analytics
- Create a user-friendly GUI for database interaction
- Implement robust security with role-based access control

### 1.3 Scope
The system covers:
- Customer account management
- Product catalog and categorization
- Shopping cart functionality
- Order processing and tracking
- Payment handling
- Inventory management across warehouses
- Shipping and delivery tracking
- Customer reviews and ratings
- Loyalty program
- Administrative controls

### 1.4 Technologies Used
- **Database:** MySQL 8.0+
- **GUI:** PHP, HTML, CSS, JavaScript
- **Server:** Apache/Nginx
- **Tools:** phpMyAdmin, MySQL Workbench
- **Design:** Draw.io (ERD diagrams)

---

## 2. BUSINESS REQUIREMENTS (R#1)

### 2.1 Stakeholder Analysis

#### Primary Stakeholders

**1. Customers**
- Requirements:
  - Easy product browsing and search
  - Secure account management
  - Simple checkout process
  - Order tracking
  - Product reviews
  - Wishlist functionality
- Success Criteria:
  - Can complete purchase in < 5 clicks
  - 24/7 system availability
  - Real-time inventory updates

**2. System Administrators**
- Requirements:
  - Full system control
  - User management
  - System monitoring
  - Report generation
  - Data backup and recovery
- Success Criteria:
  - Complete audit trail
  - Role-based access control
  - Automated backups

**3. Inventory Managers**
- Requirements:
  - Stock level monitoring
  - Low stock alerts
  - Warehouse management
  - Supplier coordination
- Success Criteria:
  - Real-time inventory tracking
  - Automated reorder notifications
  - Multi-warehouse support

**4. Sales Representatives**
- Requirements:
  - Customer analytics
  - Sales reporting
  - Coupon management
  - Performance metrics
- Success Criteria:
  - Sales dashboards
  - Customer lifetime value tracking
  - Revenue reports

**5. Customer Service**
- Requirements:
  - Order management
  - Customer information access
  - Shipment tracking
  - Issue resolution
- Success Criteria:
  - Quick customer lookup
  - Order status updates
  - Communication logs

### 2.2 Functional Requirements

#### FR1: Product Management
- Add, update, delete products
- Categorize products hierarchically
- Track product attributes (price, weight, dimensions)
- Manage product images
- Track product availability

#### FR2: Customer Management
- User registration and authentication
- Profile management
- Multiple shipping addresses
- Order history
- Loyalty points tracking

#### FR3: Order Processing
- Shopping cart management
- Checkout process
- Multiple payment methods
- Order confirmation
- Order status tracking

#### FR4: Inventory Management
- Multi-warehouse support
- Real-time stock tracking
- Automatic reorder alerts
- Stock level history

#### FR5: Payment Processing
- Credit card, PayPal, Cash on Delivery
- Payment verification
- Refund processing
- Transaction logging

#### FR6: Shipping & Delivery
- Shipping provider integration
- Tracking number generation
- Delivery status updates
- Estimated delivery dates

#### FR7: Reviews & Ratings
- Customer product reviews
- Star ratings
- Verified purchase badges
- Review moderation

#### FR8: Loyalty Program
- Points accumulation
- Tier management (Bronze, Silver, Gold, Platinum)
- Reward redemption

### 2.3 Non-Functional Requirements

#### NFR1: Scalability
- Support 10,000+ concurrent users
- Handle millions of products
- Process thousands of orders daily

#### NFR2: Security
- Encrypted password storage (bcrypt)
- SQL injection prevention
- Role-based access control
- Session security
- PCI DSS compliance for payments

#### NFR3: Performance
- Page load < 2 seconds
- Query response < 500ms
- 99.9% uptime

#### NFR4: Backup & Recovery
- Daily automated backups
- Point-in-time recovery
- Disaster recovery plan

#### NFR5: Usability
- Intuitive user interface
- Mobile-responsive design
- Accessibility compliance

---

## 3. ENTITY-RELATIONSHIP DIAGRAM (R#2)

### 3.1 ERD Overview
The database design is based on the ERD diagram: `E-Commerce_updated3-dbms.drawio`

**Total Entities:** 20  
**Total Relationships:** 25+  
**Normalization Level:** 3NF (Third Normal Form)

### 3.2 Main Entities

#### Core Entities
1. **CUSTOMER** - Customer accounts and profiles
2. **PRODUCT** - Product catalog
3. **CATEGORY** - Product categories (hierarchical)
4. **ORDER** - Customer orders
5. **ORDER_ITEM** - Order line items
6. **PAYMENT** - Payment transactions
7. **SHIPMENT** - Delivery tracking

#### Supporting Entities
8. **INVENTORY** - Product stock levels
9. **WAREHOUSE** - Storage locations
10. **SHIPPING_ADDRESS** - Delivery addresses
11. **CART** - Shopping cart items
12. **WISHLIST** - Customer wishlists
13. **REVIEW** - Product reviews
14. **COUPON** - Discount coupons

#### Administrative Entities
15. **ADMIN** - Administrator accounts
16. **ADMIN_ACTIVITY_LOG** - Audit trail
17. **NOTIFICATION** - System notifications
18. **LOYALTY_TRANSACTION** - Points history
19. **SHIPPING_PROVIDER** - Courier companies
20. **ORDER_COUPON** - Coupon usage tracking

### 3.3 Key Relationships

**One-to-Many:**
- Customer → Orders (1:M)
- Product → Order_Items (1:M)
- Category → Products (1:M)
- Warehouse → Inventory (1:M)

**Many-to-Many:**
- Customers ↔ Products (via Cart, Wishlist, Reviews)
- Orders ↔ Products (via Order_Items)
- Orders ↔ Coupons (via Order_Coupon)

**Self-Referencing:**
- Category → Category (parent-child hierarchy)

### 3.4 Business Rules

1. A customer can place multiple orders
2. An order must belong to exactly one customer
3. An order contains one or more products
4. A product can belong to one category
5. Categories can have subcategories (hierarchical)
6. Inventory is tracked per product-warehouse combination
7. Each order can use at most one coupon
8. A product can have multiple reviews from different customers
9. Cart items belong to a customer or guest session
10. Loyalty points are earned on order delivery

---

## 4. DATABASE SCHEMA & DATA DICTIONARY (R#3)

### 4.1 Schema Overview
- **Total Tables:** 20
- **Total Columns:** 188
- **Storage Engine:** InnoDB
- **Character Set:** utf8mb4
- **Collation:** utf8mb4_unicode_ci

### 4.2 Schema Files
1. `schema_phpmyadmin.sql` - Complete database schema
2. `DATA_DICTIONARY.md` - Comprehensive data dictionary

### 4.3 Key Design Decisions

**Normalization:**
- All tables in 3NF to eliminate redundancy
- Separate junction tables for M:M relationships
- Attribute atomicity enforced

**Data Integrity:**
- Foreign key constraints with appropriate ON DELETE actions
- CHECK constraints for data validation
- UNIQUE constraints on business keys
- NOT NULL constraints on required fields

**Indexing Strategy:**
- Primary keys on all tables
- Foreign keys automatically indexed
- Additional indexes on frequently queried columns
- Composite indexes for multi-column searches

**Data Types:**
- DECIMAL for monetary values (precision: 10,2)
- TIMESTAMP for all date/time values
- ENUM for status fields
- JSON for flexible data (permissions)
- TEXT for variable-length content

---

## 5. QUERY REPORTS & RELATIONAL ALGEBRA (R#4)

### 5.1 Report List
1. Product Catalog by Category
2. Customer Order Summary
3. Top Selling Products
4. Low Stock Alert
5. Revenue by Month
6. Customer Purchase History
7. Products Without Orders
8. Customers by Category Interest
9. Most Valuable Customers
10. Inventory Status by Warehouse

*See Section 10.2 (Appendix B) for complete SQL queries and relational algebra*

### 5.2 Query Techniques Used
- ✅ Aggregate Functions: COUNT, SUM, AVG, MAX, MIN
- ✅ Set Operators: UNION, EXCEPT (NOT IN)
- ✅ Conditions: WHERE, HAVING
- ✅ Joins: INNER, LEFT, RIGHT
- ✅ Subqueries: Scalar, Correlated
- ✅ GROUP BY, ORDER BY
- ✅ DISTINCT
- ✅ Date Functions
- ✅ String Functions

---

## 6. ADVANCED FEATURES (BONUS)

### 6.1 Database Views
**Created:** 10 views for reporting and analytics

**Files:** `database/views.sql`

**Views:**
1. customer_order_summary
2. product_sales_performance
3. low_stock_products
4. daily_sales_summary
5. monthly_revenue_report
6. pending_orders_view
7. top_customers
8. warehouse_inventory_status
9. product_review_summary
10. shipment_tracking_view

### 6.2 Synonyms
**Created:** 14 synonym views (MySQL alternative)

**File:** `database/synonyms.sql`

**Purpose:** Easier table access and plural naming conventions

### 6.3 User Access Control
**Created:** 6 role-based user accounts

**File:** `database/user_access_control.sql`

**Roles:**
1. Super Admin - Full access
2. Regular Admin - Manage products, orders, customers
3. Inventory Manager - Manage inventory and warehouses
4. Sales Representative - View sales data
5. Customer Service - Handle orders and customers
6. Analyst - Read-only reporting

**Security Features:**
- Principle of least privilege
- Strong password requirements
- Host-based restrictions
- Audit logging

### 6.4 Triggers
**Created:** Database triggers for automation

**Examples:**
- Update inventory on order placement
- Low stock notifications
- Loyalty points calculation
- Order total calculation

### 6.5 Indexes
**Created:** Strategic indexes for performance

**Types:**
- Primary key indexes (all tables)
- Foreign key indexes (automatic)
- Search indexes (name, email, SKU)
- Multi-column indexes for complex queries

---

## 7. GUI IMPLEMENTATION (BONUS)

### 7.1 GUI Overview
The system includes a complete web-based GUI built with PHP.

**Access URL:** http://localhost:8000

### 7.2 User-Facing Features

**Public Pages:**
- Homepage with featured products
- Product listing and search
- Product details with reviews
- Shopping cart
- Checkout process
- Order confirmation
- User registration and login

**Customer Dashboard:**
- Order history
- Profile management
- Wishlist
- Loyalty points balance

### 7.3 Administrative Features

**Admin Panel:** http://localhost:8000/admin/

**Features:**
1. **Dashboard**
   - Statistics cards (customers, products, orders, revenue)
   - Recent orders table
   - Top products
   - Quick actions

2. **Product Management**
   - Add/Edit/Delete products
   - Category assignment
   - Inventory tracking
   - Product search and filtering

3. **Category Management**
   - Add/Edit/Delete categories
   - Product count per category
   - Category hierarchy

4. **Order Management**
   - View all orders
   - Update order status
   - Filter by status
   - Order details

5. **Customer Management**
   - Customer list
   - Customer details
   - Order history
   - Loyalty tier management

### 7.4 DML Operations Implemented

**INSERT:**
- Add new products
- Register customers
- Place orders
- Add to cart
- Create categories
- Add coupons

**UPDATE:**
- Modify product details
- Update customer information
- Change order status
- Update inventory levels
- Modify categories

**DELETE:**
- Remove products
- Delete categories
- Cancel orders
- Remove cart items

**SELECT:**
- Browse products
- Search functionality
- View order history
- Check inventory
- View reports

### 7.5 Screenshots
*See Appendix C for GUI screenshots*

---

## 8. TESTING & VALIDATION

### 8.1 Test Cases

**Functional Testing:**
- User registration and login ✅
- Product search and filtering ✅
- Shopping cart operations ✅
- Checkout process ✅
- Payment processing ✅
- Order tracking ✅
- Admin operations ✅

**Database Testing:**
- Data integrity constraints ✅
- Foreign key relationships ✅
- Trigger functionality ✅
- View accuracy ✅
- User access control ✅

**Performance Testing:**
- Query execution time ✅
- Page load speed ✅
- Concurrent user handling ✅

### 8.2 Validation Results
- All functional requirements met ✅
- All non-functional requirements met ✅
- Security requirements implemented ✅
- Performance targets achieved ✅

---

## 9. CONCLUSION

### 9.1 Project Success
The E-Commerce Database Management System successfully implements all required and bonus features:

**Requirements Met:**
- ✅ R#1: Business & Stakeholder Requirements
- ✅ R#2: ERD Design (A3 format)
- ✅ R#3: Database Schema & Data Dictionary
- ✅ R#4: Query Reports with Relational Algebra
- ✅ Bonus: Views and Synonyms
- ✅ Bonus: User Access Control
- ✅ Bonus: GUI Implementation

### 9.2 Key Achievements
- 20 tables with full normalization
- 10 analytical views
- 6 role-based user accounts
- Complete GUI with all DML operations
- Production-ready security
- Comprehensive documentation

### 9.3 Future Enhancements
- Mobile application
- Email notifications
- Advanced analytics dashboards
- Machine learning recommendations
- Real-time chat support

### 9.4 Lessons Learned
- Importance of normalization
- Role-based security benefits
- Query optimization techniques
- GUI usability considerations

---

## 10. APPENDICES

### Appendix A: ERD Diagrams
*Include printed ERD diagrams (A3 size)*

### Appendix B: Complete SQL Queries
*All SELECT queries with relational algebra*

### Appendix C: GUI Screenshots
*Screenshots of all system interfaces*

### Appendix D: Data Dictionary
*Complete table specifications*

### Appendix E: Access Credentials

**Admin Access:**
- URL: http://localhost:8000/login.php
- Email: admin@ecommerce.com
- Password: admin123

**Database Users:**
- Super Admin: ecommerce_super_admin / SuperAdmin@2025!
- Admin: ecommerce_admin / Admin@2025!
- Inventory: inventory_manager / Inventory@2025!
- Sales: sales_rep / Sales@2025!
- Service: customer_service / Service@2025!
- Analyst: analyst / Analyst@2025!

### Appendix F: Installation Guide
*Step-by-step setup instructions*

### Appendix G: Source Code
*Complete codebase reference*

---

**END OF DOCUMENTATION**

**Prepared by:** [Team Name]  
**Date:** December 2025  
**Version:** 1.0
