"""
Authentication and security utilities for the Restaurant Management API.
Handles JWT tokens, password hashing, and security dependencies.
"""

from datetime import datetime, timedelta
from typing import Optional, Any, Dict
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    
    return jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token.
    
    Args:
        data: Data to encode in the token
        
    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def verify_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token to verify
        token_type: Expected token type ('access' or 'refresh')
        
    Returns:
        Dict[str, Any]: Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check expiration
        exp = payload.get("exp")
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UUID:
    """
    Get current user ID from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        UUID: Current user ID
        
    Raises:
        HTTPException: If token is invalid
    """
    payload = verify_token(credentials.credentials, "access")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        return UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_tokens_for_user(user_id: UUID, restaurant_id: Optional[UUID] = None) -> Dict[str, str]:
    """
    Create access and refresh tokens for a user.
    
    Args:
        user_id: User's UUID
        restaurant_id: User's restaurant UUID (if applicable)
        
    Returns:
        Dict[str, str]: Dictionary with access_token and refresh_token
    """
    token_data = {"sub": str(user_id)}
    
    if restaurant_id:
        token_data["restaurant_id"] = str(restaurant_id)
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a secure random token.
    
    Args:
        length: Token length in bytes
        
    Returns:
        str: Secure random token
    """
    import secrets
    return secrets.token_urlsafe(length)


class RoleChecker:
    """Role-based access control checker."""
    
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user_role: str) -> bool:
        """
        Check if user has required role.
        
        Args:
            current_user_role: User's role
            
        Returns:
            bool: True if user has required role
        """
        if not current_user_role or current_user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return True


# Common role checkers
require_owner = RoleChecker(["owner", "admin"])
require_manager = RoleChecker(["owner", "manager", "admin"]) 
require_staff = RoleChecker(["owner", "manager", "staff", "admin"])


def validate_restaurant_access(user_restaurant_id: Optional[UUID], 
                              required_restaurant_id: UUID) -> bool:
    """
    Validate that user has access to the specified restaurant.
    
    Args:
        user_restaurant_id: User's restaurant ID
        required_restaurant_id: Required restaurant ID
        
    Returns:
        bool: True if user has access
        
    Raises:
        HTTPException: If user doesn't have access
    """
    if user_restaurant_id != required_restaurant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this restaurant"
        )
    return True