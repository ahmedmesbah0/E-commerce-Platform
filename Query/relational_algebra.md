# ====================================================================
# RELATIONAL ALGEBRA FOR E-COMMERCE SQL QUERIES
# ====================================================================
# This file provides relational algebra notation for the SQL queries
# in sql_queries.sql
# ====================================================================

## NOTATION LEGEND:
```
σ (sigma)     = Selection (WHERE clause)
π (pi)        = Projection (SELECT clause)
⨝ (bowtie)    = Natural Join
⋈ (join)      = Theta Join (join with condition)
⟕             = Left Outer Join
⟖             = Right Outer Join
⟗             = Full Outer Join
∪ (union)     = Union
∩ (intersect) = Intersection
− (minus)     = Difference
× (times)     = Cartesian Product
ρ (rho)       = Rename
G (gamma)     = Grouping/Aggregation
δ (delta)     = Duplicate elimination (DISTINCT)
τ (tau)       = Ordering (ORDER BY)
```

---

## SECTION 1: BASIC SELECTION AND PROJECTION

### Query 3.1: Products with discounts
**SQL:**
```sql
SELECT product_name, final_price, 
       base_price - final_price AS discount_amount
FROM products
WHERE is_active = TRUE AND final_price < base_price
ORDER BY discount_percentage DESC;
```

**Relational Algebra:**
```
τdiscount_percentage↓(
    πproduct_name, final_price, (base_price - final_price) → discount_amount(
        σis_active=TRUE ∧ final_price<base_price(products)
    )
)
```

### Query 3.2: Count unique customers
**SQL:**
```sql
SELECT COUNT(DISTINCT customer_id) as unique_customers
FROM orders
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH);
```

**Relational Algebra:**
```
πCOUNT(DISTINCT customer_id) → unique_customers(
    σcreated_at >= (NOW() - 1 MONTH)(orders)
)
```

### Query 3.3: Product search with LIKE
**SQL:**
```sql
SELECT product_name, final_price, description
FROM products
WHERE product_name LIKE '%Pro%'
ORDER BY final_price DESC;
```

**Relational Algebra:**
```
τfinal_price↓(
    πproduct_name, final_price, description(
        σproduct_name LIKE '%Pro%'(products)
    )
)
```

---

## SECTION 2: AGGREGATION AND GROUPING

### Query 4.1: Category statistics with GROUP BY
**SQL:**
```sql
SELECT category_name, COUNT(p.product_id) as product_count,
       AVG(p.final_price) as avg_price
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_name
HAVING product_count > 0;
```

**Relational Algebra:**
```
σproduct_count>0(
    category_nameG COUNT(product_id) → product_count, AVG(final_price) → avg_price(
        categories ⟕c.category_id=p.category_id products
    )
)
```

### Query 4.2: Seller revenue with HAVING
**SQL:**
```sql
SELECT seller_id, COUNT(DISTINCT p.product_id) as products_listed,
       SUM(oi.total_price) as total_revenue
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY seller_id
HAVING total_revenue > 1000;
```

**Relational Algebra:**
```
σtotal_revenue>1000(
    seller_idG COUNT(DISTINCT product_id) → products_listed, 
                SUM(total_price) → total_revenue(
        products ⟕p.product_id=oi.product_id order_items
    )
)
```

---

## SECTION 3: JOINS

### Query 5.1: INNER JOIN - Orders with customer details
**SQL:**
```sql
SELECT o.order_number, CONCAT(u.first_name, ' ', u.last_name) as customer_name,
       o.total_amount
FROM orders o
INNER JOIN users u ON o.customer_id = u.user_id;
```

**Relational Algebra:**
```
πorder_number, (first_name || ' ' || last_name) → customer_name, total_amount(
    orders ⋈o.customer_id=u.user_id users
)
```

### Query 5.2: LEFT JOIN - Products with or without inventory
**SQL:**
```sql
SELECT p.product_name, SUM(i.available_quantity) as available_stock
FROM products p
LEFT JOIN inventory i ON p.product_id = i.product_id
WHERE p.is_active = TRUE
GROUP BY p.product_id;
```

**Relational Algebra:**
```
product_idG SUM(available_quantity) → available_stock(
    σis_active=TRUE(
        products ⟕p.product_id=i.product_id inventory
    )
)
```

