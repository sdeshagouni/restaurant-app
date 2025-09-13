"""
Menu models for restaurant menu management.
Handles menu categories, items, and options.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Integer, ForeignKey, Text, Time
from sqlalchemy import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal

from app.models.base import BaseModel


class MenuCategory(BaseModel):
    """Menu category model."""
    __tablename__ = "menu_category"
    
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    category_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    display_order = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    available_all_day = Column(Boolean, default=True, nullable=False)
    available_from = Column(Time, nullable=True)
    available_until = Column(Time, nullable=True)
    
    restaurant = relationship("Restaurant", back_populates="menu_categories")
    items = relationship("MenuItem", back_populates="category", cascade="all, delete-orphan")


class MenuItem(BaseModel):
    """Menu item model."""
    __tablename__ = "menu_item"
    
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("menu_category.id"), nullable=True, index=True)
    item_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    cost_price = Column(Numeric(10, 2), nullable=True)
    prep_time_minutes = Column(Integer, default=15, nullable=False)
    is_vegetarian = Column(Boolean, default=False, nullable=False)
    is_vegan = Column(Boolean, default=False, nullable=False)
    is_gluten_free = Column(Boolean, default=False, nullable=False)
    is_spicy = Column(Boolean, default=False, nullable=False)
    spice_level = Column(Integer, default=0, nullable=False)
    calories = Column(Integer, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    image_url = Column(String(500), nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    is_popular = Column(Boolean, default=False, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    profit_margin = Column(Numeric(10, 2), nullable=True)
    profit_margin_percent = Column(Numeric(5, 2), nullable=True)
    
    restaurant = relationship("Restaurant", back_populates="menu_items")
    category = relationship("MenuCategory", back_populates="items")
    options = relationship("MenuItemOption", back_populates="item", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="menu_item")


class MenuItemOption(BaseModel):
    """Menu item options/customizations."""
    __tablename__ = "menu_item_option"
    
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("menu_item.id"), nullable=False, index=True)
    option_group = Column(String(100), nullable=False)
    option_name = Column(String(255), nullable=False)
    price_change = Column(Numeric(6, 2), default=Decimal("0"), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    
    item = relationship("MenuItem", back_populates="options")