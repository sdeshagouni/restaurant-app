# Restaurant Management System - FastAPI Backend

A complete FastAPI backend for the restaurant management system with multi-tenant support, authentication, and comprehensive REST APIs.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Restaurant database schema deployed

### Installation

```bash
# Create virtual environment
python -m venv restaurant_api
source restaurant_api/bin/activate  # On Windows: restaurant_api\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp env.example .env
# Edit .env with your database credentials

# Run database migrations (if needed)
python -m alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access Points
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🏗️ Project Structure

```
restaurant_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   ├── dependencies.py      # Common dependencies
│   ├── security.py          # Authentication and security
│   └── api/
│       ├── __init__.py
│       ├── api_v1/
│       │   ├── __init__.py
│       │   ├── api.py       # API router aggregation
│       │   └── endpoints/   # Individual endpoint modules
│       │       ├── __init__.py
│       │       ├── auth.py
│       │       ├── restaurants.py
│       │       ├── menu.py
│       │       ├── orders.py
│       │       ├── specials.py
│       │       └── analytics.py
│       └── deps.py          # API dependencies
├── app/models/
│   ├── __init__.py
│   ├── base.py              # Base model classes
│   ├── user.py              # User models
│   ├── restaurant.py        # Restaurant models
│   ├── menu.py              # Menu models
│   ├── order.py             # Order models
│   └── payment.py           # Payment models
├── app/schemas/             # Pydantic schemas
│   ├── __init__.py
│   ├── user.py
│   ├── restaurant.py
│   ├── menu.py
│   ├── order.py
│   └── common.py
├── app/core/
│   ├── __init__.py
│   ├── business/            # Business logic
│   │   ├── __init__.py
│   │   ├── orders.py
│   │   ├── specials.py
│   │   ├── analytics.py
│   │   └── payments.py
│   └── utils/
│       ├── __init__.py
│       ├── security.py
│       └── helpers.py
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.yml
```

## 🔒 Authentication & Authorization

### JWT Token Authentication
- User registration and login
- Role-based access control (Owner, Manager, Staff)
- Multi-tenant isolation (restaurant-specific data)

### Security Features
- Password hashing with bcrypt
- JWT tokens with refresh capability
- Rate limiting on sensitive endpoints
- CORS configuration for frontend integration

## 📊 Key Features

### Multi-Tenant Architecture
- Complete data isolation between restaurants
- Automatic restaurant context from authenticated user
- Role-based permissions within each restaurant

### Business Logic Implementation
- Order creation and management
- Menu item performance analytics
- Daily specials with flexible rules
- Payment processing integration
- Real-time dashboard metrics

### API Endpoints
- **Authentication**: Login, register, refresh tokens
- **Restaurant Management**: CRUD operations, settings
- **Menu System**: Categories, items, options, performance
- **Order Processing**: Create, update, track orders
- **Daily Specials**: Promotions, discounts, usage tracking  
- **Analytics**: Dashboard metrics, sales trends
- **Payment**: Gateway management, transaction processing

## 🗄️ Database Integration

### SQLModel (Recommended)
- Type-safe database models
- Automatic Pydantic schema generation
- Perfect FastAPI integration
- Async support with SQLAlchemy 2.0+

### Connection Management
- Connection pooling for performance
- Async database sessions
- Automatic transaction handling
- Migration support with Alembic

## 📈 Performance Features

### Async-First Design
- All endpoints are async by default
- Non-blocking database operations
- Concurrent request handling
- Optimal for real-time applications

### Caching Strategy
- Redis integration for session storage
- Query result caching
- API response caching
- Rate limiting with Redis

## 🧪 Testing

### Comprehensive Test Suite
- Unit tests for business logic
- Integration tests for API endpoints  
- Database testing with fixtures
- Authentication flow testing

### Test Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_orders.py -v
```

## 🚀 Deployment

### Docker Support
- Multi-stage Docker builds
- Production-ready configuration
- Docker Compose for local development
- Health checks and monitoring

### Production Configuration
- Environment-based settings
- Logging configuration
- Error tracking integration
- Performance monitoring

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/restaurant_system
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Security
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=Restaurant Management API
VERSION=1.0.0
DESCRIPTION=Complete restaurant management with QR ordering

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

## 📚 API Documentation

### Interactive Documentation
FastAPI automatically generates interactive API documentation:
- **Swagger UI**: `/docs` - Try out APIs directly
- **ReDoc**: `/redoc` - Clean documentation format  
- **OpenAPI Schema**: `/openapi.json` - Machine-readable spec

### Sample API Calls

#### Authentication
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "owner@demo.com", "password": "demo123"}'

# Get current user
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Restaurant Management
```bash
# Get restaurant dashboard
curl -X GET "http://localhost:8000/api/v1/restaurants/dashboard" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Create menu item
curl -X POST "http://localhost:8000/api/v1/menu/items" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"category_id": "uuid", "item_name": "New Dish", "price": 19.99}'
```

## 🔍 Monitoring & Observability

### Health Checks
- Database connectivity check
- Redis connectivity check (if configured)
- Application health status
- Dependency health monitoring

### Logging
- Structured logging with JSON format
- Request/response logging
- Error tracking and reporting
- Performance metrics logging

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Run tests: `pytest`
5. Submit pull request

### Code Quality
- Black for code formatting
- isort for import sorting
- mypy for type checking
- pytest for testing
- pre-commit hooks for quality assurance

---

**This FastAPI backend provides a complete, production-ready foundation for your restaurant management system with excellent performance, security, and developer experience.** 🚀