### Query 5.3: RIGHT JOIN - All warehouses with inventory
**SQL:**
```sql
SELECT w.warehouse_name, COUNT(DISTINCT i.product_id) as unique_products
FROM inventory i
RIGHT JOIN warehouses w ON i.warehouse_id = w.warehouse_id
GROUP BY w.warehouse_id;
```

**Relational Algebra:**
```
warehouse_idG COUNT(DISTINCT product_id) → unique_products(
    inventory ⟖i.warehouse_id=w.warehouse_id warehouses
)
```

### Query 5.4: SELF JOIN - Products with similar prices
**SQL:**
```sql
SELECT p1.product_name as product1, p2.product_name as product2,
       ABS(p1.final_price - p2.final_price) as price_difference
FROM products p1
INNER JOIN products p2 ON p1.category_id = p2.category_id
WHERE p1.product_id < p2.product_id
  AND ABS(p1.final_price - p2.final_price) < 50;
```

**Relational Algebra:**
```
πp1.product_name → product1, p2.product_name → product2, 
 ABS(p1.final_price - p2.final_price) → price_difference(
    σp1.product_id<p2.product_id ∧ ABS(p1.final_price - p2.final_price)<50(
        ρp1(products) ⋈p1.category_id=p2.category_id ρp2(products)
    )
)
```

### Query 5.5: Multiple JOINS - Complete order information
**SQL:**
```sql
SELECT o.order_number, u.first_name, p.product_name, s.tracking_number
FROM orders o
JOIN users u ON o.customer_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN shipments s ON o.order_id = s.order_id;
```

**Relational Algebra:**
```
πorder_number, first_name, product_name, tracking_number(
    ((
        (orders ⋈o.customer_id=u.user_id users) 
        ⋈o.order_id=oi.order_id order_items
    ) ⋈oi.product_id=p.product_id products)
    ⟕o.order_id=s.order_id shipments
)
```

---

## SECTION 4: SUBQUERIES

### Query 6.1: Products above average price
**SQL:**
```sql
SELECT product_name, final_price
FROM products
WHERE final_price > (SELECT AVG(final_price) FROM products);
```

**Relational Algebra:**
```
Let avg_price = π AVG(final_price) → avg(products)

πproduct_name, final_price(
    σfinal_price > avg_price(products)
)
```

### Query 6.2: Correlated subquery - Customers with above-average orders
**SQL:**
```sql
SELECT u.user_id, u.first_name
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.customer_id = u.user_id
    GROUP BY o.customer_id
    HAVING COUNT(*) > (
        SELECT AVG(order_count) 
        FROM (SELECT COUNT(*) as order_count 
              FROM orders GROUP BY customer_id) as avg_orders
    )
);
```

**Relational Algebra:**
```
Let avg_order_count = πAVG(order_count)(
    customer_idG COUNT(*) → order_count(orders)
)

Let high_order_customers = πcustomer_id(
    σCOUNT(*)>avg_order_count(
        customer_idG COUNT(*)(orders)
    )
)

πuser_id, first_name(
    users ⋉user_id=customer_id high_order_customers
)
```
*Note: ⋉ represents semijoin (EXISTS)*

### Query 6.3: Subquery in FROM (derived table)
**SQL:**
```sql
SELECT category_name, product_count
FROM (
    SELECT c.category_name, COUNT(p.product_id) as product_count
    FROM categories c
    LEFT JOIN products p ON c.category_id = p.category_id
    GROUP BY c.category_name
) as category_stats;
```

**Relational Algebra:**
```
Let category_stats = ρcategory_stats(
    category_nameG COUNT(product_id) → product_count(
        categories ⟕c.category_id=p.category_id products
    )
)

πcategory_name, product_count(category_stats)
```

### Query 6.4: Subquery with IN operator
**SQL:**
```sql
SELECT product_name
FROM products p
WHERE p.product_id IN (
    SELECT product_id FROM order_items 
    GROUP BY product_id 
    HAVING COUNT(*) >= 5
);
```

**Relational Algebra:**
```
Let popular_products = πproduct_id(
    σCOUNT(*)>=5(
        product_idG COUNT(*)(order_items)
    )
)

πproduct_name(
    products ⋉p.product_id=product_id popular_products
)
```

