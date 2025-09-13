#!/bin/bash

# =================================================================
# RESTAURANT API - QUICK START SCRIPT
# Sets up and runs the FastAPI backend for development
# =================================================================

set -e  # Exit on any error

echo "🍽️  Restaurant Management API - Quick Start"
echo "===========================================" 
echo ""

# Check if Python 3 is available
if ! command -v python &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3 and try again."
    exit 1
fi

PYTHON_VERSION=$(python -c "import sys; print(sys.version_info[0])")
if [[ "$PYTHON_VERSION" -lt 3 ]]; then
    echo "❌ Python 3 is required. You have $(python --version)"
    exit 1
fi


echo "✅ Python version check passed"

# Check if PostgreSQL is available (optional for Docker setup)
echo ""
echo "🔍 Checking setup options..."

HAS_DOCKER=$(command -v docker &> /dev/null && echo "true" || echo "false")
HAS_POSTGRES=$(command -v psql &> /dev/null && echo "true" || echo "false")

echo "   Docker available: $HAS_DOCKER"
echo "   PostgreSQL available: $HAS_POSTGRES"

# Choose setup method
if [ "$HAS_DOCKER" = "true" ]; then
    echo ""
    echo "🐳 Docker is available! Choose your setup:"
    echo "   1. Full Docker setup (Recommended for beginners)"
    echo "   2. Local Python with Docker database" 
    echo "   3. Full local setup (requires PostgreSQL)"
    echo ""
    read -p "Enter your choice (1-3): " -n 1 -r SETUP_CHOICE
    echo ""
else
    if [ "$HAS_POSTGRES" = "true" ]; then
        SETUP_CHOICE=3
        echo "⚙️  Using local setup (PostgreSQL detected)"
    else
        echo "❌ Neither Docker nor PostgreSQL found."
        echo "   Please install either:"
        echo "   • Docker: https://docs.docker.com/get-docker/"
        echo "   • PostgreSQL: https://postgresql.org/download/"
        exit 1
    fi
fi

# Docker setup (full)
if [ "$SETUP_CHOICE" = "1" ]; then
    echo ""
    echo "🐳 Setting up full Docker environment..."
    
    # Check if docker-compose is available
    if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
        echo "❌ docker-compose is required but not found."
        echo "   Please install Docker Compose and try again."
        exit 1
    fi
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        echo "📝 Creating environment configuration..."
        cp .env.example .env
        echo "✅ Created .env file (you can modify it later)"
    fi
    
    # Start services
    echo "🚀 Starting Docker services..."
    if command -v docker-compose &> /dev/null; then
        docker-compose up --build -d
    else
        docker compose up --build -d
    fi
    
    echo ""
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    # Check health
    echo "🏥 Checking service health..."
    for i in {1..30}; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            echo "✅ API is running!"
            break
        fi
        if [ $i -eq 30 ]; then
            echo "⚠️  API might still be starting up..."
        fi
        sleep 2
    done

# Docker database + Local Python
elif [ "$SETUP_CHOICE" = "2" ]; then
    echo ""
    echo "🐳📍 Setting up Docker database with local Python..."
    
    # Start only database services
    if command -v docker-compose &> /dev/null; then
        docker-compose up -d postgres redis
    else
        docker compose up -d postgres redis
    fi
    
    echo "⏳ Waiting for database to start..."
    sleep 5
    
    # Set up Python environment
    echo "🐍 Setting up Python environment..."
    
    if [ ! -d "restaurant_api" ]; then
        echo "📦 Creating virtual environment..."
        python -m venv restaurant_api
        echo "✅ Virtual environment created"
    fi
    
    echo "🔧 Activating virtual environment..."
    source restaurant_api/bin/activate
    
    echo "📥 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create .env for local setup
    if [ ! -f ".env" ]; then
        cp .env.example .env
        # Update for local Python + Docker DB
        sed -i 's|DATABASE_URL=.*|DATABASE_URL=postgresql://restaurant_user:restaurant_password@localhost:5432/restaurant_system|g' .env
        echo "✅ Created .env file for local setup"
    fi
    
    # Start the API
    echo "🚀 Starting FastAPI server..."
    echo "   API will be available at: http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs"
    echo "   Press Ctrl+C to stop"
    echo ""
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Local setup
elif [ "$SETUP_CHOICE" = "3" ]; then
    echo ""
    echo "📍 Setting up local development environment..."
    
    # Check PostgreSQL connection
    echo "🔍 Checking PostgreSQL connection..."
    if ! psql -h localhost -p 5432 -U postgres -c "SELECT 1;" &> /dev/null; then
        echo "❌ Cannot connect to PostgreSQL."
        echo "   Please ensure PostgreSQL is running and accessible."
        echo ""
        echo "💡 Quick fixes:"
        echo "   • Start PostgreSQL: brew services start postgresql (macOS)"
        echo "   • Or: sudo systemctl start postgresql (Linux)"
        echo "   • Create database: createdb restaurant_system"
        exit 1
    fi
    

    # Set up Python environment
    echo "🐍 Setting up Python environment..."

    if [ ! -d "restaurant_api" ]; then
        echo "📦 Creating virtual environment..."
        python -m venv restaurant_api
        echo "✅ Virtual environment created"
    fi

    # Detect OS and activate virtual environment accordingly
    if [ -f "restaurant_api/bin/activate" ]; then
        echo "🔧 Activating virtual environment (Unix)..."
        source restaurant_api/bin/activate
    elif [ -f "restaurant_api/Scripts/activate" ]; then
        echo "🔧 Activating virtual environment (Windows)..."
        source restaurant_api/Scripts/activate
    else
        echo "❌ Could not find the virtual environment activation script."
        echo "   Please check that the virtual environment was created successfully."
        exit 1
    fi

    
    echo "📥 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Create .env for local setup
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo "✅ Created .env file"
        echo ""
        echo "⚠️  Please update the DATABASE_URL in .env file with your PostgreSQL credentials"
        echo "   Current: DATABASE_URL=postgresql://restaurant_user:restaurant_password@localhost:5432/restaurant_system"
        echo ""
        read -p "Press Enter when you've updated the .env file..."
    fi
    
    # Start the API
    echo "🚀 Starting FastAPI server..."
    echo "   API will be available at: http://localhost:8000"
    echo "   API Documentation: http://localhost:8000/docs" 
    echo "   Press Ctrl+C to stop"
    echo ""
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi

# Final success message
echo ""
echo "🎉 SUCCESS! Restaurant Management API is running!"
echo "=============================================="
echo ""
echo "📍 Access Points:"
echo "   • API Base URL: http://localhost:8000"
echo "   • Interactive Docs: http://localhost:8000/docs"
echo "   • ReDoc: http://localhost:8000/redoc"
echo "   • Health Check: http://localhost:8000/health"
echo ""

if [ "$SETUP_CHOICE" = "1" ]; then
    echo "🗄️  Database Access:"
    echo "   • pgAdmin: http://localhost:5050"
    echo "     Email: admin@restaurant.com"
    echo "     Password: admin_password"
    echo ""
fi

echo "🚀 Next Steps:"
echo "   1. Visit http://localhost:8000/docs to explore the API"
echo "   2. Create your first user account"
echo "   3. Set up a restaurant and start building!"
echo ""
echo "💡 Need help? Check README.md for detailed documentation"
echo ""