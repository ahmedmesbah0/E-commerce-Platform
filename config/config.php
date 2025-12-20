<?php
/**
 * Application Configuration
 * E-Commerce Platform
 */

// Site Configuration
define('SITE_NAME', 'E-Commerce Store');
define('SITE_URL', 'http://localhost'); // Update with your domain
define('SITE_EMAIL', 'info@ecommerce.com');

// PayPal Configuration
define('PAYPAL_CLIENT_ID', 'your_paypal_client_id_here'); // ADD YOUR PAYPAL CLIENT ID
define('PAYPAL_SECRET', 'your_paypal_secret_here'); // ADD YOUR PAYPAL SECRET
define('PAYPAL_MODE', 'sandbox'); // 'sandbox' or 'live'

// SMTP Configuration for Email Notifications
define('SMTP_HOST', 'smtp.gmail.com'); // Your SMTP host
define('SMTP_PORT', 587);
define('SMTP_USER', 'your_email@gmail.com'); // Your SMTP username
define('SMTP_PASS', 'your_app_password'); // Your SMTP password
define('SMTP_FROM', 'noreply@ecommerce.com');
define('SMTP_FROM_NAME', SITE_NAME);

// File Upload Configuration
define('UPLOAD_PATH', __DIR__ . '/../public/uploads/');
define('UPLOAD_URL', SITE_URL . '/uploads/');
define('MAX_FILE_SIZE', 5242880); // 5MB
define('ALLOWED_EXTENSIONS', ['jpg', 'jpeg', 'png', 'gif', 'webp']);

// Session Configuration
define('SESSION_LIFETIME', 7200); // 2 hours
session_start([
    'cookie_lifetime' => SESSION_LIFETIME,
    'cookie_httponly' => true,
    'cookie_secure' => false, // Set to true if using HTTPS
    'use_strict_mode' => true
]);

// Security
define('PASSWORD_MIN_LENGTH', 8);
define('HASH_ALGO', PASSWORD_BCRYPT);
define('HASH_COST', 12);

// Pagination
define('ITEMS_PER_PAGE', 12);

// Tax Rate
define('TAX_RATE', 0.10); // 10%
define('SHIPPING_COST', 5.99);

// Currency
define('CURRENCY', 'USD');
define('CURRENCY_SYMBOL', '$');

// File paths
define('ROOT_PATH', dirname(__DIR__));
define('CLASSES_PATH', ROOT_PATH . '/classes/');
define('INCLUDES_PATH', ROOT_PATH . '/includes/');
