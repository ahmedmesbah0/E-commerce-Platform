<?php
/**
 * Cart Class
 * Handles shopping cart operations
 */

require_once __DIR__ . '/Database.php';
require_once __DIR__ . '/Product.php';

class Cart
{
    private $db;
    private $product;

    public function __construct()
    {
        $this->db = Database::getInstance();
        $this->product = new Product();
    }

    /**
     * Get or create cart for customer
     */
    private function getCartId($customerId)
    {
        $sql = "SELECT cart_id FROM cart WHERE customer_id = ?";
        $cart = $this->db->fetchOne($sql, [$customerId]);

        if ($cart) {
            return $cart['cart_id'];
        }

        // Create cart if doesn't exist
        return $this->db->insert('cart', ['customer_id' => $customerId]);
    }

    /**
     * Get cart contents
     */
    public function getCart($customerId)
    {
        $cartId = $this->getCartId($customerId);

        $sql = "SELECT ci.*, p.name, p.price as current_price, p.sku,
                       COALESCE(SUM(i.quantity), 0) as stock,
                       (ci.quantity * ci.price) as subtotal
                FROM cart_item ci
                JOIN product p ON ci.product_id = p.product_id
                LEFT JOIN inventory i ON p.product_id = i.product_id
                WHERE ci.cart_id = ?
                GROUP BY ci.cart_item_id
                ORDER BY ci.added_at DESC";

        $items = $this->db->fetchAll($sql, [$cartId]);

        // Calculate totals
        $subtotal = 0;
        foreach ($items as &$item) {
            $subtotal += $item['subtotal'];
            $item['in_stock'] = $item['stock'] >= $item['quantity'];
        }

        $tax = $subtotal * TAX_RATE;
        $shipping = $subtotal > 0 ? SHIPPING_COST : 0;
        $total = $subtotal + $tax + $shipping;

        return [
            'items' => $items,
            'summary' => [
                'subtotal' => $subtotal,
                'tax' => $tax,
                'shipping' => $shipping,
                'total' => $total,
                'item_count' => count($items)
            ]
        ];
    }

    /**
     * Add item to cart
     */
    public function addItem($customerId, $productId, $quantity = 1)
    {
        // Validate product and stock
        $product = $this->product->getById($productId);
        if (!$product || !$product['is_active']) {
            return ['success' => false, 'message' => 'Product not found'];
        }

        if (!$this->product->checkStock($productId, $quantity)) {
            return ['success' => false, 'message' => 'Insufficient stock'];
        }

        $cartId = $this->getCartId($customerId);

        // Check if item already in cart
        $existing = $this->db->fetchOne(
            "SELECT cart_item_id, quantity FROM cart_item WHERE cart_id = ? AND product_id = ?",
            [$cartId, $productId]
        );

        if ($existing) {
            // Update quantity
            $newQuantity = $existing['quantity'] + $quantity;

            // Check stock for new quantity
            if (!$this->product->checkStock($productId, $newQuantity)) {
                return ['success' => false, 'message' => 'Insufficient stock for requested quantity'];
            }

            $result = $this->db->update(
                'cart_item',
                ['quantity' => $newQuantity],
                'cart_item_id = ?',
                [$existing['cart_item_id']]
            );
        } else {
            // Add new item
            $result = $this->db->insert('cart_item', [
                'cart_id' => $cartId,
                'product_id' => $productId,
                'quantity' => $quantity,
                'price' => $product['price']
            ]);
        }

        return [
            'success' => $result !== false,
            'message' => $result ? 'Item added to cart' : 'Failed to add item',
            'cart_count' => $this->getItemCount($customerId)
        ];
    }

    /**
     * Update item quantity
     */
    public function updateQuantity($customerId, $productId, $quantity)
    {
        if ($quantity < 1) {
            return $this->removeItem($customerId, $productId);
        }

        // Check stock
        if (!$this->product->checkStock($productId, $quantity)) {
            return ['success' => false, 'message' => 'Insufficient stock'];
        }

        $cartId = $this->getCartId($customerId);

        $result = $this->db->update(
            'cart_item',
            ['quantity' => $quantity],
            'cart_id = ? AND product_id = ?',
            [$cartId, $productId]
        );

        return [
            'success' => $result,
            'message' => $result ? 'Quantity updated' : 'Failed to update quantity',
            'cart' => $this->getCart($customerId)
        ];
    }

