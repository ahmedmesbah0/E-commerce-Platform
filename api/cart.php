<?php
/**
 * Cart API Endpoint
 * Handles AJAX requests for cart operations
 */

header('Content-Type: application/json');
require_once __DIR__ . '/../config/config.php';
require_once __DIR__ . '/../classes/Auth.php';
require_once __DIR__ . '/../classes/Cart.php';

$auth = new Auth();
$cart = new Cart();

// Check if logged in
if (!$auth->isLoggedIn()) {
    echo json_encode(['success' => false, 'message' => 'Please login first']);
    exit;
}

$customerId = $auth->getCustomerId();

// Get JSON input
$input = json_decode(file_get_contents('php://input'), true);
$action = $input['action'] ?? '';

switch ($action) {
    case 'add':
        $productId = intval($input['product_id'] ?? 0);
        $quantity = intval($input['quantity'] ?? 1);

        if (!$productId) {
            echo json_encode(['success' => false, 'message' => 'Invalid product']);
            exit;
        }

        $result = $cart->addItem($customerId, $productId, $quantity);
        echo json_encode($result);
        break;

    case 'update':
        $productId = intval($input['product_id'] ?? 0);
        $quantity = intval($input['quantity'] ?? 1);

        if (!$productId) {
            echo json_encode(['success' => false, 'message' => 'Invalid product']);
            exit;
        }

        $result = $cart->updateQuantity($customerId, $productId, $quantity);
        echo json_encode($result);
        break;

    case 'remove':
        $productId = intval($input['product_id'] ?? 0);

        if (!$productId) {
            echo json_encode(['success' => false, 'message' => 'Invalid product']);
            exit;
        }

        $result = $cart->removeItem($customerId, $productId);
        echo json_encode($result);
        break;

    case 'apply_coupon':
        $couponCode = $input['coupon_code'] ?? '';

        if (!$couponCode) {
            echo json_encode(['success' => false, 'message' => 'Please enter a coupon code']);
            exit;
        }

        $result = $cart->applyCoupon($customerId, $couponCode);
        echo json_encode($result);
        break;

    case 'remove_coupon':
        $result = $cart->removeCoupon();
        echo json_encode($result);
        break;

    case 'get':
        $cartData = $cart->getCart($customerId);
        echo json_encode(['success' => true, 'cart' => $cartData]);
        break;

    default:
        echo json_encode(['success' => false, 'message' => 'Invalid action']);
}
