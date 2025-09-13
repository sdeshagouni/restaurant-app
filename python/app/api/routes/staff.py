"""
Staff management API routes.
Handles staff registration, updates, and management by restaurant owners/managers.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from app.core.security import (
    get_owner_or_manager_user, get_restaurant_context, get_password_hash
)
from app.core.database import get_db
from app.models.restaurant import User, Restaurant
from app.models.base import UserRole, StaffType

router = APIRouter()


# =================================================================
# STAFF SCHEMAS
# =================================================================

class StaffRegister(BaseModel):
    """Staff registration by owner/manager."""
    email: EmailStr
    password: str = Field(min_length=8)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.STAFF
    staff_type: StaffType
    hourly_rate: Optional[float] = Field(None, ge=0)
    permissions: Optional[Dict[str, Any]] = None

class StaffUpdate(BaseModel):
    """Staff update by owner/manager."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    role: Optional[UserRole] = None
    staff_type: Optional[StaffType] = None
    hourly_rate: Optional[float] = Field(None, ge=0)
    permissions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


# =================================================================
# STAFF MANAGEMENT ENDPOINTS
# =================================================================

@router.post("/{restaurant_id}/staff", response_model=Dict[str, Any])
async def add_staff_member(
    restaurant_id: UUID,
    staff_data: StaffRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Add new staff member to restaurant (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == staff_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Only owners can add managers, managers can add staff
    if staff_data.role == UserRole.MANAGER and current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can add managers"
        )
    
    # Create new staff member
    hashed_password = get_password_hash(staff_data.password)
    new_staff = User(
        email=staff_data.email,
        password_hash=hashed_password,
        first_name=staff_data.first_name,
        last_name=staff_data.last_name,
        phone_number=staff_data.phone_number,
        role=staff_data.role,
        staff_type=staff_data.staff_type,
        restaurant_id=restaurant_id,
        hourly_rate=staff_data.hourly_rate,
        permissions=staff_data.permissions or {},
        is_active=True
    )
    
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    
    return {
        "success": True,
        "data": {
            "staff": {
                "id": str(new_staff.id),
                "email": new_staff.email,
                "first_name": new_staff.first_name,
                "last_name": new_staff.last_name,
                "full_name": new_staff.full_name,
                "phone_number": new_staff.phone_number,
                "role": new_staff.role,
                "staff_type": new_staff.staff_type,
                "hourly_rate": new_staff.hourly_rate,
                "permissions": new_staff.permissions,
                "is_active": new_staff.is_active,
                "created_at": new_staff.created_at.isoformat() + "Z"
            }
        },
        "message": "Staff member added successfully"
    }


@router.get("/{restaurant_id}/staff", response_model=Dict[str, Any])
async def list_staff_members(
    restaurant_id: UUID,
    role: Optional[List[str]] = Query(None, description="Filter by roles"),
    staff_type: Optional[List[str]] = Query(None, description="Filter by staff types"),
    active_only: bool = Query(True, description="Show only active staff"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """List all staff members for a restaurant (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Build query
    query = db.query(User).filter(User.restaurant_id == restaurant_id)
    
    if role:
        query = query.filter(User.role.in_(role))
    
    if staff_type:
        query = query.filter(User.staff_type.in_(staff_type))
    
    if active_only:
        query = query.filter(User.is_active == True)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    staff_members = query.order_by(User.created_at.desc()).offset(offset).limit(size).all()
    
    # Prepare response
    staff_data = []
    for staff in staff_members:
        staff_data.append({
            "id": str(staff.id),
            "email": staff.email,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "full_name": staff.full_name,
            "phone_number": staff.phone_number,
            "role": staff.role,
            "staff_type": staff.staff_type,
            "hourly_rate": staff.hourly_rate,
            "permissions": staff.permissions,
            "is_active": staff.is_active,
            "is_verified": staff.is_verified,
            "last_login_at": staff.last_login_at.isoformat() + "Z" if staff.last_login_at else None,
            "created_at": staff.created_at.isoformat() + "Z"
        })
    
    pages = (total + size - 1) // size
    
    return {
        "success": True,
        "data": {
            "staff": staff_data,
            "pagination": {
                "total": total,
                "page": page,
                "size": size,
                "pages": pages
            },
            "summary": {
                "total_staff": total,
                "active_staff": len([s for s in staff_members if s.is_active]),
                "managers": len([s for s in staff_members if s.role == UserRole.MANAGER]),
                "staff": len([s for s in staff_members if s.role == UserRole.STAFF])
            }
        }
    }


@router.get("/{restaurant_id}/staff/{staff_id}", response_model=Dict[str, Any])
async def get_staff_member(
    restaurant_id: UUID,
    staff_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Get staff member details (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find staff member
    staff_member = db.query(User).filter(
        User.id == staff_id,
        User.restaurant_id == restaurant_id
    ).first()
    
    if not staff_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )
    
    return {
        "success": True,
        "data": {
            "staff": {
                "id": str(staff_member.id),
                "email": staff_member.email,
                "first_name": staff_member.first_name,
                "last_name": staff_member.last_name,
                "full_name": staff_member.full_name,
                "phone_number": staff_member.phone_number,
                "role": staff_member.role,
                "staff_type": staff_member.staff_type,
                "hourly_rate": staff_member.hourly_rate,
                "permissions": staff_member.permissions,
                "preferences": staff_member.preferences,
                "is_active": staff_member.is_active,
                "is_verified": staff_member.is_verified,
                "is_locked": staff_member.is_locked,
                "last_login_at": staff_member.last_login_at.isoformat() + "Z" if staff_member.last_login_at else None,
                "created_at": staff_member.created_at.isoformat() + "Z",
                "updated_at": staff_member.updated_at.isoformat() + "Z" if staff_member.updated_at else None
            }
        }
    }


@router.put("/{restaurant_id}/staff/{staff_id}", response_model=Dict[str, Any])
async def update_staff_member(
    restaurant_id: UUID,
    staff_id: UUID,
    staff_data: StaffUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Update staff member (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find staff member
    staff_member = db.query(User).filter(
        User.id == staff_id,
        User.restaurant_id == restaurant_id
    ).first()
    
    if not staff_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )
    
    # Only owners can update managers
    if staff_member.role == UserRole.MANAGER and current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can update managers"
        )
    
    # Only owners can promote to manager
    if staff_data.role == UserRole.MANAGER and current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can promote to manager"
        )
    
    # Update only provided fields
    update_data = staff_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(staff_member, field, value)
    
    from datetime import datetime
    staff_member.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(staff_member)
    
    return {
        "success": True,
        "data": {
            "staff": {
                "id": str(staff_member.id),
                "email": staff_member.email,
                "first_name": staff_member.first_name,
                "last_name": staff_member.last_name,
                "role": staff_member.role,
                "staff_type": staff_member.staff_type,
                "hourly_rate": staff_member.hourly_rate,
                "permissions": staff_member.permissions,
                "is_active": staff_member.is_active,
                "updated_at": staff_member.updated_at.isoformat() + "Z"
            }
        },
        "message": "Staff member updated successfully"
    }


@router.delete("/{restaurant_id}/staff/{staff_id}", response_model=Dict[str, Any])
async def remove_staff_member(
    restaurant_id: UUID,
    staff_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Remove staff member (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find staff member
    staff_member = db.query(User).filter(
        User.id == staff_id,
        User.restaurant_id == restaurant_id
    ).first()
    
    if not staff_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )
    
    # Cannot remove yourself
    if staff_member.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove yourself"
        )
    
    # Only owners can remove managers
    if staff_member.role == UserRole.MANAGER and current_user.role != UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can remove managers"
        )
    
    # Cannot remove other owners
    if staff_member.role == UserRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove restaurant owner"
        )
    
    # Soft delete - deactivate instead of removing
    staff_member.is_active = False
    from datetime import datetime
    staff_member.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": f"Staff member {staff_member.full_name} has been deactivated"
        },
        "message": "Staff member removed successfully"
    }


@router.patch("/{restaurant_id}/staff/{staff_id}/activate", response_model=Dict[str, Any])
async def activate_staff_member(
    restaurant_id: UUID,
    staff_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Reactivate staff member (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find staff member
    staff_member = db.query(User).filter(
        User.id == staff_id,
        User.restaurant_id == restaurant_id
    ).first()
    
    if not staff_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )
    
    staff_member.is_active = True
    from datetime import datetime
    staff_member.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "data": {
            "staff": {
                "id": str(staff_member.id),
                "email": staff_member.email,
                "full_name": staff_member.full_name,
                "is_active": staff_member.is_active,
                "updated_at": staff_member.updated_at.isoformat() + "Z"
            }
        },
        "message": "Staff member activated successfully"
    }