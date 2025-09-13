"""
Security utilities for JWT authentication and authorization.
Handles token creation, validation, and user permissions.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.config import settings
from app.models.restaurant import User, Restaurant
from app.models.base import UserRole


# =================================================================
# PASSWORD HASHING
# =================================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


# =================================================================
# JWT TOKEN MANAGEMENT
# =================================================================

security = HTTPBearer()

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


# =================================================================
# AUTHENTICATION DEPENDENCIES
# =================================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(lambda: None)  # Will be injected properly
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    from app.main import SessionLocal
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == UUID(user_id)).first()
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user (must be active and not locked)."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    if current_user.is_locked:
        raise HTTPException(status_code=400, detail="User account is locked")
    
    return current_user

def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Require admin user."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin access required."
        )
    return current_user

def get_owner_or_manager_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Require owner or manager user."""
    if current_user.role not in [UserRole.ADMIN, UserRole.OWNER, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Owner or manager access required."
        )
    return current_user

def get_staff_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Require any staff user (owner, manager, or staff)."""
    if current_user.role not in [UserRole.ADMIN, UserRole.OWNER, UserRole.MANAGER, UserRole.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Staff access required."
        )
    return current_user


# =================================================================
# GUEST SESSION MANAGEMENT
# =================================================================

def get_guest_session_token(
    x_session_token: Optional[str] = Header(None, alias="X-Session-Token")
) -> Optional[str]:
    """Extract guest session token from header."""
    return x_session_token

def verify_guest_session(
    session_token: Optional[str] = Depends(get_guest_session_token),
    db: Session = Depends(lambda: None)
) -> "GuestSession":
    """Verify guest session token and return session."""
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token required"
        )
    
    from app.main import SessionLocal
    from app.models.table import GuestSession
    
    db = SessionLocal()
    try:
        session = db.query(GuestSession).filter(
            GuestSession.session_token == session_token,
            GuestSession.is_active == True
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session token"
            )
        
        # Check if session is expired
        if session.is_expired:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session has expired"
            )
        
        return session
    finally:
        db.close()


# =================================================================
# RESTAURANT CONTEXT MANAGEMENT
# =================================================================

def get_restaurant_context(
    restaurant_id: UUID,
    current_user: User = Depends(get_current_active_user)
) -> Restaurant:
    """Get restaurant and verify user has access to it."""
    # Admin users can access any restaurant
    if current_user.role == UserRole.ADMIN:
        from app.main import SessionLocal
        db = SessionLocal()
        try:
            restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
            if not restaurant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Restaurant not found"
                )
            return restaurant
        finally:
            db.close()
    
    # Other users can only access their own restaurant
    if current_user.restaurant_id != restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this restaurant"
        )
    
    from app.main import SessionLocal
    db = SessionLocal()
    try:
        restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        return restaurant
    finally:
        db.close()


# =================================================================
# PERMISSION HELPERS
# =================================================================

def check_permission(user: User, permission: str) -> bool:
    """Check if user has specific permission."""
    if user.role == UserRole.ADMIN:
        return True
    
    if user.role == UserRole.OWNER:
        return True
    
    if user.role == UserRole.MANAGER:
        # Managers have most permissions except sensitive ones
        restricted_permissions = ["delete_restaurant", "manage_billing", "manage_staff_salaries"]
        return permission not in restricted_permissions
    
    # Check custom permissions in user.permissions JSON field
    if user.permissions and permission in user.permissions:
        return user.permissions[permission]
    
    # Default staff permissions
    default_staff_permissions = [
        "view_orders", "update_order_status", "process_payments",
        "view_menu", "update_menu_availability"
    ]
    
    return permission in default_staff_permissions

def require_permission(permission: str):
    """Decorator to require specific permission."""
    def permission_dependency(current_user: User = Depends(get_current_active_user)) -> User:
        if not check_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission}"
            )
        return current_user
    
    return permission_dependency