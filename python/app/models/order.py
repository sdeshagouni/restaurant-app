"""
Order models for order processing and management.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Integer, ForeignKey, Text
from sqlalchemy import UUID
from sqlalchemy.orm import relationship
from decimal import Decimal

from app.models.base import BaseModel, OrderStatus, PaymentStatus, OrderType, ItemStatus


class Order(BaseModel):
    """Order model."""
    __tablename__ = "order"
    
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    table_id = Column(UUID(as_uuid=True), ForeignKey("restaurant_table.id"), nullable=True, index=True)
    guest_session_id = Column(UUID(as_uuid=True), ForeignKey("guest_session.id"), nullable=True, index=True)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True, index=True)
    
    order_number = Column(String(50), nullable=False, unique=True, index=True)
    order_type = Column(String(20), nullable=False, default=OrderType.DINE_IN)
    order_status = Column(String(20), nullable=False, default=OrderStatus.PENDING)
    payment_status = Column(String(20), nullable=False, default=PaymentStatus.PENDING)
    
    guest_name = Column(String(255), nullable=True)
    guest_phone = Column(String(20), nullable=True)
    guest_email = Column(String(255), nullable=True)
    party_size = Column(Integer, default=1, nullable=False)
    
    special_instructions = Column(Text, nullable=True)
    subtotal = Column(Numeric(10, 2), nullable=False, default=Decimal("0"))
    tax_amount = Column(Numeric(10, 2), nullable=False, default=Decimal("0"))
    service_charge = Column(Numeric(10, 2), nullable=False, default=Decimal("0"))
    discount_amount = Column(Numeric(10, 2), nullable=False, default=Decimal("0"))
    total_amount = Column(Numeric(10, 2), nullable=False, default=Decimal("0"))
    
    ordered_at = Column(DateTime(timezone=True), nullable=False)
    estimated_ready_time = Column(DateTime(timezone=True), nullable=True)
    ready_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    restaurant = relationship("Restaurant", back_populates="orders")
    table = relationship("RestaurantTable", back_populates="orders")
    guest_session = relationship("GuestSession", back_populates="orders")
    created_by_user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment_transactions = relationship("PaymentTransaction", back_populates="order", cascade="all, delete-orphan")


class OrderItem(BaseModel):
    """Order item model."""
    __tablename__ = "order_item"
    
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.id"), nullable=False, index=True)
    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_item.id"), nullable=False, index=True)
    
    item_name = Column(String(255), nullable=False)
    item_description = Column(Text, nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    item_status = Column(String(20), nullable=False, default=ItemStatus.ORDERED)
    special_instructions = Column(Text, nullable=True)
    prep_time_minutes = Column(Integer, nullable=True)
    
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")