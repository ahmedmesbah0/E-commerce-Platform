-- =====================================================
-- SAMPLE DATA FOR E-COMMERCE DATABASE
-- Egyptian Context - Categories, Products, Customers, Orders
-- =====================================================

USE ecommerce_db;

-- =====================================================
-- INSERT CATEGORIES
-- =====================================================

INSERT INTO category (name, parent_category_id, description) VALUES
('Electronics', NULL, 'Electronic devices and accessories'),
('Fashion', NULL, 'Clothing and accessories'),
('Home & Kitchen', NULL, 'Home appliances and kitchenware'),
('Books & Stationery', NULL, 'Books, notebooks, and office supplies'),
('Sports & Outdoors', NULL, 'Sports equipment and outdoor gear'),
('Beauty & Health', NULL, 'Beauty products and health items'),
('Toys & Games', NULL, 'Toys and games for all ages'),
('Automotive', NULL, 'Car accessories and parts');

-- Subcategories
INSERT INTO category (name, parent_category_id, description) VALUES
('Mobile Phones', 1, 'Smartphones and mobile devices'),
('Laptops', 1, 'Laptop computers'),
('Mens Fashion', 2, 'Mens clothing and accessories'),
('Womens Fashion', 2, 'Womens clothing and accessories'),
('Kitchen Appliances', 3, 'Kitchen tools and appliances'),
('Arabic Books', 4, 'Books in Arabic language');

-- =====================================================
-- INSERT WAREHOUSES
-- =====================================================

INSERT INTO warehouse (location, capacity) VALUES
('Cairo Distribution Center - 6th October City', 50000),
('Alexandria Warehouse - Borg El Arab', 30000),
('Giza Storage Facility - Sheikh Zayed', 40000);

-- =====================================================
-- INSERT SHIPPING PROVIDERS  
-- =====================================================

INSERT INTO delivery_partner (name, phone, region, is_active) VALUES
('Aramex Egypt', '+20233041500', 'Greater Cairo', TRUE),
('DHL Egypt', '+20227956000', 'All Egypt', TRUE),
('Bosta Delivery', '+201000077000', 'Cairo & Alex', TRUE),
('Egypt Post', '+20225775111', 'All Egypt', TRUE);

-- =====================================================
-- INSERT PRODUCTS
-- =====================================================

-- Electronics - Mobile Phones
INSERT INTO product (name, description, price, category_id, weight, dimensions, is_active) VALUES
('Samsung Galaxy S23', 'Samsung flagship smartphone with 256GB storage', 25999.00, 9, 0.2, '15x7x0.8 cm', TRUE),
('iPhone 14 Pro', 'Apple iPhone 14 Pro with 128GB storage', 35999.00, 9, 0.21, '15x7x0.8 cm', TRUE),
('Xiaomi Redmi Note 12', 'Budget-friendly smartphone with great features', 7999.00, 9, 0.19, '16x7x0.9 cm', TRUE),
('OPPO Reno 10', 'Mid-range smartphone with excellent camera', 12999.00, 9, 0.18, '16x7x0.8 cm', TRUE),
('Realme 11 Pro', 'Performance smartphone with fast charging', 9999.00, 9, 0.19, '16x7x0.85 cm', TRUE);

-- Electronics - Laptops
INSERT INTO product (name, description, price, category_id, weight, dimensions, is_active) VALUES
('Dell Inspiron 15', 'Dell laptop with Intel i5, 8GB RAM, 512GB SSD', 18999.00, 10, 2.1, '36x25x2 cm', TRUE),
('HP Pavilion 14', 'HP laptop with AMD Ryzen 5, 16GB RAM', 20999.00, 10, 1.8, '32x22x2 cm', TRUE),
('Lenovo IdeaPad 3', 'Budget laptop for students and home use', 12999.00, 10, 2.0, '36x25x2.5 cm', TRUE),
('ASUS VivoBook', 'Slim and lightweight laptop for work', 16999.00, 10, 1.6, '32x21x1.8 cm', TRUE);

