"""
Authentication API routes.
Handles user login, registration, token management, and user profile.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import Dict, Any, Optional
from uuid import uuid4
from decimal import Decimal

from app.core.security import (
    create_access_token, create_refresh_token, verify_token,
    get_password_hash, verify_password, get_current_user, get_current_active_user,
    get_admin_user
)
from app.core.config import settings
from app.core.database import get_db
from app.api.schemas import (
    UserLogin, TokenResponse, RefreshTokenRequest, UserRegister, UserProfile,
    UserUpdate, ChangePasswordRequest, SuccessResponse, RestaurantOwnerRegister
)
from app.models.restaurant import User, Restaurant
from app.models.base import UserRole, StaffType, RestaurantStatus, SubscriptionTier

router = APIRouter()


# =================================================================
# RESTAURANT OWNER REGISTRATION (PUBLIC)
# =================================================================

@router.post("/register-restaurant", response_model=Dict[str, Any])
async def register_restaurant_owner(
    registration_data: RestaurantOwnerRegister,
    db: Session = Depends(get_db)
):
    """Register new restaurant owner and create restaurant (Public access)."""
    
    try:
        # Check if owner email already exists
        existing_user = db.query(User).filter(User.email == registration_data.owner_email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if restaurant code already exists
        existing_restaurant = db.query(Restaurant).filter(
            Restaurant.restaurant_code == registration_data.restaurant_code
        ).first()
        if existing_restaurant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Restaurant code already exists"
            )
        
        # Create restaurant first
        new_restaurant = Restaurant(
            restaurant_name=registration_data.restaurant_name,
            restaurant_code=registration_data.restaurant_code,
            business_email=registration_data.business_email,
            phone_number=registration_data.business_phone,
            address=registration_data.address,
            timezone=registration_data.timezone,
            currency_code=registration_data.currency_code,
            tax_rate=Decimal("0.08"),  # Default 8% tax
            service_charge_rate=Decimal("0.10"),  # Default 10% service charge
            status=RestaurantStatus.ACTIVE,
            subscription_tier=SubscriptionTier.TRIAL,
            allows_takeout=True,
            allows_delivery=False,
            allows_reservations=True
        )
        
        db.add(new_restaurant)
        db.flush()  # Get the restaurant ID
        
        # Create owner user
        hashed_password = get_password_hash(registration_data.owner_password)
        owner_user = User(
            email=registration_data.owner_email,
            password_hash=hashed_password,
            first_name=registration_data.owner_first_name,
            last_name=registration_data.owner_last_name,
            phone_number=registration_data.owner_phone,
            role=UserRole.OWNER,
            staff_type=StaffType.OWNER,
            restaurant_id=new_restaurant.id,
            is_active=True,
            is_verified=True  # Auto-verify owners
        )
        
        db.add(owner_user)
        db.commit()
        db.refresh(new_restaurant)
        db.refresh(owner_user)
        
        # Create access token for immediate login
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"sub": str(owner_user.id)}
        access_token = create_access_token(token_data, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(token_data)
        
        return {
            "success": True,
            "data": {
                "restaurant": {
                    "id": str(new_restaurant.id),
                    "restaurant_name": new_restaurant.restaurant_name,
                    "restaurant_code": new_restaurant.restaurant_code,
                    "business_email": new_restaurant.business_email,
                    "status": new_restaurant.status,
                    "subscription_tier": new_restaurant.subscription_tier,
                    "created_at": new_restaurant.created_at.isoformat() + "Z"
                },
                "owner": {
                    "id": str(owner_user.id),
                    "email": owner_user.email,
                    "first_name": owner_user.first_name,
                    "last_name": owner_user.last_name,
                    "role": owner_user.role,
                    "staff_type": owner_user.staff_type
                },
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                }
            },
            "message": "Restaurant and owner account created successfully"
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"Error creating restaurant: {str(e)}")  # Debug logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create restaurant and owner: {str(e)}"
        )


# =================================================================
# EXISTING AUTHENTICATION ENDPOINTS
# =================================================================

@router.post("/register", response_model=SuccessResponse)
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Register a new user (Admin only)."""
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Verify restaurant exists
    restaurant = db.query(Restaurant).filter(Restaurant.id == user_data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number,
        role=user_data.role,
        staff_type=user_data.staff_type,
        restaurant_id=user_data.restaurant_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "success": True,
        "data": {
            "user": {
                "id": str(new_user.id),
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "role": new_user.role,
                "restaurant_id": str(new_user.restaurant_id),
                "is_active": new_user.is_active,
                "created_at": new_user.created_at.isoformat() + "Z"
            }
        },
        "message": "User registered successfully"
    }


