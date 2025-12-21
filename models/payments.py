"""
Payment-related models.
Includes: Payment, PaymentGateway, TransactionLog, Coupon, GiftCard, 
RefundRequest, ReturnRequest, OrderCoupon
"""

from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class PaymentStatus(enum.Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class DiscountType(enum.Enum):
    """Coupon discount type."""
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"


class RefundStatus(enum.Enum):
    """Refund request status."""
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSED = "processed"


class Payment(Base, TimestampMixin):
    """
    Payment entity - extends existing payment table.
    Payment transaction records.
    """
    __tablename__ = 'payment'
    
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False, index=True)
    payment_method = Column(String(50), nullable=False)
    payment_gateway_id = Column(Integer, ForeignKey('payment_gateway.gateway_id'))
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    transaction_id = Column(String(100))
    payment_date = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    # Relationships
    order = relationship("Order", back_populates="payments")
    gateway = relationship("PaymentGateway", back_populates="payments")
    transaction_logs = relationship("TransactionLog", back_populates="payment")
    
    def __repr__(self):
        return f"<Payment(id={self.payment_id}, order_id={self.order_id}, amount={self.amount}, status='{self.payment_status.value}')>"


class PaymentGateway(Base, TimestampMixin):
    """
    PaymentGateway entity - NEW.
    Payment service providers (Vodafone Cash, Visa, Fawry, etc.).
    """
    __tablename__ = 'payment_gateway'
    
    gateway_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    provider_code = Column(String(50), unique=True, comment='e.g., VODAFONE_CASH, VISA, FAWRY')
    api_endpoint = Column(String(255))
    api_key = Column(String(255), comment='Encrypted API key')
    transaction_fee_percentage = Column(DECIMAL(5, 2), default=0)
    fixed_transaction_fee = Column(DECIMAL(8, 2), default=0)
    supported_currencies = Column(String(200), comment='Comma-separated currency codes')
    is_active = Column(Boolean, default=True)
    
    # Relationships
    payments = relationship("Payment", back_populates="gateway")
    
    def __repr__(self):
        return f"<PaymentGateway(id={self.gateway_id}, name='{self.name}')>"


class TransactionLog(Base, TimestampMixin):
    """
    TransactionLog entity - NEW.
    Detailed log of all payment transactions for users, sellers, and banks.
    """
    __tablename__ = 'transaction_log'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey('payment.payment_id'), index=True)
    transaction_type = Column(String(50), nullable=False, comment='e.g., PAYMENT, REFUND, TRANSFER')
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(Text)
    timestamp = Column(DateTime, server_default='CURRENT_TIMESTAMP', index=True)
    status = Column(String(50), nullable=False)
    metadata = Column(Text, comment='JSON string with additional details')
    
    # Relationships
    payment = relationship("Payment", back_populates="transaction_logs")
    
    def __repr__(self):
        return f"<TransactionLog(id={self.log_id}, type='{self.transaction_type}', amount={self.amount})>"


class Coupon(Base, TimestampMixin):
    """
    Coupon entity - extends existing coupon table.
    Discount coupons and promo codes.
    """
    __tablename__ = 'coupon'
    
    coupon_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(String(200))
    discount_type = Column(Enum(DiscountType), nullable=False)
    discount_value = Column(DECIMAL(10, 2), nullable=False)
    min_order_amount = Column(DECIMAL(10, 2), default=0)
    max_discount_amount = Column(DECIMAL(10, 2))
    valid_from = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    valid_until = Column(DateTime)
    usage_limit = Column(Integer)
    times_used = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    order_coupons = relationship("OrderCoupon", back_populates="coupon")
    
    def __repr__(self):
        return f"<Coupon(id={self.coupon_id}, code='{self.code}', value={self.discount_value})>"


class OrderCoupon(Base):
    """
    OrderCoupon entity - extends existing order_coupon table.
    Tracks coupon usage in orders.
    """
    __tablename__ = 'order_coupon'
    
    order_coupon_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False, index=True)
    coupon_id = Column(Integer, ForeignKey('coupon.coupon_id'), nullable=False)
    discount_applied = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_coupons")
    coupon = relationship("Coupon", back_populates="order_coupons")
    
    def __repr__(self):
        return f"<OrderCoupon(order_id={self.order_id}, coupon_id={self.coupon_id}, discount={self.discount_applied})>"


class GiftCard(Base, TimestampMixin):
    """
    GiftCard/Voucher entity - NEW.
    Gift cards purchased by someone else for the recipient.
    """
    __tablename__ = 'gift_card'
    
    gift_card_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False, unique=True, index=True)
    initial_value = Column(DECIMAL(10, 2), nullable=False)
    current_balance = Column(DECIMAL(10, 2), nullable=False)
    purchased_by_customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    recipient_customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    purchase_date = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    expiry_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    purchaser = relationship("Customer", foreign_keys=[purchased_by_customer_id])
    recipient = relationship("Customer", foreign_keys=[recipient_customer_id])
    
    def __repr__(self):
        return f"<GiftCard(code='{self.code}', balance={self.current_balance})>"


class RefundRequest(Base, TimestampMixin):
    """
    RefundRequest entity - NEW.
    Customer refund requests.
    """
    __tablename__ = 'refund_request'
    
    refund_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    reason = Column(Text, nullable=False)
    refund_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum(RefundStatus), default=RefundStatus.REQUESTED)
    requested_date = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    processed_date = Column(DateTime)
    admin_notes = Column(Text)
    
    # Relationships
    order = relationship("Order")
    customer = relationship("Customer")
    
    def __repr__(self):
        return f"<RefundRequest(id={self.refund_id}, order_id={self.order_id}, amount={self.refund_amount}, status='{self.status.value}')>"


class ReturnRequest(Base, TimestampMixin):
    """
    ReturnRequest entity - NEW.
    Product return requests.
    """
    __tablename__ = 'return_request'
    
    return_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False, index=True)
    order_item_id = Column(Integer, ForeignKey('order_item.order_item_id'))
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    reason = Column(Text, nullable=False)
    condition = Column(String(100), comment='e.g., unopened, damaged, etc.')
    status = Column(Enum(RefundStatus), default=RefundStatus.REQUESTED)
    requested_date = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    approved_date = Column(DateTime)
    return_shipping_label = Column(String(255))
    admin_notes = Column(Text)
    
    # Relationships
    order = relationship("Order")
    order_item = relationship("OrderItem")
    customer = relationship("Customer")
    
    def __repr__(self):
        return f"<ReturnRequest(id={self.return_id}, order_id={self.order_id}, status='{self.status.value}')>"
