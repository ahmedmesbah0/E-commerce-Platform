<?php
/**
 * Customer Class
 * Handles customer operations and profile management
 */

require_once __DIR__ . '/Database.php';

class Customer
{
    private $db;

    public function __construct()
    {
        $this->db = Database::getInstance();
    }

    /**
     * Get customer by ID
     */
    public function getById($id)
    {
        $sql = "SELECT customer_id, name, email, phone, address, date_created, is_active
                FROM customer
                WHERE customer_id = ?";

        return $this->db->fetchOne($sql, [$id]);
    }

    /**
     * Get customer by email
     */
    public function getByEmail($email)
    {
        $sql = "SELECT *
                FROM customer
                WHERE email = ?";

        return $this->db->fetchOne($sql, [$email]);
    }

    /**
     * Create new customer
     */
    public function create($data)
    {
        // Check if email already exists
        if ($this->getByEmail($data['email'])) {
            return ['success' => false, 'message' => 'Email already registered'];
        }

        // Hash password
        $passwordHash = password_hash($data['password'], HASH_ALGO, ['cost' => HASH_COST]);

        $customerData = [
            'name' => $data['name'],
            'email' => $data['email'],
            'phone' => $data['phone'] ?? null,
            'address' => $data['address'] ?? null,
            'password_hash' => $passwordHash,
            'is_active' => 1
        ];

        try {
            $this->db->beginTransaction();

            $customerId = $this->db->insert('customer', $customerData);

            if ($customerId) {
                // Create cart for customer
                $this->db->insert('cart', ['customer_id' => $customerId]);

                // Initialize loyalty program
                $this->db->insert('loyality_program', [
                    'customer_id' => $customerId,
                    'points' => 0,
                    'tier' => 'bronze',
                    'join_date' => date('Y-m-d'),
                    'last_activity' => date('Y-m-d')
                ]);

                $this->db->commit();

                return ['success' => true, 'customer_id' => $customerId];
            }

            $this->db->rollback();
            return ['success' => false, 'message' => 'Failed to create customer'];

        } catch (Exception $e) {
            $this->db->rollback();
            error_log("Customer creation error: " . $e->getMessage());
            return ['success' => false, 'message' => 'Registration failed'];
        }
    }

    /**
     * Update customer profile
     */
    public function update($id, $data)
    {
        $allowedFields = ['name', 'email', 'phone', 'address'];
        $updateData = [];

        foreach ($allowedFields as $field) {
            if (isset($data[$field])) {
                $updateData[$field] = $data[$field];
            }
        }

        if (empty($updateData)) {
            return false;
        }

        return $this->db->update('customer', $updateData, 'customer_id = ?', [$id]);
    }

    /**
     * Update password
     */
    public function updatePassword($id, $oldPassword, $newPassword)
    {
        $customer = $this->db->fetchOne("SELECT password_hash FROM customer WHERE customer_id = ?", [$id]);

        if (!$customer) {
            return ['success' => false, 'message' => 'Customer not found'];
        }

        // Verify old password
        if (!password_verify($oldPassword, $customer['password_hash'])) {
            return ['success' => false, 'message' => 'Current password is incorrect'];
        }

        // Hash new password
        $newHash = password_hash($newPassword, HASH_ALGO, ['cost' => HASH_COST]);

        $result = $this->db->update('customer', ['password_hash' => $newHash], 'customer_id = ?', [$id]);

        return [
            'success' => $result,
            'message' => $result ? 'Password updated successfully' : 'Failed to update password'
        ];
    }

    /**
     * Get customer orders
     */
    public function getOrders($customerId, $limit = 10)
    {
        $sql = "SELECT o.*, 
                       p.status as payment_status,
                       s.tracking_number,
                       s.status as shipment_status
                FROM `order` o
                LEFT JOIN payment p ON o.order_id = p.order_id
                LEFT JOIN shipment s ON o.order_id = s.order_id
                WHERE o.customer_id = ?
                ORDER BY o.order_date DESC
                LIMIT ?";

        return $this->db->fetchAll($sql, [$customerId, $limit]);
    }

