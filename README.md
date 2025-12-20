# E-Commerce Platform

A comprehensive e-commerce platform with 39 entities, built with PHP, MySQL, HTML, and CSS. Designed for Nginx+PHP with PayPal integration and SMTP support.

## 🚀 Features

### Core Functionality
- **Product Management**: Full CRUD operations, categories, brands, inventory tracking
- **Customer Management**: Registration, authentication, profiles, order history
- **Shopping Cart**: Add/update/remove items, coupon support, stock validation
- **Order Processing**: Cart-to-order conversion, payment integration, order tracking
- **Payment Integration**: PayPal support (configurable for other gateways)
- **Inventory System**: Multi-warehouse support, automatic reorder alerts
- **Review System**: Customer reviews and ratings
- **Wishlist**: Save products for later

### Advanced Features
- **Loyalty Program**: Points system with tier-based rewards
- **Coupon System**: Percentage and fixed discounts with expiry dates
- **Delivery Tracking**: Integration with delivery partners,route management
- **Support Tickets**: Customer support system with messaging
- **Notifications**: Email and in-app notifications
- **Refund Management**: Automated refund processing
- **Analytics**: Sales reports, customer insights, inventory reports
- **Multi-User Support**: Customers, Sellers, Admins, Support Reps

## 📋 Requirements

- **Server**: Nginx
- **PHP**: 7.4 or higher
- **MySQL**: 5.7 or higher
- **PHP Extensions**: PDO, PDO_MySQL, OpenSSL, MBString
- **SMTP**: For email notifications
- **PayPal Account**: For payment processing

## 🛠️ Installation

### 1. Database Setup

Create the database and user:

```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

Import the SQL files in order:

```bash
mysql -u ecommerce_user -p ecommerce_db < database/schema.sql
mysql -u ecommerce_user -p ecommerce_db < database/triggers.sql
mysql -u ecommerce_user -p ecommerce_db < database/views.sql
mysql -u ecommerce_user -p ecommerce_db < database/stored_procedures.sql
```

### 2. Configuration

Update `config/database.php`:

```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'ecommerce_db');
define('DB_USER', 'ecommerce_user');
define('DB_PASS', 'your_secure_password');
```

Update `config/config.php`:

```php
// Site settings
define('SITE_URL', 'https://yourdomain.com');
define('SITE_EMAIL', 'your-email@domain.com');

// PayPal
define('PAYPAL_CLIENT_ID', 'your_paypal_client_id');
define('PAYPAL_SECRET', 'your_paypal_secret');
define('PAYPAL_MODE', 'live'); // 'sandbox' or 'live'

// SMTP
define('SMTP_HOST', 'smtp.gmail.com');
define('SMTP_USER', 'your_email@gmail.com');
define('SMTP_PASS', 'your_app_password');
```

### 3. File Permissions

```bash
chmod 755 public/
mkdir -p public/uploads
chmod 777 public/uploads
```

### 4. Nginx Configuration

Add to your Nginx server block:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /path/to/E-commerce-Platform/public;
    index index.php index.html;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

## 📚 Database Schema

The platform includes 39 entities organized in the following groups:

### Users & Roles
- Customer
- Admin
- Seller
- Marketing_Agent
- Support_Rep
- Manager
- Investor

### Products
- Product
- Category
- Brand
- Supplier
- Inventory
- Warehouse

### Orders & Shopping
- Order
- Order_Item
- Cart
- Cart_Item
- Wishlist

### Payments
- Payment
- Payment_Gateway
- Tax_Record
- Transaction_Log
- Coupon
- Voucher

### Shipping
- Shipment
- Delivery_Partner
- Route
- Route_Stops
- Packaging

### Support & Communication
- Support_Ticket
- Message
- Notification
- Review
- Feedback_Survey

### Advanced Features
- Loyalty_Program
- Subscription_Plan
- Refund_Request
- Report
- Compliance_Doc
- System_Log

## 🔧 Usage Examples

### Creating a Product

```php
require_once 'classes/Product.php';

$product = new Product();
$result = $product->create([
    'name' => 'Laptop',
    'description' => 'High-performance laptop',
    'price' => 999.99,
    'category_id' => 1,
    'brand_id' => 5,
    'stock' => 50
]);
```

### Customer Registration

```php
require_once 'classes/Customer.php';

