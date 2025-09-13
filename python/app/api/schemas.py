"""
Pydantic schemas for API request and response validation.
Core schemas for authentication, restaurants, and common responses.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID
from enum import Enum

from app.models.base import (
    UserRole, StaffType, RestaurantStatus, SubscriptionTier,
    OrderStatus, PaymentStatus, OrderType
)


# =================================================================
# COMMON SCHEMAS
# =================================================================

class SuccessResponse(BaseModel):
    """Standard success response format."""
    success: bool = True
    data: Dict[str, Any]
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

class ErrorDetail(BaseModel):
    """Error detail information."""
    field: Optional[str] = None
    reason: str
    code: Optional[str] = None

class ErrorResponse(BaseModel):
    """Standard error response format."""
    success: bool = False
    error: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

class PaginationMeta(BaseModel):
    """Pagination metadata."""
    total: int
    page: int
    size: int
    pages: int


# =================================================================
# AUTHENTICATION SCHEMAS
# =================================================================

class UserLogin(BaseModel):
    """User login request."""
    username: EmailStr
    password: str = Field(min_length=8)

class UserProfile(BaseModel):
    """User profile information."""
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str]
    role: UserRole
    staff_type: Optional[StaffType]
    restaurant_id: Optional[UUID]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: "UserProfile"

class RefreshTokenRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str

class UserRegister(BaseModel):
    """User registration request (admin only)."""
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    role: UserRole
    staff_type: Optional[StaffType] = None
    restaurant_id: UUID
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if v and not v.startswith('+'):
            raise ValueError('Phone number must start with +')
        return v

class UserUpdate(BaseModel):
    """User profile update."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    preferences: Optional[Dict[str, Any]] = None

class ChangePasswordRequest(BaseModel):
    """Change password request."""
    current_password: str
    new_password: str = Field(min_length=8)


# =================================================================
# RESTAURANT SCHEMAS
# =================================================================

class RestaurantBase(BaseModel):
    """Base restaurant information."""
    restaurant_name: str = Field(min_length=1, max_length=255)
    business_email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    website_url: Optional[str] = Field(None, max_length=500)
    currency_code: str = Field(default="USD", max_length=3)
    tax_rate: Decimal = Field(default=Decimal("0.08"), ge=0, le=1)
    service_charge_rate: Decimal = Field(default=Decimal("0.10"), ge=0, le=1)
    timezone: str = Field(default="UTC", max_length=50)

class RestaurantCreate(RestaurantBase):
    """Restaurant creation request."""
    restaurant_code: str = Field(min_length=1, max_length=50)
    address: Optional[Dict[str, Any]] = None
    operating_hours: Optional[Dict[str, Any]] = None

class RestaurantUpdate(BaseModel):
    """Restaurant update request."""
    restaurant_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)
    tax_rate: Optional[Decimal] = Field(None, ge=0, le=1)
    service_charge_rate: Optional[Decimal] = Field(None, ge=0, le=1)
    operating_hours: Optional[Dict[str, Any]] = None
    allows_takeout: Optional[bool] = None
    allows_delivery: Optional[bool] = None
    delivery_radius_km: Optional[Decimal] = Field(None, ge=0)
    minimum_delivery_amount: Optional[Decimal] = Field(None, ge=0)

class RestaurantResponse(RestaurantBase):
    """Restaurant response data."""
    id: UUID
    restaurant_code: str
    address: Optional[Dict[str, Any]]
    operating_hours: Optional[Dict[str, Any]]
    allows_takeout: bool
    allows_delivery: bool
    allows_reservations: bool
    delivery_radius_km: Optional[Decimal]
    minimum_delivery_amount: Optional[Decimal]
    status: RestaurantStatus
    subscription_tier: SubscriptionTier
    subscription_expires_at: Optional[datetime]
    logo_url: Optional[str]
    banner_url: Optional[str]
    theme_color: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    """Restaurant dashboard summary."""
    today: Dict[str, Any]
    week: Dict[str, Any]
    month: Dict[str, Any]
    operational: Dict[str, Any]
    performance: Dict[str, Any]


# =================================================================
# TABLE SCHEMAS
# =================================================================

class TableBase(BaseModel):
    """Base table information."""
    table_number: str = Field(min_length=1, max_length=20)
    table_name: Optional[str] = Field(None, max_length=100)
    capacity: int = Field(ge=1, le=20)
    location: Optional[str] = Field(None, max_length=100)

class TableCreate(TableBase):
    """Table creation request."""
    requires_reservation: bool = False
    position_x: Optional[int] = None
    position_y: Optional[int] = None

class TableUpdate(BaseModel):
    """Table update request."""
    table_name: Optional[str] = Field(None, max_length=100)
    capacity: Optional[int] = Field(None, ge=1, le=20)
    requires_reservation: Optional[bool] = None
    is_active: Optional[bool] = None
    position_x: Optional[int] = None
    position_y: Optional[int] = None

