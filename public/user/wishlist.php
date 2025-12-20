<?php
/**
 * User Wishlist Page
 */

$pageTitle = "My Wishlist";
require_once __DIR__ . '/../../includes/header.php';
require_once __DIR__ . '/../../classes/Customer.php';

// Require login
$auth->requireLogin('/login.php');

$customer = new Customer();
$customerId = $auth->getCustomerId();

// Get wishlist
$wishlist = $customer->getWishlist($customerId);
?>

<div class="container" style="padding: 2rem 1.5rem;">
    <div style="margin-bottom: 2rem;">
        <h1>❤️ My Wishlist</h1>
        <p style="color: #6b7280;">Save your favorite items for later</p>
    </div>

    <?php if (empty($wishlist)): ?>
        <div
            style="background: white; padding: 4rem 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">❤️</div>
            <h3>Your wishlist is empty</h3>
            <p style="color: #6b7280; margin-top: 0.5rem;">Add products you love to your wishlist</p>
            <a href="/products.php" class="btn btn-primary" style="margin-top: 2rem;">
                Browse Products
            </a>
        </div>
    <?php else: ?>
        <div class="product-grid">
            <?php foreach ($wishlist as $item): ?>
                <div class="product-card">
                    <div class="product-image"
                        style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;">
                        🎁
                    </div>

                    <div class="product-content">
                        <h3 class="product-title">
                            <a href="/product-detail.php?id=<?php echo $item['product_id']; ?>">
                                <?php echo htmlspecialchars($item['name']); ?>
                            </a>
                        </h3>

                        <div class="product-price">
                            <?php echo CURRENCY_SYMBOL . number_format($item['price'], 2); ?>
                        </div>

                        <div style="margin-bottom: 1rem; color: #6b7280; font-size: 0.875rem;">
                            <?php if ($item['stock'] > 0): ?>
                                <span style="color: #10b981;">✓ In Stock</span>
                            <?php else: ?>
                                <span style="color: #ef4444;">Out of Stock</span>
                            <?php endif; ?>
                        </div>

                        <div class="product-actions">
                            <?php if ($item['stock'] > 0): ?>
                                <button onclick="moveToCart(<?php echo $item['product_id']; ?>)" class="btn btn-primary btn-sm">
                                    Add to Cart
                                </button>
                            <?php endif; ?>
                            <button onclick="removeFromWishlist(<?php echo $item['product_id']; ?>)"
                                class="btn btn-danger btn-sm">
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</div>

<script>
    function moveToCart(productId) {
        fetch('/api/cart.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'add',
                product_id: productId,
                quantity: 1
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Product added to cart!');
                    removeFromWishlist(productId);
                } else {
                    alert('❌ ' + data.message);
                }
            });
    }

    function removeFromWishlist(productId) {
        if (confirm('Remove this item from your wishlist?')) {
            // You would implement this API endpoint
            location.reload();
        }
    }
</script>

<?php require_once __DIR__ . '/../../includes/footer.php'; ?>