-- Fashion - Mens
INSERT INTO product (name, description, price, category_id, weight, dimensions, is_active) VALUES
('Mens Cotton Shirt - Blue', 'Classic cotton shirt for formal occasions', 299.00, 11, 0.3, '40x30x5 cm', TRUE),
('Mens Jeans - Dark Blue', 'Comfortable denim jeans', 499.00, 11, 0.6, '40x35x5 cm', TRUE),
('Mens Sports Shoes - Nike', 'Running shoes for athletic performance', 1299.00, 11, 0.8, '35x25x15 cm', TRUE),
('Mens Leather Belt', 'Genuine leather belt', 199.00, 11, 0.2, '45x10x3 cm', TRUE);

-- Fashion - Womens
INSERT INTO product (name, description, price, category_id, weight, dimensions, is_active) VALUES
('Womens Abaya - Black', 'Elegant traditional abaya', 599.00, 12, 0.4, '45x35x5 cm', TRUE),
('Womens Hijab - Silk', 'Premium quality silk hijab', 149.00, 12, 0.1, '25x25x2 cm', TRUE),
('Womens Handbag', 'Stylish leather handbag', 799.00, 12, 0.5, '35x25x15 cm', TRUE),
('Womens Sandals', 'Comfortable summer sandals', 399.00, 12, 0.4, '30x20x12 cm', TRUE);

-- Home & Kitchen
INSERT INTO product (name, description, price, category_id, weight, dimensions, is_active) VALUES
('Tefal Air Fryer', 'Healthy cooking with air frying technology', 2499.00, 13, 4.5, '40x35x30 cm', TRUE),
('Braun Coffee Maker', 'Automatic coffee machine', 1899.00, 13, 2.5, '35x25x35 cm', TRUE),
('Toshiba Microwave', '23L microwave oven', 2199.00, 13, 12.0, '50x40x30 cm', TRUE),
('Ariston Gas Stove', '4 burner gas cooker', 4999.00, 13, 25.0, '60x60x85 cm', TRUE);

-- Books in Arabic
INSERT INTO product (name, description, price, category_id, weight, dimensions, is_active) VALUES
('روايات نجيب محفوظ - مجموعة', 'Complete works of Naguib Mahfouz', 299.00, 14, 1.2, '25x17x5 cm', TRUE),
('القرآن الكريم مع التفسير', 'Holy Quran with Tafseer', 199.00, 14, 0.8, '20x15x3 cm', TRUE),
('كتاب الأيام - طه حسين', 'Classic Egyptian literature', 89.00, 14, 0.3, '20x14x2 cm', TRUE),
('الثقافة الإسلامية', 'Islamic culture textbook', 149.00, 14, 0.5, '24x17x2 cm', TRUE);

-- Sports & Outdoors
INSERT INTO product (name, description, price, category_id, weight, dimensions, is_active) VALUES
('Football - Adidas', 'Professional football', 399.00, 5, 0.5, '25x25x25 cm', TRUE),
('Yoga Mat', 'Exercise mat for home workouts', 249.00, 5, 1.0, '180x60x1 cm', TRUE),
('Gym Bag', 'Sports bag for gym equipment', 299.00, 5, 0.4, '50x30x25 cm', TRUE);

-- =====================================================
-- INSERT CUSTOMERS
-- =====================================================

