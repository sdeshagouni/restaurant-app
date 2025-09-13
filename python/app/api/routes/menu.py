"""
Menu management API routes.
Handles menu categories, items, and options with full CRUD operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import time

from app.core.security import get_staff_user, get_owner_or_manager_user, get_restaurant_context
from app.models.menu import MenuCategory, MenuItem, MenuItemOption
from app.api.schemas import MenuCategoryCreate, MenuItemCreate, MenuItemOptionCreate, MenuCategoryUpdate, MenuItemUpdate, MenuItemOptionUpdate
from app.core.database import get_db

router = APIRouter()


# =================================================================
# PUBLIC READ-ONLY ENDPOINTS (Guests & Staff)
# =================================================================

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


# =================================================================
# MENU CATEGORY MANAGEMENT (Owner/Manager Only)
# =================================================================

@router.post("/{restaurant_id}/menu/categories", response_model=Dict[str, Any])
async def create_menu_category(
    restaurant_id: UUID,
    category_data: MenuCategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Create new menu category (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Check if category name already exists
    existing = db.query(MenuCategory).filter(
        MenuCategory.restaurant_id == restaurant_id,
        MenuCategory.category_name == category_data.category_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    
    # Create new category
    new_category = MenuCategory(
        restaurant_id=restaurant_id,
        category_name=category_data.category_name,
        description=category_data.description,
        image_url=category_data.image_url,
        display_order=category_data.display_order,
        is_active=category_data.is_active,
        available_all_day=category_data.available_all_day,
        available_from=category_data.available_from,
        available_until=category_data.available_until
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return {
        "success": True,
        "data": {
            "category": {
                "id": str(new_category.id),
                "category_name": new_category.category_name,
                "description": new_category.description,
                "image_url": new_category.image_url,
                "display_order": new_category.display_order,
                "is_active": new_category.is_active,
                "available_all_day": new_category.available_all_day,
                "created_at": new_category.created_at.isoformat() + "Z"
            }
        },
        "message": "Menu category created successfully"
    }


@router.put("/{restaurant_id}/menu/categories/{category_id}", response_model=Dict[str, Any])
async def update_menu_category(
    restaurant_id: UUID,
    category_id: UUID,
    category_data: MenuCategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Update menu category (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find category
    category = db.query(MenuCategory).filter(
        MenuCategory.id == category_id,
        MenuCategory.restaurant_id == restaurant_id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if new name already exists (if provided)
    if category_data.category_name and category_data.category_name != category.category_name:
        existing = db.query(MenuCategory).filter(
            MenuCategory.restaurant_id == restaurant_id,
            MenuCategory.category_name == category_data.category_name,
            MenuCategory.id != category_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )
    
    # Update fields
    update_data = category_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    from datetime import datetime
    category.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(category)
    
    return {
        "success": True,
        "data": {
            "category": {
                "id": str(category.id),
                "category_name": category.category_name,
                "description": category.description,
                "is_active": category.is_active,
                "updated_at": category.updated_at.isoformat() + "Z"
            }
        },
        "message": "Menu category updated successfully"
    }


@router.delete("/{restaurant_id}/menu/categories/{category_id}", response_model=Dict[str, Any])
async def delete_menu_category(
    restaurant_id: UUID,
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Delete menu category (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find category
    category = db.query(MenuCategory).filter(
        MenuCategory.id == category_id,
        MenuCategory.restaurant_id == restaurant_id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if category has items
    items_count = db.query(MenuItem).filter(MenuItem.category_id == category_id).count()
    if items_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {items_count} items. Move or delete items first."
        )
    
    db.delete(category)
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": f"Category '{category.category_name}' deleted successfully"
        },
        "message": "Menu category deleted successfully"
    }


# =================================================================
# MENU ITEM MANAGEMENT (Owner/Manager Only)
# =================================================================

@router.post("/{restaurant_id}/menu/items", response_model=Dict[str, Any])
async def create_menu_item(
    restaurant_id: UUID,
    item_data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Create new menu item (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Verify category exists (if provided)
    if item_data.category_id:
        category = db.query(MenuCategory).filter(
            MenuCategory.id == item_data.category_id,
            MenuCategory.restaurant_id == restaurant_id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # Check if item name already exists in restaurant
    existing = db.query(MenuItem).filter(
        MenuItem.restaurant_id == restaurant_id,
        MenuItem.item_name == item_data.item_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item name already exists"
        )
    
    # Calculate profit margin if cost_price provided
    profit_margin = None
    profit_margin_percent = None
    if item_data.cost_price and item_data.cost_price > 0:
        profit_margin = item_data.price - item_data.cost_price
        profit_margin_percent = float((profit_margin / item_data.price) * 100)
    
    # Create new item
    new_item = MenuItem(
        restaurant_id=restaurant_id,
        category_id=item_data.category_id,
        item_name=item_data.item_name,
        description=item_data.description,
        price=item_data.price,
        cost_price=item_data.cost_price,
        prep_time_minutes=item_data.prep_time_minutes,
        is_vegetarian=item_data.is_vegetarian,
        is_vegan=item_data.is_vegan,
        is_gluten_free=item_data.is_gluten_free,
        is_spicy=item_data.is_spicy,
        spice_level=item_data.spice_level,
        calories=item_data.calories,
        is_available=item_data.is_available,
        image_url=item_data.image_url,
        is_featured=item_data.is_featured,
        is_popular=item_data.is_popular,
        display_order=item_data.display_order,
        profit_margin=profit_margin,
        profit_margin_percent=profit_margin_percent
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {
        "success": True,
        "data": {
            "item": {
                "id": str(new_item.id),
                "item_name": new_item.item_name,
                "description": new_item.description,
                "price": float(new_item.price),
                "cost_price": float(new_item.cost_price) if new_item.cost_price else None,
                "category_id": str(new_item.category_id) if new_item.category_id else None,
                "is_available": new_item.is_available,
                "profit_margin": float(new_item.profit_margin) if new_item.profit_margin else None,
                "profit_margin_percent": new_item.profit_margin_percent,
                "created_at": new_item.created_at.isoformat() + "Z"
            }
        },
        "message": "Menu item created successfully"
    }


@router.put("/{restaurant_id}/menu/items/{item_id}", response_model=Dict[str, Any])
async def update_menu_item(
    restaurant_id: UUID,
    item_id: UUID,
    item_data: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Update menu item (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find item
    item = db.query(MenuItem).filter(
        MenuItem.id == item_id,
        MenuItem.restaurant_id == restaurant_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    # Verify category exists (if provided)
    if item_data.category_id:
        category = db.query(MenuCategory).filter(
            MenuCategory.id == item_data.category_id,
            MenuCategory.restaurant_id == restaurant_id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    # Check if new name already exists (if provided)
    if item_data.item_name and item_data.item_name != item.item_name:
        existing = db.query(MenuItem).filter(
            MenuItem.restaurant_id == restaurant_id,
            MenuItem.item_name == item_data.item_name,
            MenuItem.id != item_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item name already exists"
            )
    
    # Update fields
    update_data = item_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    # Recalculate profit margin if price or cost_price changed
    if item_data.price or item_data.cost_price:
        if item.cost_price and item.cost_price > 0:
            item.profit_margin = item.price - item.cost_price
            item.profit_margin_percent = float((item.profit_margin / item.price) * 100)
        else:
            item.profit_margin = None
            item.profit_margin_percent = None
    
    from datetime import datetime
    item.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(item)
    
    return {
        "success": True,
        "data": {
            "item": {
                "id": str(item.id),
                "item_name": item.item_name,
                "price": float(item.price),
                "cost_price": float(item.cost_price) if item.cost_price else None,
                "is_available": item.is_available,
                "profit_margin": float(item.profit_margin) if item.profit_margin else None,
                "updated_at": item.updated_at.isoformat() + "Z"
            }
        },
        "message": "Menu item updated successfully"
    }


@router.delete("/{restaurant_id}/menu/items/{item_id}", response_model=Dict[str, Any])
async def delete_menu_item(
    restaurant_id: UUID,
    item_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Delete menu item (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find item
    item = db.query(MenuItem).filter(
        MenuItem.id == item_id,
        MenuItem.restaurant_id == restaurant_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    # Delete all options first
    db.query(MenuItemOption).filter(MenuItemOption.item_id == item_id).delete()
    
    db.delete(item)
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": f"Item '{item.item_name}' and all its options deleted successfully"
        },
        "message": "Menu item deleted successfully"
    }


# =================================================================
# MENU ITEM OPTION MANAGEMENT (Owner/Manager Only)
# =================================================================

@router.post("/{restaurant_id}/menu/items/{item_id}/options", response_model=Dict[str, Any])
async def create_menu_item_option(
    restaurant_id: UUID,
    item_id: UUID,
    option_data: MenuItemOptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Create menu item option (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Verify item exists
    item = db.query(MenuItem).filter(
        MenuItem.id == item_id,
        MenuItem.restaurant_id == restaurant_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    # Check if option already exists
    existing = db.query(MenuItemOption).filter(
        MenuItemOption.item_id == item_id,
        MenuItemOption.option_group == option_data.option_group,
        MenuItemOption.option_name == option_data.option_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Option already exists for this item"
        )
    
    # Create option
    new_option = MenuItemOption(
        restaurant_id=restaurant_id,
        item_id=item_id,
        option_group=option_data.option_group,
        option_name=option_data.option_name,
        price_change=option_data.price_change,
        is_default=option_data.is_default,
        is_active=option_data.is_active,
        display_order=option_data.display_order
    )
    
    db.add(new_option)
    db.commit()
    db.refresh(new_option)
    
    return {
        "success": True,
        "data": {
            "option": {
                "id": str(new_option.id),
                "option_group": new_option.option_group,
                "option_name": new_option.option_name,
                "price_change": float(new_option.price_change),
                "is_default": new_option.is_default,
                "is_active": new_option.is_active,
                "created_at": new_option.created_at.isoformat() + "Z"
            }
        },
        "message": "Menu item option created successfully"
    }


@router.put("/{restaurant_id}/menu/items/{item_id}/options/{option_id}", response_model=Dict[str, Any])
async def update_menu_item_option(
    restaurant_id: UUID,
    item_id: UUID,
    option_id: UUID,
    option_data: MenuItemOptionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Update menu item option (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find option
    option = db.query(MenuItemOption).filter(
        MenuItemOption.id == option_id,
        MenuItemOption.item_id == item_id,
        MenuItemOption.restaurant_id == restaurant_id
    ).first()
    
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item option not found"
        )
    
    # Update fields
    update_data = option_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(option, field, value)
    
    db.commit()
    db.refresh(option)
    
    return {
        "success": True,
        "data": {
            "option": {
                "id": str(option.id),
                "option_group": option.option_group,
                "option_name": option.option_name,
                "price_change": float(option.price_change),
                "is_default": option.is_default,
                "is_active": option.is_active
            }
        },
        "message": "Menu item option updated successfully"
    }


@router.delete("/{restaurant_id}/menu/items/{item_id}/options/{option_id}", response_model=Dict[str, Any])
async def delete_menu_item_option(
    restaurant_id: UUID,
    item_id: UUID,
    option_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Delete menu item option (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    # Find option
    option = db.query(MenuItemOption).filter(
        MenuItemOption.id == option_id,
        MenuItemOption.item_id == item_id,
        MenuItemOption.restaurant_id == restaurant_id
    ).first()
    
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item option not found"
        )
    
    db.delete(option)
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": f"Option '{option.option_name}' deleted successfully"
        },
        "message": "Menu item option deleted successfully"
    }


# =================================================================
# BULK OPERATIONS (Owner/Manager Only)
# =================================================================

@router.patch("/{restaurant_id}/menu/items/bulk-price-update", response_model=Dict[str, Any])
async def bulk_price_update(
    restaurant_id: UUID,
    price_updates: List[Dict[str, Any]],
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Bulk update menu item prices (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    updated_items = []
    errors = []
    
    for update in price_updates:
        try:
            item_id = UUID(update["item_id"])
            new_price = Decimal(str(update["price"]))
            
            item = db.query(MenuItem).filter(
                MenuItem.id == item_id,
                MenuItem.restaurant_id == restaurant_id
            ).first()
            
            if item:
                item.price = new_price
                # Recalculate profit margin
                if item.cost_price and item.cost_price > 0:
                    item.profit_margin = item.price - item.cost_price
                    item.profit_margin_percent = float((item.profit_margin / item.price) * 100)
                
                updated_items.append({
                    "item_id": str(item.id),
                    "item_name": item.item_name,
                    "old_price": float(update.get("old_price", 0)),
                    "new_price": float(item.price)
                })
            else:
                errors.append(f"Item {item_id} not found")
                
        except Exception as e:
            errors.append(f"Error updating item {update.get('item_id', 'unknown')}: {str(e)}")
    
    if updated_items:
        db.commit()
    
    return {
        "success": True,
        "data": {
            "updated_items": updated_items,
            "updated_count": len(updated_items),
            "errors": errors
        },
        "message": f"Bulk price update completed. {len(updated_items)} items updated."
    }


@router.patch("/{restaurant_id}/menu/items/bulk-availability", response_model=Dict[str, Any])
async def bulk_availability_update(
    restaurant_id: UUID,
    availability_updates: Dict[str, bool],  # {"item_id": True/False}
    db: Session = Depends(get_db),
    current_user = Depends(get_owner_or_manager_user)
):
    """Bulk update menu item availability (Owner/Manager only)."""
    
    # Verify access to restaurant
    restaurant = get_restaurant_context(restaurant_id, current_user)
    
    updated_items = []
    
    for item_id_str, is_available in availability_updates.items():
        try:
            item_id = UUID(item_id_str)
            item = db.query(MenuItem).filter(
                MenuItem.id == item_id,
                MenuItem.restaurant_id == restaurant_id
            ).first()
            
            if item:
                item.is_available = is_available
                updated_items.append({
                    "item_id": str(item.id),
                    "item_name": item.item_name,
                    "is_available": item.is_available
                })
        except Exception:
            continue
    
    if updated_items:
        db.commit()
    
    return {
        "success": True,
        "data": {
            "updated_items": updated_items,
            "updated_count": len(updated_items)
        },
        "message": f"Bulk availability update completed. {len(updated_items)} items updated."
    }