### Query 6.5: Subquery with NOT EXISTS
**SQL:**
```sql
SELECT p.product_name
FROM products p
WHERE NOT EXISTS (
    SELECT 1 FROM order_items oi 
    WHERE oi.product_id = p.product_id
);
```

**Relational Algebra:**
```
πproduct_name(
    products ⋫product_id order_items
)
```
*Note: ⋫ represents antijoin (NOT EXISTS)*

---

## SECTION 5: SET OPERATORS

### Query 7.1: UNION - Combine customers and sellers
**SQL:**
```sql
(SELECT user_id, username, 'Customer' as type FROM users u
 JOIN user_roles ur ON u.user_id = ur.user_id
 WHERE ur.role_id = 1)
UNION
(SELECT user_id, username, 'Seller' as type FROM users u
 JOIN user_roles ur ON u.user_id = ur.user_id
 WHERE ur.role_id = 2);
```

**Relational Algebra:**
```
Let customers = πuser_id, username, 'Customer' → type(
    σrole_id=1(users ⋈u.user_id=ur.user_id user_roles)
)

Let sellers = πuser_id, username, 'Seller' → type(
    σrole_id=2(users ⋈u.user_id=ur.user_id user_roles)
)

customers ∪ sellers
```

### Query 7.2: UNION ALL - Product prices
**SQL:**
```sql
(SELECT product_id, base_price as price, 'Base' as type FROM products)
UNION ALL
(SELECT product_id, final_price as price, 'Final' as type FROM products);
```

**Relational Algebra:**
```
πproduct_id, base_price → price, 'Base' → type(products)
∪ (with duplicates)
πproduct_id, final_price → price, 'Final' → type(products)
```

### Query 7.3: INTERSECT - Products in both cart and wishlist
**SQL:**
```sql
SELECT DISTINCT product_id FROM shopping_cart
INTERSECT
SELECT DISTINCT product_id FROM wishlists;
```

**Relational Algebra:**
```
δ(πproduct_id(shopping_cart)) ∩ δ(πproduct_id(wishlists))
```

---

## SECTION 6: COMPLEX QUERIES

### Query 9.1: Customer Lifetime Value (Complex aggregation + joins)
**SQL:**
```sql
SELECT u.user_id, COUNT(DISTINCT o.order_id) as total_orders,
       SUM(o.total_amount) as lifetime_value
FROM users u
JOIN orders o ON u.user_id = o.customer_id
LEFT JOIN customer_loyalty cl ON u.user_id = cl.customer_id
GROUP BY u.user_id
HAVING total_orders >= 2;
```

**Relational Algebra:**
```
σtotal_orders>=2(
    user_idG COUNT(DISTINCT order_id) → total_orders, 
             SUM(total_amount) → lifetime_value(
        (users ⋈u.user_id=o.customer_id orders) 
        ⟕u.user_id=cl.customer_id customer_loyalty
    )
)
```

### Query 9.2: Product Performance Report (Multiple operations)
**SQL:**
```sql
SELECT p.product_name, c.category_name,
       COALESCE(SUM(oi.quantity), 0) as units_sold,
       COALESCE(AVG(r.rating), 0) as avg_rating
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN reviews r ON p.product_id = r.product_id
WHERE p.is_active = TRUE
GROUP BY p.product_id;
```

**Relational Algebra:**
```
product_idG COALESCE(SUM(quantity), 0) → units_sold, 
            COALESCE(AVG(rating), 0) → avg_rating(
    σis_active=TRUE(
        ((products ⟕p.category_id=c.category_id categories)
         ⟕p.product_id=oi.product_id order_items)
        ⟕p.product_id=r.product_id reviews
    )
)
```

### Query 9.3: Seller Performance Dashboard
**SQL:**
```sql
SELECT u.user_id, COUNT(DISTINCT p.product_id) as products_count,
       SUM(oi.total_price) as total_revenue,
       AVG(r.rating) as avg_rating
FROM users u
JOIN products p ON u.user_id = p.seller_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY u.user_id
HAVING total_revenue IS NOT NULL;
```

