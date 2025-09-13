"""
Table management API routes.
Handles table CRUD operations and QR code functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
from uuid import UUID
import secrets
import string

from app.core.security import (
    get_current_active_user, get_staff_user, get_owner_or_manager_user,
    get_restaurant_context, verify_guest_session, get_guest_session_token
)
from app.api.schemas import (
    TableCreate, TableUpdate, TableResponse, TableByQRResponse,
    GuestSessionCreate, GuestSessionUpdate, GuestSessionResponse,
    SuccessResponse, PaginationMeta
)
from app.models.restaurant import Restaurant
from app.models.table import RestaurantTable, GuestSession
from app.core.config import settings
from app.core.database import get_db

router = APIRouter()


# =================================================================
# HELPER FUNCTIONS
# =================================================================

def generate_qr_code(restaurant_code: str, table_number: str) -> str:
    """Generate QR code string for table."""
    return f"QR_{restaurant_code}_{table_number}"

def generate_session_token() -> str:
    """Generate secure session token."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))


# =================================================================
# STAFF TABLE MANAGEMENT
# =================================================================

@router.get("/restaurants/{restaurant_id}/tables", response_model=Dict[str, Any])
async def list_restaurant_tables(
    restaurant_id: UUID,
    active_only: bool = Query(True, description="Filter by active tables only"),
    location: Optional[str] = Query(None, description="Filter by location"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    db: Session = Depends(get_db),
    current_user = Depends(get_staff_user)
):
    """List all tables for a restaurant (Staff access required)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Build query
    query = db.query(RestaurantTable).filter(RestaurantTable.restaurant_id == restaurant_id)
    
    if active_only:
        query = query.filter(RestaurantTable.is_active == True)
    
    if location:
        query = query.filter(RestaurantTable.location.ilike(f"%{location}%"))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    tables = query.order_by(RestaurantTable.display_order, RestaurantTable.table_number).offset(offset).limit(size).all()
    
    # Prepare response
    table_data = []
    for table in tables:
        table_data.append({
            "id": str(table.id),
            "table_number": table.table_number,
            "table_name": table.table_name,
            "capacity": table.capacity,
            "location": table.location,
            "qr_code": table.qr_code,
            "qr_code_url": table.qr_code_url,
            "is_active": table.is_active,
            "requires_reservation": table.requires_reservation,
            "is_vip": table.is_vip,
            "current_status": table.current_status,
            "position_x": table.position_x,
            "position_y": table.position_y,
            "has_power_outlet": table.has_power_outlet,
            "has_view": table.has_view,
            "is_wheelchair_accessible": table.is_wheelchair_accessible,
            "display_name": table.display_name,
            "is_available": table.is_available,
            "created_at": table.created_at.isoformat() + "Z"
        })
    
    pages = (total + size - 1) // size
    
    return {
        "success": True,
        "data": {
            "tables": table_data,
            "pagination": {
                "total": total,
                "page": page,
                "size": size,
                "pages": pages
            }
        }
    }


@router.get("/restaurants/{restaurant_id}/tables/{table_id}", response_model=Dict[str, Any])
async def get_table_details(
    restaurant_id: UUID,
    table_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_staff_user)
):
    """Get table details (Staff access required)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    table = db.query(RestaurantTable).filter(
        RestaurantTable.id == table_id,
        RestaurantTable.restaurant_id == restaurant_id
    ).first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    
    return {
        "success": True,
        "data": {
            "table": {
                "id": str(table.id),
                "table_number": table.table_number,
                "table_name": table.table_name,
                "capacity": table.capacity,
                "location": table.location,
                "qr_code": table.qr_code,
                "qr_code_url": table.qr_code_url,
                "qr_code_image_url": table.qr_code_image_url,
                "is_active": table.is_active,
                "requires_reservation": table.requires_reservation,
                "is_vip": table.is_vip,
                "min_party_size": table.min_party_size,
                "max_party_size": table.max_party_size,
                "current_status": table.current_status,
                "position_x": table.position_x,
                "position_y": table.position_y,
                "shape": table.shape,
                "has_power_outlet": table.has_power_outlet,
                "has_view": table.has_view,
                "is_wheelchair_accessible": table.is_wheelchair_accessible,
                "notes": table.notes,
                "created_at": table.created_at.isoformat() + "Z",
                "updated_at": table.updated_at.isoformat() + "Z"
            }
        }
    }


@router.post("/restaurants/{restaurant_id}/tables", response_model=Dict[str, Any])
async def create_table(
    restaurant_id: UUID,
    table_data: TableCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Create new table (Manager access required)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Check if table number already exists
    existing_table = db.query(RestaurantTable).filter(
        RestaurantTable.restaurant_id == restaurant_id,
        RestaurantTable.table_number == table_data.table_number
    ).first()
    
    if existing_table:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Table number {table_data.table_number} already exists"
        )
    
    # Generate QR code
    qr_code = generate_qr_code(restaurant.restaurant_code, table_data.table_number)
    qr_code_url = f"{settings.QR_CODE_BASE_URL}/table/{qr_code}"
    
    # Create table
    new_table = RestaurantTable(
        restaurant_id=restaurant_id,
        table_number=table_data.table_number,
        table_name=table_data.table_name,
        capacity=table_data.capacity,
        location=table_data.location,
        qr_code=qr_code,
        qr_code_url=qr_code_url,
        requires_reservation=table_data.requires_reservation,
        position_x=table_data.position_x,
        position_y=table_data.position_y
    )
    
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    
    return {
        "success": True,
        "data": {
            "table": {
                "id": str(new_table.id),
                "table_number": new_table.table_number,
                "table_name": new_table.table_name,
                "capacity": new_table.capacity,
                "location": new_table.location,
                "qr_code": new_table.qr_code,
                "qr_code_url": new_table.qr_code_url,
                "is_active": new_table.is_active,
                "created_at": new_table.created_at.isoformat() + "Z"
            }
        },
        "message": "Table created successfully"
    }


@router.put("/restaurants/{restaurant_id}/tables/{table_id}", response_model=SuccessResponse)
async def update_table(
    restaurant_id: UUID,
    table_id: UUID,
    table_data: TableUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Update table (Manager access required)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    table = db.query(RestaurantTable).filter(
        RestaurantTable.id == table_id,
        RestaurantTable.restaurant_id == restaurant_id
    ).first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    
    # Update only provided fields
    update_data = table_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(table, field, value)
    
    table.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(table)
    
    return {
        "success": True,
        "data": {
            "table": {
                "id": str(table.id),
                "table_name": table.table_name,
                "capacity": table.capacity,
                "is_active": table.is_active,
                "updated_at": table.updated_at.isoformat() + "Z"
            }
        },
        "message": "Table updated successfully"
    }


@router.delete("/restaurants/{restaurant_id}/tables/{table_id}", response_model=SuccessResponse)
async def delete_table(
    restaurant_id: UUID,
    table_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Delete table (Manager access required)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    table = db.query(RestaurantTable).filter(
        RestaurantTable.id == table_id,
        RestaurantTable.restaurant_id == restaurant_id
    ).first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found"
        )
    
    # Check if table has active orders
    from app.models.order import Order
    active_orders = db.query(Order).filter(
        Order.table_id == table_id,
        Order.order_status.in_(["pending", "confirmed", "preparing", "ready"])
    ).count()
    
    if active_orders > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete table with active orders"
        )
    
    db.delete(table)
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": f"Table {table.table_number} deleted successfully"
        },
        "message": "Table deleted successfully"
    }


