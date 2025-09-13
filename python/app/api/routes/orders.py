"""
Order management API routes.
Handles order creation, processing, and status updates.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from app.core.security import (
    get_staff_user, verify_guest_session, get_restaurant_context
)
from app.models.order import Order, OrderItem
from app.models.table import GuestSession
from app.models.menu import MenuItem
from app.models.base import OrderStatus, OrderType
from app.core.database import get_db

router = APIRouter()


@router.post("/public/orders", response_model=Dict[str, Any])
async def create_order_guest(
    order_data: Dict[str, Any],
    session: GuestSession = Depends(verify_guest_session),
    db: Session = Depends(get_db)
):
    """Create order (Guest)."""
    
    # Generate order number
    order_count = db.query(Order).filter(Order.restaurant_id == session.restaurant_id).count()
    order_number = f"ORD-{session.table.table_number}-{order_count + 1:03d}"
    
    # Create order
    new_order = Order(
        restaurant_id=session.restaurant_id,
        table_id=session.table_id,
        guest_session_id=session.id,
        order_number=order_number,
        order_type=OrderType.DINE_IN,
        guest_name=session.guest_name,
        guest_phone=session.guest_phone,
        guest_email=session.guest_email,
        party_size=session.party_size,
        special_instructions=order_data.get("special_instructions"),
        total_amount=Decimal("0")  # Will be calculated
    )
    
    db.add(new_order)
    db.flush()  # Get the order ID
    
    # Add order items
    subtotal = Decimal("0")
    for item_data in order_data.get("items", []):
        menu_item = db.query(MenuItem).filter(MenuItem.id == item_data["menu_item_id"]).first()
        if not menu_item:
            continue
            
        quantity = item_data["quantity"]
        unit_price = menu_item.price
        total_price = unit_price * quantity
        
        order_item = OrderItem(
            restaurant_id=session.restaurant_id,
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            item_name=menu_item.item_name,
            item_description=menu_item.description,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price,
            special_instructions=item_data.get("special_instructions"),
            prep_time_minutes=menu_item.prep_time_minutes
        )
        
        db.add(order_item)
        subtotal += total_price
    
    # Calculate totals
    from app.models.restaurant import Restaurant
    restaurant = db.query(Restaurant).filter(Restaurant.id == session.restaurant_id).first()
    
    tax_amount = subtotal * restaurant.tax_rate
    service_charge = subtotal * restaurant.service_charge_rate
    total_amount = subtotal + tax_amount + service_charge
    
    # Update order totals
    new_order.subtotal = subtotal
    new_order.tax_amount = tax_amount
    new_order.service_charge = service_charge
    new_order.total_amount = total_amount
    
    db.commit()
    db.refresh(new_order)
    
    # Get order items for response
    order_items = db.query(OrderItem).filter(OrderItem.order_id == new_order.id).all()
    
    return {
        "success": True,
        "data": {
            "order": {
                "id": str(new_order.id),
                "order_number": new_order.order_number,
                "order_type": new_order.order_type,
                "order_status": new_order.order_status,
                "payment_status": new_order.payment_status,
                "table": {
                    "id": str(session.table.id),
                    "table_number": session.table.table_number
                },
                "guest_name": new_order.guest_name,
                "party_size": new_order.party_size,
                "items": [
                    {
                        "id": str(item.id),
                        "item_name": item.item_name,
                        "quantity": item.quantity,
                        "unit_price": float(item.unit_price),
                        "total_price": float(item.total_price),
                        "special_instructions": item.special_instructions
                    }
                    for item in order_items
                ],
                "subtotal": float(new_order.subtotal),
                "tax_amount": float(new_order.tax_amount),
                "service_charge": float(new_order.service_charge),
                "total_amount": float(new_order.total_amount),
                "estimated_prep_time": 20,  # Calculate based on items
                "ordered_at": new_order.ordered_at.isoformat() + "Z"
            }
        },
        "message": "Order created successfully"
    }


@router.get("/orders/{order_id}", response_model=Dict[str, Any])
async def get_order_details(
    order_id: UUID,
    db: Session = Depends(get_db)
):
    """Get order details."""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Get order items
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    return {
        "success": True,
        "data": {
            "order": {
                "id": str(order.id),
                "order_number": order.order_number,
                "order_type": order.order_type,
                "order_status": order.order_status,
                "payment_status": order.payment_status,
                "guest_name": order.guest_name,
                "party_size": order.party_size,
                "items": [
                    {
                        "id": str(item.id),
                        "item_name": item.item_name,
                        "quantity": item.quantity,
                        "unit_price": float(item.unit_price),
                        "total_price": float(item.total_price),
                        "item_status": item.item_status,
                        "special_instructions": item.special_instructions
                    }
                    for item in order_items
                ],
                "subtotal": float(order.subtotal),
                "tax_amount": float(order.tax_amount),
                "service_charge": float(order.service_charge),
                "discount_amount": float(order.discount_amount),
                "total_amount": float(order.total_amount),
                "ordered_at": order.ordered_at.isoformat() + "Z",
                "estimated_ready_time": order.estimated_ready_time.isoformat() + "Z" if order.estimated_ready_time else None
            }
        }
    }


@router.get("/restaurants/{restaurant_id}/orders", response_model=Dict[str, Any])
async def list_restaurant_orders(
    restaurant_id: UUID,
    status_filter: Optional[List[str]] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_staff_user)
):
    """List orders for restaurant (Staff)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    query = db.query(Order).filter(Order.restaurant_id == restaurant_id)
    
    if status_filter:
        query = query.filter(Order.order_status.in_(status_filter))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    orders = query.order_by(Order.ordered_at.desc()).offset(offset).limit(size).all()
    
    # Prepare response
    order_data = []
    for order in orders:
        # Get item count
        item_count = db.query(OrderItem).filter(OrderItem.order_id == order.id).count()
        
        # Get table info
        table_info = None
        if order.table_id:
            from app.models.table import RestaurantTable
            table = db.query(RestaurantTable).filter(RestaurantTable.id == order.table_id).first()
            if table:
                table_info = {
                    "table_number": table.table_number,
                    "location": table.location
                }
        
        order_data.append({
            "id": str(order.id),
            "order_number": order.order_number,
            "order_status": order.order_status,
            "payment_status": order.payment_status,
            "table": table_info,
            "guest_name": order.guest_name,
            "total_amount": float(order.total_amount),
            "item_count": item_count,
            "ordered_at": order.ordered_at.isoformat() + "Z",
            "estimated_ready_time": order.estimated_ready_time.isoformat() + "Z" if order.estimated_ready_time else None
        })
    
    pages = (total + size - 1) // size
    
    # Summary stats
    pending_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        Order.order_status == OrderStatus.PENDING
    ).count()
    
    preparing_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        Order.order_status == OrderStatus.PREPARING
    ).count()
    
    ready_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        Order.order_status == OrderStatus.READY
    ).count()
    
    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.restaurant_id == restaurant_id,
        Order.order_status == OrderStatus.COMPLETED
    ).scalar() or 0
    
    return {
        "success": True,
        "data": {
            "orders": order_data,
            "pagination": {
                "total": total,
                "page": page,
                "size": size,
                "pages": pages
            },
            "summary": {
                "total_orders": total,
                "pending_orders": pending_orders,
                "preparing_orders": preparing_orders,
                "ready_orders": ready_orders,
                "total_revenue": float(total_revenue)
            }
        }
    }


