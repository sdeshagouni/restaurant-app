"""
Configuration management for the Restaurant Management API.
Handles environment variables and application settings.
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application Info
    APP_NAME: str = "Restaurant Management API"
    APP_VERSION: str = "3.0.0"
    DEBUG: bool = False
    PROJECT_NAME: Optional[str] = "Restaurant Management API"
    VERSION: Optional[str] = "1.0.0"
    DESCRIPTION: Optional[str] = "Complete restaurant management system with QR ordering and analytics"
    
    # API Configuration
    API_V1_STR: Optional[str] = "/api/v1"
    DOCS_URL: Optional[str] = "/docs"
    REDOC_URL: Optional[str] = "/redoc"
    OPENAPI_URL: Optional[str] = "/openapi.json"
    
    # Database
    DATABASE_URL: str = "sqlite:///./restaurant.db"
    DATABASE_POOL_SIZE: Optional[int] = 20
    DATABASE_MAX_OVERFLOW: Optional[int] = 30
    DATABASE_POOL_TIMEOUT: Optional[int] = 30
    DATABASE_POOL_RECYCLE: Optional[int] = 3600
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    JWT_SECRET_KEY: Optional[str] = "your-super-secret-jwt-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    JWT_ALGORITHM: Optional[str] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    BACKEND_CORS_ORIGINS: Optional[str] = '["http://localhost:3000","https://yourdomain.com"]'
    
    # Environment
    ENVIRONMENT: Optional[str] = "development"
    LOG_LEVEL: Optional[str] = "INFO"
    TIMEZONE: Optional[str] = "UTC"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: Optional[int] = 100
    RATE_LIMIT_BURST: Optional[int] = 100
    
    # File Upload
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    MAX_FILE_SIZE_MB: Optional[int] = 10
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]
    UPLOAD_DIR: str = "uploads"
    UPLOAD_FOLDER: Optional[str] = "uploads"
    
    # Payment
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_CLIENT_SECRET: Optional[str] = None
    
    # QR Code
    QR_CODE_BASE_URL: str = "https://your-domain.com"
    QR_CODE_SIZE: int = 200
    
    # Session
    GUEST_SESSION_EXPIRE_HOURS: int = 4
    
    # Email (Optional)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: Optional[bool] = True
    
    # Redis (Optional for caching)
    REDIS_URL: Optional[str] = None
    REDIS_POOL_SIZE: Optional[int] = 10
    CACHE_EXPIRE_SECONDS: int = 300  # 5 minutes
    
    # Error Tracking (Optional)
    SENTRY_DSN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        # Allow extra fields to prevent validation errors
        extra = "allow"


# Global settings instance
settings = Settings()