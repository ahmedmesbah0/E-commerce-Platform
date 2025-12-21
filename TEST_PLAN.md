# E-Commerce Platform - Comprehensive Test Plan

## Test Overview
Full testing of both Admin and Customer applications across all sections.

---

## CUSTOMER APPLICATION TESTS

### 1. Browse Products Tab ✓
**Test Steps:**
1. Launch app: `python3 main_app.py`
2. Select "Customer Mode"
3. Enter Customer ID: 2
4. Navigate to "Browse Products" tab

**Expected Results:**
- Products load from database
- Search functionality works
- Product details visible (ID, Name, Price, Stock)

**Test Cases:**
- [ ] All products display correctly
- [ ] Search by product name works
- [ ] "Show All" button reloads full product list
- [ ] Stock status shows "Yes" or "Out of Stock"

---

### 2. Shopping Cart Tab ✓
**Test Steps:**
1. Select a product from Browse Products
2. Set quantity (1-10)
3. Click "Add to Cart"
4. Navigate to "Shopping Cart" tab

**Expected Results:**
- Product added to cart
- Quantity, price, subtotal calculated correctly
- Total amount updates

**Test Cases:**
- [ ] Add single product to cart
- [ ] Add multiple different products
- [ ] Add same product twice (should create separate entries)
- [ ] Total calculation: Subtotal + Tax (14%) + Shipping (50 EGP)
- [ ] Clear Cart button works
- [ ] Cart displays correctly

---

### 3. Place Order ✓
**Test Steps:**
1. Add products to cart
2. Click "Place Order" button
3. Confirm order details

**Expected Results:**
- Order created in database
- Order ID generated
- Inventory reduced
- Cart cleared
- Success message shows totals

**Test Cases:**
- [ ] Order successfully placed
- [ ] Order appears in database
- [ ] Inventory quantity decreases
- [ ] Cart empties after order
- [ ] Order confirmation shows correct amounts

---

### 4. My Orders Tab ✓
**Test Steps:**
1. Navigate to "My Orders" tab
2. Click "Refresh" button

**Expected Results:**
- All customer orders displayed
- Order details: ID, Date, Total, Status

**Test Cases:**
- [ ] Previous orders visible
- [ ] New order appears in list
- [ ] Order details accurate
- [ ] Refresh button works

---

### 5. My Profile Tab ✓
**Test Steps:**
1. Navigate to "My Profile" tab

**Expected Results:**
- Customer information displayed
- ID, Name, Email visible

**Test Cases:**
- [ ] Customer ID correct
- [ ] Customer name displayed
- [ ] Email address shown

---

## ADMIN APPLICATION TESTS

### 1. Products Tab (CRUD) ✓
**Test Steps:**
1. Launch app: `python3 main_app.py`
2. Select "Admin Mode"
3. Navigate to "Products" tab

**Test Cases:**
- [ ] **SELECT**: View all products
- [ ] **INSERT**: Add new product
  - Enter: Name, Price, Category ID
  - Click "Add Product"
- [ ] **UPDATE**: Modify product
  - Select product, change details, update
- [ ] **DELETE**: Remove product
  - Select product, click delete, confirm

---

### 2. Categories Tab (CRUD) ✓
**Test Steps:**
1. Navigate to "Categories" tab

**Test Cases:**
- [ ] **SELECT**: View all categories
- [ ] **INSERT**: Add new category
- [ ] **UPDATE**: Modify category name
- [ ] **DELETE**: Remove category

---

### 3. Customers Tab (CRUD) ✓
**Test Steps:**
1. Navigate to "Customers" tab

**Test Cases:**
- [ ] **SELECT**: View all customers
- [ ] **INSERT**: Add new customer
- [ ] **UPDATE**: Modify customer details
- [ ] **DELETE**: Remove customer

---

### 4. Orders Tab (SELECT) ✓
**Test Steps:**
1. Navigate to "Orders" tab

**Test Cases:**
- [ ] **SELECT**: View all orders
- [ ] Orders show customer info (JOIN)
- [ ] Order details visible
- [ ] Can filter/search orders

---

### 5. Reviews Tab (I/S) ✓
**Test Steps:**
1. Navigate to "Reviews" tab

**Test Cases:**
- [ ] **SELECT**: View all reviews
- [ ] **INSERT**: Add new review
- [ ] Reviews linked to products and customers

---

### 6. Coupons Tab (CRUD) ✓
**Test Steps:**
1. Navigate to "Coupons" tab

**Test Cases:**
- [ ] **SELECT**: View all coupons
- [ ] **INSERT**: Create new coupon code
- [ ] **UPDATE**: Modify coupon details
- [ ] **DELETE**: Remove coupon

---

### 7. Inventory Tab (UPDATE) ✓
**Test Steps:**
1. Navigate to "Inventory" tab

**Test Cases:**
- [ ] **SELECT**: View inventory levels
- [ ] **UPDATE**: Modify stock quantities
- [ ] Inventory linked to products and warehouses

