-- ============================================
-- Database Triggers for Automation
-- ============================================

USE ecommerce_db;

DELIMITER $$

-- Trigger: Auto-generate order number
CREATE TRIGGER before_order_insert
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.order_number IS NULL OR NEW.order_number = '' THEN
        SET NEW.order_number = CONCAT('ORD-', DATE_FORMAT(NOW(), '%Y%m%d'), '-', LPAD(FLOOR(RAND() * 999999), 6, '0'));
    END IF;
END$$

-- Trigger: Auto-generate ticket number
CREATE TRIGGER before_ticket_insert
BEFORE INSERT ON tickets
FOR EACH ROW
BEGIN
    IF NEW.ticket_number IS NULL OR NEW.ticket_number = '' THEN
        SET NEW.ticket_number = CONCAT('TKT-', DATE_FORMAT(NOW(), '%Y%m%d'), '-', LPAD(FLOOR(RAND() * 99999), 5, '0'));
    END IF;
END$$

-- Trigger: Auto-generate tracking number for shipments
CREATE TRIGGER before_shipment_insert
BEFORE INSERT ON shipments
FOR EACH ROW
BEGIN
    IF NEW.tracking_number IS NULL OR NEW.tracking_number = '' THEN
        SET NEW.tracking_number = CONCAT('TRK-', UPPER(LEFT(UUID(), 8)), '-', DATE_FORMAT(NOW(), '%y%m%d'));
    END IF;
END$$

-- Trigger: Update payment status when order is delivered
CREATE TRIGGER after_shipment_delivered
AFTER UPDATE ON shipments
FOR EACH ROW
BEGIN
    IF NEW.shipment_status = 'DELIVERED' AND OLD.shipment_status != 'DELIVERED' THEN
        UPDATE orders 
        SET order_status = 'DELIVERED',
            payment_status = 'PAID'
        WHERE order_id = NEW.order_id 
        AND payment_method = 'CASH_ON_DELIVERY';
        
        UPDATE payments
        SET payment_status = 'COMPLETED',
            payment_date = NOW()
        WHERE order_id = NEW.order_id 
        AND payment_status = 'PENDING';
    END IF;
END$$

-- Trigger: Calculate and award loyalty points on order completion
CREATE TRIGGER after_order_delivered
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    DECLARE points_to_award INT;
    
    IF NEW.order_status = 'DELIVERED' AND OLD.order_status != 'DELIVERED' THEN
        SET points_to_award = FLOOR(NEW.total_amount / 10);
        
        INSERT INTO customer_loyalty (customer_id, current_points, lifetime_points)
        VALUES (NEW.customer_id, points_to_award, points_to_award)
        ON DUPLICATE KEY UPDATE 
            current_points = current_points + points_to_award,
            lifetime_points = lifetime_points + points_to_award;
        
        INSERT INTO loyalty_transactions (customer_id, transaction_type, points, reference_type, reference_id, description)
        VALUES (NEW.customer_id, 'EARNED', points_to_award, 'ORDER', NEW.order_id, 
                CONCAT('Points earned from order ', NEW.order_number));
        
        UPDATE orders SET loyalty_points_earned = points_to_award WHERE order_id = NEW.order_id;
    END IF;
END$$

-- Trigger: Update delivery partner statistics on delivery
CREATE TRIGGER after_shipment_delivered_stats
AFTER UPDATE ON shipments
FOR EACH ROW
BEGIN
    IF NEW.shipment_status = 'DELIVERED' AND OLD.shipment_status != 'DELIVERED' AND NEW.partner_id IS NOT NULL THEN
        UPDATE delivery_partners 
        SET total_deliveries = total_deliveries + 1
        WHERE partner_id = NEW.partner_id;
    END IF;
END$$

-- Trigger: Prevent negative inventory
CREATE TRIGGER before_inventory_update
BEFORE UPDATE ON inventory
FOR EACH ROW
BEGIN
    IF NEW.quantity < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Inventory quantity cannot be negative';
    END IF;
    
    IF NEW.reserved_quantity > NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Reserved quantity cannot exceed total quantity';
    END IF;
END$$

-- Trigger: Create notification on order status change
CREATE TRIGGER after_order_status_change
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.order_status != OLD.order_status THEN
        INSERT INTO notifications (user_id, title, message, notification_type, reference_type, reference_id)
        VALUES (
            NEW.customer_id,
            CONCAT('Order ', NEW.order_number, ' Status Updated'),
            CONCAT('Your order status has been changed to: ', NEW.order_status),
            'ORDER',
            'ORDER',
            NEW.order_id
        );
    END IF;
END$$

-- Trigger: Create notification on shipment update
CREATE TRIGGER after_shipment_status_change
AFTER UPDATE ON shipments
FOR EACH ROW
BEGIN
    DECLARE customer_id_var INT;
    
    IF NEW.shipment_status != OLD.shipment_status THEN
        SELECT customer_id INTO customer_id_var 
        FROM orders 
        WHERE order_id = NEW.order_id;
        
        INSERT INTO notifications (user_id, title, message, notification_type, reference_type, reference_id)
        VALUES (
            customer_id_var,
            CONCAT('Shipment ', NEW.tracking_number, ' Updated'),
            CONCAT('Your shipment status: ', NEW.shipment_status),
            'SHIPMENT',
            'SHIPMENT',
            NEW.shipment_id
        );
    END IF;
END$$

-- Trigger: Create notification when ticket is assigned
CREATE TRIGGER after_ticket_assigned
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    IF NEW.assigned_to IS NOT NULL AND (OLD.assigned_to IS NULL OR NEW.assigned_to != OLD.assigned_to) THEN
        INSERT INTO notifications (user_id, title, message, notification_type, reference_type, reference_id)
        VALUES (
            NEW.assigned_to,
            CONCAT('Ticket ', NEW.ticket_number, ' Assigned'),
            CONCAT('You have been assigned ticket: ', NEW.subject),
            'TICKET',
            'TICKET',
            NEW.ticket_id
        );
    END IF;
END$$

-- Trigger: Update coupon usage count
CREATE TRIGGER after_order_with_coupon
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.coupon_code IS NOT NULL AND NEW.coupon_code != '' THEN
        UPDATE coupons 
        SET usage_count = usage_count + 1
        WHERE coupon_code = NEW.coupon_code;
    END IF;
END$$

-- Trigger: Auto-set review as verified purchase if order exists
CREATE TRIGGER before_review_insert
BEFORE INSERT ON reviews
FOR EACH ROW
BEGIN
    IF NEW.order_id IS NOT NULL THEN
        SET NEW.is_verified_purchase = TRUE;
    END IF;
END$$

DELIMITER ;
