<?php
/**
 * Homepage - E-Commerce Platform
 */

$pageTitle = "Home";
require_once __DIR__ . '/../includes/header.php';
require_once __DIR__ . '/../classes/Product.php';
require_once __DIR__ . '/../classes/Database.php';

$product = new Product();
$db = Database::getInstance();

// Get featured products
$featuredProducts = $product->getFeatured(8);

// Get categories
$categories = $db->fetchAll("SELECT * FROM category WHERE parent_category_id IS NULL LIMIT 6");
?>

<!-- Hero Section -->
<section class="hero">
    <div class="container">
        <h1>🎉 Welcome to <?php echo SITE_NAME; ?></h1>
        <p>Discover amazing products at unbeatable prices</p>
        <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 2rem;">
            <a href="/products.php" class="btn btn-primary btn-lg">Shop Now</a>
            <a href="/deals.php" class="btn btn-outline btn-lg" style="border-color: white; color: white;">View
                Deals</a>
        </div>
    </div>
</section>

<!-- Categories Section -->
<section class="section" style="background: #f9fafb;">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">Shop by Category</h2>
            <p class="section-subtitle">Browse our popular categories</p>
        </div>

        <div class="category-grid">
            <?php foreach ($categories as $category): ?>
                <a href="/products.php?category=<?php echo $category['category_id']; ?>" class="category-card">
                    <h3><?php echo htmlspecialchars($category['name']); ?></h3>
                    <?php if ($category['description']): ?>
                        <p style="font-size: 0.875rem; margin-top: 0.5rem; opacity: 0.9;">
                            <?php echo htmlspecialchars($category['description']); ?>
                        </p>
                    <?php endif; ?>
                </a>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- Featured Products Section -->
<section class="section">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title">⭐ Featured Products</h2>
            <p class="section-subtitle">Our best-selling items</p>
        </div>

        <?php if (empty($featuredProducts)): ?>
            <div style="text-align: center; padding: 3rem 0;">
                <p style="font-size: 1.25rem; color: #6b7280;">No products available yet.</p>
                <p style="margin-top: 1rem;">Check back soon for amazing deals!</p>
            </div>
        <?php else: ?>
            <div class="product-grid">
                <?php foreach ($featuredProducts as $p): ?>
                    <div class="product-card">
                        <?php if (isset($p['avg_rating']) && $p['avg_rating'] >= 4): ?>
                            <div class="product-badge">⭐ Top Rated</div>
                        <?php endif; ?>

                        <div class="product-image"
                            style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;">
                            🎁
                        </div>

                        <div class="product-content">
                            <h3 class="product-title">
                                <a href="/product-detail.php?id=<?php echo $p['product_id']; ?>">
                                    <?php echo htmlspecialchars($p['name']); ?>
                                </a>
                            </h3>

                            <div class="product-price">
                                <?php echo CURRENCY_SYMBOL . number_format($p['price'], 2); ?>
                            </div>

                            <?php if (isset($p['avg_rating']) && $p['avg_rating'] > 0): ?>
                                <div class="product-rating">
                                    <span class="stars">
                                        <?php
                                        $rating = round($p['avg_rating']);
                                        echo str_repeat('⭐', $rating) . str_repeat('☆', 5 - $rating);
                                        ?>
                                    </span>
                                    <span style="font-size: 0.875rem; color: #6b7280;">
                                        (<?php echo number_format($p['avg_rating'], 1); ?>)
                                    </span>
                                </div>
                            <?php endif; ?>

                            <div class="product-actions">
                                <a href="/product-detail.php?id=<?php echo $p['product_id']; ?>" class="btn btn-primary btn-sm">
                                    View Details
                                </a>
                                <?php if ($isLoggedIn): ?>
                                    <button onclick="addToCart(<?php echo $p['product_id']; ?>)" class="btn btn-secondary btn-sm">
                                        Add to Cart
                                    </button>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>

        <div style="text-align: center; margin-top: 3rem;">
            <a href="/products.php" class="btn btn-primary btn-lg">View All Products</a>
        </div>
    </div>
</section>

<!-- Features Section -->
<section class="section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
    <div class="container">
        <div class="section-header">
            <h2 class="section-title" style="color: white;">Why Shop With Us?</h2>
        </div>

        <div
            style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🚚</div>
                <h4>Free Shipping</h4>
                <p>On orders over $50</p>
            </div>

            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💯</div>
                <h4>Quality Guaranteed</h4>
                <p>Top-quality products</p>
            </div>

            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔒</div>
                <h4>Secure Payment</h4>
                <p>100% secure transactions</p>
            </div>

            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎁</div>
                <h4>Loyalty Rewards</h4>
                <p>Earn points on every purchase</p>
            </div>
        </div>
    </div>
</section>

<script>
    function addToCart(productId) {
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
                    location.reload();
                } else {
                    alert('❌ ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to add product to cart');
            });
    }
</script>

<?php require_once __DIR__ . '/../includes/footer.php'; ?>