-- Stored Procedures for E-Commerce Platform
-- Complex operations with transaction support

DELIMITER $$

-- =============================================
-- ORDER PROCESSING PROCEDURES
-- =============================================

-- Procedure: Create order from cart
CREATE PROCEDURE process_cart_to_order(
    IN p_customer_id INT,
    IN p_cart_id INT,
    IN p_shipping_address TEXT,
    IN p_billing_address TEXT,
    IN p_coupon_code VARCHAR(50),
    OUT p_order_id INT,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_subtotal DECIMAL(10,2) DEFAULT 0;
    DECLARE v_tax_rate DECIMAL(5,2) DEFAULT 0.10; -- 10% tax
    DECLARE v_tax_amount DECIMAL(10,2) DEFAULT 0;
    DECLARE v_shipping_cost DECIMAL(10,2) DEFAULT 5.99;
    DECLARE v_discount_amount DECIMAL(10,2) DEFAULT 0;
    DECLARE v_total DECIMAL(10,2) DEFAULT 0;
    DECLARE v_coupon_id INT  DEFAULT NULL;
    DECLARE v_coupon_type VARCHAR(20);
    DECLARE v_discount_value DECIMAL(10,2);
    DECLARE v_error_count INT DEFAULT 0;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_message = 'Error processing order';
        SET p_order_id = NULL;
    END;
    
    START TRANSACTION;
    
    -- Calculate subtotal from cart
    SELECT SUM(ci.quantity * ci.price) INTO v_subtotal
    FROM cart_item ci
    WHERE ci.cart_id = p_cart_id;
    
    IF v_subtotal IS NULL OR v_subtotal = 0 THEN
        SET p_message = 'Cart is empty';
        ROLLBACK;
    ELSE
        -- Validate and apply coupon if provided
        IF p_coupon_code IS NOT NULL THEN
            SELECT coupon_id, discount_type, discount_value 
            INTO v_coupon_id, v_coupon_type, v_discount_value
            FROM coupon
            WHERE code = p_coupon_code
              AND is_active = TRUE
              AND (expiry_date IS NULL OR expiry_date >= CURDATE())
              AND times_used < usage_limit
            LIMIT 1;
            
            IF v_coupon_id IS NOT NULL THEN
                IF v_coupon_type = 'percentage' THEN
                    SET v_discount_amount = v_subtotal * (v_discount_value / 100);
                ELSE
                    SET v_discount_amount = v_discount_value;
                END IF;
            END IF;
        END IF;
        
        -- Calculate totals
        SET v_tax_amount = (v_subtotal - v_discount_amount) * v_tax_rate;
        SET v_total = v_subtotal - v_discount_amount + v_tax_amount + v_shipping_cost;
        
        -- Create order
        INSERT INTO `order` (
            customer_id, subtotal, tax_amount, shipping_cost, 
            discount_amount, total_amount, shipping_address, 
            billing_address, coupon_id, status
        ) VALUES (
            p_customer_id, v_subtotal, v_tax_amount, v_shipping_cost,
            v_discount_amount, v_total, p_shipping_address,
            COALESCE(p_billing_address, p_shipping_address), v_coupon_id, 'pending'
        );
        
        SET p_order_id = LAST_INSERT_ID();
        
        -- Copy cart items to order items
        INSERT INTO order_item (order_id, product_id, quantity, price, subtotal)
        SELECT p_order_id, ci.product_id, ci.quantity, ci.price, (ci.quantity * ci.price)
        FROM cart_item ci
        WHERE ci.cart_id = p_cart_id;
        
        -- Clear cart
        DELETE FROM cart_item WHERE cart_id = p_cart_id;
        
        SET p_message = 'Order created successfully';
        COMMIT;
    END IF;
END$$

-- Procedure: Cancel order and restore inventory
CREATE PROCEDURE cancel_order(
    IN p_order_id INT,
    IN p_reason TEXT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_order_status VARCHAR(20);
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Error cancelling order';
    END;
    
    START TRANSACTION;
    
    -- Get current order status
    SELECT status INTO v_order_status
    FROM `order`
    WHERE order_id = p_order_id;
    
    IF v_order_status IN ('delivered', 'cancelled', 'refunded') THEN
        SET p_success = FALSE;
        SET p_message = CONCAT('Cannot cancel order with status: ', v_order_status);
        ROLLBACK;
    ELSE
        -- Update order status
        UPDATE `order`
        SET status = 'cancelled',
            notes = CONCAT(COALESCE(notes, ''), ' Cancelled: ', p_reason)
        WHERE order_id = p_order_id;
        
        SET p_success = TRUE;
        SET p_message = 'Order cancelled successfully';
        COMMIT;
    END IF;
END$$

-- =============================================
-- PAYMENT PROCESSING PROCEDURES
-- =============================================

-- Procedure: Process payment
CREATE PROCEDURE process_payment(
    IN p_order_id INT,
    IN p_payment_method VARCHAR(50),
    IN p_gateway_id INT,
    IN p_transaction_id VARCHAR(100),
    OUT p_payment_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_order_amount DECIMAL(10,2);
    DECLARE v_order_status VARCHAR(20);
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Payment processing failed';
    END;
    
    START TRANSACTION;
    
    -- Get order details
    SELECT total_amount, status 
    INTO v_order_amount, v_order_status
    FROM `order`
    WHERE order_id = p_order_id;
    
    IF v_order_status != 'pending' THEN
        SET p_success = FALSE;
        SET p_message = 'Order is not pending';
        ROLLBACK;
    ELSE
        -- Insert payment record
        INSERT INTO payment (
            order_id, gateway_id, payment_method, 
            amount, status, transaction_id
        ) VALUES (
            p_order_id, p_gateway_id, p_payment_method,
            v_order_amount, 'completed', p_transaction_id
        );
        
        SET p_payment_id = LAST_INSERT_ID();
        
        -- Update order status
        UPDATE `order`
        SET status = 'processing'
        WHERE order_id = p_order_id;
        
        SET p_success = TRUE;
        SET p_message = 'Payment processed successfully';
        COMMIT;
    END IF;
END$$

-- =============================================
-- INVENTORY MANAGEMENT PROCEDURES
-- =============================================

-- Procedure: Restock inventory
CREATE PROCEDURE restock_inventory(
    IN p_product_id INT,
    IN p_warehouse_id INT,
    IN p_quantity INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Error restocking inventory';
    END;
    
    START TRANSACTION;
    
    -- Update inventory
    INSERT INTO inventory (product_id, warehouse_id, quantity, last_restock_date)
    VALUES (p_product_id, p_warehouse_id, p_quantity, CURDATE())
    ON DUPLICATE KEY UPDATE 
        quantity = quantity + p_quantity,
        last_restock_date = CURDATE();
    
    SET p_success = TRUE;
    SET p_message = CONCAT('Added ', p_quantity, ' units to inventory');
    COMMIT;
END$$

-- Procedure: Transfer stock between warehouses
CREATE PROCEDURE transfer_stock(
    IN p_product_id INT,
    IN p_from_warehouse INT,
    IN p_to_warehouse INT,
    IN p_quantity INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_available_qty INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Error transferring stock';
    END;
    
    START TRANSACTION;
    
    -- Check available quantity at source warehouse
    SELECT quantity INTO v_available_qty
    FROM inventory
    WHERE product_id = p_product_id AND warehouse_id = p_from_warehouse;
    
    IF v_available_qty < p_quantity THEN
        SET p_success = FALSE;
        SET p_message = 'Insufficient stock at source warehouse';
        ROLLBACK;
    ELSE
        -- Decrease from source
        UPDATE inventory
        SET quantity = quantity - p_quantity
        WHERE product_id = p_product_id AND warehouse_id = p_from_warehouse;
        
        -- Increase at destination
        INSERT INTO inventory (product_id, warehouse_id, quantity)
        VALUES (p_product_id, p_to_warehouse, p_quantity)
        ON DUPLICATE KEY UPDATE quantity = quantity + p_quantity;
        
        SET p_success = TRUE;
        SET p_message = 'Stock transferred successfully';
        COMMIT;
    END IF;
END$$

-- =============================================
-- CUSTOMER MANAGEMENT PROCEDURES
-- =============================================

-- Procedure: Register new customer
CREATE PROCEDURE register_customer(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_phone VARCHAR(20),
    IN p_address TEXT,
    IN p_password VARCHAR(255),
    OUT p_customer_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_existing_email INT DEFAULT 0;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Error registering customer';
    END;
    
    START TRANSACTION;
    
    -- Check if email already exists
    SELECT COUNT(*) INTO v_existing_email
    FROM customer
    WHERE email = p_email;
    
    IF v_existing_email > 0 THEN
        SET p_success = FALSE;
        SET p_message = 'Email already registered';
        ROLLBACK;
    ELSE
        -- Insert new customer
        INSERT INTO customer (name, email, phone, address, password_hash, is_active)
        VALUES (p_name, p_email, p_phone, p_address, p_password, TRUE);
        
        SET p_customer_id = LAST_INSERT_ID();
        
        -- Create cart for customer
        INSERT INTO cart (customer_id) VALUES (p_customer_id);
        
        -- Initialize loyalty program
        INSERT INTO loyality_program (customer_id, points, join_date, last_activity)
        VALUES (p_customer_id, 0, CURDATE(), CURDATE());
        
        SET p_success = TRUE;
        SET p_message = 'Customer registered successfully';
        COMMIT;
    END IF;
END$$

-- =============================================
-- REFUND PROCESSING PROCEDURES
-- =============================================

-- Procedure: Process refund request
CREATE PROCEDURE process_refund(
    IN p_refund_id INT,
    IN p_approved BOOLEAN,
    IN p_admin_id INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_order_id INT;
    DECLARE v_refund_amount DECIMAL(10,2);
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_success = FALSE;
        SET p_message = 'Error processing refund';
    END;
    
    START TRANSACTION;
    
    -- Get refund details
    SELECT order_id, refund_amount
    INTO v_order_id, v_refund_amount
    FROM refund_request
    WHERE refund_id = p_refund_id;
    
    IF p_approved THEN
        -- Approve and process refund
        UPDATE refund_request
        SET status = 'processed',
            processed_date = NOW()
        WHERE refund_id = p_refund_id;
        
        -- Restore inventory (items will be returned)
        UPDATE inventory i
        INNER JOIN order_item oi ON i.product_id = oi.product_id
        SET i.quantity = i.quantity + oi.quantity
        WHERE oi.order_id = v_order_id;
        
        SET p_success = TRUE;
        SET p_message = 'Refund approved and processed';
    ELSE
        -- Reject refund
        UPDATE refund_request
        SET status = 'rejected',
            processed_date = NOW()
        WHERE refund_id = p_refund_id;
        
        SET p_success = TRUE;
        SET p_message = 'Refund request rejected';
    END IF;
    
    COMMIT;
END$$

-- =============================================
-- REPORTING PROCEDURES
-- =============================================

-- Procedure: Generate sales report
CREATE PROCEDURE generate_sales_report(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT 
        DATE(order_date) as date,
        COUNT(DISTINCT order_id) as total_orders,
        COUNT(DISTINCT customer_id) as unique_customers,
        SUM(subtotal) as gross_sales,
        SUM(discount_amount) as total_discounts,
        SUM(tax_amount) as total_tax,
        SUM(shipping_cost) as total_shipping,
        SUM(total_amount) as net_sales
    FROM `order`
    WHERE order_date BETWEEN p_start_date AND p_end_date
      AND status NOT IN ('cancelled', 'refunded')
    GROUP BY DATE(order_date)
    ORDER BY date DESC;
END$$

-- Procedure: Get customer lifetime value
CREATE PROCEDURE get_customer_ltv(
    IN p_customer_id INT
)
BEGIN
    SELECT 
        c.customer_id,
        c.name,
        c.email,
        c.date_created,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(o.total_amount) as lifetime_value,
        AVG(o.total_amount) as avg_order_value,
        MAX(o.order_date) as last_order_date,
        DATEDIFF(NOW(), c.date_created) as customer_age_days,
        COALESCE(lp.points, 0) as loyalty_points,
        COALESCE(lp.tier, 'bronze') as loyalty_tier
    FROM customer c
    LEFT JOIN `order` o ON c.customer_id = o.customer_id AND o.status NOT IN ('cancelled', 'refunded')
    LEFT JOIN loyality_program lp ON c.customer_id = lp.customer_id
    WHERE c.customer_id = p_customer_id
    GROUP BY c.customer_id, c.name, c.email, c.date_created, lp.points, lp.tier;
END$$

DELIMITER ;
