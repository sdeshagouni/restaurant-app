"""
Menu management API routes.
Handles menu categories, items, and options.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from uuid import UUID
from decimal import Decimal

from app.core.security import get_staff_user, get_owner_or_manager_user, get_restaurant_context
from app.models.menu import MenuCategory, MenuItem, MenuItemOption
from app.core.database import get_db

router = APIRouter()


@router.get("/{restaurant_id}/menu/categories", response_model=Dict[str, Any])
async def list_menu_categories(
    restaurant_id: UUID,
    active_only: bool = Query(True),
    include_items: bool = Query(False),
    db: Session = Depends(get_db)
):
    """List menu categories (Public & Staff)."""
    
    query = db.query(MenuCategory).filter(MenuCategory.restaurant_id == restaurant_id)
    
    if active_only:
        query = query.filter(MenuCategory.is_active == True)
    
    categories = query.order_by(MenuCategory.display_order).all()
    
    category_data = []
    for category in categories:
        category_info = {
            "id": str(category.id),
            "category_name": category.category_name,
            "description": category.description,
            "image_url": category.image_url,
            "display_order": category.display_order,
            "is_active": category.is_active,
            "available_all_day": category.available_all_day,
            "available_from": category.available_from.isoformat() if category.available_from else None,
            "available_until": category.available_until.isoformat() if category.available_until else None,
            "created_at": category.created_at.isoformat() + "Z"
        }
        
        if include_items:
            items = db.query(MenuItem).filter(
                MenuItem.category_id == category.id,
                MenuItem.is_available == True if active_only else True
            ).all()
            category_info["items"] = len(items)
        
        category_data.append(category_info)
    
    return {
        "success": True,
        "data": {
            "categories": category_data
        }
    }


@router.get("/{restaurant_id}/menu/items", response_model=Dict[str, Any])
async def list_menu_items(
    restaurant_id: UUID,
    category_id: Optional[UUID] = Query(None),
    available_only: bool = Query(True),
    featured_only: bool = Query(False),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List menu items (Public & Staff)."""
    
    query = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)
    
    if category_id:
        query = query.filter(MenuItem.category_id == category_id)
    
    if available_only:
        query = query.filter(MenuItem.is_available == True)
    
    if featured_only:
        query = query.filter(MenuItem.is_featured == True)
    
    if search:
        query = query.filter(
            MenuItem.item_name.ilike(f"%{search}%") |
            MenuItem.description.ilike(f"%{search}%")
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    items = query.order_by(MenuItem.display_order, MenuItem.item_name).offset(offset).limit(size).all()
    
    # Prepare response
    item_data = []
    for item in items:
        # Get category info
        category = db.query(MenuCategory).filter(MenuCategory.id == item.category_id).first()
        
        # Get options
        options = db.query(MenuItemOption).filter(
            MenuItemOption.item_id == item.id,
            MenuItemOption.is_active == True
        ).order_by(MenuItemOption.display_order).all()
        
        item_info = {
            "id": str(item.id),
            "item_name": item.item_name,
            "description": item.description,
            "price": float(item.price),
            "cost_price": float(item.cost_price) if item.cost_price else None,
            "category": {
                "id": str(category.id),
                "name": category.category_name
            } if category else None,
            "is_vegetarian": item.is_vegetarian,
            "is_vegan": item.is_vegan,
            "is_gluten_free": item.is_gluten_free,
            "is_spicy": item.is_spicy,
            "spice_level": item.spice_level,
            "calories": item.calories,
            "is_available": item.is_available,
            "prep_time_minutes": item.prep_time_minutes,
            "image_url": item.image_url,
            "is_featured": item.is_featured,
            "is_popular": item.is_popular,
            "display_order": item.display_order,
            "options": [
                {
                    "id": str(option.id),
                    "option_group": option.option_group,
                    "option_name": option.option_name,
                    "price_change": float(option.price_change),
                    "is_default": option.is_default,
                    "display_order": option.display_order
                }
                for option in options
            ],
            "profit_margin": float(item.profit_margin) if item.profit_margin else None,
            "profit_margin_percent": item.profit_margin_percent,
            "created_at": item.created_at.isoformat() + "Z"
        }
        
        item_data.append(item_info)
    
    pages = (total + size - 1) // size
    
    return {
        "success": True,
        "data": {
            "items": item_data,
            "pagination": {
                "total": total,
                "page": page,
                "size": size,
                "pages": pages
            }
        }
    }


@router.get("/{restaurant_id}/menu/search", response_model=Dict[str, Any])
async def search_menu_items(
    restaurant_id: UUID,
    q: str = Query(..., min_length=2),
    category: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Search menu items (Public)."""
    
    query = db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id,
        MenuItem.is_available == True
    )
    
    # Search in name and description
    query = query.filter(
        MenuItem.item_name.ilike(f"%{q}%") |
        MenuItem.description.ilike(f"%{q}%")
    )
    
    if category:
        cat = db.query(MenuCategory).filter(
            MenuCategory.restaurant_id == restaurant_id,
            MenuCategory.category_name.ilike(f"%{category}%")
        ).first()
        if cat:
            query = query.filter(MenuItem.category_id == cat.id)
    
    items = query.order_by(MenuItem.is_featured.desc(), MenuItem.item_name).limit(limit).all()
    
    # Prepare response
    search_results = []
    for item in items:
        category = db.query(MenuCategory).filter(MenuCategory.id == item.category_id).first()
        
        search_results.append({
            "id": str(item.id),
            "item_name": item.item_name,
            "description": item.description,
            "price": float(item.price),
            "category": category.category_name if category else None,
            "is_vegetarian": item.is_vegetarian,
            "is_vegan": item.is_vegan,
            "is_gluten_free": item.is_gluten_free,
            "is_spicy": item.is_spicy,
            "image_url": item.image_url,
            "is_featured": item.is_featured
        })
    
    return {
        "success": True,
        "data": {
            "results": search_results,
            "query": q,
            "total_results": len(search_results)
        }
    }