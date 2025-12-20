# Quick Reference Guide

## 📁 Project Structure
```
E-commerce-Platform/
├── database/               # Database files
│   ├── schema.sql         # All 39 tables ✅
│   ├── triggers.sql       # 12 automated triggers ✅
│   ├── views.sql          # 20+ reporting views ✅
│   └── stored_procedures.sql # 8 procedures ✅
├── config/                # Configuration
│   ├── database.php       # DB credentials ✅
│   └── config.php         # App settings (PayPal, SMTP) ✅
├── classes/               # Backend logic
│   ├── Database.php       # DB wrapper ✅
│   ├── Product.php        # Products ✅
│   ├── Customer.php       # Customers ✅
│   ├── Auth.php           # Authentication ✅
│   ├── Cart.php           # Shopping cart ✅
│   └── Order.php          # Orders ✅
├── public/                # Frontend (NEEDED)
├── admin/                 # Admin panel (NEEDED)
├── assets/                # CSS/JS/Images
├── README.md              # Full documentation ✅
├── STATUS.md              # Progress tracker ✅
└── GETTING_STARTED.md     # Setup guide ✅
```

## 🚀 Quick Setup (5 Minutes)

```bash
# 1. Create database
mysql -u root -p << EOF
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'SecurePass123!';
GRANT ALL ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EOF

# 2. Import SQL (IN ORDER!)
cd /home/mesbah7/Github/Repos/E-commerce-Platform
mysql -u ecommerce_user -p ecommerce_db < database/schema.sql
mysql -u ecommerce_user -p ecommerce_db < database/triggers.sql
mysql -u ecommerce_user -p ecommerce_db < database/views.sql
mysql -u ecommerce_user -p ecommerce_db < database/stored_procedures.sql

# 3. Update credentials in config files
nano config/database.php  # Update DB_PASS
nano config/config.php    # Update PayPal, SMTP

# 4. Test
php -r "require 'classes/Database.php'; echo 'DB OK: ' . (Database::getInstance() ? 'YES' : 'NO');"
```

## 💻 Code Examples

### Register a Customer
```php
require_once 'classes/Customer.php';
$customer = new Customer();

$result = $customer->create([
    'name' => 'John Doe',
    'email' => 'john@example.com',
    'password' => 'password123',
    'phone' => '1234567890',
    'address' => '123 Main St'
]);

// Returns: ['success' => true, 'customer_id' => 1]
```

### Login
```php
require_once 'classes/Auth.php';
$auth = new Auth();

$result = $auth->login('john@example.com', 'password123');

if ($result['success']) {
    // User is logged in, session is set
    $customerId = $auth->getCustomerId();
}
```

### Add to Cart
```php
require_once 'classes/Cart.php';
$cart = new Cart();

$result = $cart->addItem($customerId, $productId, $quantity);
// Returns: ['success' => true, 'message' => 'Item added', 'cart_count' => 3]
```

### Checkout (Create Order)
```php
require_once 'classes/Order.php';
$order = new Order();

$result = $order->createFromCart(
    $customerId,
    '123 Shipping Address',
    '456 Billing Address'  // Optional
);

// Returns: ['success' => true, 'order_id' => 15, 'total' => 99.99]
```

### Get Products
```php
require_once 'classes/Product.php';
$product = new Product();

// Get all with filters
$products = $product->getAll(1, 12, [
    'category_id' => 1,
    'min_price' => 10,
    'max_price' => 100,
    'search' => 'laptop'
]);

// Get featured
$featured = $product->getFeatured(8);

// Get by ID
$item = $product->getById($productId);
```

## 🗄️ Database Quick Reference

### Main Tables

| Table | Primary Key | Description |
|-------|-------------|-------------|
| `customer` | customer_id | User accounts |
| `product` | product_id | Products catalog |
| `cart` | cart_id | Shopping carts |
| `cart_item` | cart_item_id | Items in carts |
| `order` | order_id | Customer orders |
| `order_item` | order_item_id | Items in orders |
| `payment` | payment_id | Payment records |
| `shipment` | shipment_id | Delivery tracking |
| `inventory` | inventory_id | Stock levels |
| `coupon` | coupon_id | Discount codes |

