"""
Loyalty and subscription-related models.
Includes: LoyaltyProgram, LoyaltyTransaction, SubscriptionPlan, Wishlist
"""

from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class TransactionType(enum.Enum):
    """Loyalty transaction type."""
    EARNED = "earned"
    REDEEMED = "redeemed"
    EXPIRED = "expired"


class SubscriptionStatus(enum.Enum):
    """Subscription status."""
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class LoyaltyProgram(Base, TimestampMixin):
    """
    LoyaltyProgram entity - NEW.
    Loyalty program definitions with point exchange rates.
    """
    __tablename__ = 'loyalty_program'
    
    program_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    points_per_currency = Column(Integer, default=1, comment='Points earned per EGP spent')
    currency_per_point = Column(DECIMAL(10, 2), comment='EGP value per point when redeeming')
    min_points_to_redeem = Column(Integer, default=100)
    tier_bronze_threshold = Column(Integer, default=0)
    tier_silver_threshold = Column(Integer, default=1000)
    tier_gold_threshold = Column(Integer, default=5000)
    tier_platinum_threshold = Column(Integer, default=10000)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<LoyaltyProgram(id={self.program_id}, name='{self.name}')>"


class LoyaltyTransaction(Base, TimestampMixin):
    """
    LoyaltyTransaction entity - extends existing loyalty_transaction table.
    Track loyalty points earned, redeemed, or expired.
    """
    __tablename__ = 'loyalty_transaction'
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False, index=True)
    points = Column(Integer, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    order_id = Column(Integer, ForeignKey('order.order_id'))
    description = Column(String(200))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    # Relationships
    customer = relationship("Customer", back_populates="loyalty_transactions")
    order = relationship("Order", back_populates="loyalty_transactions")
    
    def __repr__(self):
        return f"<LoyaltyTransaction(id={self.transaction_id}, customer_id={self.customer_id}, points={self.points}, type='{self.transaction_type.value}')>"


class SubscriptionPlan(Base, TimestampMixin):
    """
    SubscriptionPlan entity - NEW.
    Premium subscription plans for the platform.
    """
    __tablename__ = 'subscription_plan'
    
    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False)
    billing_cycle = Column(String(50), comment='monthly, yearly')
    benefits = Column(Text, comment='JSON string of benefits')
    max_orders_per_month = Column(Integer)
    free_shipping = Column(Boolean, default=False)
    priority_support = Column(Boolean, default=False)
    discount_percentage = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    subscriptions = relationship("CustomerSubscription", back_populates="plan")
    
    def __repr__(self):
        return f"<SubscriptionPlan(id={self.plan_id}, name='{self.name}', price={self.price})>"


class CustomerSubscription(Base, TimestampMixin):
    """
    CustomerSubscription entity - NEW.
    Tracks customer subscriptions to plans.
    """
    __tablename__ = 'customer_subscription'
    
    subscription_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey('subscription_plan.plan_id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    auto_renew = Column(Boolean, default=True)
    
    # Relationships
    customer = relationship("Customer")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<CustomerSubscription(id={self.subscription_id}, customer_id={self.customer_id}, status='{self.status.value}')>"


class Wishlist(Base, TimestampMixin):
    """
    Wishlist entity - extends existing wishlist table.
    Customer product wishlists.
    """
    __tablename__ = 'wishlist'
    
    wishlist_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    added_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    # Relationships
    customer = relationship("Customer", back_populates="wishlists")
    product = relationship("Product", back_populates="wishlists")
    
    def __repr__(self):
        return f"<Wishlist(id={self.wishlist_id}, customer_id={self.customer_id}, product_id={self.product_id})>"
