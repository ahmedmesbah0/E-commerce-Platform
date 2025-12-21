"""
E-Commerce Platform ORM Models
SQLAlchemy models for all 39 entities.

Usage:
    from models import Customer, Product, Order
    from models.base import get_db, init_db
    
    # Initialize database
    init_db()
    
    # Get session
    db = get_db()
    
    # Query
    customers = db.query(Customer).all()
"""

# Base and utilities
from .base import (
    Base,
    engine,
    Session,
    SessionLocal,
    get_db,
    init_db,
    drop_all,
    DatabaseSession,
    TimestampMixin,
    SoftDeleteMixin
)

# User models
from .users import (
    Customer,
    Seller,
    Admin,
    DeliveryPartner,
    Supplier,
    MarketingAgent,
    SupportRep,
    Manager,
    Investor,
    LoyaltyTier,
    AdminRole,
    SellerStatus,
)

# Product models
from .products import (
    Product,
    Category,
    Brand,
    Packaging,
    ProductPackaging,
    PackagingType,
)

# Order models
from .orders import (
    Order,
    OrderItem,
    Cart,
    ShippingAddress,
    OrderStatus,
    PaymentMethod,
)

# Payment models
from .payments import (
    Payment,
    PaymentGateway,
    TransactionLog,
    Coupon,
    OrderCoupon,
    GiftCard,
    RefundRequest,
    ReturnRequest,
    PaymentStatus,
    DiscountType,
    RefundStatus,
)

# Shipping models
from .shipping import (
    Shipment,
    ShippingProvider,
    Warehouse,
    Inventory,
    DeliverySchedule,
    ShipmentStatus,
)

# Review models
from .reviews import (
    Review,
    FeedbackSurvey,
)

# Support models
from .support import (
    CustomerSupportTicket,
    ChatLog,
    Message,
    TicketStatus,
    TicketPriority,
)

# Notification models
from .notifications import (
    Notification,
    NotificationType,
)

# Loyalty models
from .loyalty import (
    LoyaltyProgram,
    LoyaltyTransaction,
    SubscriptionPlan,
    CustomerSubscription,
    Wishlist,
    TransactionType,
    SubscriptionStatus,
)

# System models
from .system import (
    SystemLog,
    TaxRecord,
    Report,
    AnalyticsDashboard,
    AdminActivityLog,
)

__all__ = [
    # Base
    'Base', 'engine', 'Session', 'SessionLocal', 'get_db', 'init_db', 'drop_all', 'DatabaseSession',
    'TimestampMixin', 'SoftDeleteMixin',
    
    # Users (9 models)
    'Customer', 'Seller', 'Admin', 'DeliveryPartner', 'Supplier', 'MarketingAgent', 
    'SupportRep', 'Manager', 'Investor',
    'LoyaltyTier', 'AdminRole', 'SellerStatus',
    
    # Products (5 models)
    'Product', 'Category', 'Brand', 'Packaging', 'ProductPackaging', 'PackagingType',
    
    # Orders (4 models)
    'Order', 'OrderItem', 'Cart', 'ShippingAddress', 'OrderStatus', 'PaymentMethod',
    
    # Payments (8 models)
    'Payment', 'PaymentGateway', 'TransactionLog', 'Coupon', 'OrderCoupon', 
    'GiftCard', 'RefundRequest', 'ReturnRequest',
    'PaymentStatus', 'DiscountType', 'RefundStatus',
    
    # Shipping (5 models)
    'Shipment', 'ShippingProvider', 'Warehouse', 'Inventory', 'DeliverySchedule', 'ShipmentStatus',
    
    # Reviews (2 models)
    'Review', 'FeedbackSurvey',
    
    # Support (3 models)
    'CustomerSupportTicket', 'ChatLog', 'Message', 'TicketStatus', 'TicketPriority',
    
    # Notifications (1 model)
    'Notification', 'NotificationType',
    
    # Loyalty (5 models)
    'LoyaltyProgram', 'LoyaltyTransaction', 'SubscriptionPlan', 'CustomerSubscription', 'Wishlist',
    'TransactionType', 'SubscriptionStatus',
    
    # System (5 models)
    'SystemLog', 'TaxRecord', 'Report', 'AnalyticsDashboard', 'AdminActivityLog',
]

__version__ = '1.0.0'