### Useful Views

```sql
-- Customer stats
SELECT * FROM customer_order_summary WHERE customer_id = 1;

-- Product performance
SELECT * FROM product_sales_performance ORDER BY total_revenue DESC LIMIT 10;

-- Daily sales
SELECT * FROM daily_sales_summary WHERE sale_date >= '2025-01-01';

-- Low stock
SELECT * FROM low_stock_products;

-- Top customers
SELECT * FROM top_customers LIMIT 50;
```

### Default Login

**Admin:**
- Email: `admin@ecommerce.com`
- Password: `admin123` ⚠️ CHANGE THIS!

```sql
-- Update admin password
UPDATE admin 
SET password_hash = '$2y$12$YOUR_NEW_HASH' 
WHERE email = 'admin@ecommerce.com';
```

## 🎨 Frontend Template (Basic Example)

```php
<?php
// public/index.php - Homepage Example
require_once '../config/config.php';
require_once '../classes/Product.php';
require_once '../classes/Auth.php';

$auth = new Auth();
$product = new Product();

// Get featured products
$featuredProducts = $product->getFeatured(8);
?>
<!DOCTYPE html>
<html>
<head>
    <title><?php echo SITE_NAME; ?></title>
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
    <header>
        <h1><?php echo SITE_NAME; ?></h1>
        <?php if ($auth->isLoggedIn()): ?>
            <span>Welcome, <?php echo htmlspecialchars($_SESSION['customer_name']); ?></span>
        <?php else: ?>
            <a href="/login.php">Login</a>
        <?php endif; ?>
    </header>
    
    <main>
        <h2>Featured Products</h2>
        <div class="product-grid">
            <?php foreach ($featuredProducts as $p): ?>
                <div class="product-card">
                    <h3><?php echo htmlspecialchars($p['name']); ?></h3>
                    <p><?php echo CURRENCY_SYMBOL . number_format($p['price'], 2); ?></p>
                    <a href="/product-detail.php?id=<?php echo $p['product_id']; ?>">View</a>
                </div>
            <?php endforeach; ?>
        </div>
    </main>
</body>
</html>
```

## 🔑 Environment Variables to Set

Update in `config/config.php`:

```php
// REQUIRED
SITE_URL              // Your domain
DB_PASS               // Database password
PAYPAL_CLIENT_ID      // PayPal credentials
PAYPAL_SECRET         // PayPal credentials
SMTP_USER             // Email credentials
SMTP_PASS             // Email password

// OPTIONAL
TAX_RATE              // Default: 0.10 (10%)
SHIPPING_COST         // Default: 5.99
CURRENCY              // Default: USD
```

## 📊 What's Complete vs. What's Needed

### ✅ Complete (Backend - 100%)
- Database (39 tables, triggers, views, procedures)
- PHP Classes (Product, Customer, Auth, Cart, Order)
- Configuration files
- Security implementation
- Documentation

### 🚧 Needed (Frontend - 0%)
- Homepage
- Product pages
- Cart page
- Checkout page
- User dashboard
- Admin panel
- CSS styling
- JavaScript for AJAX

## 🎯 Your Next 3 Steps

1. **Set up database** (5 min)
2. **Update config files** (2 min)
3. **Create `public/index.php`** (30 min)

Then you'll have a working homepage!

## 📞 Common Issues

**Database connection fails:**
```php
// Check credentials in config/database.php
// Verify MySQL is running: sudo service mysql status
```

**Class not found:**
```php
// Always use require_once with correct path
require_once __DIR__ . '/../classes/Product.php';
```

**Session not working:**
```php
// Make sure session_start() is called
// Already done in config/config.php
```

---

**You're ready to go! Start with the database setup above.** 🚀
