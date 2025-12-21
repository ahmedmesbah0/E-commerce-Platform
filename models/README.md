# E-Commerce Platform - Python ORM Models

Complete SQLAlchemy ORM models for all 39 entities in the e-commerce platform.

## 📦 Overview

This package provides comprehensive Python models for:
- **User Management**: 9 user/role types (Customer, Seller, Admin, etc.)
- **Product Catalog**: Products, Categories, Brands, Packaging
- **Order Processing**: Orders, Cart, Shipping Addresses
- **Payments**: Payment processing, Gateways, Refunds, Coupons
- **Shipping**: Shipments, Warehouses, Inventory, Delivery Schedules
- **Reviews & Feedback**: Product reviews and system feedback
- **Support System**: Tickets, Chat logs, Messages
- **Loyalty & Subscriptions**: Points, Programs, Plans
- **Analytics**: Reports, Dashboards, Tax records, System logs

## 🚀 Quick Start

### Installation

```bash
cd models
pip install -r requirements.txt
```

### Configuration

Set database credentials in environment variables or edit `base.py`:

```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=ecommerce_db
export DB_USER=root
export DB_PASSWORD=your_password
```

### Initialize Database

```python
from models import init_db

# Create all tables
init_db()
```

### Basic Usage

```python
from models import Customer, Product, Order, get_db, DatabaseSession

# Using context manager (recommended)
with DatabaseSession() as db:
    customer = Customer(
        name="Ahmed Hassan",
        email="ahmed@example.com",
        password_hash="hashed_password"
    )
    db.add(customer)
    # Automatic commit/rollback

# Manual session management
db = get_db()
try:
    products = db.query(Product).filter(Product.is_active == True).all()
    db.commit()
finally:
    db.close()
```

## 📋 All 39 Entities

### User & Role Models (`users.py`)
1. **Customer** - Regular shoppers
2. **Seller** - Product vendors
3. **Admin** - System administrators
4. **DeliveryPartner** - Shipping company reps
5. **Supplier** - Material/product suppliers
6. **MarketingAgent** - Marketing personnel
7. **SupportRep** - Customer support staff
8. **Manager** - Business managers
9. **Investor** - Financial stakeholders

### Product Models (`products.py`)
10. **Product** - Products for sale
11. **Category** - Product categories (hierarchical)
12. **Brand** - Product brands
13. **Packaging** - Packaging options
14. **ProductPackaging** - Product-packaging junction

### Order Models (`orders.py`)
15. **Order** - Customer orders
16. **OrderItem** - Order line items
17. **Cart** - Shopping cart
18. **ShippingAddress** - Delivery addresses

### Payment Models (`payments.py`)
19. **Payment** - Payment transactions
20. **PaymentGateway** - Payment providers (Vodafone Cash, Visa, Fawry)
21. **TransactionLog** - Transaction history
22. **Coupon** - Discount coupons
23. **OrderCoupon** - Coupon usage tracking
24. **GiftCard** - Gift cards and vouchers
25. **RefundRequest** - Refund requests
26. **ReturnRequest** - Return requests

### Shipping Models (`shipping.py`)
27. **Shipment** - Order deliveries
28. **ShippingProvider** - Courier companies
29. **Warehouse** - Storage facilities
30. **Inventory** - Stock levels
31. **DeliverySchedule** - Delivery time slots

### Review Models (`reviews.py`)
32. **Review** - Product reviews and ratings
33. **FeedbackSurvey** - System feedback

### Support Models (`support.py`)
34. **CustomerSupportTicket** - Support tickets
35. **ChatLog** - Chat sessions
36. **Message** - Individual messages

### Notification Models (`notifications.py`)
37. **Notification** - Multi-recipient notifications

### Loyalty Models (`loyalty.py`)
38. **LoyaltyProgram** - Loyalty program definitions
39. **LoyaltyTransaction** - Points history (also includes SubscriptionPlan, CustomerSubscription, Wishlist)

### System Models (`system.py`)
- **SystemLog** - System activity logs
- **TaxRecord** - Tax records
- **Report** - Generated reports
- **AnalyticsDashboard** - Dashboard configs
- **AdminActivityLog** - Admin audit trail

## 📚 Examples

See [`examples.py`](examples.py) for complete examples:

```python
from models.examples import (
    example_create_customer,
    example_create_product,
    example_place_order,
    example_add_to_cart,
    example_add_review,
    example_create_support_ticket
)

# Run examples
customer_id = example_create_customer()
product_id = example_create_product()
example_place_order(customer_id, product_id)
```

## 🔧 Utilities

The `database.py` module provides helpful utilities:

```python
from models.database import (
    test_connection,
    get_table_names,
    get_table_info,
    bulk_insert,
    export_schema_sql
)

# Test connection
test_connection()

# Get all tables
tables = get_table_names()

# Export schema
export_schema_sql("my_schema.sql")
```

## 🏗️ Model Relationships

All models include proper SQLAlchemy relationships:

```python
# One-to-Many: Customer → Orders
customer = db.query(Customer).first()
for order in customer.orders:
    print(order.total_amount)

# Many-to-Many: Product → Packaging
product = db.query(Product).first()
for pkg in product.packaging_options:
    print(pkg.packaging.name)

# Query with joins
orders_with_items = db.query(Order).join(OrderItem).join(Product).all()
```

## 📊 Features

- ✅ Complete SQLAlchemy 2.0+ ORM models
- ✅ Type hints and documentation
- ✅ Timestamp tracking (created_at, updated_at)
- ✅ Soft delete support (mixin available)
- ✅ Connection pooling
- ✅ Session management (context manager)
- ✅ Enums for status fields
- ✅ JSON fields for flexible data
- ✅ Foreign key relationships
- ✅ Indexes for performance

## 🗂️ File Structure

```
models/
├── __init__.py          # Package exports
├── base.py              # Database config & base
├── users.py             # User/role models (9)
├── products.py          # Product models (5)
├── orders.py            # Order models (4)
├── payments.py          # Payment models (8)
├── shipping.py          # Shipping models (5)
├── reviews.py           # Review models (2)
├── support.py           # Support models (3)
├── notifications.py     # Notification model (1)
├── loyalty.py           # Loyalty models (5)
├── system.py            # System models (5)
├── database.py          # Utilities
├── examples.py          # Usage examples
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## ⚙️ Integration with Existing Database

These models are designed to:
- **Extend** existing 20 tables in your database
- **Add** 19+ new tables for additional entities
- **Maintain compatibility** with existing SQL schema

To integrate:
1. Models map to existing table names where applicable
2. New models create additional tables
3. Use Alembic for migrations (optional)
4. Or run `init_db()` to create new tables only

## 📝 Notes

- Models use existing table names (`customer`, `product`, `order`, etc.)
- New entities get new tables (`seller`, `supplier`, `support_rep`, etc.)
- All foreign keys properly defined
- Enums match your existing database enums
- Compatible with MySQL 8.0+

## 🤝 Integration with GUI

To use with your existing GUI applications:

```python
# In your GUI code
from models import Customer, Product, Order, get_db

class EcommerceGUI:
    def __init__(self):
        self.db = get_db()
    
    def load_products(self):
        products = self.db.query(Product).filter_by(is_active=True).all()
        return products
```

## 📄 License

Part of E-Commerce Platform Database Project
