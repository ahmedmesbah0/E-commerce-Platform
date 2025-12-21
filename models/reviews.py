"""
Review and feedback-related models.
Includes: Review, FeedbackSurvey
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Review(Base, TimestampMixin):
    """
    Review/Rating entity - extends existing review table.
    Product reviews and ratings from customers.
    """
    __tablename__ = 'review'
    
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False, index=True)
    rating = Column(Integer, nullable=False, comment='1-5 stars')
    title = Column(String(200))
    comment = Column(Text)
    review_date = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    is_verified_purchase = Column(Boolean, default=False)
    
    # Relationships
    product = relationship("Product", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(id={self.review_id}, product_id={self.product_id}, rating={self.rating})>"


class FeedbackSurvey(Base, TimestampMixin):
    """
    FeedbackSurvey entity - NEW.
    System feedback surveys (different from product reviews).
    Results directed to IT/admin team.
    """
    __tablename__ = 'feedback_survey'
    
    survey_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    survey_type = Column(String(50), nullable=False, comment='e.g., POST_PURCHASE, WEBSITE_EXPERIENCE, SUPPORT')
    rating = Column(Integer, comment='Overall rating 1-5')
    feedback_text = Column(Text)
    page_url = Column(String(255), comment='URL where feedback was given')
    submitted_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    is_reviewed = Column(Boolean, default=False)
    admin_response = Column(Text)
    
    # Relationships
    customer = relationship("Customer")
    
    def __repr__(self):
        return f"<FeedbackSurvey(id={self.survey_id}, type='{self.survey_type}', rating={self.rating})>"
