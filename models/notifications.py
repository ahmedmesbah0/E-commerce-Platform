"""
Notification-related models.
Includes: Notification
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class NotificationType(enum.Enum):
    """Notification type enumeration."""
    LOW_STOCK = "LOW_STOCK"
    ORDER_PLACED = "ORDER_PLACED"
    ORDER_CONFIRMATION = "ORDER_CONFIRMATION"
    SHIPMENT_UPDATE = "SHIPMENT_UPDATE"
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    SUPPORT_TICKET_RECEIVED = "SUPPORT_TICKET_RECEIVED"
    SYSTEM = "SYSTEM"


class Notification(Base, TimestampMixin):
    """
    Notification entity - extends existing notification table.
    System notifications for users, sellers, delivery partners, and payment gateways.
    Can be sent to multiple recipient types.
    """
    __tablename__ = 'notification'
    
    notification_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum(NotificationType), nullable=False, index=True)
    message = Column(Text, nullable=False)
    recipient_type = Column(String(50), comment='customer, seller, admin, delivery_partner, etc.')
    recipient_id = Column(Integer, comment='ID of the recipient')
    related_entity_type = Column(String(50), comment='order, payment, shipment, etc.')
    related_entity_id = Column(Integer, comment='ID of related entity')
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    read_at = Column(DateTime)
    
    def __repr__(self):
        return f"<Notification(id={self.notification_id}, type='{self.type.value}', recipient_type='{self.recipient_type}', is_read={self.is_read})>"
