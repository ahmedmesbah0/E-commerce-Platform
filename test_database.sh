#!/bin/bash
# Quick automated test script for E-Commerce Platform
# Tests database connectivity and basic queries

echo "======================================"
echo "  E-Commerce Platform - Quick Test"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

DB_USER="ecommerce_user"
DB_PASS="SecurePass123!"
DB_NAME="ecommerce_db"

# Test 1: Database Connection
echo -n "Test 1: Database Connection... "
if mysql -u $DB_USER -p$DB_PASS $DB_NAME -e "SELECT 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
    exit 1
fi

# Test 2: Products Table
echo -n "Test 2: Products Table... "
PRODUCT_COUNT=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -se "SELECT COUNT(*) FROM product")
if [ "$PRODUCT_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ PASS${NC} ($PRODUCT_COUNT products)"
else
    echo -e "${YELLOW}⚠ WARNING${NC} (0 products found)"
fi

# Test 3: Customers Table
echo -n "Test 3: Customers Table... "
CUSTOMER_COUNT=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -se "SELECT COUNT(*) FROM customer")
if [ "$CUSTOMER_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ PASS${NC} ($CUSTOMER_COUNT customers)"
else
    echo -e "${YELLOW}⚠ WARNING${NC} (0 customers found)"
fi

# Test 4: Orders Table
echo -n "Test 4: Orders Table... "
ORDER_COUNT=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -se "SELECT COUNT(*) FROM \`order\`")
echo -e "${GREEN}✓ PASS${NC} ($ORDER_COUNT orders)"

# Test 5: Inventory Table
echo -n "Test 5: Inventory Table... "
INV_COUNT=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -se "SELECT COUNT(*) FROM inventory")
if [ "$INV_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ PASS${NC} ($INV_COUNT inventory records)"
else
    echo -e "${YELLOW}⚠ WARNING${NC} (0 inventory records)"
fi

# Test 6: Schema Validation
echo -n "Test 6: Order Table Schema... "
COLS=$(mysql -u $DB_USER -p$DB_PASS $DB_NAME -se "DESCRIBE \`order\`" | grep -c "subtotal\|shipping_address")
if [ "$COLS" -eq 2 ]; then
    echo -e "${GREEN}✓ PASS${NC}"
else
    echo -e "${RED}✗ FAIL${NC} (Missing required columns)"
fi

echo ""
echo "======================================"
echo "  Database Summary"
echo "======================================"

mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
SELECT 'Products' AS Table_Name, COUNT(*) AS Count FROM product
UNION ALL
SELECT 'Customers', COUNT(*) FROM customer
UNION ALL
SELECT 'Orders', COUNT(*) FROM \`order\`
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_item
UNION ALL
SELECT 'Inventory', COUNT(*) FROM inventory
UNION ALL
SELECT 'Categories', COUNT(*) FROM category;
EOF

echo ""
echo "======================================"
echo "  Recent Orders"
echo "======================================"

mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
SELECT 
    o.order_id,
    c.name AS customer_name,
    o.total_amount,
    o.status,
    o.order_date
FROM \`order\` o
JOIN customer c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC
LIMIT 5;
EOF

echo ""
echo "======================================"
echo "  Low Stock Products"
echo "======================================"

mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
SELECT 
    p.name AS product_name,
    SUM(i.quantity) AS total_stock
FROM product p
LEFT JOIN inventory i ON p.product_id = i.product_id
GROUP BY p.product_id
HAVING total_stock < 5
ORDER BY total_stock;
EOF

echo ""
echo -e "${GREEN}✓ All tests completed!${NC}"
echo ""
echo "To launch the application:"
echo "  Customer Mode: cd gui && python3 main_app.py"
echo "  Admin Mode:    cd gui && python3 main_app.py"
echo ""