    /**
     * Get specific order details
     */
    public function getOrderDetails($customerId, $orderId)
    {
        // Get order info
        $sql = "SELECT o.*, 
                       p.payment_method, p.status as payment_status, p.transaction_id,
                       s.tracking_number, s.status as shipment_status, s.estimated_delivery
                FROM `order` o
                LEFT JOIN payment p ON o.order_id = p.order_id
                LEFT JOIN shipment s ON o.order_id = s.order_id
                WHERE o.customer_id = ? AND o.order_id = ?";

        $order = $this->db->fetchOne($sql, [$customerId, $orderId]);

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
     * Get customer wishlist
     */
    public function getWishlist($customerId)
    {
        $sql = "SELECT w.*, p.name, p.price, p.sku,
                       COALESCE(SUM(i.quantity), 0) as stock
                FROM wishlist w
                JOIN product p ON w.product_id = p.product_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE w.customer_id = ?
                GROUP BY w.wishlist_id
                ORDER BY w.added_at DESC";

        return $this->db->fetchAll($sql, [$customerId]);
    }

    /**
     * Add to wishlist
     */
    public function addToWishlist($customerId, $productId)
    {
        // Check if already in wishlist
        if ($this->db->exists('wishlist', 'customer_id = ? AND product_id = ?', [$customerId, $productId])) {
            return ['success' => false, 'message' => 'Already in wishlist'];
        }

        $result = $this->db->insert('wishlist', [
            'customer_id' => $customerId,
            'product_id' => $productId
        ]);

        return [
            'success' => $result !== false,
            'message' => $result ? 'Added to wishlist' : 'Failed to add to wishlist'
        ];
    }

    /**
     * Remove from wishlist
     */
    public function removeFromWishlist($customerId, $productId)
    {
        $result = $this->db->delete('wishlist', 'customer_id = ? AND product_id = ?', [$customerId, $productId]);

        return [
            'success' => $result,
            'message' => $result ? 'Removed from wishlist' : 'Failed to remove from wishlist'
        ];
    }

    /**
     * Get loyalty program info
     */
    public function getLoyaltyInfo($customerId)
    {
        $sql = "SELECT * FROM loyality_program WHERE customer_id = ?";
        return $this->db->fetchOne($sql, [$customerId]);
    }

    /**
     * Get customer notifications
     */
    public function getNotifications($customerId, $unreadOnly = false)
    {
        $sql = "SELECT * FROM notification 
                WHERE customer_id = ?";

        if ($unreadOnly) {
            $sql .= " AND read_status = 0";
        }

        $sql .= " ORDER BY created_at DESC LIMIT 20";

        return $this->db->fetchAll($sql, [$customerId]);
    }

    /**
     * Mark notification as read
     */
    public function markNotificationRead($notificationId)
    {
        return $this->db->update('notification', ['read_status' => 1], 'notification_id = ?', [$notificationId]);
    }

    /**
     * Get customer statistics
     */
    public function getStatistics($customerId)
    {
        $sql = "SELECT 
                    COUNT(DISTINCT o.order_id) as total_orders,
                    COALESCE(SUM(o.total_amount), 0) as total_spent,
                    COALESCE(AVG(o.total_amount), 0) as avg_order_value,
                    COUNT(DISTINCT r.review_id) as reviews_count,
                    COUNT(DISTINCT w.wishlist_id) as wishlist_count,
                    COALESCE(lp.points, 0) as loyalty_points,
                    COALESCE(lp.tier, 'bronze') as loyalty_tier
                FROM customer c
                LEFT JOIN `order` o ON c.customer_id = o.customer_id AND o.status NOT IN ('cancelled', 'refunded')
                LEFT JOIN review r ON c.customer_id = r.customer_id
                LEFT JOIN wishlist w ON c.customer_id = w.customer_id
                LEFT JOIN loyality_program lp ON c.customer_id = lp.customer_id
                WHERE c.customer_id = ?
                GROUP BY c.customer_id, lp.points, lp.tier";

        return $this->db->fetchOne($sql, [$customerId]);
    }

    /**
     * Deactivate customer account
     */
    public function deactivate($id)
    {
        return $this->db->update('customer', ['is_active' => 0], 'customer_id = ?', [$id]);
    }

    /**
     * Reactivate customer account
     */
    public function reactivate($id)
    {
        return $this->db->update('customer', ['is_active' => 1], 'customer_id = ?', [$id]);
    }
}
