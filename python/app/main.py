"""
Enhanced FastAPI application with comprehensive REST API endpoints.
Implements the complete restaurant management system API specification.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, text
from app.models.base import Base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional, List
import uvicorn
import logging

# Import all the complete models
from app.models import *
from app.api.routes import auth, restaurants, tables, menu, orders, specials, payments, analytics, staff
from app.core.config import settings
from app.core.security import get_current_user, get_current_active_user
from app.core.database import get_db, check_database_health, SessionLocal, engine, DATABASE_URL


# =================================================================
# LOGGING CONFIGURATION
# =================================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# =================================================================
# FASTAPI APPLICATION
# =================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting Restaurant Management API...")
    
    # Create all tables
    logger.info("📊 Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
    
    # Check database health
    if check_database_health():
        logger.info("✅ Database connection healthy")
    else:
        logger.error("❌ Database connection failed")
    
    logger.info("🎯 API Features loaded:")
    logger.info("   • Authentication & User Management")
    logger.info("   • Restaurant Management")
    logger.info("   • Table & QR Code Management")
    logger.info("   • Menu Management (Categories, Items, Options)")
    logger.info("   • Order Processing & Management")
    logger.info("   • Daily Specials & Promotions")
    logger.info("   • Payment Processing")
    logger.info("   • Analytics & Reporting")
    logger.info("   • Staff Management")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Restaurant Management API...")


# Create FastAPI app
app = FastAPI(
    title="Restaurant Management API",
    description="""
    🍽️ **Complete REST API for Restaurant Management System**
    
    Features:
    - 🔐 JWT Authentication & Role-based Access
    - 🏢 Multi-tenant Restaurant Management  
    - 📱 QR Code Guest Ordering
    - 🍽️ Complete Menu Management
    - 📝 Order Processing Workflow
    - 🎁 Daily Specials & Promotions
    - 💳 Multi-Gateway Payment Processing
    - 📊 Analytics & Reporting
    - 👥 Staff Management
    
    **Base URL:** `/api/v1`
    """,
    version="3.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()


# =================================================================
# API ROUTES
# =================================================================

# Include API routers with proper prefixes
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    restaurants.router,
    prefix="/api/v1/restaurants",
    tags=["Restaurant Management"]
)

app.include_router(
    tables.router,
    prefix="/api/v1",
    tags=["Table Management"]
)

app.include_router(
    menu.router,
    prefix="/api/v1/restaurants",
    tags=["Menu Management"]
)

app.include_router(
    orders.router,
    prefix="/api/v1",
    tags=["Order Management"]
)

app.include_router(
    specials.router,
    prefix="/api/v1/restaurants",
    tags=["Daily Specials"]
)

app.include_router(
    payments.router,
    prefix="/api/v1",
    tags=["Payment Processing"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/restaurants",
    tags=["Analytics & Reporting"]
)
app.include_router(
    staff.router,
    prefix="/api/v1/staff",
    tags=["Staff Management"]
)

# =================================================================
# HEALTH CHECK ENDPOINTS
# =================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint with database connectivity test."""
    db_healthy = check_database_health()
    
    return {
        "success": True,
        "data": {
            "status": "healthy" if db_healthy else "unhealthy",
            "message": "Restaurant Management API is running",
            "database": "connected" if db_healthy else "disconnected",
            "version": "3.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "features": [
                "Authentication & User Management",
                "Restaurant Management", 
                "QR Code Table Ordering",
                "Menu Management",
                "Order Processing",
                "Daily Specials",
                "Payment Processing",
                "Analytics & Reporting",
                "Staff Management"
            ]
        }
    }


@app.get("/health/database")
async def database_health():
    """Detailed database health check."""
    try:
        db = SessionLocal()
        
        # Test basic query
        result = db.execute(text("SELECT 1 as test"))
        test_value = result.fetchone()[0]
        
        # Test table existence
        if "sqlite" in DATABASE_URL:
            table_check = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        else:
            table_check = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        
        tables = [row[0] for row in table_check.fetchall()]
        db.close()
        
        return {
            "success": True,
            "data": {
                "status": "healthy",
                "database_responsive": True,
                "test_query_result": test_value,
                "tables_found": len(tables),
                "table_names": tables[:10],  # Show first 10 tables
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Database health check failed",
                "details": str(e)
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


@app.get("/api/v1/status")
async def system_status():
    """System status endpoint for monitoring."""
    return {
        "success": True,
        "data": {
            "api_version": "3.0.0",
            "status": "operational",
            "database_status": "connected" if check_database_health() else "disconnected",
            "uptime": "System running",
            "endpoints": {
                "total_routes": len(app.routes),
                "authentication": "/api/v1/auth/*",
                "restaurants": "/api/v1/restaurants/*", 
                "menu": "/api/v1/restaurants/{id}/menu/*",
                "orders": "/api/v1/orders/*",
                "payments": "/api/v1/orders/{id}/payment/*",
                "public": "/api/v1/public/*"
            },
            "features": {
                "multi_tenant": True,
                "qr_ordering": True,
                "payment_processing": True,
                "analytics": True,
                "real_time_orders": True
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }


# =================================================================
# ROOT ENDPOINT
# =================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "success": True,
        "data": {
            "message": "🍽️ Restaurant Management API",
            "version": "3.0.0", 
            "description": "Complete REST API for restaurant management with QR ordering",
            "documentation": {
                "interactive_docs": "/docs",
                "redoc": "/redoc",
                "openapi_spec": "/openapi.json"
            },
            "endpoints": {
                "health": "/health",
                "system_status": "/api/v1/status",
                "authentication": "/api/v1/auth/*",
                "restaurants": "/api/v1/restaurants/*",
                "public_menu": "/api/v1/restaurants/{id}/menu/*",
                "public_ordering": "/api/v1/public/*",
                "staff_management": "/api/v1/restaurants/{id}/staff/*",
                "analytics": "/api/v1/restaurants/{id}/analytics/*"
            },
            "features": [
                "🔐 JWT Authentication & Authorization",
                "🏢 Multi-tenant Restaurant Management",
                "📱 QR Code Guest Ordering (No Registration)",
                "🍽️ Complete Menu Management",
                "📝 Real-time Order Processing",
                "🎁 Daily Specials & Promotions",
                "💳 Multi-Gateway Payment Processing",
                "📊 Advanced Analytics & Reporting",
                "👥 Staff & Role Management",
                "🔍 Advanced Search & Filtering"
            ],
            "getting_started": {
                "1": "Visit /docs for interactive API documentation",
                "2": "Use /api/v1/auth/login for staff authentication", 
                "3": "Scan QR codes to start guest ordering at /api/v1/public/*",
                "4": "Manage restaurants at /api/v1/restaurants/{id}/*"
            }
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# =================================================================
# STARTUP
# =================================================================

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )