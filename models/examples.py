"""
Example usage of E-Commerce Platform ORM Models.
Demonstrates how to use the models for common operations.
"""

from models import (
    get_db, init_db, DatabaseSession,
    Customer, Product, Order, OrderItem, Category, Brand,
    Cart, Wishlist, Review, Payment, Shipment,
    Coupon, LoyaltyTransaction, CustomerSupportTicket,
    Notification, Seller, Admin
)
from datetime import datetime

# Initialize database (creates all tables)
# Uncomment to create tables
# init_db()


def example_create_customer():
    """Example: Create a new customer."""
    with DatabaseSession() as db:
        customer = Customer(
            name="Ahmed Mohamed Hassan",
            email="ahmed.hassan@example.com",
            phone="+201234567890",
            address="123 Tahrir Street, Cairo",
            password_hash="hashed_password_here",
            loyalty_points=0
        )
        db.add(customer)
        db.commit()
        print(f"✅ Created customer: {customer}")
        return customer.customer_id


def example_create_product():
    """Example: Create a new product with category and brand."""
    with DatabaseSession() as db:
        # Create category
        category = Category(
            name="Electronics",
            description="Electronic devices and accessories"
        )
        db.add(category)
        db.flush()  # Get category_id
        
        # Create brand
        brand = Brand(
            name="Samsung",
            country_of_origin="South Korea"
        )
        db.add(brand)
        db.flush()
        
        # Create product
        product = Product(
            name="Samsung Galaxy S21",
            description="Latest Samsung smartphone",
            price=15999.99,
            category_id=category.category_id,
            brand_id=brand.brand_id,
            weight=0.169,
            is_active=True
        )
        db.add(product)
        db.commit()
        print(f"✅ Created product: {product}")
        return product.product_id


def example_place_order(customer_id: int, product_id: int):
    """Example: Place an order."""
    with DatabaseSession() as db:
        # Create order
        order = Order(
            customer_id=customer_id,
            status="pending",
            total_amount=15999.99,
            shipping_cost=50.00,
            tax_amount=240.00,
            payment_method="credit_card"
        )
        db.add(order)
        db.flush()
        
        # Add order item
        order_item = OrderItem(
            order_id=order.order_id,
            product_id=product_id,
            quantity=1,
            unit_price=15999.99,
            subtotal=15999.99
        )
        db.add(order_item)
        
        # Create payment
        payment = Payment(
            order_id=order.order_id,
            payment_method="credit_card",
            amount=16289.99,  # total + shipping + tax
            payment_status="pending",
            transaction_id="TXN123456789"
        )
        db.add(payment)
        
        db.commit()
        print(f"✅ Created order: {order}")
        return order.order_id


def example_add_to_cart(customer_id: int, product_id: int):
    """Example: Add product to cart."""
    with DatabaseSession() as db:
        cart_item = Cart(
            customer_id=customer_id,
            product_id=product_id,
            quantity=2
        )
        db.add(cart_item)
        db.commit()
        print(f"✅ Added to cart: {cart_item}")


def example_add_review(customer_id: int, product_id: int):
    """Example: Add product review."""
    with DatabaseSession() as db:
        review = Review(
            product_id=product_id,
            customer_id=customer_id,
            rating=5,
            title="Excellent product!",
            comment="Very satisfied with this purchase. Highly recommended!",
            is_verified_purchase=True
        )
        db.add(review)
        db.commit()
        print(f"✅ Created review: {review}")


def example_create_support_ticket(customer_id: int):
    """Example: Create customer support ticket."""
    with DatabaseSession() as db:
        ticket = CustomerSupportTicket(
            customer_id=customer_id,
            subject="Issue with order delivery",
            description="My order hasn't arrived yet after 10 days",
            category="Shipping",
            priority="high",
            status="open"
        )
        db.add(ticket)
        db.commit()
        print(f"✅ Created support ticket: {ticket}")


def example_apply_coupon():
    """Example: Create and use a coupon."""
    with DatabaseSession() as db:
        coupon = Coupon(
            code="SUMMER2025",
            description="Summer sale 20% off",
            discount_type="percentage",
            discount_value=20.00,
            min_order_amount=500.00,
            valid_until=datetime(2025, 8, 31),
            usage_limit=100,
            is_active=True
        )
        db.add(coupon)
        db.commit()
        print(f"✅ Created coupon: {coupon}")


def example_query_products():
    """Example: Query products with filters."""
    db = get_db()
    try:
        # Get all active products
        products = db.query(Product).filter(Product.is_active == True).all()
        print(f"\n📦 Found {len(products)} active products:")
        for product in products[:5]:  # Show first 5
            print(f"  - {product.name}: {product.price} EGP")
        
        # Get products by category
        electronics = db.query(Product).join(Category).filter(
            Category.name == "Electronics"
        ).all()
        print(f"\n💻 Found {len(electronics)} electronics")
        
        # Get products with reviews
        products_with_reviews = db.query(Product).join(Review).distinct().all()
        print(f"\n⭐ Found {len(products_with_reviews)} products with reviews")
        
    finally:
        db.close()


def example_query_customer_orders(customer_id: int):
    """Example: Get customer order history."""
    db = get_db()
    try:
        customer = db.query(Customer).filter_by(customer_id=customer_id).first()
        if customer:
            print(f"\n👤 Customer: {customer.name}")
            print(f"📧 Email: {customer.email}")
            print(f"🎁 Loyalty Points: {customer.loyalty_points}")
            print(f"\n📦 Orders:")
            for order in customer.orders:
                print(f"  Order #{order.order_id}: {order.status} - {order.total_amount} EGP")
                for item in order.order_items:
                    print(f"    - {item.product.name} x{item.quantity}")
    finally:
        db.close()


def example_create_notification(customer_id: int):
    """Example: Create notification for customer."""
    with DatabaseSession() as db:
        notification = Notification(
            type="ORDER_PLACED",
            message="Your order has been confirmed! Thank you for shopping with us.",
            recipient_type="customer",
            recipient_id=customer_id,
            related_entity_type="order",
            is_read=False
        )
        db.add(notification)
        db.commit()
        print(f"✅ Created notification: {notification}")


if __name__ == "__main__":
    print("=== E-Commerce Platform ORM Examples ===\n")
    
    # Uncomment to run examples
    # customer_id = example_create_customer()
    # product_id = example_create_product()
    # example_add_to_cart(customer_id, product_id)
    # example_add_review(customer_id, product_id)
    # order_id = example_place_order(customer_id, product_id)
    # example_create_support_ticket(customer_id)
    # example_apply_coupon()
    # example_create_notification(customer_id)
    # example_query_products()
    # example_query_customer_orders(customer_id)
    
    print("\n✅ Examples ready to run!")
    print("Uncomment the examples you want to test in __main__")
