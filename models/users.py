"""
User and role-related models.
Includes: Customer, Seller, Admin, DeliveryPartner, Supplier, 
MarketingAgent, SupportRep, Manager, Investor
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, Enum, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


# Enums for user roles and statuses
class LoyaltyTier(enum.Enum):
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


class AdminRole(enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    INVENTORY_MANAGER = "inventory_manager"
    SALES_REP = "sales_rep"


class SellerStatus(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class Customer(Base, TimestampMixin):
    """
    Customer entity - extends existing customer table.
    Regular users who purchase products.
    """
    __tablename__ = 'customer'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    address = Column(Text)
    password_hash = Column(String(255), nullable=False)
    date_created = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    is_active = Column(Boolean, default=True)
    loyalty_points = Column(Integer, default=0)
    loyalty_tier = Column(Enum(LoyaltyTier), default=LoyaltyTier.BRONZE)
    
    # Relationships
    orders = relationship("Order", back_populates="customer")
    cart_items = relationship("Cart", back_populates="customer")
    wishlists = relationship("Wishlist", back_populates="customer")
    reviews = relationship("Review", back_populates="customer")
    shipping_addresses = relationship("ShippingAddress", back_populates="customer")
    loyalty_transactions = relationship("LoyaltyTransaction", back_populates="customer")
    support_tickets = relationship("CustomerSupportTicket", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer(id={self.customer_id}, name='{self.name}', email='{self.email}')>"


class Seller(Base, TimestampMixin):
    """
    Seller/Vendor entity - NEW.
    Individuals or companies who sell products on the platform.
    """
    __tablename__ = 'seller'
    
    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    business_name = Column(String(200), nullable=False)
    contact_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    address = Column(Text)
    password_hash = Column(String(255), nullable=False)
    business_license = Column(String(100))
    tax_id = Column(String(50))
    status = Column(Enum(SellerStatus), default=SellerStatus.PENDING)
    commission_rate = Column(Integer, default=10, comment='Percentage commission')
    is_active = Column(Boolean, default=True)
    
    # Relationships
    products = relationship("Product", back_populates="seller")
    
    def __repr__(self):
        return f"<Seller(id={self.seller_id}, business='{self.business_name}', status='{self.status.value}')>"


class Admin(Base, TimestampMixin):
    """
    Admin entity - extends existing admin table.
    System administrators with various permission levels.
    """
    __tablename__ = 'admin'
    
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(AdminRole), default=AdminRole.ADMIN)
    permissions = Column(JSON)
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    activity_logs = relationship("AdminActivityLog", back_populates="admin")
    
    def __repr__(self):
        return f"<Admin(id={self.admin_id}, email='{self.email}', role='{self.role.value}')>"


class DeliveryPartner(Base, TimestampMixin):
    """
    Delivery Partner entity - NEW.
    Representatives from shipping companies (Aramex, DHL, Egypt Post, etc.).
    """
    __tablename__ = 'delivery_partner'
    
    partner_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(100), nullable=False)
    contact_person = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    service_areas = Column(JSON, comment='List of cities/regions served')
    is_active = Column(Boolean, default=True)
    
    # Relationships
    shipments = relationship("Shipment", back_populates="delivery_partner")
    delivery_schedules = relationship("DeliverySchedule", back_populates="delivery_partner")
    
    def __repr__(self):
        return f"<DeliveryPartner(id={self.partner_id}, company='{self.company_name}')>"


class Supplier(Base, TimestampMixin):
    """
    Supplier entity - NEW.
    Suppliers who provide materials/products to the business.
    """
    __tablename__ = 'supplier'
    
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(200), nullable=False)
    contact_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    address = Column(Text)
    tax_id = Column(String(50))
    payment_terms = Column(String(100), comment='e.g., Net 30, Net 60')
    is_active = Column(Boolean, default=True)
    
    # Relationships
    inventory_supplies = relationship("Inventory", back_populates="supplier")
    
    def __repr__(self):
        return f"<Supplier(id={self.supplier_id}, company='{self.company_name}')>"


class MarketingAgent(Base, TimestampMixin):
    """
    Marketing Agent entity - NEW.
    Personnel responsible for marketing and promoting products.
    """
    __tablename__ = 'marketing_agent'
    
    agent_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    specialization = Column(String(100), comment='e.g., Social Media, Email, SEO')
    commission_rate = Column(Integer, default=5, comment='Percentage commission')
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<MarketingAgent(id={self.agent_id}, name='{self.name}')>"


class SupportRep(Base, TimestampMixin):
    """
    Support Representative entity - NEW.
    Customer support staff who handle tickets and chats.
    """
    __tablename__ = 'support_rep'
    
    rep_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    department = Column(String(50), comment='e.g., Technical, Billing, General')
    is_active = Column(Boolean, default=True)
    
    # Relationships
    assigned_tickets = relationship("CustomerSupportTicket", back_populates="assigned_rep")
    chat_sessions = relationship("ChatLog", back_populates="support_rep")
    
    def __repr__(self):
        return f"<SupportRep(id={self.rep_id}, name='{self.name}', dept='{self.department}')>"


class Manager(Base, TimestampMixin):
    """
    Manager/Supervisor entity - NEW.
    Business managers without technical database access.
    """
    __tablename__ = 'manager'
    
    manager_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    department = Column(String(100), comment='e.g., Sales, Operations, HR')
    level = Column(String(50), comment='e.g., Senior, Mid-level, Junior')
    is_active = Column(Boolean, default=True)
    
    # Relationships
    supervised_employees = relationship("Admin", foreign_keys='Admin.manager_id')
    
    def __repr__(self):
        return f"<Manager(id={self.manager_id}, name='{self.name}', dept='{self.department}')>"


class Investor(Base, TimestampMixin):
    """
    Investor/Shareholder entity - NEW.
    Financial stakeholders who can view reports but not manage operations.
    """
    __tablename__ = 'investor'
    
    investor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    investment_amount = Column(Integer, comment='Investment in currency')
    ownership_percentage = Column(Integer, comment='Ownership stake percentage')
    investment_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Investor(id={self.investor_id}, name='{self.name}', ownership={self.ownership_percentage}%)>"