# =================================================================
# PUBLIC QR CODE ACCESS
# =================================================================

@router.get("/public/tables/qr/{qr_code}", response_model=Dict[str, Any])
async def get_table_by_qr_code(
    qr_code: str,
    db: Session = Depends(get_db)
):
    """Get table information by QR code (Public access)."""
    
    table = db.query(RestaurantTable).filter(
        RestaurantTable.qr_code == qr_code,
        RestaurantTable.is_active == True
    ).first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found or inactive"
        )
    
    # Get restaurant info
    restaurant = db.query(Restaurant).filter(Restaurant.id == table.restaurant_id).first()
    
    return {
        "success": True,
        "data": {
            "table": {
                "id": str(table.id),
                "table_number": table.table_number,
                "table_name": table.table_name,
                "capacity": table.capacity,
                "location": table.location,
                "is_available": table.is_available
            },
            "restaurant": {
                "id": str(restaurant.id),
                "name": restaurant.restaurant_name,
                "cuisine_type": "Restaurant",  # Could be added to model
                "phone_number": restaurant.phone_number,
                "currency_code": restaurant.currency_code,
                "theme_color": restaurant.theme_color
            },
            "session_url": "/api/v1/public/guest-sessions"
        }
    }


# =================================================================
# GUEST SESSION MANAGEMENT
# =================================================================

