<?php
/**
 * Common Header Include
 */
require_once __DIR__ . '/../config/config.php';
require_once __DIR__ . '/../classes/Auth.php';
require_once __DIR__ . '/../classes/Cart.php';

$auth = new Auth();
$cart = new Cart();

$isLoggedIn = $auth->isLoggedIn();
$customerId = $auth->getCustomerId();
$cartCount = $isLoggedIn ? $cart->getItemCount($customerId) : 0;
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo isset($pageTitle) ? $pageTitle . ' - ' . SITE_NAME : SITE_NAME; ?></title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&display=swap"
        rel="stylesheet">
</head>

<body>
    <header>
        <div class="header-top">
            <div class="container">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>📧 <?php echo SITE_EMAIL; ?></span>
                    <span>🚚 Free Shipping on Orders Over $50</span>
                </div>
            </div>
        </div>

        <div class="header-main">
            <div class="container">
                <div class="header-content">
                    <a href="/" class="logo">
                        🛒 <?php echo SITE_NAME; ?>
                    </a>

                    <div class="search-bar">
                        <form action="/search.php" method="GET" class="search-form">
                            <input type="text" name="q" class="search-input" placeholder="Search for products..."
                                value="<?php echo htmlspecialchars($_GET['q'] ?? ''); ?>">
                            <button type="submit" class="search-btn">Search</button>
                        </form>
                    </div>

                    <div class="header-actions">
                        <?php if ($isLoggedIn): ?>
                            <a href="/user/dashboard.php" class="header-icon">
                                <span style="font-size: 1.5rem;">👤</span>
                                <span style="font-size: 0.75rem;">Account</span>
                            </a>
                        <?php else: ?>
                            <a href="/login.php" class="header-icon">
                                <span style="font-size: 1.5rem;">👤</span>
                                <span style="font-size: 0.75rem;">Login</span>
                            </a>
                        <?php endif; ?>

                        <a href="/cart.php" class="header-icon">
                            <span style="font-size: 1.5rem;">🛒</span>
                            <span style="font-size: 0.75rem;">Cart</span>
                            <?php if ($cartCount > 0): ?>
                                <span class="icon-badge"><?php echo $cartCount; ?></span>
                            <?php endif; ?>
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <nav>
            <div class="container">
                <ul class="nav-menu">
                    <li><a href="/" class="<?php echo ($_SERVER['REQUEST_URI'] == '/' ? 'active' : ''); ?>">Home</a>
                    </li>
                    <li><a href="/products.php">Products</a></li>
                    <li><a href="/categories.php">Categories</a></li>
                    <li><a href="/deals.php">Deals</a></li>
                    <li><a href="/contact.php">Contact</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main>