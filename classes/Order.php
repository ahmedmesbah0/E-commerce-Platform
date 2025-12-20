<?php
/**
 * Order Class
 * Handles order processing and management
 */

require_once __DIR__ . '/Database.php';
require_once __DIR__ . '/Cart.php';

class Order
{
    private $db;
    private $cart;

    public function __construct()
    {
        $this->db = Database::getInstance();
        $this->cart = new Cart();
    }

    /**
     * Create order from cart
     */
    public function createFromCart($customerId, $shippingAddress, $billingAddress = null)
    {
        // Validate cart
        $validation = $this->cart->validateCart($customerId);
        if (!$validation['valid']) {
            return [
                'success' => false,
                'message' => 'Cart validation failed',
                'errors' => $validation['errors']
            ];
        }

        $cart = $validation['cart'];
        $coupon = $this->cart->getAppliedCoupon();

        try {
            $this->db->beginTransaction();

            // Prepare order data
            $orderData = [
                'customer_id' => $customerId,
                'subtotal' => $cart['summary']['subtotal'],
                'tax_amount' => $cart['summary']['tax'],
                'shipping_cost' => $cart['summary']['shipping'],
                'discount_amount' => $coupon['discount'] ?? 0,
                'total_amount' => $cart['summary']['total'] - ($coupon['discount'] ?? 0),
                'shipping_address' => $shippingAddress,
                'billing_address' => $billingAddress ?? $shippingAddress,
                'coupon_id' => $coupon['coupon_id'] ?? null,
                'status' => 'pending'
            ];

            // Create order
            $orderId = $this->db->insert('order', $orderData);

            if (!$orderId) {
                throw new Exception('Failed to create order');
            }

            // Create order items
            foreach ($cart['items'] as $item) {
                $orderItemData = [
                    'order_id' => $orderId,
                    'product_id' => $item['product_id'],
                    'quantity' => $item['quantity'],
                    'price' => $item['price'],
                    'subtotal' => $item['subtotal']
                ];

                $this->db->insert('order_item', $orderItemData);
            }

            // Create tax record
            if ($cart['summary']['tax'] > 0) {
                $this->db->insert('tax_record', [
                    'order_id' => $orderId,
                    'tax_type' => 'sales_tax',
                    'tax_rate' => TAX_RATE * 100,
                    'tax_amount' => $cart['summary']['tax']
                ]);
            }

            // Clear cart
            $this->cart->clearCart($customerId);

            // Remove coupon from session
            if ($coupon) {
                $this->cart->removeCoupon();
            }

            $this->db->commit();

            return [
                'success' => true,
                'message' => 'Order created successfully',
                'order_id' => $orderId,
                'total' => $orderData['total_amount']
            ];

        } catch (Exception $e) {
            $this->db->rollback();
            error_log("Order creation error: " . $e->getMessage());
            return [
                'success' => false,
                'message' => 'Failed to create order'
            ];
        }
    }

    /**
     * Get order by ID
     */
    public function getById($orderId, $customerId = null)
    {
        $sql = "SELECT o.*, 
                       c.name as customer_name, c.email as customer_email,
                       p.payment_method, p.status as payment_status, p.transaction_id,
                       s.tracking_number, s.status as shipment_status, s.estimated_delivery,
                       cp.code as coupon_code
                FROM `order` o
                JOIN customer c ON o.customer_id = c.customer_id
                LEFT JOIN payment p ON o.order_id = p.order_id
                LEFT JOIN shipment s ON o.order_id = s.order_id
                LEFT JOIN coupon cp ON o.coupon_id = cp.coupon_id
                WHERE o.order_id = ?";

        $params = [$orderId];

        if ($customerId) {
            $sql .= " AND o.customer_id = ?";
            $params[] = $customerId;
        }

        $order = $this->db->fetchOne($sql, $params);

        if ($order) {
            // Get order items
            $itemsSql = "SELECT oi.*, p.name as product_name, p.sku
                        FROM order_item oi
                        JOIN product p ON oi.product_id = p.product_id
                        WHERE oi.order_id = ?";

            $order['items'] = $this->db->fetchAll($itemsSql, [$orderId]);
        }

        return $order;
    }

