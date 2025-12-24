-- ============================================
-- Stored Procedures
-- ============================================

USE ecommerce_db;

DELIMITER $$

-- Procedure: Place Order
CREATE PROCEDURE sp_place_order(
    IN p_customer_id INT,
    IN p_shipping_address TEXT,
    IN p_shipping_city VARCHAR(50),
    IN p_shipping_state VARCHAR(50),
    IN p_shipping_country VARCHAR(50),
    IN p_shipping_postal_code VARCHAR(20),
    IN p_shipping_phone VARCHAR(20),
    IN p_coupon_code VARCHAR(50),
    IN p_loyalty_points_used INT,
    OUT p_order_id INT,
    OUT p_error_message VARCHAR(255)
)
BEGIN
    DECLARE v_subtotal DECIMAL(10,2) DEFAULT 0;
    DECLARE v_discount_amount DECIMAL(10,2) DEFAULT 0;
    DECLARE v_tax_amount DECIMAL(10,2) DEFAULT 0;
    DECLARE v_shipping_fee DECIMAL(10,2) DEFAULT 5.00;
    DECLARE v_total_amount DECIMAL(10,2);
    DECLARE v_coupon_valid BOOLEAN DEFAULT FALSE;
    DECLARE v_coupon_discount_type VARCHAR(20);
    DECLARE v_coupon_discount_value DECIMAL(10,2);
    DECLARE v_cart_count INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_error_message = 'Error placing order';
        SET p_order_id = NULL;
    END;
    
    START TRANSACTION;
    
    -- Check if cart has items
    SELECT COUNT(*) INTO v_cart_count
    FROM shopping_cart
    WHERE customer_id = p_customer_id;
    
    IF v_cart_count = 0 THEN
        SET p_error_message = 'Shopping cart is empty';
        SET p_order_id = NULL;
        ROLLBACK;
    ELSE
        -- Calculate subtotal from cart
        SELECT SUM(p.final_price * sc.quantity) INTO v_subtotal
        FROM shopping_cart sc
        JOIN products p ON sc.product_id = p.product_id
        WHERE sc.customer_id = p_customer_id;
        
        -- Validate and apply coupon
        IF p_coupon_code IS NOT NULL AND p_coupon_code != '' THEN
            SELECT 
                (COUNT(*) > 0 AND MIN(is_active) = 1 AND MIN(valid_until) >= NOW() 
                 AND v_subtotal >= MIN(min_purchase_amount)
                 AND (MIN(usage_limit) IS NULL OR MIN(usage_count) < MIN(usage_limit))),
                MIN(discount_type),
                MIN(discount_value)
            INTO v_coupon_valid, v_coupon_discount_type, v_coupon_discount_value
            FROM coupons
            WHERE coupon_code = p_coupon_code;
            
            IF v_coupon_valid THEN
                IF v_coupon_discount_type = 'PERCENTAGE' THEN
                    SET v_discount_amount = v_subtotal * (v_coupon_discount_value / 100);
                ELSE
                    SET v_discount_amount = v_coupon_discount_value;
                END IF;
            END IF;
        END IF;
        
        -- Apply loyalty points discount (1 point = $0.01)
        IF p_loyalty_points_used > 0 THEN
            SET v_discount_amount = v_discount_amount + (p_loyalty_points_used * 0.01);
        END IF;
        
        -- Calculate tax (10% for demo)
        SET v_tax_amount = (v_subtotal - v_discount_amount) * 0.10;
        
        -- Calculate total
        SET v_total_amount = v_subtotal - v_discount_amount + v_tax_amount + v_shipping_fee;
        
        -- Create order
        INSERT INTO orders (
            customer_id, order_status, payment_status, payment_method,
            subtotal, discount_amount, tax_amount, shipping_fee, total_amount,
            shipping_address, shipping_city, shipping_state, shipping_country,
            shipping_postal_code, shipping_phone, coupon_code, loyalty_points_used
        ) VALUES (
            p_customer_id, 'PENDING', 'PAY_ON_ARRIVAL', 'CASH_ON_DELIVERY',
            v_subtotal, v_discount_amount, v_tax_amount, v_shipping_fee, v_total_amount,
            p_shipping_address, p_shipping_city, p_shipping_state, p_shipping_country,
            p_shipping_postal_code, p_shipping_phone, p_coupon_code, p_loyalty_points_used
        );
        
        SET p_order_id = LAST_INSERT_ID();
        
        -- Create order items from cart
        INSERT INTO order_items (order_id, product_id, seller_id, quantity, unit_price, total_price)
        SELECT 
            p_order_id,
            sc.product_id,
            p.seller_id,
            sc.quantity,
            p.final_price,
            p.final_price * sc.quantity
        FROM shopping_cart sc
        JOIN products p ON sc.product_id = p.product_id
        WHERE sc.customer_id = p_customer_id;
        
        -- Reserve inventory
        UPDATE inventory i
        JOIN shopping_cart sc ON i.product_id = sc.product_id
        SET i.reserved_quantity = i.reserved_quantity + sc.quantity
        WHERE sc.customer_id = p_customer_id
        AND i.warehouse_id = (
            SELECT warehouse_id FROM warehouses WHERE is_active = TRUE LIMIT 1
        );
        
        -- Deduct loyalty points if used
        IF p_loyalty_points_used > 0 THEN
            UPDATE customer_loyalty
            SET current_points = current_points - p_loyalty_points_used
            WHERE customer_id = p_customer_id;
            
            INSERT INTO loyalty_transactions (customer_id, transaction_type, points, reference_type, reference_id)
            VALUES (p_customer_id, 'REDEEMED', -p_loyalty_points_used, 'ORDER', p_order_id);
        END IF;
        
        -- Create payment record
        INSERT INTO payments (order_id, payment_method, amount, payment_status)
        VALUES (p_order_id, 'CASH_ON_DELIVERY', v_total_amount, 'PENDING');
        
        -- Create shipment record
        INSERT INTO shipments (order_id, shipment_status)
        VALUES (p_order_id, 'PENDING');
        
        -- Clear cart
        DELETE FROM shopping_cart WHERE customer_id = p_customer_id;
        
        SET p_error_message = NULL;
        COMMIT;
    END IF;
