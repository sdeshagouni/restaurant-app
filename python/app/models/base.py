"""
Base models and enums for the restaurant management system.
Defines common enums, base model class, and shared functionality.
"""

from sqlalchemy import Column, DateTime, UUID, Boolean, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from uuid import uuid4
from enum import Enum
import uuid

# =================================================================
# SQLAlchemy Base
# =================================================================

Base = declarative_base()

# =================================================================
# ENUMS
# =================================================================

class UserRole(str, Enum):
    """User roles in the system."""
    ADMIN = "ADMIN"
    OWNER = "OWNER" 
    MANAGER = "MANAGER"
    STAFF = "STAFF"
    CUSTOMER = "CUSTOMER"

class StaffType(str, Enum):
    """Staff types for restaurant employees."""
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    HEAD_CHEF = "HEAD_CHEF"
    CHEF = "CHEF"
    WAITER = "WAITER"
    CASHIER = "CASHIER"
    HOST = "HOST"
    BARTENDER = "BARTENDER"
    KITCHEN = "KITCHEN"
    CLEANER = "CLEANER"
    DELIVERY = "DELIVERY"

class RestaurantStatus(str, Enum):
    """Restaurant operational status."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING = "PENDING"
    CLOSED = "CLOSED"

class SubscriptionTier(str, Enum):
    """Subscription tiers for restaurants."""
    TRIAL = "TRIAL"
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"
    ENTERPRISE = "ENTERPRISE"

class OrderStatus(str, Enum):
    """Order processing status."""
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    SERVED = "SERVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

class PaymentStatus(str, Enum):
    """Payment processing status."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"

class OrderType(str, Enum):
    """Type of order."""
    DINE_IN = "DINE_IN"
    TAKEOUT = "TAKEOUT"
    DELIVERY = "DELIVERY"
    CATERING = "CATERING"

class ItemStatus(str, Enum):
    """Order item status."""
    ORDERED = "ORDERED"
    PREPARING = "PREPARING"
    READY = "READY"
    SERVED = "SERVED"
    CANCELLED = "CANCELLED"

class PaymentMethod(str, Enum):
    """Payment methods."""
    CASH = "CASH"
    CARD = "CARD"
    DIGITAL_WALLET = "DIGITAL_WALLET"
    BANK_TRANSFER = "BANK_TRANSFER"
    CRYPTO = "CRYPTO"

class SpecialType(str, Enum):
    """Daily special types."""
    DISCOUNT = "DISCOUNT"
    COMBO = "COMBO"
    FEATURED = "FEATURED"
    LIMITED_TIME = "LIMITED_TIME"
    BUY_ONE_GET_ONE = "BUY_ONE_GET_ONE"

class DiscountType(str, Enum):
    """Discount calculation types."""
    PERCENTAGE = "PERCENTAGE"
    FIXED_AMOUNT = "FIXED_AMOUNT"
    BUY_X_GET_Y = "BUY_X_GET_Y"

class GatewayProvider(str, Enum):
    """Payment gateway providers."""
    STRIPE = "STRIPE"
    PAYPAL = "PAYPAL"
    SQUARE = "SQUARE"
    RAZORPAY = "RAZORPAY"
    PAYU = "PAYU"

# =================================================================
# BASE MODEL
# =================================================================

class BaseModel(Base):
    """Base model with common fields."""
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
