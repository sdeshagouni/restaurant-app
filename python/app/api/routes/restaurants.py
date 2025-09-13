"""
Restaurant management API routes.
Handles restaurant CRUD operations and dashboard analytics.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import Dict, Any, Optional
from datetime import datetime, date, timedelta
from uuid import UUID

from app.core.security import (
    get_current_active_user, get_owner_or_manager_user, get_restaurant_context
)
from app.api.schemas import (
    RestaurantCreate, RestaurantUpdate, RestaurantResponse, 
    DashboardSummary, SuccessResponse
)
from app.models.restaurant import Restaurant, User
from app.models.table import RestaurantTable
from app.models.order import Order
from app.models.payment import PaymentTransaction
from app.core.database import get_db

router = APIRouter()


# =================================================================
# RESTAURANT ENDPOINTS
# =================================================================

@router.get("/{restaurant_id}", response_model=Dict[str, Any])
async def get_restaurant_details(
    restaurant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get restaurant details."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    return {
        "success": True,
        "data": {
            "restaurant": {
                "id": str(restaurant.id),
                "restaurant_name": restaurant.restaurant_name,
                "restaurant_code": restaurant.restaurant_code,
                "business_email": restaurant.business_email,
                "phone_number": restaurant.phone_number,
                "website_url": restaurant.website_url,
                "address": restaurant.address,
                "currency_code": restaurant.currency_code,
                "tax_rate": float(restaurant.tax_rate),
                "service_charge_rate": float(restaurant.service_charge_rate),
                "timezone": restaurant.timezone,
                "operating_hours": restaurant.operating_hours,
                "allows_takeout": restaurant.allows_takeout,
                "allows_delivery": restaurant.allows_delivery,
                "allows_reservations": restaurant.allows_reservations,
                "delivery_radius_km": float(restaurant.delivery_radius_km) if restaurant.delivery_radius_km else None,
                "minimum_delivery_amount": float(restaurant.minimum_delivery_amount) if restaurant.minimum_delivery_amount else None,
                "status": restaurant.status,
                "subscription_tier": restaurant.subscription_tier,
                "subscription_expires_at": restaurant.subscription_expires_at.isoformat() + "Z" if restaurant.subscription_expires_at else None,
                "logo_url": restaurant.logo_url,
                "banner_url": restaurant.banner_url,
                "theme_color": restaurant.theme_color,
                "settings": restaurant.settings,
                "is_active": restaurant.is_active,
                "subscription_active": restaurant.subscription_active,
                "created_at": restaurant.created_at.isoformat() + "Z"
            }
        }
    }


@router.put("/{restaurant_id}", response_model=SuccessResponse)
async def update_restaurant_settings(
    restaurant_id: UUID,
    restaurant_data: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Update restaurant settings (Owner/Manager only)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Update only provided fields
    update_data = restaurant_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(restaurant, field, value)
    
    # Update timestamp
    restaurant.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(restaurant)
    
    return {
        "success": True,
        "data": {
            "restaurant": {
                "id": str(restaurant.id),
                "restaurant_name": restaurant.restaurant_name,
                "phone_number": restaurant.phone_number,
                "tax_rate": float(restaurant.tax_rate),
                "service_charge_rate": float(restaurant.service_charge_rate),
                "updated_at": restaurant.updated_at.isoformat() + "Z"
            }
        },
        "message": "Restaurant settings updated successfully"
    }


@router.get("/{restaurant_id}/dashboard", response_model=Dict[str, Any])
async def get_restaurant_dashboard(
    restaurant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Get restaurant dashboard metrics."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Calculate date ranges
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    # Previous periods for growth calculation
    prev_week_start = week_start - timedelta(days=7)
    prev_month_start = (month_start - timedelta(days=1)).replace(day=1)
    
    # Today's metrics
    today_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        func.date(Order.ordered_at) == today
    )
    
    today_stats = {
        "orders": today_orders.count(),
        "revenue": float(sum([order.total_amount for order in today_orders.all()])),
        "avg_order_value": 0,
        "active_orders": today_orders.filter(
            Order.order_status.in_(["pending", "confirmed", "preparing", "ready"])
        ).count()
    }
    
    if today_stats["orders"] > 0:
        today_stats["avg_order_value"] = round(today_stats["revenue"] / today_stats["orders"], 2)
    
    # Week's metrics
    week_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        func.date(Order.ordered_at) >= week_start
    ).all()
    
    prev_week_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        func.date(Order.ordered_at) >= prev_week_start,
        func.date(Order.ordered_at) < week_start
    ).all()
    
    week_revenue = sum([order.total_amount for order in week_orders])
    prev_week_revenue = sum([order.total_amount for order in prev_week_orders])
    week_growth = 0
    if prev_week_revenue > 0:
        week_growth = round(((week_revenue - prev_week_revenue) / prev_week_revenue) * 100, 1)
    
    week_stats = {
        "orders": len(week_orders),
        "revenue": float(week_revenue),
        "growth_percent": week_growth
    }
    
    # Month's metrics
    month_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        func.date(Order.ordered_at) >= month_start
    ).all()
    
    prev_month_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        func.date(Order.ordered_at) >= prev_month_start,
        func.date(Order.ordered_at) < month_start
    ).all()
    
    month_revenue = sum([order.total_amount for order in month_orders])
    prev_month_revenue = sum([order.total_amount for order in prev_month_orders])
    month_growth = 0
    if prev_month_revenue > 0:
        month_growth = round(((month_revenue - prev_month_revenue) / prev_month_revenue) * 100, 1)
    
    month_stats = {
        "orders": len(month_orders),
        "revenue": float(month_revenue),
        "growth_percent": month_growth
    }
    
    # Operational metrics
    total_tables = db.query(RestaurantTable).filter(RestaurantTable.restaurant_id == restaurant_id).count()
    active_tables_today = db.query(RestaurantTable).filter(
        RestaurantTable.restaurant_id == restaurant_id,
        RestaurantTable.is_active == True
    ).count()
    
    total_staff = db.query(User).filter(User.restaurant_id == restaurant_id, User.is_active == True).count()
    
    # Active payment gateways
    from app.models.payment import PaymentGateway
    active_gateways = db.query(PaymentGateway).filter(
        PaymentGateway.restaurant_id == restaurant_id,
        PaymentGateway.status == "active"
    ).count()
    
    # Active specials
    from app.models.special import DailySpecial
    active_specials = db.query(DailySpecial).filter(
        DailySpecial.restaurant_id == restaurant_id,
        DailySpecial.is_active == True,
        DailySpecial.valid_from <= today,
        DailySpecial.valid_until >= today
    ).count()
    
    operational_stats = {
        "total_tables": total_tables,
        "active_tables_today": active_tables_today,
        "total_staff": total_staff,
        "active_payment_gateways": active_gateways,
        "active_specials": active_specials
    }
    
    # Performance metrics
    completed_orders_today = [order for order in today_orders.all() if order.order_status == "completed"]
    avg_fulfillment_time = 0
    if completed_orders_today:
        fulfillment_times = []
        for order in completed_orders_today:
            if order.completed_at and order.ordered_at:
                fulfillment_time = (order.completed_at - order.ordered_at).total_seconds() / 60
                fulfillment_times.append(fulfillment_time)
        
        if fulfillment_times:
            avg_fulfillment_time = round(sum(fulfillment_times) / len(fulfillment_times), 1)
    
    # Customer satisfaction (mock data - would come from reviews/ratings)
    customer_satisfaction = 4.5  # Would be calculated from actual customer feedback
    
    performance_stats = {
        "avg_fulfillment_time_minutes": avg_fulfillment_time,
        "customer_satisfaction": customer_satisfaction
    }
    
    return {
        "success": True,
        "data": {
            "dashboard": {
                "today": today_stats,
                "week": week_stats,
                "month": month_stats,
                "operational": operational_stats,
                "performance": performance_stats
            }
        }
    }


@router.get("/{restaurant_id}/settings", response_model=Dict[str, Any])
async def get_restaurant_settings(
    restaurant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Get restaurant settings."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    return {
        "success": True,
        "data": {
            "settings": {
                "restaurant_id": str(restaurant.id),
                "timezone": restaurant.timezone,
                "currency_code": restaurant.currency_code,
                "tax_rate": float(restaurant.tax_rate),
                "service_charge_rate": float(restaurant.service_charge_rate),
                "operating_hours": restaurant.operating_hours,
                "allows_takeout": restaurant.allows_takeout,
                "allows_delivery": restaurant.allows_delivery,
                "allows_reservations": restaurant.allows_reservations,
                "delivery_radius_km": float(restaurant.delivery_radius_km) if restaurant.delivery_radius_km else None,
                "minimum_delivery_amount": float(restaurant.minimum_delivery_amount) if restaurant.minimum_delivery_amount else None,
                "theme_color": restaurant.theme_color,
                "settings": restaurant.settings
            }
        }
    }


@router.put("/{restaurant_id}/settings", response_model=SuccessResponse)
async def update_restaurant_settings_detailed(
    restaurant_id: UUID,
    settings_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_owner_or_manager_user)
):
    """Update detailed restaurant settings (Owner/Manager only)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Update settings
    allowed_settings = [
        'timezone', 'currency_code', 'tax_rate', 'service_charge_rate',
        'operating_hours', 'allows_takeout', 'allows_delivery', 'allows_reservations',
        'delivery_radius_km', 'minimum_delivery_amount', 'theme_color'
    ]
    
    for key, value in settings_data.items():
        if key in allowed_settings and hasattr(restaurant, key):
            setattr(restaurant, key, value)
        elif key == 'notification_settings':
            # Update nested settings
            if not restaurant.settings:
                restaurant.settings = {}
            restaurant.settings['notification_settings'] = value
    
    restaurant.updated_at = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": "Restaurant settings updated successfully",
            "updated_at": restaurant.updated_at.isoformat() + "Z"
        },
        "message": "Settings updated successfully"
    }