    /**
     * Remove item from cart
     */
    public function removeItem($customerId, $productId)
    {
        $cartId = $this->getCartId($customerId);

        $result = $this->db->delete(
            'cart_item',
            'cart_id = ? AND product_id = ?',
            [$cartId, $productId]
        );

        return [
            'success' => $result,
            'message' => $result ? 'Item removed from cart' : 'Failed to remove item',
            'cart_count' => $this->getItemCount($customerId)
        ];
    }

    /**
     * Clear cart
     */
    public function clearCart($customerId)
    {
        $cartId = $this->getCartId($customerId);

        $result = $this->db->delete('cart_item', 'cart_id = ?', [$cartId]);

        return [
            'success' => $result,
            'message' => 'Cart cleared'
        ];
    }

    /**
     * Get cart item count
     */
    public function getItemCount($customerId)
    {
        $cartId = $this->getCartId($customerId);

        $sql = "SELECT COUNT(*) as count FROM cart_item WHERE cart_id = ?";
        $result = $this->db->fetchOne($sql, [$cartId]);

        return $result['count'];
    }

    /**
     * Validate cart before checkout
     */
    public function validateCart($customerId)
    {
        $cart = $this->getCart($customerId);
        $errors = [];

        if (empty($cart['items'])) {
            $errors[] = 'Cart is empty';
            return ['valid' => false, 'errors' => $errors];
        }

        foreach ($cart['items'] as $item) {
            // Check if product still exists and is active
            $product = $this->product->getById($item['product_id']);
            if (!$product || !$product['is_active']) {
                $errors[] = "Product '{$item['name']}' is no longer available";
                continue;
            }

            // Check stock
            if (!$item['in_stock']) {
                $errors[] = "Insufficient stock for '{$item['name']}'";
            }

            // Check if price changed
            if ($item['price'] != $item['current_price']) {
                $errors[] = "Price for '{$item['name']}' has changed";
            }
        }

        return [
            'valid' => empty($errors),
            'errors' => $errors,
            'cart' => $cart
        ];
    }

    /**
     * Apply coupon to cart
     */
    public function applyCoupon($customerId, $couponCode)
    {
        $sql = "SELECT * FROM coupon 
                WHERE code = ? 
                  AND is_active = 1 
                  AND (expiry_date IS NULL OR expiry_date >= CURDATE())
                  AND times_used < usage_limit";

        $coupon = $this->db->fetchOne($sql, [$couponCode]);

        if (!$coupon) {
            return ['success' => false, 'message' => 'Invalid or expired coupon'];
        }

        $cart = $this->getCart($customerId);
        $subtotal = $cart['summary']['subtotal'];

        // Check minimum purchase
        if ($subtotal < $coupon['min_purchase_amount']) {
            return [
                'success' => false,
                'message' => "Minimum purchase of " . CURRENCY_SYMBOL . number_format($coupon['min_purchase_amount'], 2) . " required"
            ];
        }

        // Calculate discount
        if ($coupon['discount_type'] == 'percentage') {
            $discount = $subtotal * ($coupon['discount_value'] / 100);
            if ($coupon['max_discount'] && $discount > $coupon['max_discount']) {
                $discount = $coupon['max_discount'];
            }
        } else {
            $discount = $coupon['discount_value'];
        }

        // Store coupon in session for checkout
        $_SESSION['applied_coupon'] = [
            'code' => $couponCode,
            'coupon_id' => $coupon['coupon_id'],
            'discount' => $discount
        ];

        return [
            'success' => true,
            'message' => 'Coupon applied successfully',
            'discount' => $discount,
            'new_total' => $cart['summary']['total'] - $discount
        ];
    }

    /**
     * Remove applied coupon
     */
    public function removeCoupon()
    {
        unset($_SESSION['applied_coupon']);
        return ['success' => true, 'message' => 'Coupon removed'];
    }

    /**
     * Get applied coupon
     */
    public function getAppliedCoupon()
    {
        return $_SESSION['applied_coupon'] ?? null;
    }

    /**
     * Move wishlist item to cart
     */
    public function moveFromWishlist($customerId, $productId)
    {
        // Add to cart
        $result = $this->addItem($customerId, $productId, 1);

        if ($result['success']) {
            // Remove from wishlist
            $this->db->delete('wishlist', 'customer_id = ? AND product_id = ?', [$customerId, $productId]);
        }

        return $result;
    }
}