INSERT INTO customer (name, email, phone, address, password_hash, is_active) VALUES
('Ahmed Mohamed Hassan', 'ahmed.mohamed@email.com', '+201012345678', '15 Tahrir Street, Downtown, Cairo', '$2y$10$demoHashForAcademicProject123', TRUE),
('Fatima Ali Ibrahim', 'fatima.ali@email.com', '+201123456789', '23 El Horreya Road, Alexandria', '$2y$10$demoHashForAcademicProject123', TRUE),
('Mohamed Mahmoud Said', 'mohamed.mahmoud@email.com', '+201234567890', '45 Pyramids Road, Giza', '$2y$10$demoHashForAcademicProject123', TRUE),
('Noha Hussein Ali', 'noha.hussein@email.com', '+201111222333', '12 Nasr City, Cairo', '$2y$10$demoHashForAcademicProject123', TRUE),
('Khaled Mostafa Ahmed', 'khaled.mostafa@email.com', '+201222333444', '8 El Maadi, Cairo', '$2y$10$demoHashForAcademicProject123', TRUE),
('Mariam Yasser Salah', 'mariam.yasser@email.com', '+201333444555', '34 Heliopolis, Cairo', '$2y$10$demoHashForAcademicProject123', TRUE),
('Omar Hesham Khalil', 'omar.hesham@email.com', '+201444555666', '56 October 6th City, Giza', '$2y$10$demoHashForAcademicProject123', TRUE),
('Sara Tarek Nabil', 'sara.tarek@email.com', '+201555666777', '78 Zamalek, Cairo', '$2y$10$demoHashForAcademicProject123', TRUE),
('Youssef Ashraf Metwally', 'youssef.ashraf@email.com', '+201666777888', '90 Mohandessin, Giza', '$2y$10$demoHashForAcademicProject123', TRUE),
('Heba Kamal Fahmy', 'heba.kamal@email.com', '+201777888999', '101 New Cairo', '$2y$10$demoHashForAcademicProject123', TRUE);

-- =====================================================
-- INSERT SHIPPING ADDRESSES (table may not exist in current schema)
-- =====================================================

-- INSERT INTO shipping_address (customer_id, address_label, street_address, city, state, postal_code, country, is_default) VALUES
-- (1, 'Home', '15 Tahrir Street', 'Cairo', 'Cairo Governorate', '11511', 'Egypt', TRUE),
-- ... etc

-- =====================================================
-- INSERT INVENTORY
-- =====================================================

-- Products in Cairo warehouse
INSERT INTO inventory (product_id, warehouse_id, quantity, reorder_level) VALUES
(1, 1, 45, 10),  -- Samsung Galaxy S23
(2, 1, 30, 10),  -- iPhone 14 Pro
(3, 1, 80, 15),  -- Xiaomi Redmi
(4, 1, 60, 15),  -- OPPO Reno
(5, 1, 70, 15),  -- Realme 11 Pro
(6, 1, 25, 5),   -- Dell Laptop
(7, 1, 30, 5),   -- HP Laptop
(8, 1, 40, 8),   -- Lenovo Laptop
(9, 1, 35, 5),   -- ASUS Laptop
(10, 1, 150, 30), -- Mens Shirt
(11, 1, 200, 40), -- Mens Jeans
(12, 1, 100, 20), -- Nike Shoes
(13, 1, 120, 25), -- Leather Belt
(14, 1, 180, 35), -- Womens Abaya
(15, 1, 250, 50), -- Silk Hijab
(16, 1, 90, 20),  -- Handbag
(17, 1, 110, 25), -- Sandals
(18, 1, 50, 10),  -- Air Fryer
(19, 1, 60, 12),  -- Coffee Maker
(20, 1, 45, 10),  -- Microwave
(21, 1, 25, 5);   -- Gas Stove

-- Products in Alexandria warehouse
INSERT INTO inventory (product_id, warehouse_id, quantity, reorder_level) VALUES
(1, 2, 35, 10),
(3, 2, 90, 15),
(5, 2, 80, 15),
(6, 2, 20, 5),
(10, 2, 100, 25),
(14, 2, 150, 30),
(15, 2, 200, 40);

-- Products in Giza warehouse
INSERT INTO inventory (product_id, warehouse_id, quantity, reorder_level) VALUES
(2, 3, 25, 10),
(4, 3, 70, 15),
(7, 3, 28, 5),
(11, 3, 180, 35),
(18, 3, 55, 10),
(19, 3, 50, 10);

-- =====================================================
-- INSERT ORDERS
-- =====================================================

