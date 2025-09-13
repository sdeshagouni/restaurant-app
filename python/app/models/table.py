"""
Table and guest session models.
Handles restaurant tables and guest ordering sessions.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from typing import Optional

from app.models.base import BaseModel
from app.core.config import settings


# =================================================================
# RESTAURANT TABLE MODEL
# =================================================================

class RestaurantTable(BaseModel):
    """Restaurant table model for QR ordering."""
    __tablename__ = "restaurant_table"
    
    # Foreign Keys
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    
    # Table Information
    table_number = Column(String(20), nullable=False)
    table_name = Column(String(100), nullable=True)
    capacity = Column(Integer, nullable=False, default=4)
    location = Column(String(100), nullable=True)
    
    # QR Code
    qr_code = Column(String(100), nullable=False, unique=True, index=True)
    qr_code_url = Column(String(500), nullable=True)
    qr_code_image_url = Column(String(500), nullable=True)
    
    # Table Features
    is_active = Column(Boolean, default=True, nullable=False)
    requires_reservation = Column(Boolean, default=False, nullable=False)
    is_vip = Column(Boolean, default=False, nullable=False)
    position_x = Column(Integer, nullable=True)
    position_y = Column(Integer, nullable=True)
    has_power_outlet = Column(Boolean, default=False, nullable=False)
    has_view = Column(Boolean, default=False, nullable=False)
    is_wheelchair_accessible = Column(Boolean, default=True, nullable=False)
    
    # Status
    current_status = Column(String(20), default="available", nullable=False)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="tables")
    guest_sessions = relationship("GuestSession", back_populates="table", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="table")
    
    @property
    def display_name(self) -> str:
        """Get display name for table."""
        return self.table_name or f"Table {self.table_number}"
    
    @property
    def is_available(self) -> bool:
        """Check if table is available."""
        return self.is_active and self.current_status == "available"
    
    def __repr__(self):
        return f"<RestaurantTable(number={self.table_number}, restaurant_id={self.restaurant_id})>"


# =================================================================
# GUEST SESSION MODEL
# =================================================================

class GuestSession(BaseModel):
    """Guest session for QR code ordering."""
    __tablename__ = "guest_session"
    
    # Foreign Keys
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=False, index=True)
    table_id = Column(UUID(as_uuid=True), ForeignKey("restaurant_table.id"), nullable=False, index=True)
    
    # Session Information
    session_token = Column(String(100), nullable=False, unique=True, index=True)
    guest_name = Column(String(255), nullable=True)
    guest_phone = Column(String(20), nullable=True)
    guest_email = Column(String(255), nullable=True)
    party_size = Column(Integer, nullable=False, default=1)
    
    # Session Data
    special_requests = Column(Text, nullable=True)
    cart_data = Column(String, nullable=True)  # JSON string for cart items
    preferences = Column(String, nullable=True)  # JSON string for preferences
    
    # Session Control
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="guest_sessions")
    table = relationship("RestaurantTable", back_populates="guest_sessions")
    orders = relationship("Order", back_populates="guest_session")
    
    @property
    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def time_remaining_minutes(self) -> int:
        """Get remaining time in minutes."""
        if self.is_expired:
            return 0
        delta = self.expires_at - datetime.utcnow()
        return int(delta.total_seconds() / 60)
    
    @property
    def cart_item_count(self) -> int:
        """Get number of items in cart."""
        # This would parse cart_data JSON and count items
        return 0  # Placeholder
    
    def extend_session(self, hours: int = None) -> None:
        """Extend session expiry."""
        if not hours:
            hours = settings.GUEST_SESSION_EXPIRE_HOURS
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    def __repr__(self):
        return f"<GuestSession(token={self.session_token[:8]}..., table_id={self.table_id})>"