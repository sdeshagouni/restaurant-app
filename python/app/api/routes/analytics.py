"""
Analytics and reporting API routes.
Handles sales analytics, menu performance, and business metrics.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import Dict, Any, Optional, List
from datetime import datetime, date, timedelta
from uuid import UUID

from app.core.security import get_owner_or_manager_user, get_restaurant_context
from app.models.order import Order, OrderItem
from app.models.menu import MenuItem, MenuCategory
from app.models.table import RestaurantTable
from app.models.base import OrderStatus
from app.core.database import get_db

router = APIRouter()


@router.get("/{restaurant_id}/analytics/sales", response_model=Dict[str, Any])
async def get_sales_analytics(
    restaurant_id: UUID,
    period: str = Query("month", regex="^(today|week|month|quarter|year|custom)$"),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    group_by: str = Query("day", regex="^(day|week|month|hour)$"),
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Get sales analytics (Manager/Owner)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Calculate date range
    today = date.today()
    if period == "today":
        date_from = date_to = today
    elif period == "week":
        date_from = today - timedelta(days=today.weekday())
        date_to = today
    elif period == "month":
        date_from = today.replace(day=1)
        date_to = today
    elif period == "quarter":
        quarter_start_month = ((today.month - 1) // 3) * 3 + 1
        date_from = today.replace(month=quarter_start_month, day=1)
        date_to = today
    elif period == "year":
        date_from = today.replace(month=1, day=1)
        date_to = today
    
    if not date_from or not date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date range required for custom period"
        )
    
    # Calculate previous period for growth comparison
    period_days = (date_to - date_from).days + 1
    prev_date_from = date_from - timedelta(days=period_days)
    prev_date_to = date_from - timedelta(days=1)
    
    # Current period orders
    current_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        func.date(Order.ordered_at) >= date_from,
        func.date(Order.ordered_at) <= date_to,
        Order.order_status == OrderStatus.COMPLETED
    ).all()
    
    # Previous period orders
    prev_orders = db.query(Order).filter(
        Order.restaurant_id == restaurant_id,
        func.date(Order.ordered_at) >= prev_date_from,
        func.date(Order.ordered_at) <= prev_date_to,
        Order.order_status == OrderStatus.COMPLETED
    ).all()
    
    # Calculate metrics
    total_revenue = sum([order.total_amount for order in current_orders])
    total_orders = len(current_orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    prev_revenue = sum([order.total_amount for order in prev_orders])
    growth_percent = 0
    if prev_revenue > 0:
        growth_percent = ((total_revenue - prev_revenue) / prev_revenue) * 100
    
    # Order type breakdown
    dine_in_orders = [order for order in current_orders if order.order_type == "dine_in"]
    takeout_orders = [order for order in current_orders if order.order_type == "takeout"]
    
    # Payment method breakdown (mock data - would come from payment transactions)
    card_orders = int(total_orders * 0.7)  # Assume 70% card payments
    cash_orders = total_orders - card_orders
    
    # Daily breakdown
    breakdown = []
    current_date = date_from
    while current_date <= date_to:
        day_orders = [order for order in current_orders 
                     if order.ordered_at.date() == current_date]
        day_revenue = sum([order.total_amount for order in day_orders])
        day_avg = day_revenue / len(day_orders) if day_orders else 0
        
        breakdown.append({
            "period": current_date.isoformat(),
            "revenue": float(day_revenue),
            "orders": len(day_orders),
            "avg_order_value": round(float(day_avg), 2)
        })
        
        current_date += timedelta(days=1)
    
    return {
        "success": True,
        "data": {
            "summary": {
                "total_revenue": float(total_revenue),
                "total_orders": total_orders,
                "avg_order_value": round(float(avg_order_value), 2),
                "growth_percent": round(growth_percent, 1),
                "previous_period_revenue": float(prev_revenue)
            },
            "breakdown": breakdown,
            "order_types": {
                "dine_in": {
                    "orders": len(dine_in_orders),
                    "revenue": float(sum([order.total_amount for order in dine_in_orders]))
                },
                "takeout": {
                    "orders": len(takeout_orders),
                    "revenue": float(sum([order.total_amount for order in takeout_orders]))
                }
            },
            "payment_methods": {
                "card": {
                    "orders": card_orders,
                    "revenue": float(total_revenue * 0.7)
                },
                "cash": {
                    "orders": cash_orders,
                    "revenue": float(total_revenue * 0.3)
                }
            }
        }
    }


@router.get("/{restaurant_id}/analytics/menu", response_model=Dict[str, Any])
async def get_menu_analytics(
    restaurant_id: UUID,
    period: str = Query("month", regex="^(week|month|quarter)$"),
    category_id: Optional[UUID] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    sort_by: str = Query("popularity", regex="^(popularity|revenue|profit_margin)$"),
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Get menu performance analytics (Manager/Owner)."""
    
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Calculate date range
    today = date.today()
    if period == "week":
        date_from = today - timedelta(days=today.weekday())
    elif period == "month":
        date_from = today.replace(day=1)
    elif period == "quarter":
        quarter_start_month = ((today.month - 1) // 3) * 3 + 1
        date_from = today.replace(month=quarter_start_month, day=1)
    
    # Get order items for the period
    query = db.query(OrderItem).join(Order).filter(
        Order.restaurant_id == restaurant_id,
        func.date(Order.ordered_at) >= date_from,
        func.date(Order.ordered_at) <= today,
        Order.order_status == OrderStatus.COMPLETED
    )
    
    if category_id:
        query = query.join(MenuItem).filter(MenuItem.category_id == category_id)
    
    order_items = query.all()
    
    # Group by menu item
    item_stats = {}
    for item in order_items:
        item_id = str(item.menu_item_id)
        if item_id not in item_stats:
            item_stats[item_id] = {
                "item_id": item_id,
                "item_name": item.item_name,
                "category_name": "",
                "times_ordered": 0,
                "total_quantity": 0,
                "total_revenue": 0,
                "avg_selling_price": 0,
                "profit_margin": 0,
                "profit_margin_percent": 0
            }
        
        item_stats[item_id]["times_ordered"] += 1
        item_stats[item_id]["total_quantity"] += item.quantity
        item_stats[item_id]["total_revenue"] += float(item.total_price)
    
    # Get menu item details and calculate metrics
    top_items = []
    for item_id, stats in item_stats.items():
        menu_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if menu_item:
            stats["avg_selling_price"] = round(stats["total_revenue"] / stats["total_quantity"], 2)
            
            if menu_item.cost_price:
                profit_per_item = float(menu_item.price - menu_item.cost_price)
                stats["profit_margin"] = profit_per_item * stats["total_quantity"]
                stats["profit_margin_percent"] = round((profit_per_item / float(menu_item.price)) * 100, 1)
            
            # Get category name
            category = db.query(MenuCategory).filter(MenuCategory.id == menu_item.category_id).first()
            if category:
                stats["category_name"] = category.category_name
            
            top_items.append(stats)
    
    # Sort and limit results
    if sort_by == "popularity":
        top_items.sort(key=lambda x: x["times_ordered"], reverse=True)
    elif sort_by == "revenue":
        top_items.sort(key=lambda x: x["total_revenue"], reverse=True)
    elif sort_by == "profit_margin":
        top_items.sort(key=lambda x: x["profit_margin"], reverse=True)
    
    top_items = top_items[:limit]
    
    # Add ranking
    for i, item in enumerate(top_items):
        item["popularity_rank"] = i + 1
        item["revenue_rank"] = i + 1  # Simplified
    
    # Category performance
    category_stats = {}
    for item in order_items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        if menu_item and menu_item.category_id:
            cat_id = str(menu_item.category_id)
            if cat_id not in category_stats:
                category = db.query(MenuCategory).filter(MenuCategory.id == menu_item.category_id).first()
                category_stats[cat_id] = {
                    "category_id": cat_id,
                    "category_name": category.category_name if category else "Unknown",
                    "total_revenue": 0,
                    "order_count": 0,
                    "item_count": 0
                }
            
            category_stats[cat_id]["total_revenue"] += float(item.total_price)
            category_stats[cat_id]["order_count"] += 1
    
    categories = list(category_stats.values())
    for cat in categories:
        cat["avg_order_value"] = round(cat["total_revenue"] / cat["order_count"], 2) if cat["order_count"] > 0 else 0
        # Count unique items in category
        cat["item_count"] = db.query(MenuItem).filter(
            MenuItem.category_id == cat["category_id"],
            MenuItem.restaurant_id == restaurant_id
        ).count()
    
    return {
        "success": True,
        "data": {
            "top_items": top_items,
            "categories": categories
        }
    }