$customer = new Customer();
$result = $customer->create([
    'name' => 'John Doe',
    'email' => 'john@example.com',
    'password' => 'securepassword',
    'phone' => '1234567890',
    'address' => '123 Main St'
]);
```

### Adding to Cart

```php
require_once 'classes/Cart.php';

$cart = new Cart();
$result = $cart->addItem($customerId, $productId, $quantity);
```

### Creating an Order

```php
require_once 'classes/Order.php';

$order = new Order();
$result = $order->createFromCart(
    $customerId,
    $shippingAddress,
    $billingAddress
);
```

## 🎯 Default Credentials

**Admin Login:**
- Email: `admin@ecommerce.com`
- Password: `admin123` (⚠️ **CHANGE THIS IMMEDIATELY!**)

To change the admin password:

```php
$newHash = password_hash('your_new_password', PASSWORD_BCRYPT, ['cost' => 12]);
// Update in database: UPDATE admin SET password_hash = '$newHash' WHERE email = 'admin@ecommerce.com';
```

## 📊 Database Triggers

The system includes automated triggers for:

1. **Inventory Management**: Automatic stock updates when orders are placed
2. **Low Stock Alerts**: Notifications when inventory falls below reorder level
3. **Order Processing**: Coupon usage tracking, order confirmations
4. **Loyalty Points**: Automatic point awards on order delivery
5. **Payment Logging**: Transaction logging for all payments
6. **Refund Processing**: Automated inventory restoration on refunds

## 📈 Available Views

Pre-built views for reporting:

- `customer_order_summary`: Customer purchase history
- `product_sales_performance`: Top-selling products
- `daily_sales_summary`: Daily revenue reports
- `revenue_by_category`: Sales by product category
- `low_stock_products`: Inventory alerts
- `active_support_tickets`: Open customer issues
- `shipment_tracking_view`: Delivery status
- `top_customers`: Customer lifetime value

## 🔐 Security Features

- Password hashing with bcrypt
- Prepared statements (SQL injection prevention)
- Session management with timeout
- CSRF token support (implement in forms)
- Input validation and sanitization
- Role-based access control
- Activity logging

## 📝 API Structure

### Product Class Methods
- `getAll()` - Get products with pagination and filters
- `getById()` - Get specific product
- `search()` - Search products
- `create()` - Add new product
- `update()` - Update product
- `delete()` - Soft delete product
- `getReviews()` - Get product reviews
- `getFeatured()` - Get featured products
- `checkStock()` - Verify availability

### Customer Class Methods
- `create()` - Register customer
- `getById()` - Get customer details
- `update()` - Update profile
- `updatePassword()` - Change password
- `getOrders()` - Order history
- `getWishlist()` - Get wishlist
- `addToWishlist()` - Add product to wishlist
- `getLoyaltyInfo()` - Get loyalty points

### Cart Class Methods
- `getCart()` - Get cart contents
- `addItem()` - Add product to cart
- `updateQuantity()` - Update item quantity
- `removeItem()` - Remove from cart
- `clearCart()` - Empty cart
- `applyCoupon()` - Apply discount code
- `validateCart()` - Validate before checkout

### Order Class Methods
- `createFromCart()` - Create order
- `getById()` - Get order details
- `updateStatus()` - Change order status
- `cancel()` - Cancel order
- `requestRefund()` - Submit refund request
- `getStatistics()` - Order analytics

## 🚦 Next Steps

1. **Create Frontend Pages**:
   - Homepage (`public/index.php`)
   - Product listings (`public/products.php`)
   - Product detail (`public/product-detail.php`)
   - Shopping cart (`public/cart.php`)
   - Checkout (`public/checkout.php`)

2. **Implement PayPal Integration**:
   - Create `classes/Payment.php`
   - Integrate PayPal SDK
   - Handle callbacks

3. **Build Admin Dashboard**:
   - Order management
   - Product management
   - Customer management
   - Reports and analytics

4. **Add Email Notifications**:
   - Order confirmations
   - Shipping updates
   - Password resets

## 📞 Support

For issues or questions, create a support ticket in the system or contact the development team.

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

Built with modern PHP practices and MySQL optimization techniques.

---

**Version**: 1.0.0  
**Last Updated**: December 2025