@router.patch("/orders/{order_id}/status", response_model=Dict[str, Any])
async def update_order_status(
    order_id: UUID,
    status_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user = Depends(get_staff_user)
):
    """Update order status (Staff)."""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Verify staff has access to this restaurant
    get_restaurant_context(order.restaurant_id, current_user)
    
    # Update status
    new_status = status_data.get("status")
    if new_status:
        order.order_status = OrderStatus(new_status)
        
        # Update timestamps based on status
        now = datetime.utcnow()
        if new_status == OrderStatus.CONFIRMED:
            order.confirmed_at = now
        elif new_status == OrderStatus.PREPARING:
            order.preparation_started_at = now
        elif new_status == OrderStatus.READY:
            order.ready_at = now
        elif new_status == OrderStatus.COMPLETED:
            order.completed_at = now
    
    if status_data.get("estimated_ready_time"):
        order.estimated_ready_time = datetime.fromisoformat(status_data["estimated_ready_time"].replace("Z", ""))
    
    if status_data.get("notes"):
        order.internal_notes = status_data["notes"]
    
    order.updated_at = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "data": {
            "order": {
                "id": str(order.id),
                "order_number": order.order_number,
                "order_status": order.order_status,
                "estimated_ready_time": order.estimated_ready_time.isoformat() + "Z" if order.estimated_ready_time else None,
                "updated_at": order.updated_at.isoformat() + "Z"
            }
        },
        "message": "Order status updated successfully"
    }


# Import required for annotations
from sqlalchemy import func