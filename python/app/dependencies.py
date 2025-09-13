"""
Common dependencies for the Restaurant Management API.
Provides reusable dependencies for authentication, database sessions, and context management.
"""

from typing import Optional, AsyncGenerator
from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.security import get_current_user_id, verify_token, validate_restaurant_access
from app.models.restaurant import User
from sqlmodel import select


class RestaurantContext:
    """Restaurant context for multi-tenant operations."""
    
    def __init__(self, user: User):
        self.user_id = user.id
        self.restaurant_id = user.restaurant_id
        self.user_role = user.role
        self.user = user
    
    def __repr__(self):
        return f"RestaurantContext(user_id={self.user_id}, restaurant_id={self.restaurant_id}, role={self.user_role})"


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    current_user_id: UUID = Depends(get_current_user_id)
) -> User:
    """
    Get current authenticated user from database.
    
    Args:
        session: Database session
        current_user_id: Current user ID from JWT token
        
    Returns:
        User: Current user object
        
    Raises:
        HTTPException: If user not found or inactive
    """
    # Query user from database
    result = await session.execute(
        select(User).where(User.id == current_user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    return user


async def get_restaurant_context(
    current_user: User = Depends(get_current_user)
) -> RestaurantContext:
    """
    Get restaurant context for multi-tenant operations.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        RestaurantContext: Restaurant context object
        
    Raises:
        HTTPException: If user doesn't belong to a restaurant
    """
    if not current_user.restaurant_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User must belong to a restaurant"
        )
    
    return RestaurantContext(current_user)


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Ensure current user is system admin.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Admin user object
        
    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


async def get_owner_user(
    context: RestaurantContext = Depends(get_restaurant_context)
) -> User:
    """
    Ensure current user is restaurant owner or admin.
    
    Args:
        context: Restaurant context
        
    Returns:
        User: Owner user object
        
    Raises:
        HTTPException: If user is not owner or admin
    """
    if not (context.user.is_owner or context.user.is_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner access required"
        )
    
    return context.user


async def get_manager_user(
    context: RestaurantContext = Depends(get_restaurant_context)
) -> User:
    """
    Ensure current user is restaurant manager, owner, or admin.
    
    Args:
        context: Restaurant context
        
    Returns:
        User: Manager user object
        
    Raises:
        HTTPException: If user doesn't have manager access
    """
    if not context.user.can_manage_restaurant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required"
        )
    
    return context.user


async def get_staff_user(
    context: RestaurantContext = Depends(get_restaurant_context)
) -> User:
    """
    Ensure current user is restaurant staff, manager, owner, or admin.
    
    Args:
        context: Restaurant context
        
    Returns:
        User: Staff user object
    """
    # All authenticated restaurant users have staff access
    return context.user


def require_restaurant_access(required_restaurant_id: UUID):
    """
    Create dependency that requires access to specific restaurant.
    
    Args:
        required_restaurant_id: Required restaurant ID
        
    Returns:
        Callable: Dependency function
    """
    async def _check_restaurant_access(
        context: RestaurantContext = Depends(get_restaurant_context)
    ) -> RestaurantContext:
        if context.user.is_admin:
            return context  # Admin has access to all restaurants
        
        validate_restaurant_access(context.restaurant_id, required_restaurant_id)
        return context
    
    return _check_restaurant_access


class PermissionChecker:
    """Permission checker for specific actions."""
    
    def __init__(self, required_permissions: list):
        self.required_permissions = required_permissions
    
    async def __call__(self, context: RestaurantContext = Depends(get_restaurant_context)) -> RestaurantContext:
        """Check if user has required permissions."""
        user_permissions = context.user.permissions or {}
        
        # Admin always has all permissions
        if context.user.is_admin:
            return context
        
        # Check role-based permissions
        role_permissions = {
            "owner": ["*"],  # All permissions
            "manager": ["view_analytics", "manage_menu", "manage_orders", "view_reports"],
            "staff": ["view_orders", "update_orders", "process_payments"]
        }
        
        user_role_permissions = role_permissions.get(context.user_role, [])
        
        # Check if user has required permissions
        has_permission = (
            "*" in user_role_permissions or
            any(perm in user_role_permissions for perm in self.required_permissions) or
            any(perm in user_permissions for perm in self.required_permissions)
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required permissions: {self.required_permissions}"
            )
        
        return context


# Common permission checkers
require_analytics_permission = PermissionChecker(["view_analytics"])
require_menu_management = PermissionChecker(["manage_menu"])
require_order_management = PermissionChecker(["manage_orders", "view_orders"])
require_payment_management = PermissionChecker(["manage_payments", "process_payments"])
require_staff_management = PermissionChecker(["manage_staff"])


# Pagination dependency
class PaginationParams:
    """Pagination parameters."""
    
    def __init__(self, page: int = 1, size: int = 20):
        self.page = max(1, page)
        self.size = min(100, max(1, size))  # Limit to 100 items per page
        self.offset = (self.page - 1) * self.size
    
    def __repr__(self):
        return f"PaginationParams(page={self.page}, size={self.size}, offset={self.offset})"


def get_pagination_params(page: int = 1, size: int = 20) -> PaginationParams:
    """Get pagination parameters."""
    return PaginationParams(page, size)


# Search parameters
class SearchParams:
    """Search parameters."""
    
    def __init__(self, q: Optional[str] = None, sort_by: str = "created_at", sort_order: str = "desc"):
        self.query = q
        self.sort_by = sort_by
        self.sort_order = sort_order.lower()
        
        if self.sort_order not in ["asc", "desc"]:
            self.sort_order = "desc"
    
    def __repr__(self):
        return f"SearchParams(query='{self.query}', sort_by={self.sort_by}, sort_order={self.sort_order})"


def get_search_params(q: Optional[str] = None, sort_by: str = "created_at", sort_order: str = "desc") -> SearchParams:
    """Get search parameters."""
    return SearchParams(q, sort_by, sort_order)