INSERT INTO `order` (customer_id, order_date, status, subtotal, tax_amount, shipping_cost, total_amount, shipping_address, payment_method) VALUES
(1, '2025-12-15 10:30:00', 'delivered', 25999.00, 250.00, 50.00, 26299.00, '15 Tahrir Street, Downtown, Cairo', 'credit_card'),
(2, '2025-12-16 14:20:00', 'delivered', 8299.00, 150.00, 50.00, 8498.00, '23 El Horreya Road, Alexandria', 'cash'),
(3, '2025-12-17 09:15:00', 'shipped', 21248.00, 200.00, 50.00, 21498.00, '45 Pyramids Road, Giza', 'credit_card'),
(4, '2025-12-18 16:45:00', 'processing', 1147.00, 20.00, 30.00, 1197.00, '12 Nasr City, Cairo', 'cash'),
(5, '2025-12-19 11:30:00', 'pending', 37398.00, 500.00, 100.00, 37998.00, '8 El Maadi, Cairo', 'credit_card'),
(6, '2025-12-19 13:00:00', 'processing', 698.00, 20.00, 30.00, 748.00, '34 Heliopolis, Cairo', 'cash'),
(7, '2025-12-20 08:30:00', 'pending', 2658.00, 50.00, 40.00, 2748.00, '56 October 6th City, Giza', 'cash');

-- =====================================================
-- INSERT ORDER ITEMS
-- =====================================================

-- Order 1 (Ahmed - Samsung phone)
INSERT INTO order_item (order_id, product_id, quantity, price, subtotal) VALUES
(1, 1, 1, 25999.00, 25999.00);

-- Order 2 (Fatima - Xiaomi phone + accessories)
INSERT INTO order_item (order_id, product_id, quantity, price, subtotal) VALUES
(2, 3, 1, 7999.00, 7999.00),
(2, 13, 1, 199.00, 199.00),
(2, 25, 1, 249.00, 249.00);

-- Order 3 (Mohamed - Dell Laptop + Bag)
INSERT INTO order_item (order_id, product_id, quantity, price, subtotal) VALUES
(3, 6, 1, 18999.00, 18999.00),
(3, 26, 1, 299.00, 299.00),
(3, 23, 5, 399.00, 1995.00);

-- Order 4 (Noha - Fashion items)
INSERT INTO order_item (order_id, product_id, quantity, price, subtotal) VALUES
(4, 14, 1, 599.00, 599.00),
(4, 15, 3, 149.00, 447.00),
(4, 17, 1, 399.00, 399.00);

-- Order 5 (Khaled - iPhone)
INSERT INTO order_item (order_id, product_id, quantity, price, subtotal) VALUES
(5, 2, 1, 35999.00, 35999.00),
(5, 12, 1, 1299.00, 1299.00);

-- Order 6 (Mariam - Books)
INSERT INTO order_item (order_id, product_id, quantity, price, subtotal) VALUES
(6, 22, 1, 299.00, 299.00),
(6, 23, 1, 199.00, 199.00),
(6, 24, 1, 89.00, 89.00),
(6, 25, 1, 149.00, 149.00);

-- Order 7 (Omar - Kitchen appliances)
INSERT INTO order_item (order_id, product_id, quantity, price, subtotal) VALUES
(7, 18, 1, 2499.00, 2499.00),
(7, 24, 1, 89.00, 89.00),
(7, 15, 1, 149.00, 149.00);

-- =====================================================
-- INSERT PAYMENTS
-- =====================================================

INSERT INTO payment (order_id, payment_method, amount, payment_status, transaction_id, payment_date) VALUES
(1, 'credit_card', 26299.00, 'completed', 'TXN2025121501', '2025-12-15 10:31:00'),
(2, 'cash_on_delivery', 8498.00, 'completed', NULL, '2025-12-16 18:30:00'),
(3, 'credit_card', 21498.00, 'completed', 'TXN2025121701', '2025-12-17 09:16:00'),
(4, 'cash_on_delivery', 1197.00, 'pending', NULL, NULL),
(5, 'credit_card', 37998.00, 'pending', NULL, NULL),
(6, 'cash_on_delivery', 748.00, 'pending', NULL, NULL),
(7, 'cash_on_delivery', 2748.00, 'pending', NULL, NULL);

