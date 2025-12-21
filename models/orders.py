"""
Order and cart-related models.
Includes: Order, OrderItem, Cart, CartItem
"""

from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class OrderStatus(enum.Enum):
    """Order status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(enum.Enum):
    """Payment method enumeration."""
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    CASH_ON_DELIVERY = "cash_on_delivery"


class Order(Base, TimestampMixin):
    """
    Order entity - extends existing order table.
    Customer purchase orders.
    """
    __tablename__ = 'order'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False, index=True)
    order_date = Column(DateTime, server_default='CURRENT_TIMESTAMP', index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    shipping_cost = Column(DECIMAL(8, 2), default=0)
    tax_amount = Column(DECIMAL(8, 2), default=0)
    shipping_address_id = Column(Integer, ForeignKey('shipping_address.address_id'))
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CASH_ON_DELIVERY)
    notes = Column(Text)
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    shipping_address = relationship("ShippingAddress")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")
    shipments = relationship("Shipment", back_populates="order")
    order_coupons = relationship("OrderCoupon", back_populates="order")
    loyalty_transactions = relationship("LoyaltyTransaction", back_populates="order")
    
    def __repr__(self):
        return f"<Order(id={self.order_id}, customer_id={self.customer_id}, status='{self.status.value}', total={self.total_amount})>"


class OrderItem(Base):
    """
    OrderItem entity - extends existing order_item table.
    Individual line items in an order.
    """
    __tablename__ = 'order_item'
    
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(id={self.order_item_id}, order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity})>"


class Cart(Base, TimestampMixin):
    """
    Cart entity - extends existing cart table.
    Shopping cart for customers (and guest users via session).
    """
    __tablename__ = 'cart'
    
    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), index=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    session_id = Column(String(100), index=True, comment='For guest users')
    
    # Relationships
    customer = relationship("Customer", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
    
    def __repr__(self):
        return f"<Cart(id={self.cart_id}, customer_id={self.customer_id}, product_id={self.product_id}, qty={self.quantity})>"


class ShippingAddress(Base, TimestampMixin):
    """
    ShippingAddress entity - extends existing shipping_address table.
    Customer delivery addresses.
    """
    __tablename__ = 'shipping_address'
    
    address_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False, index=True)
    address_label = Column(String(50), comment='e.g., Home, Office')
    street_address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100))
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False, default='Egypt')
    is_default = Column(Boolean, default=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="shipping_addresses")
    
    def __repr__(self):
        return f"<ShippingAddress(id={self.address_id}, customer_id={self.customer_id}, city='{self.city}')>"
