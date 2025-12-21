"""
Customer support-related models.
Includes: CustomerSupportTicket, ChatLog, Message
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class TicketStatus(enum.Enum):
    """Support ticket status enumeration."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(enum.Enum):
    """Ticket priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class CustomerSupportTicket(Base, TimestampMixin):
    """
    CustomerSupportTicket entity - NEW.
    Support tickets for customer issues and inquiries.
    """
    __tablename__ = 'customer_support_ticket'
    
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False, index=True)
    assigned_rep_id = Column(Integer, ForeignKey('support_rep.rep_id'), index=True)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), comment='e.g., Technical, Billing, General')
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, index=True)
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, onupdate='CURRENT_TIMESTAMP')
    resolved_at = Column(DateTime)
    
    # Relationships
    customer = relationship("Customer", back_populates="support_tickets")
    assigned_rep = relationship("SupportRep", back_populates="assigned_tickets")
    chat_logs = relationship("ChatLog", back_populates="ticket")
    
    def __repr__(self):
        return f"<CustomerSupportTicket(id={self.ticket_id}, customer_id={self.customer_id}, status='{self.status.value}')>"


class ChatLog(Base, TimestampMixin):
    """
    ChatLog entity - NEW.
    Support chat sessions associated with tickets.
    """
    __tablename__ = 'chat_log'
    
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('customer_support_ticket.ticket_id'), nullable=False, index=True)
    support_rep_id = Column(Integer, ForeignKey('support_rep.rep_id'))
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    started_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    ended_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    ticket = relationship("CustomerSupportTicket", back_populates="chat_logs")
    support_rep = relationship("SupportRep", back_populates="chat_sessions")
    messages = relationship("Message", back_populates="chat_log", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ChatLog(id={self.chat_id}, ticket_id={self.ticket_id})>"


class Message(Base, TimestampMixin):
    """
    Message entity - NEW.
    Individual messages within chat logs.
    """
    __tablename__ = 'message'
    
    message_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chat_log.chat_id'), nullable=False, index=True)
    sender_type = Column(String(20), nullable=False, comment='customer or support_rep')
    sender_id = Column(Integer, nullable=False, comment='ID of customer or support rep')
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default='CURRENT_TIMESTAMP', index=True)
    is_read = Column(Boolean, default=False)
    attachment_url = Column(String(255))
    
    # Relationships
    chat_log = relationship("ChatLog", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.message_id}, chat_id={self.chat_id}, sender_type='{self.sender_type}')>"
