-- Database Triggers for E-Commerce Platform
-- Automated operations for inventory, orders, and notifications

DELIMITER $$

-- =============================================
-- INVENTORY MANAGEMENT TRIGGERS
-- =============================================

-- Trigger: Update inventory when order is placed
CREATE TRIGGER after_order_item_insert
AFTER INSERT ON order_item
FOR EACH ROW
BEGIN
    -- Decrease inventory quantity
    UPDATE inventory 
    SET quantity = quantity - NEW.quantity
    WHERE product_id = NEW.product_id
    AND warehouse_id = (
        SELECT warehouse_id FROM inventory 
        WHERE product_id = NEW.product_id 
        ORDER BY quantity DESC 
        LIMIT 1
    );
    
    -- Check if reorder is needed
    IF (SELECT quantity FROM inventory 
        WHERE product_id = NEW.product_id 
        AND warehouse_id = (
            SELECT warehouse_id FROM inventory 
            WHERE product_id = NEW.product_id 
            ORDER BY quantity DESC 
            LIMIT 1
        )) < (SELECT reorder_level FROM inventory 
              WHERE product_id = NEW.product_id 
              LIMIT 1) THEN
        -- Create notification for low stock
        INSERT INTO notification (admin_id, content, type, created_at)
        SELECT 1, 
               CONCAT('Low stock alert: Product ID ', NEW.product_id, ' needs reordering'),
               'system',
               NOW()
        FROM dual;
    END IF;
END$$

-- Trigger: Restore inventory on order cancellation
CREATE TRIGGER after_order_cancel
AFTER UPDATE ON `order`
FOR EACH ROW
BEGIN
    IF OLD.status != 'cancelled' AND NEW.status = 'cancelled' THEN
        -- Restore inventory for cancelled orders
        UPDATE inventory i
        INNER JOIN order_item oi ON i.product_id = oi.product_id
        SET i.quantity = i.quantity + oi.quantity
        WHERE oi.order_id = NEW.order_id;
    END IF;
END$$

-- =============================================
-- ORDER MANAGEMENT TRIGGERS
-- =============================================

-- Trigger: Update coupon usage count
CREATE TRIGGER after_order_insert
AFTER INSERT ON `order`
FOR EACH ROW
BEGIN
    IF NEW.coupon_id IS NOT NULL THEN
        UPDATE coupon 
        SET times_used = times_used + 1
        WHERE coupon_id = NEW.coupon_id;
    END IF;
    
    -- Create order confirmation notification
    INSERT INTO notification (customer_id, content, type, created_at)
    VALUES (NEW.customer_id, 
            CONCAT('Order #', NEW.order_id, ' has been placed successfully. Total: $', NEW.total_amount),
            'order',
            NOW());
END$$

-- Trigger: Notify on order status change
CREATE TRIGGER after_order_status_update
AFTER UPDATE ON `order`
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO notification (customer_id, content, type, created_at)
        VALUES (NEW.customer_id,
                CONCAT('Order #', NEW.order_id, ' status changed to: ', NEW.status),
                'order',
                NOW());
    END IF;
END$$

-- =============================================
-- PAYMENT TRIGGERS
-- =============================================

-- Trigger: Log transaction on payment
CREATE TRIGGER after_payment_insert
AFTER INSERT ON payment
FOR EACH ROW
BEGIN
    DECLARE customer_id INT;
    
    SELECT o.customer_id INTO customer_id
    FROM `order` o
    WHERE o.order_id = NEW.order_id;
    
    INSERT INTO transaction_log (customer_id, order_id, payment_id, transaction_type, amount, description, created_at)
    VALUES (customer_id,
            NEW.order_id,
            NEW.payment_id,
            'purchase',
            NEW.amount,
            CONCAT('Payment via ', NEW.payment_method),
            NOW());
    
    -- Update order status if payment is completed
    IF NEW.status = 'completed' THEN
        UPDATE `order`
        SET status = 'processing'
        WHERE order_id = NEW.order_id AND status = 'pending';
    END IF;
END$$

-- =============================================
-- SHIPMENT TRIGGERS
-- =============================================

