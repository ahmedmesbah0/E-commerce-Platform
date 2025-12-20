<?php
/**
 * Checkout Page - Order Placement
 */

$pageTitle = "Checkout";
require_once __DIR__ . '/../includes/header.php';
require_once __DIR__ . '/../classes/Cart.php';
require_once __DIR__ . '/../classes/Order.php';

// Require login
$auth->requireLogin('/login.php?redirect=/checkout.php');

$cart = new Cart();
$order = new Order();
$customerId = $auth->getCustomerId();

// Validate cart
$validation = $cart->validateCart($customerId);
if (!$validation['valid']) {
    header('Location: /cart.php');
    exit;
}

$cartData = $validation['cart'];
$appliedCoupon = $cart->getAppliedCoupon();

$error = '';
$success = false;

// Process order
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $shippingAddress = $_POST['shipping_address'] ?? '';
    $billingAddress = $_POST['billing_address'] ?? '';
    $useSameAddress = isset($_POST['same_address']);

    if ($useSameAddress) {
        $billingAddress = $shippingAddress;
    }

    if (empty($shippingAddress)) {
        $error = 'Please enter a shipping address';
    } else {
        $result = $order->createFromCart($customerId, $shippingAddress, $billingAddress);

        if ($result['success']) {
            $success = true;
            $orderId = $result['order_id'];
            // Redirect to order confirmation
            header('Location: /order-confirmation.php?order=' . $orderId);
            exit;
        } else {
            $error = $result['message'];
            if (isset($result['errors'])) {
                $error .= ': ' . implode(', ', $result['errors']);
            }
        }
    }
}

// Get customer details for pre-filling
$customer = new Customer();
$customerData = $customer->getById($customerId);
?>

