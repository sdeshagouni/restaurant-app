"""
Daily specials and promotions models.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Integer, ForeignKey, Text, Date
from sqlalchemy import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal

from app.models.base import BaseModel, SpecialType, DiscountType


class DailySpecial(BaseModel):
    """Daily special model."""
    __tablename__ = "daily_special"
    
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    special_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    special_type = Column(String(20), nullable=False, default=SpecialType.DISCOUNT)
    discount_type = Column(String(20), nullable=False, default=DiscountType.PERCENTAGE)
    discount_value = Column(Numeric(10, 2), nullable=False)
    minimum_order_amount = Column(Numeric(10, 2), nullable=True)
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    usage_limit = Column(Integer, nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    
    restaurant = relationship("Restaurant", back_populates="daily_specials")
    usage_records = relationship("SpecialUsage", back_populates="special", cascade="all, delete-orphan")


class SpecialUsage(BaseModel):
    """Special usage tracking."""
    __tablename__ = "special_usage"
    
    special_id = Column(UUID(as_uuid=True), ForeignKey("daily_special.id"), nullable=False, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False, index=True)
    discount_amount = Column(Numeric(10, 2), nullable=False)
    
    special = relationship("DailySpecial", back_populates="usage_records")