**Relational Algebra:**
```
σtotal_revenue IS NOT NULL(
    user_idG COUNT(DISTINCT product_id) → products_count, 
             SUM(total_price) → total_revenue, 
             AVG(rating) → avg_rating(
        ((users ⋈u.user_id=p.seller_id products)
         ⟕p.product_id=oi.product_id order_items)
        ⟕p.product_id=r.product_id reviews
    )
)
```

---

## SECTION 7: CONDITIONAL LOGIC

### Query 10.1: Customer segmentation with CASE
**SQL:**
```sql
SELECT user_id, total_spent,
       CASE 
           WHEN total_spent >= 5000 THEN 'VIP'
           WHEN total_spent >= 2000 THEN 'Premium'
           ELSE 'Regular'
       END as segment
FROM (
    SELECT customer_id, SUM(total_amount) as total_spent
    FROM orders
    GROUP BY customer_id
) as customer_stats;
```

**Relational Algebra:**
```
Let customer_stats = customer_idG SUM(total_amount) → total_spent(orders)

πuser_id, total_spent, 
 CASE_WHEN(total_spent>=5000, 'VIP', 
          total_spent>=2000, 'Premium', 
          'Regular') → segment(
    customer_stats
)
```

---

## SECTION 8: WINDOW FUNCTIONS

### Query 8.1: Rank products by price within category
**SQL:**
```sql
SELECT category_name, product_name, final_price,
       ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY final_price DESC) as rank
FROM products p
JOIN categories c ON p.category_id = c.category_id;
```

**Relational Algebra (Extended):**
```
πcategory_name, product_name, final_price,
 ROW_NUMBER() OVER PARTITION BY category_id ORDER BY final_price DESC → rank(
    products ⋈p.category_id=c.category_id categories
)
```
*Note: Window functions extend relational algebra and don't have direct traditional notation*

### Query 8.2: Cumulative revenue
**SQL:**
```sql
SELECT DATE(created_at) as order_date,
       SUM(total_amount) as daily_revenue,
       SUM(SUM(total_amount)) OVER (ORDER BY DATE(created_at)) as cumulative
FROM orders
GROUP BY DATE(created_at);
```

**Relational Algebra (Extended):**
```
πorder_date, daily_revenue,
 SUM(daily_revenue) OVER ORDER BY order_date → cumulative(
    DATE(created_at)G SUM(total_amount) → daily_revenue(orders)
)
```

---

## KEY CONCEPTS SUMMARY

### Basic Operations:
1. **Selection (σ)**: Filter rows based on condition
2. **Projection (π)**: Select specific columns
3. **Join (⋈)**: Combine tables based on condition
4. **Aggregation (G)**: GROUP BY with aggregate functions
5. **Ordering (τ)**: ORDER BY clause

### Set Operations:
1. **Union (∪)**: Combine results (eliminate duplicates)
2. **Intersection (∩)**: Common rows
3. **Difference (−)**: Rows in first but not second

### Advanced Operations:
1. **Semijoin (⋉)**: Like EXISTS
2. **Antijoin (⋫)**: Like NOT EXISTS
3. **Outer Joins (⟕, ⟖, ⟗)**: LEFT, RIGHT, FULL OUTER JOIN
4. **Rename (ρ)**: Alias tables/columns

### Aggregate Functions:
- COUNT, SUM, AVG, MIN, MAX
- Used with G operator for grouping

---

## EQUIVALENCE EXAMPLES

### SQL to Relational Algebra Patterns:

1. **Simple SELECT**:
   ```
   SELECT col FROM table WHERE condition
   ≡ πcol(σcondition(table))
   ```

2. **JOIN with GROUP BY**:
   ```
   SELECT col, COUNT(*) FROM t1 JOIN t2 GROUP BY col
   ≡ colG COUNT(*)(t1 ⋈ t2)
   ```

3. **Subquery in WHERE**:
   ```
   SELECT * FROM t1 WHERE col IN (SELECT col FROM t2)
   ≡ t1 ⋉col=col t2
   ```

4. **UNION**:
   ```
   SELECT col FROM t1 UNION SELECT col FROM t2
   ≡ πcol(t1) ∪ πcol(t2)
   ```

---

# END OF RELATIONAL ALGEBRA DOCUMENTATION
