"""
Daily specials and promotions API routes.
Handles special offers, discounts, and promotion tracking.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import date

from app.core.security import get_owner_or_manager_user, get_restaurant_context
from app.models.special import DailySpecial, SpecialUsage
from app.models.base import SpecialType
from app.core.database import get_db

router = APIRouter()


@router.get("/{restaurant_id}/specials", response_model=Dict[str, Any])
async def list_active_specials(
    restaurant_id: UUID,
    active_only: bool = Query(True),
    valid_now: bool = Query(True),
    db: Session = Depends(get_db)
):
    """List active specials (Public)."""
    
    query = db.query(DailySpecial).filter(DailySpecial.restaurant_id == restaurant_id)
    
    if active_only:
        query = query.filter(DailySpecial.is_active == True)
    
    if valid_now:
        today = date.today()
        query = query.filter(
            DailySpecial.valid_from <= today,
            DailySpecial.valid_until >= today
        )
    
    specials = query.order_by(DailySpecial.display_order).all()
    
    special_data = []
    for special in specials:
        special_data.append({
            "id": str(special.id),
            "special_name": special.special_name,
            "description": special.description,
            "special_type": special.special_type,
            "discount_type": special.discount_type,
            "discount_value": float(special.discount_value) if special.discount_value else None,
            "minimum_order_amount": float(special.minimum_order_amount),
            "valid_from": special.valid_from.isoformat(),
            "valid_until": special.valid_until.isoformat(),
            "valid_days": special.valid_days,
            "valid_from_time": special.valid_from_time.isoformat(),
            "valid_until_time": special.valid_until_time.isoformat(),
            "max_uses_per_customer": special.max_uses_per_customer,
            "max_total_uses": special.max_total_uses,
            "current_uses": special.current_uses,
            "is_active": special.is_active,
            "banner_text": special.banner_text,
            "banner_color": special.banner_color,
            "show_on_menu": special.show_on_menu,
            "is_currently_valid": special.is_currently_valid,
            "applicable_items": special.applicable_items,
            "applies_to": special.applies_to,
            "discount_description": special.discount_description,
            "usage_remaining": special.usage_remaining
        })
    
    return {
        "success": True,
        "data": {
            "specials": special_data
        }
    }


@router.get("/{restaurant_id}/specials/{special_id}", response_model=Dict[str, Any])
async def get_special_details(
    restaurant_id: UUID,
    special_id: UUID,
    db: Session = Depends(get_db)
):
    """Get special details."""
    
    special = db.query(DailySpecial).filter(
        DailySpecial.id == special_id,
        DailySpecial.restaurant_id == restaurant_id
    ).first()
    
    if not special:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Special not found"
        )
    
    return {
        "success": True,
        "data": {
            "special": {
                "id": str(special.id),
                "special_name": special.special_name,
                "description": special.description,
                "special_type": special.special_type,
                "discount_type": special.discount_type,
                "discount_value": float(special.discount_value) if special.discount_value else None,
                "minimum_order_amount": float(special.minimum_order_amount),
                "valid_from": special.valid_from.isoformat(),
                "valid_until": special.valid_until.isoformat(),
                "valid_days": special.valid_days,
                "valid_from_time": special.valid_from_time.isoformat(),
                "valid_until_time": special.valid_until_time.isoformat(),
                "banner_text": special.banner_text,
                "banner_color": special.banner_color,
                "applicable_items": special.applicable_items,
                "applies_to": special.applies_to,
                "terms_and_conditions": special.terms_and_conditions,
                "is_currently_valid": special.is_currently_valid,
                "discount_description": special.discount_description,
                "created_at": special.created_at.isoformat() + "Z"
            }
        }
    }