-- =====================================================
-- INSERT SHIPMENTS
-- =====================================================

INSERT INTO shipment (order_id, courier_id, tracking_number, shipped_date, estimated_delivery, actual_delivery, status) VALUES
(1, 1, 'ARM2025121501EG', '2025-12-15 14:00:00', '2025-12-17', '2025-12-17 15:30:00', 'delivered'),
(2, 3, 'BOSTA2025121601', '2025-12-16 16:00:00', '2025-12-18', '2025-12-18 14:20:00', 'delivered'),
(3, 2, 'DHL2025121701EG', '2025-12-17 11:00:00', '2025-12-20', NULL, 'in_transit');

-- =====================================================
-- INSERT REVIEWS
-- =====================================================

INSERT INTO review (product_id, customer_id, rating, title, comment, review_date, is_verified_purchase) VALUES
(1, 1, 5, 'ممتاز جداً', 'الموبايل رائع والأداء ممتاز. شحن سريع وجودة عالية', '2025-12-18 10:00:00', TRUE),
(3, 2, 4, 'قيمة ممتازة مقابل السعر', 'موبايل جيد جداً للسعر، الكاميرا جيدة والبطارية تدوم', '2025-12-19 11:00:00', TRUE),
(6, 3, 5, 'لابتوب رائع للعمل', 'سريع جداً ومناسب للعمل والدراسة', '2025-12-20 09:00:00', TRUE);

-- =====================================================
-- INSERT COUPONS
-- =====================================================

INSERT INTO coupon (code, description, discount_type, discount_value, min_order_amount, valid_from, valid_until, usage_limit, is_active) VALUES
('WELCOME2025', 'Welcome discount for new customers', 'percentage', 10.00, 500.00, '2025-01-01', '2025-12-31', 1000, TRUE),
('RAMADAN25', 'Ramadan special discount', 'percentage', 25.00, 1000.00, '2025-03-01', '2025-04-30', 500, TRUE),
('SUMMER100', 'Summer sale - 100 EGP off', 'fixed_amount', 100.00, 500.00, '2025-06-01', '2025-08-31', 2000, TRUE),
('ELECTRONICS15', 'Electronics discount', 'percentage', 15.00, 2000.00, '2025-01-01', '2025-12-31', 300, TRUE);

-- =====================================================
-- INSERT WISHLISTS (if table exists)
-- =====================================================

-- INSERT INTO wishlist (customer_id, product_id) VALUES
-- (1, 7),  -- Ahmed wishlist HP Laptop
-- (1, 18), -- Ahmed wishlist Air Fryer
-- (2, 2),  -- Fatima wishlist iPhone
-- (3, 21), -- Mohamed wishlist Gas Stove
-- (4, 16), -- Noha wishlist Handbag
-- (5, 9);  -- Khaled wishlist ASUS Laptop

-- =====================================================
-- INSERT LOYALTY TRANSACTIONS (if table exists)
-- =====================================================

-- INSERT INTO loyalty_transaction (customer_id, points, transaction_type, order_id, description) VALUES
-- (1, 262, 'earned', 1, 'Earned 262 points from order #1'),
-- (2, 84, 'earned', 2, 'Earned 84 points from order #2'),
-- (3, 214, 'earned', 3, 'Earned 214 points from order #3');

-- =====================================================
-- END OF SAMPLE DATA
-- =====================================================

SELECT 'Sample data inserted successfully!' as Status;
SELECT CONCAT('Total Products: ', COUNT(*)) as ProductCount FROM product;
SELECT CONCAT('Total Customers: ', COUNT(*)) as CustomerCount FROM customer;
SELECT CONCAT('Total Orders: ', COUNT(*)) as OrderCount FROM `order`;
SELECT CONCAT('Total Inventory Records: ', COUNT(*)) as InventoryCount FROM inventory;
