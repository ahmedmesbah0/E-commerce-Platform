<?php
/**
 * Shopping Cart Page
 */

$pageTitle = "Shopping Cart";
require_once __DIR__ . '/../includes/header.php';
require_once __DIR__ . '/../classes/Cart.php';

// Require login
$auth->requireLogin('/login.php?redirect=/cart.php');

$cart = new Cart();
$customerId = $auth->getCustomerId();

// Get cart data
$cartData = $cart->getCart($customerId);
$items = $cartData['items'];
$summary = $cartData['summary'];

// Get applied coupon
$appliedCoupon = $cart->getAppliedCoupon();
?>

<div class="container" style="padding: 2rem 1.5rem;">
    <h1 style="margin-bottom: 2rem;">🛒 Shopping Cart</h1>

    <?php if (empty($items)): ?>
        <!-- Empty Cart -->
        <div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 1rem;">
            <div style="font-size: 6rem; margin-bottom: 1rem;">🛒</div>
            <h2>Your cart is empty</h2>
            <p style="color: #6b7280; margin-top: 1rem;">Add some products to get started!</p>
            <a href="/products.php" class="btn btn-primary" style="margin-top: 2rem;">
                Continue Shopping
            </a>
        </div>
    <?php else: ?>
        <!-- Cart Items -->
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
            <!-- Items List -->
            <div>
                <div
                    style="background: white; border-radius: 1rem; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <?php foreach ($items as $index => $item): ?>
                        <div style="padding: 1.5rem; <?php echo $index > 0 ? 'border-top: 1px solid #e5e7eb;' : ''; ?>">
                            <div
                                style="display: grid; grid-template-columns: 100px 1fr auto; gap: 1.5rem; align-items: center;">
                                <!-- Product Image -->
                                <div
                                    style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 0.5rem; height: 100px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem;">
                                    🎁
                                </div>

                                <!-- Product Info -->
                                <div>
                                    <h3 style="margin-bottom: 0.5rem;">
                                        <a href="/product-detail.php?id=<?php echo $item['product_id']; ?>">
                                            <?php echo htmlspecialchars($item['name']); ?>
                                        </a>
                                    </h3>
                                    <p style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">
                                        SKU: <?php echo htmlspecialchars($item['sku']); ?>
                                    </p>
                                    <div style="color: #6366f1; font-weight: 600; font-size: 1.125rem;">
                                        <?php echo CURRENCY_SYMBOL . number_format($item['price'], 2); ?> each
                                    </div>

                                    <?php if (!$item['in_stock']): ?>
                                        <div class="alert alert-error" style="margin-top: 0.5rem; padding: 0.5rem;">
                                            ⚠️ Insufficient stock available
                                        </div>
                                    <?php endif; ?>
                                </div>

                                <!-- Quantity & Actions -->
                                <div style="text-align: right;">
                                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                                        <label style="font-weight: 600;">Qty:</label>
                                        <input type="number" value="<?php echo $item['quantity']; ?>" min="1"
                                            max="<?php echo $item['stock']; ?>"
                                            onchange="updateQuantity(<?php echo $item['product_id']; ?>, this.value)"
                                            style="width: 80px; padding: 0.5rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; text-align: center;">
                                    </div>
                                    <div style="font-weight: 700; font-size: 1.25rem; color: #111827; margin-bottom: 1rem;">
                                        <?php echo CURRENCY_SYMBOL . number_format($item['subtotal'], 2); ?>
                                    </div>
                                    <button onclick="removeItem(<?php echo $item['product_id']; ?>)"
                                        class="btn btn-danger btn-sm">
                                        Remove
                                    </button>
                                </div>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>

                <div style="margin-top: 1.5rem;">
                    <a href="/products.php" class="btn btn-outline">
                        ← Continue Shopping
                    </a>
                </div>
            </div>

            <!-- Order Summary -->
            <div>
                <div
                    style="background: white; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: sticky; top: 100px;">
                    <h3 style="margin-bottom: 1.5rem;">Order Summary</h3>

                    <!-- Coupon -->
                    <div style="margin-bottom: 1.5rem;">
                        <form id="couponForm" onsubmit="applyCoupon(event)">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Coupon Code</label>
                            <div style="display: flex; gap: 0.5rem;">
                                <input type="text" id="couponCode" name="coupon" placeholder="Enter code"
                                    value="<?php echo $appliedCoupon ? htmlspecialchars($appliedCoupon['code']) : ''; ?>"
                                    style="flex: 1; padding: 0.5rem; border: 2px solid #e5e7eb; border-radius: 0.5rem;">
                                <?php if ($appliedCoupon): ?>
                                    <button type="button" onclick="removeCoupon()" class="btn btn-danger btn-sm">Remove</button>
                                <?php else: ?>
                                    <button type="submit" class="btn btn-primary btn-sm">Apply</button>
                                <?php endif; ?>
                            </div>
                        </form>
                        <?php if ($appliedCoupon): ?>
                            <p style="color: #10b981; font-size: 0.875rem; margin-top: 0.5rem;">
                                ✓ Coupon applied: -<?php echo CURRENCY_SYMBOL . number_format($appliedCoupon['discount'], 2); ?>
                            </p>
                        <?php endif; ?>
                    </div>

                    <!-- Summary -->
                    <div style="border-top: 1px solid #e5e7eb; padding-top: 1.5rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                            <span>Subtotal:</span>
                            <span><?php echo CURRENCY_SYMBOL . number_format($summary['subtotal'], 2); ?></span>
                        </div>

                        <?php if ($appliedCoupon): ?>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem; color: #10b981;">
                                <span>Discount:</span>
                                <span>-<?php echo CURRENCY_SYMBOL . number_format($appliedCoupon['discount'], 2); ?></span>
                            </div>
                        <?php endif; ?>

                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                            <span>Tax:</span>
                            <span><?php echo CURRENCY_SYMBOL . number_format($summary['tax'], 2); ?></span>
                        </div>

                        <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                            <span>Shipping:</span>
                            <span><?php echo CURRENCY_SYMBOL . number_format($summary['shipping'], 2); ?></span>
                        </div>

                        <div
                            style="display: flex; justify-content: space-between; padding-top: 1.5rem; border-top: 2px solid #e5e7eb; font-size: 1.25rem; font-weight: 700;">
                            <span>Total:</span>
                            <span style="color: #6366f1;">
                                <?php
                                $finalTotal = $summary['total'] - ($appliedCoupon['discount'] ?? 0);
                                echo CURRENCY_SYMBOL . number_format($finalTotal, 2);
                                ?>
                            </span>
                        </div>
                    </div>

                    <a href="/checkout.php" class="btn btn-primary"
                        style="width: 100%; margin-top: 1.5rem; padding: 1rem; font-size: 1.125rem; text-align: center; display: block;">
                        Proceed to Checkout →
                    </a>
                </div>
            </div>
        </div>
    <?php endif; ?>
</div>

<script>
    function updateQuantity(productId, quantity) {
        fetch('/api/cart.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'update',
                product_id: productId,
                quantity: parseInt(quantity)
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('❌ ' + data.message);
                }
            });
    }

    function removeItem(productId) {
        if (confirm('Remove this item from cart?')) {
            fetch('/api/cart.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'remove',
                    product_id: productId
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('❌ ' + data.message);
                    }
                });
        }
    }

    function applyCoupon(event) {
        event.preventDefault();
        const code = document.getElementById('couponCode').value;

        fetch('/api/cart.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'apply_coupon',
                coupon_code: code
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('✅ ' + data.message);
                    location.reload();
                } else {
                    alert('❌ ' + data.message);
                }
            });
    }

    function removeCoupon() {
        fetch('/api/cart.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: 'remove_coupon'
            })
        })
            .then(response => response.json())
            .then(data => {
                location.reload();
            });
    }
</script>

<?php require_once __DIR__ . '/../includes/footer.php'; ?>