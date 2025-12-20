<?php
/**
 * Products Page - Browse and filter products
 */

$pageTitle = "Products";
require_once __DIR__ . '/../includes/header.php';
require_once __DIR__ . '/../classes/Product.php';
require_once __DIR__ . '/../classes/Database.php';

$product = new Product();
$db = Database::getInstance();

// Get filters from query string
$filters = [
    'category_id' => $_GET['category'] ?? null,
    'brand_id' => $_GET['brand'] ?? null,
    'min_price' => $_GET['min_price'] ?? null,
    'max_price' => $_GET['max_price'] ?? null,
    'search' => $_GET['q'] ?? null
];

// Remove empty filters
$filters = array_filter($filters);

// Pagination
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$perPage = 12;

// Get products and total count
$products = $product->getAll($page, $perPage, $filters);
$totalProducts = $product->getTotalCount($filters);
$totalPages = ceil($totalProducts / $perPage);

// Get categories and brands for filters
$categories = $db->fetchAll("SELECT * FROM category WHERE parent_category_id IS NULL ORDER BY name");
$brands = $db->fetchAll("SELECT * FROM brand ORDER BY name");
?>

<div class="container" style="padding: 2rem 1.5rem;">
    <div style="display: flex; gap: 2rem;">
        <!-- Sidebar Filters -->
        <aside style="flex: 0 0 250px;">
            <div
                style="background: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: sticky; top: 100px;">
                <h3 style="margin-bottom: 1.5rem;">Filters</h3>

                <form method="GET" action="/products.php">
                    <!-- Search -->
                    <?php if (isset($_GET['q'])): ?>
                        <input type="hidden" name="q" value="<?php echo htmlspecialchars($_GET['q']); ?>">
                    <?php endif; ?>

                    <!-- Category Filter -->
                    <div style="margin-bottom: 1.5rem;">
                        <label style="font-weight: 600; display: block; margin-bottom: 0.5rem;">Category</label>
                        <select name="category" class="form-control"
                            style="width: 100%; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.5rem;">
                            <option value="">All Categories</option>
                            <?php foreach ($categories as $cat): ?>
                                <option value="<?php echo $cat['category_id']; ?>" <?php echo (isset($_GET['category']) && $_GET['category'] == $cat['category_id']) ? 'selected' : ''; ?>>
                                    <?php echo htmlspecialchars($cat['name']); ?>
                                </option>
                            <?php endforeach; ?>
                        </select>
                    </div>

                    <!-- Brand Filter -->
                    <div style="margin-bottom: 1.5rem;">
                        <label style="font-weight: 600; display: block; margin-bottom: 0.5rem;">Brand</label>
                        <select name="brand" class="form-control"
                            style="width: 100%; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.5rem;">
                            <option value="">All Brands</option>
                            <?php foreach ($brands as $brand): ?>
                                <option value="<?php echo $brand['brand_id']; ?>" <?php echo (isset($_GET['brand']) && $_GET['brand'] == $brand['brand_id']) ? 'selected' : ''; ?>>
                                    <?php echo htmlspecialchars($brand['name']); ?>
                                </option>
                            <?php endforeach; ?>
                        </select>
                    </div>

                    <!-- Price Range -->
                    <div style="margin-bottom: 1.5rem;">
                        <label style="font-weight: 600; display: block; margin-bottom: 0.5rem;">Price Range</label>
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <input type="number" name="min_price" placeholder="Min"
                                value="<?php echo $_GET['min_price'] ?? ''; ?>"
                                style="width: 100%; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.5rem;">
                            <span>-</span>
                            <input type="number" name="max_price" placeholder="Max"
                                value="<?php echo $_GET['max_price'] ?? ''; ?>"
                                style="width: 100%; padding: 0.5rem; border: 1px solid #e5e7eb; border-radius: 0.5rem;">
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary" style="width: 100%; margin-bottom: 0.5rem;">Apply
                        Filters</button>
                    <a href="/products.php" class="btn btn-outline"
                        style="width: 100%; display: block; text-align: center;">Clear Filters</a>
                </form>
            </div>
        </aside>

        <!-- Products Grid -->
        <main style="flex: 1;">
            <!-- Header -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                <div>
                    <h1>Products</h1>
                    <p style="color: #6b7280;">Showing <?php echo count($products); ?> of <?php echo $totalProducts; ?>
                        products</p>
                </div>
            </div>

            <!-- Products -->
            <?php if (empty($products)): ?>
                <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 1rem;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
                    <h3>No products found</h3>
                    <p style="color: #6b7280; margin-top: 0.5rem;">Try adjusting your filters or search terms</p>
                    <a href="/products.php" class="btn btn-primary" style="margin-top: 1.5rem;">View All Products</a>
                </div>
            <?php else: ?>
                <div class="product-grid">
                    <?php foreach ($products as $p): ?>
                        <div class="product-card">
                            <?php if ($p['avg_rating'] >= 4.5): ?>
                                <div class="product-badge">⭐ Top Rated</div>
                            <?php elseif ($p['stock'] < 10 && $p['stock'] > 0): ?>
                                <div class="product-badge" style="background: #ef4444;">Low Stock</div>
                            <?php elseif ($p['stock'] == 0): ?>
                                <div class="product-badge" style="background: #6b7280;">Out of Stock</div>
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

                                <?php if ($p['brand_name']): ?>
                                    <p style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">
                                        <?php echo htmlspecialchars($p['brand_name']); ?>
                                    </p>
                                <?php endif; ?>

                                <div class="product-price">
                                    <?php echo CURRENCY_SYMBOL . number_format($p['price'], 2); ?>
                                </div>

                                <?php if ($p['avg_rating'] > 0): ?>
                                    <div class="product-rating">
                                        <span class="stars">
                                            <?php
                                            $rating = round($p['avg_rating']);
                                            echo str_repeat('⭐', $rating) . str_repeat('☆', 5 - $rating);
                                            ?>
                                        </span>
                                        <span style="font-size: 0.875rem; color: #6b7280;">
                                            (<?php echo $p['review_count']; ?>)
                                        </span>
                                    </div>
                                <?php endif; ?>

                                <div class="product-actions">
                                    <a href="/product-detail.php?id=<?php echo $p['product_id']; ?>"
                                        class="btn btn-primary btn-sm">
                                        View Details
                                    </a>
                                    <?php if ($isLoggedIn && $p['stock'] > 0): ?>
                                        <button onclick="addToCart(<?php echo $p['product_id']; ?>)"
                                            class="btn btn-secondary btn-sm">
                                            Add to Cart
                                        </button>
                                    <?php endif; ?>
                                </div>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>

                <!-- Pagination -->
                <?php if ($totalPages > 1): ?>
                    <div style="display: flex; justify-content: center; gap: 0.5rem; margin-top: 3rem;">
                        <?php if ($page > 1): ?>
                            <a href="?<?php echo http_build_query(array_merge($_GET, ['page' => $page - 1])); ?>"
                                class="btn btn-outline">
                                ← Previous
                            </a>
                        <?php endif; ?>

                        <?php for ($i = max(1, $page - 2); $i <= min($totalPages, $page + 2); $i++): ?>
                            <a href="?<?php echo http_build_query(array_merge($_GET, ['page' => $i])); ?>"
                                class="btn <?php echo $i == $page ? 'btn-primary' : 'btn-outline'; ?>">
                                <?php echo $i; ?>
                            </a>
                        <?php endfor; ?>

                        <?php if ($page < $totalPages): ?>
                            <a href="?<?php echo http_build_query(array_merge($_GET, ['page' => $page + 1])); ?>"
                                class="btn btn-outline">
                                Next →
                            </a>
                        <?php endif; ?>
                    </div>
                <?php endif; ?>
            <?php endif; ?>
        </main>
    </div>
</div>

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