@router.post("/public/guest-sessions", response_model=Dict[str, Any])
async def create_guest_session(
    session_data: GuestSessionCreate,
    db: Session = Depends(get_db)
):
    """Create guest session (Public access)."""
    
    # Verify table exists and is active
    table = db.query(RestaurantTable).filter(
        RestaurantTable.id == session_data.table_id,
        RestaurantTable.is_active == True
    ).first()
    
    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Table not found or inactive"
        )
    
    # Generate session token and expiry
    session_token = generate_session_token()
    expires_at = datetime.utcnow() + timedelta(hours=settings.GUEST_SESSION_EXPIRE_HOURS)
    
    # Create guest session
    new_session = GuestSession(
        restaurant_id=table.restaurant_id,
        table_id=session_data.table_id,
        guest_name=session_data.guest_name,
        guest_phone=session_data.guest_phone,
        guest_email=session_data.guest_email,
        party_size=session_data.party_size,
        special_requests=session_data.special_requests,
        session_token=session_token,
        expires_at=expires_at
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    # Get restaurant info
    restaurant = db.query(Restaurant).filter(Restaurant.id == table.restaurant_id).first()
    
    return {
        "success": True,
        "data": {
            "session": {
                "id": str(new_session.id),
                "session_token": new_session.session_token,
                "table": {
                    "id": str(table.id),
                    "table_number": table.table_number,
                    "table_name": table.table_name,
                    "capacity": table.capacity
                },
                "guest_name": new_session.guest_name,
                "party_size": new_session.party_size,
                "expires_at": new_session.expires_at.isoformat() + "Z",
                "is_active": new_session.is_active
            },
            "restaurant": {
                "id": str(restaurant.id),
                "name": restaurant.restaurant_name,
                "currency_code": restaurant.currency_code
            }
        },
        "message": "Guest session created successfully"
    }


@router.get("/public/guest-sessions/{session_id}", response_model=Dict[str, Any])
async def get_guest_session(
    session_id: UUID,
    session: GuestSession = Depends(verify_guest_session),
    db: Session = Depends(get_db)
):
    """Get guest session details."""
    
    if str(session.id) != str(session_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this session"
        )
    
    # Get related data
    table = db.query(RestaurantTable).filter(RestaurantTable.id == session.table_id).first()
    restaurant = db.query(Restaurant).filter(Restaurant.id == session.restaurant_id).first()
    
    return {
        "success": True,
        "data": {
            "session": {
                "id": str(session.id),
                "table": {
                    "id": str(table.id),
                    "table_number": table.table_number,
                    "table_name": table.table_name
                },
                "restaurant": {
                    "id": str(restaurant.id),
                    "name": restaurant.restaurant_name,
                    "currency_code": restaurant.currency_code
                },
                "guest_name": session.guest_name,
                "party_size": session.party_size,
                "cart_item_count": session.cart_item_count,
                "cart_total": float(session.cart_total),
                "expires_at": session.expires_at.isoformat() + "Z",
                "is_active": session.is_active,
                "is_valid": session.is_valid
            }
        }
    }


@router.put("/public/guest-sessions/{session_id}", response_model=SuccessResponse)
async def update_guest_session(
    session_id: UUID,
    session_data: GuestSessionUpdate,
    session: GuestSession = Depends(verify_guest_session),
    db: Session = Depends(get_db)
):
    """Update guest session."""
    
    if str(session.id) != str(session_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this session"
        )
    
    # Update only provided fields
    update_data = session_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)
    
    session.last_activity_at = datetime.utcnow()
    session.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(session)
    
    return {
        "success": True,
        "data": {
            "session": {
                "id": str(session.id),
                "guest_name": session.guest_name,
                "party_size": session.party_size,
                "cart_item_count": session.cart_item_count,
                "cart_total": float(session.cart_total),
                "updated_at": session.updated_at.isoformat() + "Z"
            }
        },
        "message": "Session updated successfully"
    }


@router.delete("/public/guest-sessions/{session_id}", response_model=SuccessResponse)
async def end_guest_session(
    session_id: UUID,
    session: GuestSession = Depends(verify_guest_session),
    db: Session = Depends(get_db)
):
    """End guest session."""
    
    if str(session.id) != str(session_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this session"
        )
    
    session.is_active = False
    session.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": "Guest session ended successfully"
        },
        "message": "Session ended successfully"
    }