    /**
     * Update order status
     */
    public function updateStatus($orderId, $status, $notes = null)
    {
        $validStatuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded'];

        if (!in_array($status, $validStatuses)) {
            return ['success' => false, 'message' => 'Invalid status'];
        }

        $updateData = ['status' => $status];

        if ($notes) {
            $order = $this->getById($orderId);
            $updateData['notes'] = ($order['notes'] ?? '') . "\n" . date('Y-m-d H:i:s') . ": " . $notes;
        }

        $result = $this->db->update('order', $updateData, 'order_id = ?', [$orderId]);

        return [
            'success' => $result,
            'message' => $result ? 'Order status updated' : 'Failed to update status'
        ];
    }

    /**
     * Cancel order
     */
    public function cancel($orderId, $customerId, $reason)
    {
        $order = $this->getById($orderId, $customerId);

        if (!$order) {
            return ['success' => false, 'message' => 'Order not found'];
        }

        if (in_array($order['status'], ['delivered', 'cancelled', 'refunded'])) {
            return [
                'success' => false,
                'message' => 'Cannot cancel order with status: ' . $order['status']
            ];
        }

        try {
            $this->db->beginTransaction();

            // Update order status
            $this->updateStatus($orderId, 'cancelled', "Cancelled by customer: " . $reason);

            // Inventory will be restored by trigger

            $this->db->commit();

            return [
                'success' => true,
                'message' => 'Order cancelled successfully'
            ];

        } catch (Exception $e) {
            $this->db->rollback();
            return ['success' => false, 'message' => 'Failed to cancel order'];
        }
    }

    /**
     * Get orders by customer
     */
    public function getByCustomer($customerId, $limit = 10, $offset = 0)
    {
        $sql = "SELECT o.*, 
                       p.status as payment_status,
                       s.tracking_number, s.status as shipment_status
                FROM `order` o
                LEFT JOIN payment p ON o.order_id = p.order_id
                LEFT JOIN shipment s ON o.order_id = s.order_id
                WHERE o.customer_id = ?
                ORDER BY o.order_date DESC
                LIMIT ? OFFSET ?";

        return $this->db->fetchAll($sql, [$customerId, $limit, $offset]);
    }

    /**
     * Get all orders with filters (admin)
     */
    public function getAll($filters = [], $limit = 50, $offset = 0)
    {
        $conditions = [];
        $params = [];

        if (!empty($filters['status'])) {
            $conditions[] = "o.status = ?";
            $params[] = $filters['status'];
        }

        if (!empty($filters['customer_id'])) {
            $conditions[] = "o.customer_id = ?";
            $params[] = $filters['customer_id'];
        }

        if (!empty($filters['date_from'])) {
            $conditions[] = "DATE(o.order_date) >= ?";
            $params[] = $filters['date_from'];
        }

        if (!empty($filters['date_to'])) {
            $conditions[] = "DATE(o.order_date) <= ?";
            $params[] = $filters['date_to'];
        }

        $where = !empty($conditions) ? 'WHERE ' . implode(' AND ', $conditions) : '';

        $sql = "SELECT o.*, c.name as customer_name, c.email as customer_email,
                       p.payment_method, p.status as payment_status
                FROM `order` o
                JOIN customer c ON o.customer_id = c.customer_id
                LEFT JOIN payment p ON o.order_id = p.order_id
                {$where}
                ORDER BY o.order_date DESC
                LIMIT ? OFFSET ?";

        $params[] = $limit;
        $params[] = $offset;

        return $this->db->fetchAll($sql, $params);
    }