@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """User login with email and password."""
    
    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Check if account is locked
    if hasattr(user, 'is_locked') and user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is locked"
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    if hasattr(user, 'failed_login_attempts'):
        user.failed_login_attempts = 0  # Reset failed attempts
    db.commit()
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(token_data)
    
    # Create user profile data
    user_profile = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "role": user.role,
        "staff_type": user.staff_type,
        "restaurant_id": user.restaurant_id,
        "is_active": user.is_active,
        "created_at": user.created_at
    }
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user_profile
    }


@router.post("/refresh", response_model=Dict[str, Any])
async def refresh_token(
    token_request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    
    payload = verify_token(token_request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Verify user still exists and is active
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(token_data, expires_delta=access_token_expires)
    
    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    }


@router.get("/me", response_model=Dict[str, Any])
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile."""
    
    return {
        "success": True,
        "data": {
            "user": {
                "id": str(current_user.id),
                "email": current_user.email,
                "first_name": current_user.first_name,
                "last_name": current_user.last_name,
                "full_name": getattr(current_user, 'full_name', f"{current_user.first_name} {current_user.last_name}"),
                "phone_number": current_user.phone_number,
                "role": current_user.role,
                "staff_type": current_user.staff_type,
                "restaurant_id": str(current_user.restaurant_id) if current_user.restaurant_id else None,
                "is_active": current_user.is_active,
                "is_verified": getattr(current_user, 'is_verified', True),
                "last_login_at": current_user.last_login_at.isoformat() + "Z" if current_user.last_login_at else None,
                "permissions": getattr(current_user, 'permissions', {}),
                "preferences": getattr(current_user, 'preferences', {}),
                "created_at": current_user.created_at.isoformat() + "Z"
            }
        }
    }


@router.put("/me", response_model=SuccessResponse)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    
    # Update only provided fields
    if user_data.first_name is not None:
        current_user.first_name = user_data.first_name
    
    if user_data.last_name is not None:
        current_user.last_name = user_data.last_name
    
    if user_data.phone_number is not None:
        current_user.phone_number = user_data.phone_number
    
    if user_data.preferences is not None and hasattr(current_user, 'preferences'):
        current_user.preferences = user_data.preferences
    
    # Update timestamp
    if hasattr(current_user, 'updated_at'):
        current_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "success": True,
        "data": {
            "user": {
                "id": str(current_user.id),
                "email": current_user.email,
                "first_name": current_user.first_name,
                "last_name": current_user.last_name,
                "phone_number": current_user.phone_number,
                "preferences": getattr(current_user, 'preferences', {}),
                "updated_at": getattr(current_user, 'updated_at', datetime.utcnow()).isoformat() + "Z"
            }
        },
        "message": "Profile updated successfully"
    }


@router.post("/change-password", response_model=SuccessResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Change user password."""
    
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(password_data.new_password)
    
    # Update password changed timestamp
    if hasattr(current_user, 'password_changed_at'):
        current_user.password_changed_at = datetime.utcnow()
    if hasattr(current_user, 'updated_at'):
        current_user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": "Password changed successfully",
            "password_changed_at": getattr(current_user, 'password_changed_at', datetime.utcnow()).isoformat() + "Z"
        },
        "message": "Password changed successfully"
    }


@router.post("/logout", response_model=SuccessResponse)
async def logout_user(
    current_user: User = Depends(get_current_active_user)
):
    """User logout (client-side token invalidation)."""
    
    return {
        "success": True,
        "data": {
            "message": "Logged out successfully"
        },
        "message": "Logged out successfully. Please remove the token from client storage."
    }