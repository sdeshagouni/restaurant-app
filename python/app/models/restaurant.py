"""
Restaurant and User models.
Core models for restaurant management and user authentication.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Integer, Text, ForeignKey, Date, JSON
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any
from uuid import uuid4

from app.models.base import BaseModel, UserRole, StaffType, RestaurantStatus, SubscriptionTier


# =================================================================
# RESTAURANT MODEL
# =================================================================

class Restaurant(BaseModel):
    """Restaurant entity model."""
    __tablename__ = "restaurant"
    
    # Basic Information
    restaurant_name = Column(String(255), nullable=False, index=True)
    restaurant_code = Column(String(50), nullable=False, unique=True, index=True)
    business_email = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    website_url = Column(String(500), nullable=True)
    
    # Address (stored as JSON)
    address = Column(JSON, nullable=True)
    
    # Business Configuration
    currency_code = Column(String(3), nullable=False, default="USD")
    tax_rate = Column(Numeric(5, 4), nullable=False, default=Decimal("0.08"))
    service_charge_rate = Column(Numeric(5, 4), nullable=False, default=Decimal("0.10"))
    timezone = Column(String(50), nullable=False, default="UTC")
    
    # Operating Hours (stored as JSON)
    operating_hours = Column(JSON, nullable=True)
    
    # Business Features
    allows_takeout = Column(Boolean, default=True, nullable=False)
    allows_delivery = Column(Boolean, default=False, nullable=False)
    allows_reservations = Column(Boolean, default=True, nullable=False)
    delivery_radius_km = Column(Numeric(6, 2), nullable=True)
    minimum_delivery_amount = Column(Numeric(10, 2), nullable=True)
    
    # Status and Subscription
    status = Column(String(20), nullable=False, default=RestaurantStatus.ACTIVE)
    subscription_tier = Column(String(20), nullable=False, default=SubscriptionTier.TRIAL)
    subscription_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Branding
    logo_url = Column(String(500), nullable=True)
    banner_url = Column(String(500), nullable=True)
    theme_color = Column(String(7), nullable=True)  # Hex color code
    
    # Additional Settings (stored as JSON)
    settings = Column(JSON, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="restaurant", cascade="all, delete-orphan")
    tables = relationship("RestaurantTable", back_populates="restaurant", cascade="all, delete-orphan")
    menu_categories = relationship("MenuCategory", back_populates="restaurant", cascade="all, delete-orphan")
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="restaurant", cascade="all, delete-orphan")
    daily_specials = relationship("DailySpecial", back_populates="restaurant", cascade="all, delete-orphan")
    payment_gateways = relationship("PaymentGateway", back_populates="restaurant", cascade="all, delete-orphan")
    guest_sessions = relationship("GuestSession", back_populates="restaurant", cascade="all, delete-orphan")
    
    @property
    def is_active(self) -> bool:
        """Check if restaurant is active."""
        return self.status == RestaurantStatus.ACTIVE
    
    @property
    def subscription_active(self) -> bool:
        """Check if subscription is active."""
        if not self.subscription_expires_at:
            return True
        return datetime.utcnow() < self.subscription_expires_at
    
    def __repr__(self):
        return f"<Restaurant(name={self.restaurant_name}, code={self.restaurant_code})>"


# =================================================================
# USER MODEL
# =================================================================

class User(BaseModel):
    """User model for restaurant staff and owners."""
    __tablename__ = "user"
    
    # Foreign Keys
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurant.id"), nullable=True, index=True)
    
    # Authentication
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    
    # Role and Permissions
    role = Column(String(20), nullable=False, default=UserRole.STAFF)
    staff_type = Column(String(20), nullable=True)
    permissions = Column(JSON, nullable=True, default=dict)
    
    # Employment Information
    employee_id = Column(String(50), nullable=True)
    hire_date = Column(Date, nullable=True)
    salary = Column(Numeric(10, 2), nullable=True)
    hourly_rate = Column(Numeric(6, 2), nullable=True)
    
    # Account Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Security
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Profile
    profile_image_url = Column(String(500), nullable=True)
    language = Column(String(10), default="en", nullable=False)
    timezone = Column(String(50), default="UTC", nullable=False)
    preferences = Column(JSON, nullable=True, default=dict)
    
    # Notifications
    notification_email = Column(Boolean, default=True, nullable=False)
    notification_sms = Column(Boolean, default=False, nullable=False)
    notification_push = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="users")
    orders = relationship("Order", back_populates="created_by_user", foreign_keys="Order.created_by_user_id")
    
    @property
    def full_name(self) -> str:
        """Get full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_locked(self) -> bool:
        """Check if account is locked."""
        if not self.locked_until:
            return False
        return datetime.utcnow() < self.locked_until
    
    @property
    def is_owner(self) -> bool:
        """Check if user is restaurant owner."""
        return self.role == UserRole.OWNER
    
    @property
    def is_manager(self) -> bool:
        """Check if user is manager or owner."""
        return self.role in [UserRole.OWNER, UserRole.MANAGER]
    
    @property
    def is_staff(self) -> bool:
        """Check if user is staff member."""
        return self.role in [UserRole.OWNER, UserRole.MANAGER, UserRole.STAFF]
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission."""
        if self.role == UserRole.OWNER:
            return True
        return self.permissions.get(permission, False) if self.permissions else False
    
    def __repr__(self):
        return f"<User(email={self.email}, role={self.role})>"