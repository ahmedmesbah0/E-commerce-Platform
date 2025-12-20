<?php
/**
 * Database Configuration
 * E-Commerce Platform
 */

// Database credentials for Nginx + PHP environment
define('DB_HOST', 'localhost');
define('DB_NAME', 'ecommerce_db');
define('DB_USER', 'ecommerce_user');
define('DB_PASS', 'your_secure_password_here'); // CHANGE THIS!

// Database charset
define('DB_CHARSET', 'utf8mb4');

// Timezone
date_default_timezone_set('UTC');

// Error reporting (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 1);
