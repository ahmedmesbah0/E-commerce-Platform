"""
System and analytics-related models.
Includes: SystemLog, TaxRecord, Report, AnalyticsDashboard, AdminActivityLog
"""

from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class SystemLog(Base, TimestampMixin):
    """
    SystemLog entity - NEW.
    System activity and error logs.
    """
    __tablename__ = 'system_log'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    log_level = Column(String(20), nullable=False, comment='INFO, WARNING, ERROR, CRITICAL', index=True)
    module = Column(String(100), comment='Module/component name')
    message = Column(Text, nullable=False)
    stack_trace = Column(Text)
    user_id = Column(Integer, comment='User who triggered the event')
    user_type = Column(String(50), comment='customer, admin, seller, etc.')
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    timestamp = Column(DateTime, server_default='CURRENT_TIMESTAMP', index=True)
    
    def __repr__(self):
        return f"<SystemLog(id={self.log_id}, level='{self.log_level}', module='{self.module}')>"


class TaxRecord(Base, TimestampMixin):
    """
    TaxRecord entity - NEW.
    Tax records for accounting purposes.
    """
    __tablename__ = 'tax_record'
    
    tax_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), index=True)
    tax_type = Column(String(50), nullable=False, comment='VAT, Sales Tax, etc.')
    tax_rate = Column(DECIMAL(5, 2), nullable=False, comment='Tax percentage')
    taxable_amount = Column(DECIMAL(10, 2), nullable=False)
    tax_amount = Column(DECIMAL(10, 2), nullable=False)
    tax_period = Column(String(20), comment='e.g., 2025-Q1')
    fiscal_year = Column(Integer)
    recorded_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    # Relationships
    order = relationship("Order")
    
    def __repr__(self):
        return f"<TaxRecord(id={self.tax_id}, order_id={self.order_id}, type='{self.tax_type}', amount={self.tax_amount})>"


class Report(Base, TimestampMixin):
    """
    Report entity - NEW.
    Generated business reports for managers and investors.
    """
    __tablename__ = 'report'
    
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    report_type = Column(String(100), nullable=False, comment='SALES, INVENTORY, CUSTOMER, FINANCIAL')
    title = Column(String(200), nullable=False)
    description = Column(Text)
    generated_by_admin_id = Column(Integer, ForeignKey('admin.admin_id'))
    report_period_start = Column(DateTime)
    report_period_end = Column(DateTime)
    report_data = Column(JSON, comment='JSON data for the report')
    file_path = Column(String(255), comment='Path to generated PDF/Excel file')
    generated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    # Relationships
    generated_by = relationship("Admin")
    
    def __repr__(self):
        return f"<Report(id={self.report_id}, type='{self.report_type}', title='{self.title}')>"


class AnalyticsDashboard(Base, TimestampMixin):
    """
    AnalyticsDashboard entity - NEW.
    Dashboard configurations for managers and investors.
    Similar to Spotify Wrapped but for e-commerce analytics.
    """
    __tablename__ = 'analytics_dashboard'
    
    dashboard_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    owner_type = Column(String(50), comment='manager, investor, admin')
    owner_id = Column(Integer, comment='ID of the owner')
    dashboard_config = Column(JSON, comment='Widget configuration')
    metrics = Column(JSON, comment='Selected metrics to display')
    date_range = Column(String(50), comment='e.g., last_30_days, this_quarter')
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<AnalyticsDashboard(id={self.dashboard_id}, name='{self.name}', owner_type='{self.owner_type}')>"


class AdminActivityLog(Base, TimestampMixin):
    """
    AdminActivityLog entity - extends existing admin_activity_log table.
    Audit trail for admin actions.
    """
    __tablename__ = 'admin_activity_log'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admin.admin_id'), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    table_affected = Column(String(50))
    record_id = Column(Integer)
    details = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP', index=True)
    
    # Relationships
    admin = relationship("Admin", back_populates="activity_logs")
    
    def __repr__(self):
        return f"<AdminActivityLog(id={self.log_id}, admin_id={self.admin_id}, action='{self.action}')>"