---

### 8. Shipments Tab (S/U) ✓
**Test Steps:**
1. Navigate to "Shipments" tab

**Test Cases:**
- [ ] **SELECT**: View all shipments
- [ ] **UPDATE**: Update shipment status
- [ ] Tracking numbers visible

---

### 9. Custom Query Tab ✓
**Test Steps:**
1. Navigate to "Custom Query" tab

**Test Cases:**
- [ ] Execute SELECT queries
- [ ] Execute INSERT queries
- [ ] Execute UPDATE queries
- [ ] Execute DELETE queries
- [ ] Results display correctly
- [ ] Error handling for invalid SQL

---

## DATABASE VALIDATION TESTS

### Inventory Reduction ✓
**Test Steps:**
1. Check inventory before order: `SELECT * FROM inventory WHERE product_id = X;`
2. Place order with quantity Y
3. Check inventory after: Should be reduced by Y

**SQL Verification:**
```sql
-- Before order
SELECT product_id, quantity FROM inventory WHERE product_id = 1;

-- After placing order with qty=2
-- Quantity should decrease by 2
```

### Order Creation ✓
**Test Steps:**
1. Place order through customer GUI
2. Query database for new order

**SQL Verification:**
```sql
-- Check latest order
SELECT * FROM `order` ORDER BY order_id DESC LIMIT 1;

-- Check order items
SELECT * FROM order_item WHERE order_id = (SELECT MAX(order_id) FROM `order`);
```

### Data Integrity ✓
**Test Cases:**
- [ ] Foreign keys enforced
- [ ] Cascading deletes work correctly
- [ ] Constraints validated (price >= 0, etc.)

---

## PERFORMANCE TESTS

### Load Testing ✓
- [ ] Load 100+ products - GUI responsive
- [ ] Load 50+ orders - Query performance acceptable
- [ ] Multiple cart items - Calculations fast

### Concurrent Users
- [ ] Multiple customers can browse simultaneously
- [ ] Admin and customer can operate concurrently

---

## ERROR HANDLING TESTS

### Customer Application
- [ ] Empty cart - Place Order shows warning
- [ ] Out of stock product - Add to cart blocked
- [ ] Invalid customer ID - Graceful error
- [ ] Database connection lost - Error message

### Admin Application
- [ ] Invalid SQL syntax - Error displayed
- [ ] Delete product with orders - FK constraint error shown
- [ ] Duplicate category name - UNIQUE constraint error
- [ ] Empty required fields - Validation error

---

## INTEGRATION TESTS

### Full Purchase Flow ✓
1. Customer browses products
2. Adds 3 products to cart
3. Places order
4. Admin views order in Orders tab
5. Admin updates inventory
6. Admin marks shipment as delivered

### Admin Management Flow ✓
1. Admin adds new product
2. Admin sets inventory
3. Customer sees new product
4. Customer purchases product
5. Inventory automatically reduced

---

## TEST RESULTS RECORDING

| Test Case | Status | Notes |
|-----------|--------|-------|
| Customer - Browse Products | ⏳ Pending | |
| Customer - Add to Cart | ⏳ Pending | |
| Customer - Place Order | ⏳ Pending | Fixed schema mismatch |
| Customer - View Orders | ⏳ Pending | |
| Customer - View Profile | ⏳ Pending | |
| Admin - Products CRUD | ⏳ Pending | |
| Admin - Categories CRUD | ⏳ Pending | |
| Admin - Customers CRUD | ⏳ Pending | |
| Admin - Orders SELECT | ⏳ Pending | |
| Admin - Reviews I/S | ⏳ Pending | |
| Admin - Coupons CRUD | ⏳ Pending | |
| Admin - Inventory UPDATE | ⏳ Pending | |
| Admin - Shipments S/U | ⏳ Pending | |
| Admin - Custom Query | ⏳ Pending | |
| Inventory Reduction | ⏳ Pending | |
| Order Creation | ⏳ Pending | |
| Error Handling | ⏳ Pending | |

---

## QUICK TEST COMMANDS

```bash
# Launch Customer Mode
cd gui && python3 main_app.py
# Select Customer Mode, enter ID: 2

# Launch Admin Mode  
cd gui && python3 main_app.py
# Select Admin Mode

# Check Database State
mysql -u ecommerce_user -pSecurePass123! ecommerce_db

# Useful SQL Queries
SELECT * FROM product LIMIT 10;
SELECT * FROM `order` ORDER BY order_date DESC LIMIT 5;
SELECT * FROM inventory WHERE quantity < 10;
SELECT p.name, i.quantity FROM product p 
  JOIN inventory i ON p.product_id = i.product_id;
```

---

## NOTES

- Schema Fixed: Using actual database columns (subtotal, shipping_address as TEXT, price in order_item)
- Inventory reduction implemented
- All GUIs use proper error handling
- Database credentials: ecommerce_user / SecurePass123!
