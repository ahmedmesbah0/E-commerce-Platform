"""
Product and catalog-related models.
Includes: Product, Category, Brand, Packaging
"""

from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class Product(Base, TimestampMixin):
    """
    Product entity - extends existing product table.
    Items available for purchase.
    """
    __tablename__ = 'product'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    price = Column(DECIMAL(10, 2), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey('category.category_id'), index=True)
    brand_id = Column(Integer, ForeignKey('brand.brand_id'))
    seller_id = Column(Integer, ForeignKey('seller.seller_id'))
    image_url = Column(String(255))
    weight = Column(DECIMAL(8, 2), comment='Weight in kg')
    dimensions = Column(String(50), comment='L x W x H')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    updated_at = Column(DateTime, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP')
    
    # Relationships
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    seller = relationship("Seller", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    inventory_records = relationship("Inventory", back_populates="product")
    cart_items = relationship("Cart", back_populates="product")
    wishlists = relationship("Wishlist", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    packaging_options = relationship("ProductPackaging", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.product_id}, name='{self.name}', price={self.price})>"


class Category(Base, TimestampMixin):
    """
    Category entity - extends existing category table.
    Product categories with hierarchical support.
    """
    __tablename__ = 'category'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    parent_category_id = Column(Integer, ForeignKey('category.category_id'))
    description = Column(Text)
    created_at = Column(DateTime, server_default='CURRENT_TIMESTAMP')
    
    # Self-referencing relationship for hierarchy
    parent = relationship("Category", remote_side=[category_id], backref="subcategories")
    
    # Relationships
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.category_id}, name='{self.name}')>"


class Brand(Base, TimestampMixin):
    """
    Brand entity - NEW.
    Product brands (separate from sellers - a seller can sell multiple brands).
    """
    __tablename__ = 'brand'
    
    brand_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    logo_url = Column(String(255))
    country_of_origin = Column(String(100))
    website = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    products = relationship("Product", back_populates="brand")
    
    def __repr__(self):
        return f"<Brand(id={self.brand_id}, name='{self.name}')>"


class PackagingType(enum.Enum):
    """Packaging types for products."""
    STANDARD = "standard"
    GIFT_WRAP = "gift_wrap"
    PREMIUM = "premium"
    ECO_FRIENDLY = "eco_friendly"
    CUSTOM = "custom"


class Packaging(Base, TimestampMixin):
    """
    Packaging entity - NEW.
    Available packaging options (for gift items, special products).
    """
    __tablename__ = 'packaging'
    
    packaging_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    packaging_type = Column(Enum(PackagingType), nullable=False)
    description = Column(Text)
    additional_cost = Column(DECIMAL(8, 2), default=0)
    image_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    product_packaging = relationship("ProductPackaging", back_populates="packaging")
    
    def __repr__(self):
        return f"<Packaging(id={self.packaging_id}, name='{self.name}', type='{self.packaging_type.value}')>"


class ProductPackaging(Base):
    """
    Product-Packaging junction table - NEW.
    Many-to-many relationship between products and packaging options.
    """
    __tablename__ = 'product_packaging'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), nullable=False)
    packaging_id = Column(Integer, ForeignKey('packaging.packaging_id'), nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="packaging_options")
    packaging = relationship("Packaging", back_populates="product_packaging")
    
    def __repr__(self):
        return f"<ProductPackaging(product_id={self.product_id}, packaging_id={self.packaging_id})>"
