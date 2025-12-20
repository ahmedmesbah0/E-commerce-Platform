<?php
/**
 * User Dashboard
 */

$pageTitle = "My Dashboard";
require_once __DIR__ . '/../../includes/header.php';
require_once __DIR__ . '/../../classes/Customer.php';
require_once __DIR__ . '/../../classes/Order.php';

// Require login
$auth->requireLogin('/login.php');

$customer = new Customer();
$order = new Order();
$customerId = $auth->getCustomerId();

// Get customer stats
$stats = $customer->getStatistics($customerId);

// Get recent orders
$recentOrders = $order->getByCustomer($customerId, 5);

// Get loyalty info
$loyalty = $customer->getLoyaltyInfo($customerId);
?>

<div class="container" style="padding: 2rem 1.5rem;">
    <!-- Header -->
    <div style="margin-bottom: 2rem;">
        <h1>Welcome back, <?php echo htmlspecialchars($_SESSION['customer_name']); ?>! 👋</h1>
        <p style="color: #6b7280;">Manage your orders, profile, and more</p>
    </div>

    <!-- Stats Cards -->
    <div
        style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
        <div
            style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 0.5rem;">Total Orders</div>
            <div style="font-size: 2rem; font-weight: 700;"><?php echo $stats['total_orders']; ?></div>
        </div>

        <div
            style="background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%); color: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 0.5rem;">Total Spent</div>
            <div style="font-size: 2rem; font-weight: 700;">
                <?php echo CURRENCY_SYMBOL . number_format($stats['total_spent'], 2); ?></div>
        </div>

        <div
            style="background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%); color: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 0.5rem;">Loyalty Points</div>
            <div style="font-size: 2rem; font-weight: 700;"><?php echo $stats['loyalty_points']; ?> pts</div>
        </div>

        <div
            style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 0.875rem; opacity: 0.9; margin-bottom: 0.5rem;">Wishlist Items</div>
            <div style="font-size: 2rem; font-weight: 700;"><?php echo $stats['wishlist_count']; ?></div>
        </div>
    </div>

    <!-- Quick Actions -->
    <div
        style="background: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 2rem;">
        <h3 style="margin-bottom: 1.5rem;">Quick Actions</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <a href="/user/orders.php" class="btn btn-outline" style="text-align: center;">
                📦 View Orders
            </a>
            <a href="/user/profile.php" class="btn btn-outline" style="text-align: center;">
                👤 Edit Profile
            </a>
            <a href="/user/wishlist.php" class="btn btn-outline" style="text-align: center;">
                ❤️ My Wishlist
            </a>
            <a href="/products.php" class="btn btn-primary" style="text-align: center;">
                🛍️ Shop Now
            </a>
        </div>
    </div>

    <!-- Loyalty Program -->
    <?php if ($loyalty): ?>
        <div
            style="background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%); color: white; padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin-bottom: 0.5rem;">Loyalty Status: <?php echo ucfirst($loyalty['tier']); ?> Tier</h3>
                    <p style="opacity: 0.9;">You have <?php echo $loyalty['points']; ?> reward points</p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.875rem; opacity: 0.9;">Next tier at</div>
                    <div style="font-size: 1.5rem; font-weight: 700;">
                        <?php
                        $nextTier = ['bronze' => 200, 'silver' => 500, 'gold' => 1000, 'platinum' => 999999];
                        echo $nextTier[$loyalty['tier']] ?? 'Max';
                        ?> pts
                    </div>
                </div>
            </div>
        </div>
    <?php endif; ?>

    <!-- Recent Orders -->
    <div style="background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h3>Recent Orders</h3>
            <a href="/user/orders.php" style="color: #6366f1;">View All →</a>
        </div>

        <?php if (empty($recentOrders)): ?>
            <div style="text-align: center; padding: 3rem 1rem; color: #6b7280;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
                <p>No orders yet</p>
                <a href="/products.php" class="btn btn-primary" style="margin-top: 1rem;">
                    Start Shopping
                </a>
            </div>
        <?php else: ?>
            <div style="display: grid; gap: 1rem;">
                <?php foreach ($recentOrders as $ord): ?>
                    <div style="border: 1px solid #e5e7eb; padding: 1.5rem; border-radius: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                            <div>
                                <div style="font-weight: 700; font-size: 1.125rem; margin-bottom: 0.25rem;">
                                    Order #<?php echo str_pad($ord['order_id'], 6, '0', STR_PAD_LEFT); ?>
                                </div>
                                <div style="color: #6b7280; font-size: 0.875rem;">
                                    <?php echo date('M d, Y', strtotime($ord['order_date'])); ?>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.25rem; font-weight: 700; color: #111827;">
                                    <?php echo CURRENCY_SYMBOL . number_format($ord['total_amount'], 2); ?>
                                </div>
                                <div>
                                    <?php
                                    $statusColors = [
                                        'pending' => '#fef3c7',
                                        'processing' => '#dbeafe',
                                        'shipped' => '#e0e7ff',
                                        'delivered' => '#d1fae5',
                                        'cancelled' => '#fee2e2'
                                    ];
                                    $statusTextColors = [
                                        'pending' => '#92400e',
                                        'processing' => '#1e40af',
                                        'shipped' => '#4338ca',
                                        'delivered' => '#065f46',
                                        'cancelled' => '#991b1b'
                                    ];
                                    $bgColor = $statusColors[$ord['status']] ?? '#e5e7eb';
                                    $textColor = $statusTextColors[$ord['status']] ?? '#374151';
                                    ?>
                                    <span
                                        style="background: <?php echo $bgColor; ?>; color: <?php echo $textColor; ?>; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600;">
                                        <?php echo ucfirst($ord['status']); ?>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <?php if ($ord['tracking_number']): ?>
                            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
                                <div style="font-size: 0.875rem; color: #6b7280;">
                                    <strong>Tracking:</strong> <?php echo htmlspecialchars($ord['tracking_number']); ?>
                                </div>
                            </div>
                        <?php endif; ?>

                        <div style="margin-top: 1rem;">
                            <a href="/user/order-detail.php?id=<?php echo $ord['order_id']; ?>" class="btn btn-outline btn-sm">
                                View Details
                            </a>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </div>
</div>

<?php require_once __DIR__ . '/../../includes/footer.php'; ?>