<div class="container" style="padding: 2rem 1.5rem;">
    <h1 style="margin-bottom: 2rem;">🛍️ Checkout</h1>

    <?php if ($error): ?>
        <div class="alert alert-error">
            <?php echo htmlspecialchars($error); ?>
        </div>
    <?php endif; ?>

    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
        <!-- Checkout Form -->
        <div>
            <form method="POST" action="">
                <!-- Shipping Address -->
                <div
                    style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 2rem;">
                    <h3 style="margin-bottom: 1.5rem;">📦 Shipping Address</h3>

                    <div style="margin-bottom: 1.5rem;">
                        <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Full Address *</label>
                        <textarea name="shipping_address" rows="4" required
                            style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                            placeholder="Street Address, City, State, ZIP Code"><?php echo htmlspecialchars($customerData['address'] ?? ''); ?></textarea>
                    </div>
                </div>

                <!-- Billing Address -->
                <div
                    style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 2rem;">
                    <h3 style="margin-bottom: 1.5rem;">💳 Billing Address</h3>

                    <div style="margin-bottom: 1.5rem;">
                        <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                            <input type="checkbox" name="same_address" checked onchange="toggleBillingAddress(this)"
                                style="width: 18px; height: 18px;">
                            <span>Same as shipping address</span>
                        </label>
                    </div>

                    <div id="billingAddressFields" style="display: none;">
                        <div style="margin-bottom: 1.5rem;">
                            <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Full Address</label>
                            <textarea name="billing_address" rows="4"
                                style="width: 100%; padding: 0.75rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; font-size: 1rem;"
                                placeholder="Street Address, City, State, ZIP Code"></textarea>
                        </div>
                    </div>
                </div>

                <!-- Payment Method -->
                <div
                    style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 2rem;">
                    <h3 style="margin-bottom: 1.5rem;">💰 Payment Method</h3>

                    <div style="display: grid; gap: 1rem;">
                        <label
                            style="display: flex; align-items: center; gap: 1rem; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; cursor: pointer;">
                            <input type="radio" name="payment_method" value="paypal" checked
                                style="width: 20px; height: 20px;">
                            <div>
                                <strong>PayPal</strong>
                                <p style="font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem;">
                                    You will be redirected to PayPal to complete your purchase securely
                                </p>
                            </div>
                        </label>

                        <label
                            style="display: flex; align-items: center; gap: 1rem; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 0.5rem; cursor: pointer; opacity: 0.5;">
                            <input type="radio" name="payment_method" value="card" disabled
                                style="width: 20px; height: 20px;">
                            <div>
                                <strong>Credit/Debit Card</strong>
                                <p style="font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem;">
                                    Coming soon
                                </p>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Terms -->
                <div style="margin-bottom: 2rem;">
                    <label style="display: flex; align-items: start; gap: 0.5rem; cursor: pointer;">
                        <input type="checkbox" required style="margin-top: 0.25rem; width: 18px; height: 18px;">
                        <span style="font-size: 0.875rem; color: #6b7280;">
                            I agree to the <a href="/terms.php" target="_blank">Terms & Conditions</a> and
                            <a href="/privacy.php" target="_blank">Privacy Policy</a>
                        </span>
                    </label>
                </div>

                <button type="submit" class="btn btn-primary"
                    style="width: 100%; padding: 1.25rem; font-size: 1.25rem;">
                    Place Order →
                </button>
            </form>
        </div>

        <!-- Order Summary -->
        <div>
            <div
                style="background: white; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: sticky; top: 100px;">
                <h3 style="margin-bottom: 1.5rem;">Order Summary</h3>

                <!-- Items -->
                <div style="max-height: 300px; overflow-y: auto; margin-bottom: 1.5rem;">
                    <?php foreach ($cartData['items'] as $item): ?>
                        <div
                            style="display: flex; gap: 1rem; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #e5e7eb;">
                            <div
                                style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 0.5rem; width: 60px; height: 60px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; color: white;">
                                🎁
                            </div>
                            <div style="flex: 1;">
                                <div style="font-weight: 600; margin-bottom: 0.25rem; font-size: 0.875rem;">
                                    <?php echo htmlspecialchars($item['name']); ?>
                                </div>
                                <div style="font-size: 0.875rem; color: #6b7280;">
                                    Qty: <?php echo $item['quantity']; ?> ×
                                    <?php echo CURRENCY_SYMBOL . number_format($item['price'], 2); ?>
                                </div>
                            </div>
                            <div style="font-weight: 600;">
                                <?php echo CURRENCY_SYMBOL . number_format($item['subtotal'], 2); ?>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>

                <!-- Totals -->
                <div style="border-top: 1px solid #e5e7eb; padding-top: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                        <span>Subtotal:</span>
                        <span><?php echo CURRENCY_SYMBOL . number_format($cartData['summary']['subtotal'], 2); ?></span>
                    </div>

                    <?php if ($appliedCoupon): ?>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem; color: #10b981;">
                            <span>Discount (<?php echo htmlspecialchars($appliedCoupon['code']); ?>):</span>
                            <span>-<?php echo CURRENCY_SYMBOL . number_format($appliedCoupon['discount'], 2); ?></span>
                        </div>
                    <?php endif; ?>

                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                        <span>Tax:</span>
                        <span><?php echo CURRENCY_SYMBOL . number_format($cartData['summary']['tax'], 2); ?></span>
                    </div>

                    <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                        <span>Shipping:</span>
                        <span><?php echo CURRENCY_SYMBOL . number_format($cartData['summary']['shipping'], 2); ?></span>
                    </div>

                    <div
                        style="display: flex; justify-content: space-between; padding-top: 1.5rem; border-top: 2px solid #e5e7eb; font-size: 1.5rem; font-weight: 700;">
                        <span>Total:</span>
                        <span style="color: #6366f1;">
                            <?php
                            $finalTotal = $cartData['summary']['total'] - ($appliedCoupon['discount'] ?? 0);
                            echo CURRENCY_SYMBOL . number_format($finalTotal, 2);
                            ?>
                        </span>
                    </div>
                </div>

                <div
                    style="margin-top: 1.5rem; padding: 1rem; background: #f0fdf4; border-radius: 0.5rem; border-left: 4px solid #10b981;">
                    <div style="font-weight: 600; color: #065f46; margin-bottom: 0.25rem;">✓ Secure Checkout</div>
                    <div style="font-size: 0.875rem; color: #047857;">
                        Your payment information is encrypted and secure
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    function toggleBillingAddress(checkbox) {
        const billingFields = document.getElementById('billingAddressFields');
        billingFields.style.display = checkbox.checked ? 'none' : 'block';
    }
</script>

<?php require_once __DIR__ . '/../includes/footer.php'; ?>