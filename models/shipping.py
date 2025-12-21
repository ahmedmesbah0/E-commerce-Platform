"""
Shipping and inventory-related models.
Includes: Shipment, Warehouse, Inventory, DeliverySchedule
"""

from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class ShipmentStatus(enum.Enum):
    """Shipment status enumeration."""
    PREPARING = "preparing"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED = "failed"


class Shipment(Base, TimestampMixin):
    """
    Shipment entity - extends existing shipment table.
    Order delivery tracking.
    """
    __tablename__ = 'shipment'
    
    shipment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), nullable=False, index=True)
    provider_id = Column(Integer, ForeignKey('shipping_provider.provider_id'))
    delivery_partner_id = Column(Integer, ForeignKey('delivery_partner.partner_id'))
    tracking_number = Column(String(100), index=True)
    shipped_date = Column(DateTime)
    estimated_delivery = Column(DateTime)
    actual_delivery = Column(DateTime)
    status = Column(Enum(ShipmentStatus), default=ShipmentStatus.PREPARING)
    
    # Relationships
    order = relationship("Order", back_populates="shipments")
    shipping_provider = relationship("ShippingProvider", back_populates="shipments")
    delivery_partner = relationship("DeliveryPartner", back_populates="shipments")
    
    def __repr__(self):
        return f"<Shipment(id={self.shipment_id}, order_id={self.order_id}, tracking='{self.tracking_number}', status='{self.status.value}')>"


class ShippingProvider(Base, TimestampMixin):
    """
    ShippingProvider entity - extends existing shipping_provider table.
    Delivery/courier companies (Aramex, DHL, Egypt Post, etc.).
    """
    __tablename__ = 'shipping_provider'
    
    provider_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    tracking_url_template = Column(String(255), comment='URL pattern with {tracking_number} placeholder')
    is_active = Column(Boolean, default=True)
    
    # Relationships
    shipments = relationship("Shipment", back_populates="shipping_provider")
    
    def __repr__(self):
        return f"<ShippingProvider(id={self.provider_id}, name='{self.name}')>"


class Warehouse(Base, TimestampMixin):
    """
    Warehouse entity - extends existing warehouse table.
    Storage facilities for inventory.
    """
    __tablename__ = 'warehouse'
    
    warehouse_id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String(200), nullable=False)
    capacity = Column(Integer)
    manager_name = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    # Relationships
    inventory_records = relationship("Inventory", back_populates="warehouse")
    
    def __repr__(self):
        return f"<Warehouse(id={self.warehouse_id}, location='{self.location}')>"


class Inventory(Base, TimestampMixin):
    """
    Inventory entity - extends existing inventory table.
    Product stock levels by warehouse.
    """
    __tablename__ = 'inventory'
    
    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False, index=True)
    warehouse_id = Column(Integer, ForeignKey('warehouse.warehouse_id'), nullable=False, index=True)
    supplier_id = Column(Integer, ForeignKey('supplier.supplier_id'))
    quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, default=10)
    last_updated = Column(DateTime, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    
    # Relationships
    product = relationship("Product", back_populates="inventory_records")
    warehouse = relationship("Warehouse", back_populates="inventory_records")
    supplier = relationship("Supplier", back_populates="inventory_supplies")
    
    def __repr__(self):
        return f"<Inventory(id={self.inventory_id}, product_id={self.product_id}, warehouse_id={self.warehouse_id}, qty={self.quantity})>"


class DeliverySchedule(Base, TimestampMixin):
    """
    DeliverySchedule entity - NEW.
    Scheduled delivery times for orders and shipments.
    """
    __tablename__ = 'delivery_schedule'
    
    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    shipment_id = Column(Integer, ForeignKey('shipment.shipment_id'), nullable=False, index=True)
    delivery_partner_id = Column(Integer, ForeignKey('delivery_partner.partner_id'))
    scheduled_date = Column(DateTime, nullable=False)
    time_window_start = Column(DateTime)
    time_window_end = Column(DateTime)
    delivery_instructions = Column(Text)
    recipient_phone = Column(String(20))
    is_confirmed = Column(Boolean, default=False)
    
    # Relationships
    shipment = relationship("Shipment")
    delivery_partner = relationship("DeliveryPartner", back_populates="delivery_schedules")
    
    def __repr__(self):
        return f"<DeliverySchedule(id={self.schedule_id}, shipment_id={self.shipment_id}, date={self.scheduled_date})>"
