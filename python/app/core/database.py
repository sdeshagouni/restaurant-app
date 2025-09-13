"""
Database configuration and session management.
Handles SQLAlchemy engine, session maker, and database dependencies.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
DATABASE_URL = settings.DATABASE_URL
# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_health():
    """Check database connectivity."""
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


def create_tables():
    """Create all database tables."""
    try:
        # Import Base from models
        from app.models.base import Base
        
        # Import all models to ensure they are registered
        import app.models.restaurant
        import app.models.table
        import app.models.menu
        import app.models.order
        import app.models.special
        import app.models.payment
        
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False