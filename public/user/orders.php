<?php
/**
 * User Orders Page - Order History
 */

$pageTitle = "My Orders";
require_once __DIR__ . '/../../includes/header.php';
require_once __DIR__ . '/../../classes/Order.php';

// Require login
$auth->requireLogin('/login.php');

$order = new Order();
$customerId = $auth->getCustomerId();

// Pagination
$page = isset($_GET['page']) ? max(1, intval($_GET['page'])) : 1;
$perPage = 10;
$offset = ($page - 1) * $perPage;

// Get orders
$orders = $order->getByCustomer($customerId, $perPage, $offset);
$stats = $order->getStatistics($customerId);
?>

<div class="container" style="padding: 2rem 1.5rem;">
    <!-- Header -->
    <div style="margin-bottom: 2rem;">
        <h1>My Orders</h1>
        <p style="color: #6b7280;">Track and manage your orders</p>
    </div>

    <!-- Stats -->
    <div
        style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
        <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">Total Orders</div>
            <div style="font-size: 2rem; font-weight: 700; color: #6366f1;"><?php echo $stats['total_orders']; ?></div>
        </div>

        <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">Delivered</div>
            <div style="font-size: 2rem; font-weight: 700; color: #10b981;"><?php echo $stats['delivered_orders']; ?>
            </div>
        </div>

        <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">In Progress</div>
            <div style="font-size: 2rem; font-weight: 700; color: #3b82f6;">
                <?php echo $stats['processing_orders'] + $stats['shipped_orders']; ?></div>
        </div>

        <div style="background: white; padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.5rem;">Total Spent</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #111827;">
                <?php echo CURRENCY_SYMBOL . number_format($stats['total_revenue'], 2); ?></div>
        </div>
    </div>

    <!-- Orders List -->
    <?php if (empty($orders)): ?>
        <div
            style="background: white; padding: 4rem 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📦</div>
            <h3>No orders yet</h3>
            <p style="color: #6b7280; margin-top: 0.5rem;">Start shopping to see your orders here</p>
            <a href="/products.php" class="btn btn-primary" style="margin-top: 2rem;">
                Browse Products
            </a>
        </div>
    <?php else: ?>
        <div style="display: grid; gap: 1.5rem;">
            <?php foreach ($orders as $ord): ?>
                <div style="background: white; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden;">
                    <!-- Order Header -->
                    <div style="background: #f9fafb; padding: 1.5rem; border-bottom: 1px solid #e5e7eb;">
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                            <div>
                                <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Order Number</div>
                                <div style="font-weight: 700; font-size: 1.125rem;">
                                    #<?php echo str_pad($ord['order_id'], 6, '0', STR_PAD_LEFT); ?>
                                </div>
                            </div>

                            <div>
                                <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Order Date</div>
                                <div style="font-weight: 600;">
                                    <?php echo date('M d, Y', strtotime($ord['order_date'])); ?>
                                </div>
                            </div>

                            <div>
                                <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Total Amount</div>
                                <div style="font-weight: 700; font-size: 1.125rem; color: #6366f1;">
                                    <?php echo CURRENCY_SYMBOL . number_format($ord['total_amount'], 2); ?>
                                </div>
                            </div>

                            <div>
                                <div style="color: #6b7280; font-size: 0.875rem; margin-bottom: 0.25rem;">Status</div>
                                <?php
                                $statusColors = [
                                    'pending' => '#fef3c7',
                                    'processing' => '#dbeafe',
                                    'shipped' => '#e0e7ff',
                                    'delivered' => '#d1fae5',
                                    'cancelled' => '#fee2e2',
                                    'refunded' => '#f3e8ff'
                                ];
                                $statusTextColors = [
                                    'pending' => '#92400e',
                                    'processing' => '#1e40af',
                                    'shipped' => '#4338ca',
                                    'delivered' => '#065f46',
                                    'cancelled' => '#991b1b',
                                    'refunded' => '#6b21a8'
                                ];
                                $bgColor = $statusColors[$ord['status']] ?? '#e5e7eb';
                                $textColor = $statusTextColors[$ord['status']] ?? '#374151';
                                ?>
                                <span
                                    style="background: <?php echo $bgColor; ?>; color: <?php echo $textColor; ?>; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600; display: inline-block;">
                                    <?php echo ucfirst($ord['status']); ?>
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Order Details -->
                    <div style="padding: 1.5rem;">
                        <div style="display: grid; gap: 1rem;">
                            <?php if ($ord['tracking_number']): ?>
                                <div
                                    style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 1rem; border-radius: 0.5rem;">
                                    <div style="color: #065f46; font-weight: 600; margin-bottom: 0.25rem;">Tracking Number</div>
                                    <div style="color: #047857; font-family: monospace;">
                                        <?php echo htmlspecialchars($ord['tracking_number']); ?></div>
                                </div>
                            <?php endif; ?>

                            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                                <a href="/user/order-detail.php?id=<?php echo $ord['order_id']; ?>"
                                    class="btn btn-primary btn-sm">
                                    View Details
                                </a>

                                <?php if ($ord['status'] === 'pending' || $ord['status'] === 'processing'): ?>
                                    <button onclick="cancelOrder(<?php echo $ord['order_id']; ?>)" class="btn btn-danger btn-sm">
                                        Cancel Order
                                    </button>
                                <?php endif; ?>

                                <?php if ($ord['status'] === 'delivered'): ?>
                                    <a href="/user/request-refund.php?order=<?php echo $ord['order_id']; ?>"
                                        class="btn btn-outline btn-sm">
                                        Request Refund
                                    </a>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</div>

<script>
    function cancelOrder(orderId) {
        if (confirm('Are you sure you want to cancel this order?')) {
            const reason = prompt('Please provide a reason for cancellation:');
            if (reason) {
                // You would implement this API endpoint
                alert('Order cancellation request submitted');
            }
        }
    }
</script>

<?php require_once __DIR__ . '/../../includes/footer.php'; ?>