END$$

-- Procedure: Process Refund
CREATE PROCEDURE sp_process_refund(
    IN p_refund_id INT,
    IN p_approved_by INT,
    IN p_approve BOOLEAN,
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
    
    SELECT order_id, refund_amount INTO v_order_id, v_refund_amount
    FROM refunds
    WHERE refund_id = p_refund_id;
    
    IF p_approve THEN
        UPDATE refunds
        SET refund_status = 'APPROVED',
            approved_by = p_approved_by,
            processed_at = NOW()
        WHERE refund_id = p_refund_id;
        
        UPDATE orders
        SET order_status = 'REFUNDED',
            payment_status = 'REFUNDED'
        WHERE order_id = v_order_id;
        
        UPDATE payments
        SET payment_status = 'REFUNDED'
        WHERE order_id = v_order_id;
        
        -- Restore inventory
        UPDATE inventory i
        JOIN order_items oi ON i.product_id = oi.product_id
        SET i.quantity = i.quantity + oi.quantity,
            i.reserved_quantity = GREATEST(0, i.reserved_quantity - oi.quantity)
        WHERE oi.order_id = v_order_id;
        
        SET p_success = TRUE;
        SET p_message = 'Refund approved and processed';
    ELSE
        UPDATE refunds
        SET refund_status = 'REJECTED',
            approved_by = p_approved_by,
            processed_at = NOW()
        WHERE refund_id = p_refund_id;
        
        SET p_success = TRUE;
        SET p_message = 'Refund rejected';
    END IF;
    
    COMMIT;
END$$

-- Procedure: Assign Delivery Partner
CREATE PROCEDURE sp_assign_delivery_partner(
    IN p_shipment_id INT,
    OUT p_partner_id INT,
    OUT p_message VARCHAR(255)
)
BEGIN
    DECLARE v_shipping_city VARCHAR(50);
    DECLARE v_region_id INT;
    
    -- Get shipping city from order
    SELECT o.shipping_city INTO v_shipping_city
    FROM shipments s
    JOIN orders o ON s.order_id = o.order_id
    WHERE s.shipment_id = p_shipment_id;
    
    -- Find region matching city
    SELECT region_id INTO v_region_id
    FROM regions
    WHERE FIND_IN_SET(v_shipping_city, REPLACE(cities, ',', ',')) > 0
    AND is_active = TRUE
    LIMIT 1;
    
    -- Find available delivery partner in region
    SELECT partner_id INTO p_partner_id
    FROM delivery_partners
    WHERE region_id = v_region_id
    AND is_active = TRUE
    ORDER BY total_deliveries ASC, rating DESC
    LIMIT 1;
    
    IF p_partner_id IS NOT NULL THEN
        UPDATE shipments
        SET partner_id = p_partner_id,
            shipment_status = 'ASSIGNED'
        WHERE shipment_id = p_shipment_id;
        
        SET p_message = 'Delivery partner assigned successfully';
    ELSE
        SET p_message = 'No available delivery partner found';
    END IF;
END$$

-- Procedure: Calculate Loyalty Tier
CREATE PROCEDURE sp_update_loyalty_tier(
    IN p_customer_id INT
)
BEGIN
    DECLARE v_current_points INT;
    DECLARE v_new_tier_id INT;
    
    SELECT current_points INTO v_current_points
    FROM customer_loyalty
    WHERE customer_id = p_customer_id;
    
    SELECT tier_id INTO v_new_tier_id
    FROM loyalty_tiers
    WHERE v_current_points >= min_points
    AND (max_points IS NULL OR v_current_points <= max_points)
    ORDER BY min_points DESC
    LIMIT 1;
    
    UPDATE customer_loyalty
    SET tier_id = v_new_tier_id
    WHERE customer_id = p_customer_id;
END$$

-- Procedure: Generate Sales Report
CREATE PROCEDURE sp_generate_sales_report(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT 
        DATE(o.created_at) as sale_date,
        COUNT(DISTINCT o.order_id) as total_orders,
        SUM(o.total_amount) as total_revenue,
        AVG(o.total_amount) as avg_order_value,
        SUM(o.discount_amount) as total_discounts,
        COUNT(DISTINCT o.customer_id) as unique_customers
    FROM orders o
    WHERE DATE(o.created_at) BETWEEN p_start_date AND p_end_date
    AND o.order_status NOT IN ('CANCELLED', 'REFUNDED')
    GROUP BY DATE(o.created_at)
    ORDER BY sale_date;
END$$

DELIMITER ;