class TableResponse(TableBase):
    """Table response data."""
    id: UUID
    qr_code: str
    qr_code_url: Optional[str]
    qr_code_image_url: Optional[str]
    is_active: bool
    requires_reservation: bool
    is_vip: bool
    position_x: Optional[int]
    position_y: Optional[int]
    current_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TableByQRResponse(BaseModel):
    """Table info from QR code scan."""
    table: Dict[str, Any]
    restaurant: Dict[str, Any]
    session_url: str


# =================================================================
# GUEST SESSION SCHEMAS
# =================================================================

class GuestSessionCreate(BaseModel):
    """Guest session creation."""
    table_id: UUID
    guest_name: Optional[str] = Field(None, max_length=255)
    guest_phone: Optional[str] = Field(None, max_length=20)
    guest_email: Optional[EmailStr] = None
    party_size: int = Field(default=1, ge=1, le=20)
    special_requests: Optional[str] = None

class GuestSessionUpdate(BaseModel):
    """Guest session update."""
    guest_name: Optional[str] = Field(None, max_length=255)
    party_size: Optional[int] = Field(None, ge=1, le=20)
    cart_data: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None

class GuestSessionResponse(BaseModel):
    """Guest session response."""
    id: UUID
    session_token: str
    table: Dict[str, Any]
    restaurant: Dict[str, Any]
    guest_name: Optional[str]
    party_size: int
    expires_at: datetime
    is_active: bool
    cart_item_count: int = 0
    cart_total: Decimal = Decimal("0")
    
    class Config:
        from_attributes = True


# =================================================================
# MENU SCHEMAS
# =================================================================

class MenuCategoryBase(BaseModel):
    """Base menu category."""
    category_name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)

class MenuCategoryCreate(MenuCategoryBase):
    """Menu category creation."""
    display_order: int = 0
    available_all_day: bool = True
    available_from: Optional[time] = None
    available_until: Optional[time] = None

class MenuCategoryUpdate(BaseModel):
    """Menu category update."""
    category_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None

class MenuCategoryResponse(MenuCategoryBase):
    """Menu category response."""
    id: UUID
    display_order: int
    is_active: bool
    available_all_day: bool
    available_from: Optional[time]
    available_until: Optional[time]
    item_count: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True

class MenuItemBase(BaseModel):
    """Base menu item."""
    item_name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(gt=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)

class MenuItemCreate(MenuItemBase):
    """Menu item creation."""
    category_id: Optional[UUID] = None
    prep_time_minutes: int = Field(default=15, ge=0, le=180)
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_spicy: bool = False
    spice_level: int = Field(default=0, ge=0, le=5)
    calories: Optional[int] = Field(None, ge=0)
    display_order: int = 0
    is_featured: bool = False

class MenuItemUpdate(BaseModel):
    """Menu item update."""
    item_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    cost_price: Optional[Decimal] = Field(None, ge=0)
    is_available: Optional[bool] = None
    is_featured: Optional[bool] = None

class MenuItemResponse(MenuItemBase):
    """Menu item response."""
    id: UUID
    category: Optional[Dict[str, Any]]
    is_vegetarian: bool
    is_vegan: bool
    is_gluten_free: bool
    is_spicy: bool
    spice_level: int
    calories: Optional[int]
    is_available: bool
    prep_time_minutes: int
    image_url: Optional[str]
    is_featured: bool
    is_popular: bool
    display_order: int
    options: List[Dict[str, Any]] = []
    profit_margin: Optional[Decimal] = None
    profit_margin_percent: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# =================================================================
# ORDER SCHEMAS
# =================================================================

class OrderItemCreate(BaseModel):
    """Order item creation."""
    menu_item_id: UUID
    quantity: int = Field(ge=1, le=50)
    selected_options: List[UUID] = []
    special_instructions: Optional[str] = None

class OrderCreate(BaseModel):
    """Order creation."""
    guest_session_id: Optional[UUID] = None
    table_id: Optional[UUID] = None
    order_type: OrderType = OrderType.DINE_IN
    items: List[OrderItemCreate]
    special_instructions: Optional[str] = None
    estimated_pickup_time: Optional[datetime] = None

class OrderStatusUpdate(BaseModel):
    """Order status update."""
    status: OrderStatus
    notes: Optional[str] = None
    estimated_ready_time: Optional[datetime] = None

class OrderResponse(BaseModel):
    """Order response."""
    id: UUID
    order_number: str
    order_type: OrderType
    order_status: OrderStatus
    payment_status: PaymentStatus
    table: Optional[Dict[str, Any]]
    guest_name: Optional[str]
    party_size: int
    items: List[Dict[str, Any]]
    subtotal: Decimal
    tax_amount: Decimal
    service_charge: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    estimated_prep_time: Optional[int]
    ordered_at: datetime
    estimated_ready_time: Optional[datetime]
    
    class Config:
        from_attributes = True