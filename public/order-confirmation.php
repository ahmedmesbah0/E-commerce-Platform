<?php
/**
 * Order Confirmation Page
 */

$pageTitle = "Order Confirmation";
require_once __DIR__ . '/../includes/header.php';
require_once __DIR__ . '/../classes/Order.php';

// Require login
$auth->requireLogin('/login.php');

$order = new Order();
$customerId = $auth->getCustomerId();

// Get order ID
$orderId = isset($_GET['order']) ? intval($_GET['order']) : 0;

if (!$orderId) {
    header('Location: /');
    exit;
}

// Get order details
$orderData = $order->getById($orderId, $customerId);

if (!$orderData) {
    header('Location: /user/orders.php');
    exit;
}
?>

<div class="container" style="padding: 3rem 1.5rem;">
    <div style="max-width: 800px; margin: 0 auto; text-align: center;">
        <!-- Success Message -->
        <div
            style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 3rem 2rem; border-radius: 1rem; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">✅</div>
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">Order Placed Successfully!</h1>
            <p style="font-size: 1.25rem; opacity: 0.95;">
                Thank you for your purchase. Your order has been confirmed.
            </p>
        </div>

        <!-- Order Details -->
        <div
            style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 2rem; text-align: left;">
            <h2 style="margin-bottom: 1.5rem; text-align: center;">Order Details</h2>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
                <div>
                    <div style="font-weight: 600; color: #6b7280; margin-bottom: 0.5rem;">Order Number</div>
                    <div style="font-size: 1.25rem; font-weight: 700; color: #6366f1;">
                        #<?php echo str_pad($orderData['order_id'], 6, '0', STR_PAD_LEFT); ?>
                    </div>
                </div>

                <div>
                    <div style="font-weight: 600; color: #6b7280; margin-bottom: 0.5rem;">Order Date</div>
                    <div style="font-size: 1.125rem;">
                        <?php echo date('M d, Y', strtotime($orderData['order_date'])); ?>
                    </div>
                </div>

                <div>
                    <div style="font-weight: 600; color: #6b7280; margin-bottom: 0.5rem;">Total Amount</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #111827;">
                        <?php echo CURRENCY_SYMBOL . number_format($orderData['total_amount'], 2); ?>
                    </div>
                </div>

                <div>
                    <div style="font-weight: 600; color: #6b7280; margin-bottom: 0.5rem;">Payment Status</div>
                    <div>
                        <span
                            style="background: #fef3c7; color: #92400e; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600;">
                            <?php echo ucfirst($orderData['payment_status'] ?? 'Pending'); ?>
                        </span>
                    </div>
                </div>
            </div>

            <!-- Items -->
            <div style="border-top: 1px solid #e5e7eb; padding-top: 1.5rem;">
                <h3 style="margin-bottom: 1rem;">Order Items</h3>
                <?php foreach ($orderData['items'] as $item): ?>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                        <div>
                            <span style="font-weight: 600;"><?php echo htmlspecialchars($item['product_name']); ?></span>
                            <span style="color: #6b7280;"> × <?php echo $item['quantity']; ?></span>
                        </div>
                        <div style="font-weight: 600;">
                            <?php echo CURRENCY_SYMBOL . number_format($item['subtotal'], 2); ?>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>

            <!-- Shipping Address -->
            <div style="border-top: 1px solid #e5e7eb; padding-top: 1.5rem; margin-top: 1.5rem;">
                <h3 style="margin-bottom: 0.5rem;">Shipping Address</h3>
                <p style="color: #4b5563; white-space: pre-line;">
                    <?php echo htmlspecialchars($orderData['shipping_address']); ?>
                </p>
            </div>
        </div>

        <!-- Next Steps -->
        <div style="background: #f9fafb; padding: 2rem; border-radius: 1rem; margin-bottom: 2rem;">
            <h3 style="margin-bottom: 1.5rem;">What's Next?</h3>
            <div style="display: grid; gap: 1rem; text-align: left;">
                <div style="display: flex; gap: 1rem; align-items: start;">
                    <div
                        style="background: #6366f1; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 700;">
                        1
                    </div>
                    <div>
                        <div style="font-weight: 600; margin-bottom: 0.25rem;">Order Confirmation Email</div>
                        <div style="color: #6b7280; font-size: 0.875rem;">
                            We've sent a confirmation email to
                            <?php echo htmlspecialchars($orderData['customer_email']); ?>
                        </div>
                    </div>
                </div>

                <div style="display: flex; gap: 1rem; align-items: start;">
                    <div
                        style="background: #6366f1; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 700;">
                        2
                    </div>
                    <div>
                        <div style="font-weight: 600; margin-bottom: 0.25rem;">Order Processing</div>
                        <div style="color: #6b7280; font-size: 0.875rem;">
                            We'll prepare your items for shipment within 1-2 business days
                        </div>
                    </div>
                </div>

                <div style="display: flex; gap: 1rem; align-items: start;">
                    <div
                        style="background: #6366f1; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-weight: 700;">
                        3
                    </div>
                    <div>
                        <div style="font-weight: 600; margin-bottom: 0.25rem;">Shipping Updates</div>
                        <div style="color: #6b7280; font-size: 0.875rem;">
                            You'll receive tracking information once your order ships
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Actions -->
        <div style="display: flex; gap: 1rem; justify-content: center;">
            <a href="/user/orders.php" class="btn btn-primary btn-lg">
                View Order History
            </a>
            <a href="/products.php" class="btn btn-outline btn-lg">
                Continue Shopping
            </a>
        </div>
    </div>
</div>

<?php require_once __DIR__ . '/../includes/footer.php'; ?>