    /**
     * Get order statistics
     */
    public function getStatistics($customerId = null)
    {
        $where = $customerId ? "WHERE customer_id = ?" : "";
        $params = $customerId ? [$customerId] : [];

        $sql = "SELECT 
                    COUNT(DISTINCT order_id) as total_orders,
                    COUNT(DISTINCT CASE WHEN status = 'pending' THEN order_id END) as pending_orders,
                    COUNT(DISTINCT CASE WHEN status = 'processing' THEN order_id END) as processing_orders,
                    COUNT(DISTINCT CASE WHEN status = 'shipped' THEN order_id END) as shipped_orders,
                    COUNT(DISTINCT CASE WHEN status = 'delivered' THEN order_id END) as delivered_orders,
                    COUNT(DISTINCT CASE WHEN status = 'cancelled' THEN order_id END) as cancelled_orders,
                    COALESCE(SUM(CASE WHEN status NOT IN ('cancelled', 'refunded') THEN total_amount ELSE 0 END), 0) as total_revenue,
                    COALESCE(AVG(CASE WHEN status NOT IN ('cancelled', 'refunded') THEN total_amount END), 0) as avg_order_value
                FROM `order`
                {$where}";

        return $this->db->fetchOne($sql, $params);
    }

    /**
     * Request refund
     */
    public function requestRefund($orderId, $customerId, $reason)
    {
        $order = $this->getById($orderId, $customerId);

        if (!$order) {
            return ['success' => false, 'message' => 'Order not found'];
        }

        if ($order['status'] != 'delivered') {
            return ['success' => false, 'message' => 'Only delivered orders can be refunded'];
        }

        // Check if refund already requested
        if ($this->db->exists('refund_request', 'order_id = ?', [$orderId])) {
            return ['success' => false, 'message' => 'Refund already requested'];
        }

        $refundData = [
            'order_id' => $orderId,
            'customer_id' => $customerId,
            'reason' => $reason,
            'refund_amount' => $order['total_amount'],
            'status' => 'pending'
        ];

        $result = $this->db->insert('refund_request', $refundData);

        return [
            'success' => $result !== false,
            'message' => $result ? 'Refund request submitted' : 'Failed to submit refund request'
        ];
    }

    /**
     * Get refund requests
     */
    public function getRefundRequests($customerId = null, $status = null)
    {
        $conditions = [];
        $params = [];

        if ($customerId) {
            $conditions[] = "rr.customer_id = ?";
            $params[] = $customerId;
        }

        if ($status) {
            $conditions[] = "rr.status = ?";
            $params[] = $status;
        }

        $where = !empty($conditions) ? 'WHERE ' . implode(' AND ', $conditions) : '';

        $sql = "SELECT rr.*, o.order_date, o.total_amount as order_total,
                       c.name as customer_name, c.email as customer_email
                FROM refund_request rr
                JOIN `order` o ON rr.order_id = o.order_id
                JOIN customer c ON rr.customer_id = c.customer_id
                {$where}
                ORDER BY rr.request_date DESC";

        return $this->db->fetchAll($sql, $params);
    }

    /**
     * Get recent orders (admin dashboard)
     */
    public function getRecent($limit = 10)
    {
        $sql = "SELECT o.order_id, o.order_date, o.status, o.total_amount,
                       c.name as customer_name,
                       p.status as payment_status
                FROM `order` o
                JOIN customer c ON o.customer_id = c.customer_id
                LEFT JOIN payment p ON o.order_id = p.order_id
                ORDER BY o.order_date DESC
                LIMIT ?";

        return $this->db->fetchAll($sql, [$limit]);
    }

    /**
     * Generate invoice data
     */
    public function getInvoice($orderId, $customerId = null)
    {
        $order = $this->getById($orderId, $customerId);

        if (!$order) {
            return null;
        }

        // Add site information
        $order['site_name'] = SITE_NAME;
        $order['site_email'] = SITE_EMAIL;

        return $order;
    }
}