-- Trigger: Notify on shipment creation
CREATE TRIGGER after_shipment_insert
AFTER INSERT ON shipment
FOR EACH ROW
BEGIN
    DECLARE customer_id INT;
    
    SELECT o.customer_id INTO customer_id
    FROM `order` o
    WHERE o.order_id = NEW.order_id;
    
    INSERT INTO notification (customer_id, content, type, created_at)
    VALUES (customer_id,
            CONCAT('Your order #', NEW.order_id, ' has been shipped. Tracking: ', NEW.tracking_number),
            'shipping',
            NOW());
END$$

-- Trigger: Update order status when delivered
CREATE TRIGGER after_shipment_delivered
AFTER UPDATE ON shipment
FOR EACH ROW
BEGIN
    IF OLD.status != 'delivered' AND NEW.status = 'delivered' THEN
        UPDATE `order`
        SET status = 'delivered'
        WHERE order_id = NEW.order_id;
        
        -- Update actual delivery timestamp
        UPDATE shipment
        SET actual_delivery = NOW()
        WHERE shipment_id = NEW.shipment_id;
    END IF;
END$$

-- =============================================
-- LOYALTY PROGRAM TRIGGERS
-- =============================================

-- Trigger: Award loyalty points on order completion
CREATE TRIGGER award_loyalty_points
AFTER UPDATE ON `order`
FOR EACH ROW
BEGIN
    DECLARE points_earned INT;
    
    IF OLD.status != 'delivered' AND NEW.status = 'delivered' THEN
        -- Award 1 point per $10 spent
        SET points_earned = FLOOR(NEW.total_amount / 10);
        
        INSERT INTO loyality_program (customer_id, points, join_date, last_activity)
        VALUES (NEW.customer_id, points_earned, CURDATE(), CURDATE())
        ON DUPLICATE KEY UPDATE 
            points = points + points_earned,
            last_activity = CURDATE();
        
        -- Update tier based on total points
        UPDATE loyality_program
        SET tier = CASE
            WHEN points >= 1000 THEN 'platinum'
            WHEN points >= 500 THEN 'gold'
            WHEN points >= 200 THEN 'silver'
            ELSE 'bronze'
        END
        WHERE customer_id = NEW.customer_id;
    END IF;
END$$

-- =============================================
-- REVIEW TRIGGERS
-- =============================================

-- Trigger: Update product rating on review insert
CREATE TRIGGER after_review_insert
AFTER INSERT ON review
FOR EACH ROW
BEGIN
    IF NEW.is_approved = TRUE THEN
        -- Could update a product rating summary table here
        INSERT INTO notification (customer_id, content, type, created_at)
        VALUES (NEW.customer_id,
                'Thank you for your review!',
                'system',
                NOW());
    END IF;
END$$

-- =============================================
-- REFUND TRIGGERS
-- =============================================

-- Trigger: Process refund
CREATE TRIGGER after_refund_approved
AFTER UPDATE ON refund_request
FOR EACH ROW
BEGIN
    IF OLD.status != 'processed' AND NEW.status = 'processed' THEN
        -- Create refund payment record
        INSERT INTO payment (order_id, payment_method, amount, status, payment_date)
        SELECT order_id, 'refund', refund_amount, 'completed', NOW()
        FROM refund_request
        WHERE refund_id = NEW.refund_id;
        
        -- Log transaction
        INSERT INTO transaction_log (customer_id, order_id, transaction_type, amount, description, created_at)
        SELECT o.customer_id, o.order_id, 'refund', NEW.refund_amount, 
               CONCAT('Refund for order #', o.order_id), NOW()
        FROM `order` o
        WHERE o.order_id = NEW.order_id;
        
        -- Update order status
        UPDATE `order`
        SET status = 'refunded'
        WHERE order_id = NEW.order_id;
        
        -- Notify customer
        INSERT INTO notification (customer_id, content, type, created_at)
        SELECT customer_id,
               CONCAT('Your refund of $', NEW.refund_amount, ' has been processed'),
               'payment',
               NOW()
        FROM `order`
        WHERE order_id = NEW.order_id;
    END IF;
END$$

-- =============================================
-- CART TRIGGERS
-- =============================================

-- Trigger: Update cart timestamp on item change
CREATE TRIGGER update_cart_timestamp
AFTER INSERT ON cart_item
FOR EACH ROW
BEGIN
    UPDATE cart
    SET updated_at = NOW()
    WHERE cart_id = NEW.cart_id;
END$$

DELIMITER ;
