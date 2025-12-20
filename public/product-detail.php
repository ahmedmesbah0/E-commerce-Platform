<?php
/**
 * Product Detail Page
 */

$pageTitle = "Product Details";
require_once __DIR__ . '/../includes/header.php';
require_once __DIR__ . '/../classes/Product.php';

$product = new Product();

// Get product ID
$productId = isset($_GET['id']) ? intval($_GET['id']) : 0;

if (!$productId) {
    header('Location: /products.php');
    exit;
}

// Get product details
$p = $product->getById($productId);

if (!$p) {
    header('Location: /products.php');
    exit;
}

// Get reviews
$reviews = $product->getReviews($productId);

// Get related products
$relatedProducts = $product->getRelated($productId, 4);

// Check if in stock
$inStock = $p['stock'] > 0;
?>

<div class="container" style="padding: 2rem 1.5rem;">
    <!-- Breadcrumb -->
    <div style="margin-bottom: 2rem; color: #6b7280;">
        <a href="/">Home</a> /
        <a href="/products.php">Products</a> /
        <?php if ($p['category_name']): ?>
            <a
                href="/products.php?category=<?php echo $p['category_id']; ?>"><?php echo htmlspecialchars($p['category_name']); ?></a>
            /
        <?php endif; ?>
        <span><?php echo htmlspecialchars($p['name']); ?></span>
    </div>

    <!-- Product Details -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; margin-bottom: 3rem;">
        <!-- Product Image -->
        <div>
            <div
                style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 1rem; height: 500px; display: flex; align-items: center; justify-content: center; color: white; font-size: 6rem;">
                🎁
            </div>
        </div>

        <!-- Product Info -->
        <div>
            <h1 style="font-size: 2rem; margin-bottom: 1rem;"><?php echo htmlspecialchars($p['name']); ?></h1>

            <?php if ($p['brand_name']): ?>
                <p style="color: #6b7280; margin-bottom: 1rem;">
                    Brand: <strong><?php echo htmlspecialchars($p['brand_name']); ?></strong>
                </p>
            <?php endif; ?>

            <!-- Rating -->
            <?php if ($p['avg_rating'] > 0): ?>
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                    <div style="color: #f59e0b; font-size: 1.25rem;">
                        <?php
                        $rating = round($p['avg_rating']);
                        echo str_repeat('⭐', $rating) . str_repeat('☆', 5 - $rating);
                        ?>
                    </div>
                    <span style="color: #6b7280;">
                        <?php echo number_format($p['avg_rating'], 1); ?> (<?php echo $p['review_count']; ?> reviews)
                    </span>
                </div>
            <?php endif; ?>

            <!-- Price -->
            <div style="font-size: 2.5rem; font-weight: 700; color: #6366f1; margin-bottom: 1.5rem;">
                <?php echo CURRENCY_SYMBOL . number_format($p['price'], 2); ?>
            </div>

            <!-- Stock Status -->
            <div style="margin-bottom: 1.5rem;">
                <?php if ($inStock): ?>
                    <span style="color: #10b981; font-weight: 600;">✓ In Stock (<?php echo $p['stock']; ?> available)</span>
                <?php else: ?>
                    <span style="color: #ef4444; font-weight: 600;">✗ Out of Stock</span>
                <?php endif; ?>
            </div>

            <!-- Description -->
            <?php if ($p['description']): ?>
                <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 1.5rem;">
                    <h3 style="margin-bottom: 1rem;">Description</h3>
                    <p style="color: #4b5563; line-height: 1.6;">
                        <?php echo nl2br(htmlspecialchars($p['description'])); ?>
                    </p>
                </div>
            <?php endif; ?>

            <!-- Product Details -->
            <div style="background: #f9fafb; padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 2rem;">
                <h3 style="margin-bottom: 1rem;">Product Details</h3>
                <div style="display: grid; gap: 0.5rem;">
                    <?php if ($p['sku']): ?>
                        <div><strong>SKU:</strong> <?php echo htmlspecialchars($p['sku']); ?></div>
                    <?php endif; ?>
                    <?php if ($p['weight']): ?>
                        <div><strong>Weight:</strong> <?php echo $p['weight']; ?> kg</div>
                    <?php endif; ?>
                    <?php if ($p['dimensions']): ?>
                        <div><strong>Dimensions:</strong> <?php echo htmlspecialchars($p['dimensions']); ?></div>
                    <?php endif; ?>
                    <?php if ($p['seller_name']): ?>
                        <div><strong>Seller:</strong> <?php echo htmlspecialchars($p['seller_name']); ?></div>
                    <?php endif; ?>
                </div>
            </div>

            <!-- Actions -->
            <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                <?php if ($isLoggedIn && $inStock): ?>
                    <div style="flex: 1;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Quantity:</label>
                        <input type="number" id="quantity" value="1" min="1" max="<?php echo $p['stock']; ?>"
                            style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;">
                    </div>
                    <div style="flex: 2; display: flex; flex-direction: column; justify-content: flex-end;">
                        <button onclick="addToCart()" class="btn btn-primary"
                            style="width: 100%; padding: 1rem; font-size: 1.125rem;">
                            🛒 Add to Cart
                        </button>
                    </div>
                <?php elseif (!$isLoggedIn): ?>
                    <a href="/login.php?redirect=<?php echo urlencode($_SERVER['REQUEST_URI']); ?>" class="btn btn-primary"
                        style="flex: 1; text-align: center; padding: 1rem; font-size: 1.125rem;">
                        Login to Purchase
                    </a>
                <?php endif; ?>
            </div>

            <?php if ($isLoggedIn): ?>
                <button onclick="addToWishlist()" class="btn btn-outline" style="width: 100%;">
                    ❤️ Add to Wishlist
                </button>
            <?php endif; ?>
        </div>
    </div>

    <!-- Reviews Section -->
    <div style="margin-bottom: 3rem;">
        <h2 style="margin-bottom: 2rem;">Customer Reviews</h2>

        <?php if (empty($reviews)): ?>
            <div style="text-align: center; padding: 3rem; background: #f9fafb; border-radius: 1rem;">
                <p style="color: #6b7280;">No reviews yet. Be the first to review this product!</p>
            </div>
        <?php else: ?>
            <div style="display: grid; gap: 1.5rem;">
                <?php foreach ($reviews as $review): ?>
                    <div
                        style="background: white; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                            <div>
                                <div style="font-weight: 600; margin-bottom: 0.25rem;">
                                    <?php echo htmlspecialchars($review['customer_name']); ?>
                                </div>
                                <div style="color: #f59e0b;">
                                    <?php echo str_repeat('⭐', $review['rating']) . str_repeat('☆', 5 - $review['rating']); ?>
                                </div>
                            </div>
                            <div style="color: #6b7280; font-size: 0.875rem;">
                                <?php echo date('M d, Y', strtotime($review['created_at'])); ?>
                            </div>
                        </div>

                        <?php if ($review['title']): ?>
                            <h4 style="margin-bottom: 0.5rem;"><?php echo htmlspecialchars($review['title']); ?></h4>
                        <?php endif; ?>

                        <?php if ($review['comment']): ?>
                            <p style="color: #4b5563; line-height: 1.6;">
                                <?php echo nl2br(htmlspecialchars($review['comment'])); ?>
                            </p>
                        <?php endif; ?>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </div>

    <!-- Related Products -->
    <?php if (!empty($relatedProducts)): ?>
        <div>
            <h2 style="margin-bottom: 2rem;">Related Products</h2>
            <div class="product-grid" style="grid-template-columns: repeat(4, 1fr);">
                <?php foreach ($relatedProducts as $rp): ?>
                    <div class="product-card">
                        <div class="product-image"
                            style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;">
                            🎁
                        </div>
                        <div class="product-content">
                            <h3 class="product-title">
                                <a href="/product-detail.php?id=<?php echo $rp['product_id']; ?>">
                                    <?php echo htmlspecialchars($rp['name']); ?>
                                </a>
                            </h3>
                            <div class="product-price">
                                <?php echo CURRENCY_SYMBOL . number_format($rp['price'], 2); ?>
                            </div>
                            <a href="/product-detail.php?id=<?php echo $rp['product_id']; ?>" class="btn btn-primary btn-sm"
                                style="width: 100%;">
                                View Details
                            </a>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    <?php endif; ?>
</div>

<script>
    function addToCart() {
        const quantity = document.getElementById('quantity').value;

        fetch('/api/cart.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'add',
                product_id: <?php echo $productId; ?>,
                quantity: parseInt(quantity)
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Product added to cart!');
                    window.location.href = '/cart.php';
                } else {
                    alert('❌ ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to add product to cart');
            });
    }

    function addToWishlist() {
        fetch('/api/wishlist.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'add',
                product_id: <?php echo $productId; ?>
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ Added to wishlist!');
                } else {
                    alert('❌ ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to add to wishlist');
            });
    }
</script>

<?php require_once __DIR__ . '/../includes/footer.php'; ?>