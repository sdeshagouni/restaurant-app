# Restaurant Management System - Complete REST API Design

A comprehensive REST API specification covering all scenarios for the restaurant management system with QR-based guest ordering, multi-tenant architecture, and role-based access control.

---

## 🏗️ API Architecture Overview

### **Base URL Structure**
```
https://api.restaurant-system.com/api/v1
```

### **Authentication**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

### **Standard Response Format**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "timestamp": "2025-09-13T11:46:00Z",
  "request_id": "req_abc123"
}
```

### **Error Response Format**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    }
  },
  "timestamp": "2025-09-13T11:46:00Z",
  "request_id": "req_abc123"
}
```

---

## 🔐 Authentication & User Management

### **1. Authentication Endpoints**

#### **User Registration (Admin Only)**
```http
POST /api/v1/auth/register
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json

{
  "email": "manager@restaurant.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1-555-0123",
  "role": "manager",
  "staff_type": "manager",
  "restaurant_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_12345",
      "email": "manager@restaurant.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "manager",
      "restaurant_id": "550e8400-e29b-41d4-a716-446655440000",
      "is_active": true,
      "created_at": "2025-09-13T11:46:00Z"
    }
  },
  "message": "User registered successfully"
}
```

#### **User Login**
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=manager@restaurant.com&password=SecurePass123
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 1800,
    "user": {
      "id": "user_12345",
      "email": "manager@restaurant.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "manager",
      "restaurant_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

#### **Token Refresh**
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### **Get Current User**
```http
GET /api/v1/auth/me
Authorization: Bearer <ACCESS_TOKEN>
```

#### **Update Current User**
```http
PUT /api/v1/auth/me
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+1-555-0124",
  "preferences": {
    "language": "en",
    "notifications": true
  }
}
```

#### **Change Password**
```http
POST /api/v1/auth/change-password
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json

{
  "current_password": "OldPass123",
  "new_password": "NewSecurePass456"
}
```

#### **Logout**
```http
POST /api/v1/auth/logout
Authorization: Bearer <ACCESS_TOKEN>
```

---

## 🏢 Restaurant Management

### **2. Restaurant Endpoints**

#### **Get Restaurant Details**
```http
GET /api/v1/restaurants/{restaurant_id}
Authorization: Bearer <ACCESS_TOKEN>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "restaurant": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "restaurant_name": "Mario's Italian Kitchen",
      "restaurant_code": "MARIO001",
      "business_email": "info@marioskitchen.com",
      "phone_number": "+1-555-0100",
      "address": {
        "street": "123 Main Street",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "USA"
      },
      "currency_code": "USD",
      "tax_rate": 0.0875,
      "service_charge_rate": 0.15,
      "timezone": "America/New_York",
      "operating_hours": {
        "monday": {"open": "11:00", "close": "22:00", "closed": false},
        "tuesday": {"open": "11:00", "close": "22:00", "closed": false},
        "wednesday": {"open": "11:00", "close": "22:00", "closed": false},
        "thursday": {"open": "11:00", "close": "22:00", "closed": false},
        "friday": {"open": "11:00", "close": "23:00", "closed": false},
        "saturday": {"open": "10:00", "close": "23:00", "closed": false},
        "sunday": {"open": "10:00", "close": "21:00", "closed": false}
      },
      "allows_takeout": true,
      "allows_delivery": true,
      "delivery_radius_km": 8.0,
      "minimum_delivery_amount": 25.00,
      "status": "active",
      "subscription_tier": "premium",
      "created_at": "2025-01-15T10:30:00Z"
    }
  }
}
```

#### **Update Restaurant Settings**
```http
PUT /api/v1/restaurants/{restaurant_id}
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "restaurant_name": "Mario's Italian Kitchen & Bar",
  "phone_number": "+1-555-0101",
  "tax_rate": 0.09,
  "service_charge_rate": 0.18,
  "operating_hours": {
    "friday": {"open": "11:00", "close": "24:00", "closed": false}
  },
  "allows_delivery": true,
  "delivery_radius_km": 10.0,
  "minimum_delivery_amount": 30.00
}
```

#### **Get Restaurant Dashboard**
```http
GET /api/v1/restaurants/{restaurant_id}/dashboard
Authorization: Bearer <MANAGER_TOKEN>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "dashboard": {
      "today": {
        "orders": 45,
        "revenue": 1250.75,
        "avg_order_value": 27.83,
        "active_orders": 8
      },
      "week": {
        "orders": 312,
        "revenue": 8642.50,
        "growth_percent": 15.3
      },
      "month": {
        "orders": 1205,
        "revenue": 33480.25,
        "growth_percent": 22.7
      },
      "operational": {
        "total_tables": 15,
        "active_tables_today": 12,
        "total_staff": 8,
        "active_payment_gateways": 2,
        "active_specials": 3
      },
      "performance": {
        "avg_fulfillment_time_minutes": 18.5,
        "customer_satisfaction": 4.6
      }
    }
  }
}
```

---

## 🪑 Table Management

### **3. Restaurant Table Endpoints**

#### **List All Tables**
```http
GET /api/v1/restaurants/{restaurant_id}/tables
Authorization: Bearer <STAFF_TOKEN>
Query Parameters:
- active_only: boolean (default: true)
- location: string (optional filter)
- page: integer (default: 1)
- size: integer (default: 20)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "tables": [
      {
        "id": "table_001",
        "table_number": "T01",
        "table_name": "Window Table 1",
        "capacity": 4,
        "location": "Main Dining",
        "qr_code": "QR_MARIO001_T01",
        "qr_code_url": "https://order.marioskitchen.com/table/T01",
        "is_active": true,
        "requires_reservation": false,
        "position_x": 100,
        "position_y": 150,
        "created_at": "2025-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "total": 15,
      "page": 1,
      "size": 20,
      "pages": 1
    }
  }
}
```

#### **Get Table Details**
```http
GET /api/v1/restaurants/{restaurant_id}/tables/{table_id}
Authorization: Bearer <STAFF_TOKEN>
```

#### **Create New Table**
```http
POST /api/v1/restaurants/{restaurant_id}/tables
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "table_number": "T16",
  "table_name": "Patio Table 1",
  "capacity": 6,
  "location": "Outdoor Patio",
  "requires_reservation": false,
  "position_x": 200,
  "position_y": 300
}
```

#### **Update Table**
```http
PUT /api/v1/restaurants/{restaurant_id}/tables/{table_id}
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "table_name": "Premium Window Table",
  "capacity": 4,
  "requires_reservation": true,
  "is_active": true
}
```

#### **Delete Table**
```http
DELETE /api/v1/restaurants/{restaurant_id}/tables/{table_id}
Authorization: Bearer <MANAGER_TOKEN>
```

#### **Get Table by QR Code (Public)**
```http
GET /api/v1/public/tables/qr/{qr_code}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "table": {
      "id": "table_001",
      "table_number": "T01",
      "table_name": "Window Table 1",
      "capacity": 4,
      "restaurant": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Mario's Italian Kitchen",
        "cuisine_type": "Italian",
        "phone_number": "+1-555-0100"
      }
    },
    "session_url": "/api/v1/public/guest-sessions/create"
  }
}
```

---

## 👥 Guest Session Management (QR Ordering)

### **4. Guest Session Endpoints**

#### **Create Guest Session (Public)**
```http
POST /api/v1/public/guest-sessions
Content-Type: application/json

{
  "table_id": "table_001",
  "guest_name": "John Customer",
  "guest_phone": "+1-555-0199",
  "guest_email": "john@example.com",
  "party_size": 4,
  "special_requests": "Please seat away from kitchen"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "session": {
      "id": "session_abc123",
      "session_token": "sess_token_xyz789",
      "table": {
        "id": "table_001",
        "table_number": "T01",
        "table_name": "Window Table 1"
      },
      "guest_name": "John Customer",
      "party_size": 4,
      "expires_at": "2025-09-13T15:46:00Z",
      "is_active": true
    },
    "restaurant": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Mario's Italian Kitchen",
      "currency_code": "USD"
    }
  }
}
```

#### **Get Guest Session (Public)**
```http
GET /api/v1/public/guest-sessions/{session_id}
X-Session-Token: sess_token_xyz789
```

#### **Update Guest Session (Public)**
```http
PUT /api/v1/public/guest-sessions/{session_id}
X-Session-Token: sess_token_xyz789
Content-Type: application/json

{
  "guest_name": "John & Mary Customer",
  "party_size": 2,
  "cart_data": {
    "items": [
      {
        "menu_item_id": "item_001",
        "quantity": 2,
        "selected_options": ["large_size", "extra_cheese"],
        "special_instructions": "Medium rare"
      }
    ]
  }
}
```

#### **End Guest Session**
```http
DELETE /api/v1/public/guest-sessions/{session_id}
X-Session-Token: sess_token_xyz789
```

---

## 🍽️ Menu Management

### **5. Menu Category Endpoints**

#### **List Menu Categories (Public & Staff)**
```http
GET /api/v1/restaurants/{restaurant_id}/menu/categories
Query Parameters:
- active_only: boolean (default: true)
- include_items: boolean (default: false)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "categories": [
      {
        "id": "cat_001",
        "category_name": "Appetizers",
        "description": "Start your meal with our delicious appetizers",
        "image_url": "https://cdn.marioskitchen.com/categories/appetizers.jpg",
        "display_order": 1,
        "is_active": true,
        "available_all_day": true,
        "available_from": null,
        "available_until": null,
        "item_count": 8,
        "created_at": "2025-01-15T10:30:00Z"
      }
    ]
  }
}
```

#### **Create Menu Category**
```http
POST /api/v1/restaurants/{restaurant_id}/menu/categories
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "category_name": "Desserts",
  "description": "Sweet endings to your perfect meal",
  "image_url": "https://cdn.marioskitchen.com/categories/desserts.jpg",
  "display_order": 5,
  "available_all_day": true
}
```

#### **Update Menu Category**
```http
PUT /api/v1/restaurants/{restaurant_id}/menu/categories/{category_id}
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "category_name": "Decadent Desserts",
  "description": "Indulgent sweet treats crafted by our pastry chef",
  "display_order": 5,
  "is_active": true
}
```

#### **Delete Menu Category**
```http
DELETE /api/v1/restaurants/{restaurant_id}/menu/categories/{category_id}
Authorization: Bearer <MANAGER_TOKEN>
```

### **6. Menu Item Endpoints**

#### **List Menu Items (Public & Staff)**
```http
GET /api/v1/restaurants/{restaurant_id}/menu/items
Query Parameters:
- category_id: UUID (optional filter)
- available_only: boolean (default: true)
- featured_only: boolean (default: false)
- search: string (search in name/description)
- min_price: decimal (filter by minimum price)
- max_price: decimal (filter by maximum price)
- dietary: string[] (vegetarian, vegan, gluten_free)
- page: integer (default: 1)
- size: integer (default: 50)
- sort_by: string (name, price, popularity, created_at)
- sort_order: string (asc, desc)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "item_001",
        "item_name": "Margherita Pizza",
        "description": "Fresh mozzarella, tomato sauce, basil, and olive oil",
        "price": 16.99,
        "cost_price": 5.25,
        "category": {
          "id": "cat_002",
          "name": "Main Courses"
        },
        "is_vegetarian": true,
        "is_vegan": false,
        "is_gluten_free": false,
        "is_spicy": false,
        "spice_level": 0,
        "contains_nuts": false,
        "contains_dairy": true,
        "contains_shellfish": false,
        "calories": 320,
        "protein_g": 15.5,
        "carbs_g": 45.2,
        "fat_g": 12.8,
        "is_available": true,
        "prep_time_minutes": 15,
        "image_url": "https://cdn.marioskitchen.com/items/margherita-pizza.jpg",
        "is_featured": true,
        "is_popular": true,
        "display_order": 1,
        "options": [
          {
            "id": "opt_001",
            "option_group": "Size",
            "option_name": "Large",
            "price_change": 3.00,
            "is_default": false,
            "display_order": 2
          }
        ],
        "created_at": "2025-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "total": 45,
      "page": 1,
      "size": 50,
      "pages": 1
    }
  }
}
```

#### **Get Menu Item Details**
```http
GET /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}
```

#### **Create Menu Item**
```http
POST /api/v1/restaurants/{restaurant_id}/menu/items
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "category_id": "cat_002",
  "item_name": "Chicken Parmigiana",
  "description": "Breaded chicken breast with marinara sauce and mozzarella",
  "price": 22.99,
  "cost_price": 8.50,
  "prep_time_minutes": 25,
  "is_vegetarian": false,
  "is_spicy": false,
  "contains_dairy": true,
  "calories": 580,
  "is_featured": false,
  "display_order": 10,
  "image_url": "https://cdn.marioskitchen.com/items/chicken-parm.jpg"
}
```

#### **Update Menu Item**
```http
PUT /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "price": 24.99,
  "is_available": true,
  "is_featured": true,
  "description": "Breaded chicken breast with our signature marinara sauce and fresh mozzarella"
}
```

#### **Update Menu Item Availability**
```http
PATCH /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}/availability
Authorization: Bearer <STAFF_TOKEN>
Content-Type: application/json

{
  "is_available": false,
  "reason": "Ingredient shortage"
}
```

#### **Delete Menu Item**
```http
DELETE /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}
Authorization: Bearer <MANAGER_TOKEN>
```

#### **Bulk Update Menu Items**
```http
PATCH /api/v1/restaurants/{restaurant_id}/menu/items/bulk
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "action": "update_availability",
  "item_ids": ["item_001", "item_002", "item_003"],
  "data": {
    "is_available": false
  }
}
```

### **7. Menu Item Options**

#### **List Item Options**
```http
GET /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}/options
```

#### **Create Item Option**
```http
POST /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}/options
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "option_group": "Size",
  "option_name": "Extra Large",
  "price_change": 5.00,
  "is_default": false,
  "is_required": false,
  "max_selections": 1,
  "display_order": 3
}
```

#### **Update Item Option**
```http
PUT /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}/options/{option_id}
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "option_name": "Extra Large (16\")",
  "price_change": 4.50,
  "display_order": 3
}
```

#### **Delete Item Option**
```http
DELETE /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}/options/{option_id}
Authorization: Bearer <MANAGER_TOKEN>
```

---

## 🛒 Order Management

### **8. Order Endpoints**

#### **Create Order (Guest)**
```http
POST /api/v1/public/orders
X-Session-Token: sess_token_xyz789
Content-Type: application/json

{
  "guest_session_id": "session_abc123",
  "order_type": "dine_in",
  "items": [
    {
      "menu_item_id": "item_001",
      "quantity": 2,
      "selected_options": ["opt_001", "opt_002"],
      "special_instructions": "Extra crispy, light sauce"
    },
    {
      "menu_item_id": "item_005",
      "quantity": 1,
      "selected_options": [],
      "special_instructions": ""
    }
  ],
  "special_instructions": "Table near window if possible",
  "estimated_pickup_time": "2025-09-13T13:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "order": {
      "id": "order_12345",
      "order_number": "MARIO-T01-067",
      "order_type": "dine_in",
      "order_status": "pending",
      "payment_status": "pending",
      "table": {
        "id": "table_001",
        "table_number": "T01"
      },
      "guest_name": "John Customer",
      "party_size": 4,
      "items": [
        {
          "id": "order_item_001",
          "item_name": "Margherita Pizza",
          "quantity": 2,
          "unit_price": 19.99,
          "total_price": 39.98,
          "selected_options": {
            "Size": "Large"
          },
          "special_instructions": "Extra crispy, light sauce"
        }
      ],
      "subtotal": 45.98,
      "tax_amount": 4.02,
      "service_charge": 6.90,
      "discount_amount": 0.00,
      "total_amount": 56.90,
      "estimated_prep_time": 20,
      "ordered_at": "2025-09-13T12:15:00Z"
    }
  }
}
```

#### **Get Order Details**
```http
GET /api/v1/orders/{order_id}
Authorization: Bearer <STAFF_TOKEN> OR X-Session-Token: sess_token_xyz789
```

#### **List Orders (Staff)**
```http
GET /api/v1/restaurants/{restaurant_id}/orders
Authorization: Bearer <STAFF_TOKEN>
Query Parameters:
- status: string[] (pending, confirmed, preparing, ready, served, completed, cancelled)
- order_type: string[] (dine_in, takeout, delivery)
- table_id: UUID (filter by table)
- date_from: datetime (ISO format)
- date_to: datetime (ISO format)
- guest_phone: string (search by guest phone)
- page: integer (default: 1)
- size: integer (default: 20)
- sort_by: string (ordered_at, total_amount, status)
- sort_order: string (asc, desc)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "orders": [
      {
        "id": "order_12345",
        "order_number": "MARIO-T01-067",
        "order_status": "preparing",
        "payment_status": "paid",
        "table": {
          "table_number": "T01",
          "location": "Main Dining"
        },
        "guest_name": "John Customer",
        "total_amount": 56.90,
        "item_count": 3,
        "ordered_at": "2025-09-13T12:15:00Z",
        "estimated_ready_time": "2025-09-13T12:35:00Z"
      }
    ],
    "pagination": {
      "total": 156,
      "page": 1,
      "size": 20,
      "pages": 8
    },
    "summary": {
      "total_orders": 156,
      "pending_orders": 12,
      "preparing_orders": 8,
      "ready_orders": 3,
      "total_revenue": 4250.75
    }
  }
}
```

#### **Update Order Status**
```http
PATCH /api/v1/orders/{order_id}/status
Authorization: Bearer <STAFF_TOKEN>
Content-Type: application/json

{
  "status": "preparing",
  "notes": "Started cooking at 12:20 PM",
  "estimated_ready_time": "2025-09-13T12:35:00Z"
}
```

#### **Cancel Order**
```http
PATCH /api/v1/orders/{order_id}/cancel
Authorization: Bearer <STAFF_TOKEN> OR X-Session-Token: sess_token_xyz789
Content-Type: application/json

{
  "reason": "Customer requested cancellation",
  "refund_amount": 56.90
}
```

#### **Add Items to Order**
```http
POST /api/v1/orders/{order_id}/items
Authorization: Bearer <STAFF_TOKEN> OR X-Session-Token: sess_token_xyz789
Content-Type: application/json

{
  "items": [
    {
      "menu_item_id": "item_010",
      "quantity": 1,
      "selected_options": [],
      "special_instructions": "On the side"
    }
  ]
}
```

#### **Update Order Item**
```http
PUT /api/v1/orders/{order_id}/items/{order_item_id}
Authorization: Bearer <STAFF_TOKEN>
Content-Type: application/json

{
  "quantity": 3,
  "special_instructions": "Extra crispy, no salt"
}
```

#### **Remove Order Item**
```http
DELETE /api/v1/orders/{order_id}/items/{order_item_id}
Authorization: Bearer <STAFF_TOKEN>
```

---

## 🎁 Daily Specials & Promotions

### **9. Daily Specials Endpoints**

#### **List Active Specials (Public)**
```http
GET /api/v1/restaurants/{restaurant_id}/specials
Query Parameters:
- active_only: boolean (default: true)
- valid_now: boolean (default: true)
- type: string[] (discount, combo, featured, limited_time)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "specials": [
      {
        "id": "special_001",
        "special_name": "Happy Hour Special",
        "description": "20% off all appetizers and drinks",
        "special_type": "discount",
        "discount_type": "percentage",
        "discount_value": 20.00,
        "minimum_order_amount": 0.00,
        "valid_from": "2025-09-13",
        "valid_until": "2025-12-31",
        "valid_days": [1, 2, 3, 4, 5],
        "valid_from_time": "15:00:00",
        "valid_until_time": "18:00:00",
        "max_uses_per_customer": 1,
        "max_total_uses": 100,
        "current_uses": 23,
        "is_active": true,
        "banner_text": "🍻 Happy Hour: 20% OFF Appetizers & Drinks!",
        "banner_color": "#FF6B35",
        "show_on_menu": true,
        "is_currently_valid": true,
        "applicable_items": ["cat_001", "cat_006"],
        "applies_to": "categories"
      }
    ]
  }
}
```

#### **Get Special Details**
```http
GET /api/v1/restaurants/{restaurant_id}/specials/{special_id}
```

#### **Create Daily Special**
```http
POST /api/v1/restaurants/{restaurant_id}/specials
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "special_name": "Weekend Combo Deal",
  "description": "Buy any pizza, get 50% off a dessert",
  "special_type": "combo",
  "discount_type": "buy_x_get_y",
  "discount_value": 50.00,
  "buy_quantity": 1,
  "get_quantity": 1,
  "get_discount_percent": 50.00,
  "valid_from": "2025-09-14",
  "valid_until": "2025-12-31",
  "valid_days": [6, 7],
  "banner_text": "🍕 Weekend Special: 50% OFF Dessert with Pizza!",
  "banner_color": "#28A745",
  "applicable_items": ["cat_002"],
  "applies_to": "categories",
  "max_total_uses": 200
}
```

#### **Update Special**
```http
PUT /api/v1/restaurants/{restaurant_id}/specials/{special_id}
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "discount_value": 25.00,
  "valid_until": "2025-11-30",
  "max_total_uses": 150,
  "is_active": true
}
```

#### **Toggle Special Status**
```http
PATCH /api/v1/restaurants/{restaurant_id}/specials/{special_id}/toggle
Authorization: Bearer <MANAGER_TOKEN>
```

#### **Apply Special to Order (Internal)**
```http
POST /api/v1/orders/{order_id}/apply-special
Authorization: Bearer <STAFF_TOKEN> OR X-Session-Token: sess_token_xyz789
Content-Type: application/json

{
  "special_id": "special_001",
  "guest_phone": "+1-555-0199"
}
```

#### **Get Special Usage Analytics**
```http
GET /api/v1/restaurants/{restaurant_id}/specials/{special_id}/usage
Authorization: Bearer <MANAGER_TOKEN>
Query Parameters:
- date_from: date (default: 30 days ago)
- date_to: date (default: today)
```

---

## 💳 Payment Processing

### **10. Payment Gateway Management**

#### **List Payment Gateways**
```http
GET /api/v1/restaurants/{restaurant_id}/payment-gateways
Authorization: Bearer <MANAGER_TOKEN>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "gateways": [
      {
        "id": "gateway_001",
        "provider": "stripe",
        "gateway_name": "Main Credit Card Processing",
        "description": "Primary payment processor for cards and digital wallets",
        "status": "active",
        "is_default": true,
        "is_sandbox": false,
        "features": {
          "supports_cards": true,
          "supports_digital_wallets": true,
          "supports_bank_transfers": false,
          "supports_cash_on_delivery": false
        },
        "fees": {
          "transaction_fee_percent": 0.029,
          "transaction_fee_fixed": 0.30,
          "minimum_amount": 0.50,
          "maximum_amount": 5000.00
        },
        "last_tested_at": "2025-09-12T10:30:00Z",
        "created_at": "2025-01-15T10:30:00Z"
      }
    ]
  }
}
```

#### **Create Payment Gateway**
```http
POST /api/v1/restaurants/{restaurant_id}/payment-gateways
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "provider": "paypal",
  "gateway_name": "PayPal Processing",
  "description": "PayPal and digital wallet payments",
  "configuration": {
    "client_id": "paypal_client_id_here",
    "client_secret": "paypal_client_secret_here",
    "environment": "production"
  },
  "supports_digital_wallets": true,
  "transaction_fee_percent": 0.034,
  "is_sandbox": false
}
```

#### **Update Payment Gateway**
```http
PUT /api/v1/restaurants/{restaurant_id}/payment-gateways/{gateway_id}
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "gateway_name": "Updated Stripe Processing",
  "status": "active",
  "transaction_fee_percent": 0.032,
  "transaction_fee_fixed": 0.25
}
```

#### **Set Default Gateway**
```http
PATCH /api/v1/restaurants/{restaurant_id}/payment-gateways/{gateway_id}/set-default
Authorization: Bearer <OWNER_TOKEN>
```

#### **Test Gateway Connection**
```http
POST /api/v1/restaurants/{restaurant_id}/payment-gateways/{gateway_id}/test
Authorization: Bearer <OWNER_TOKEN>
```

### **11. Payment Processing**

#### **Create Payment Intent**
```http
POST /api/v1/orders/{order_id}/payment-intent
Authorization: Bearer <STAFF_TOKEN> OR X-Session-Token: sess_token_xyz789
Content-Type: application/json

{
  "payment_method": "card",
  "gateway_id": "gateway_001",
  "return_url": "https://marioskitchen.com/payment/success",
  "cancel_url": "https://marioskitchen.com/payment/cancel"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "payment_intent": {
      "id": "pi_12345",
      "client_secret": "pi_12345_secret_xyz",
      "amount": 56.90,
      "currency": "USD",
      "status": "requires_payment_method",
      "payment_url": "https://checkout.stripe.com/pay/cs_12345"
    }
  }
}
```

#### **Confirm Payment**
```http
POST /api/v1/orders/{order_id}/payment/confirm
Authorization: Bearer <STAFF_TOKEN> OR X-Session-Token: sess_token_xyz789
Content-Type: application/json

{
  "payment_intent_id": "pi_12345",
  "payment_method_id": "pm_card_visa"
}
```

#### **Process Cash Payment**
```http
POST /api/v1/orders/{order_id}/payment/cash
Authorization: Bearer <STAFF_TOKEN>
Content-Type: application/json

{
  "amount_paid": 60.00,
  "change_given": 3.10,
  "payment_notes": "Paid in cash at table"
}
```

#### **Refund Payment**
```http
POST /api/v1/orders/{order_id}/payment/refund
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "amount": 56.90,
  "reason": "Customer complaint - food quality",
  "refund_method": "original_payment_method"
}
```

#### **List Payment Transactions**
```http
GET /api/v1/restaurants/{restaurant_id}/payments
Authorization: Bearer <MANAGER_TOKEN>
Query Parameters:
- status: string[] (pending, completed, failed, refunded)
- gateway_id: UUID (filter by gateway)
- date_from: datetime
- date_to: datetime
- page: integer
- size: integer
```

---

## 📊 Analytics & Reporting

### **12. Analytics Endpoints**

#### **Sales Analytics**
```http
GET /api/v1/restaurants/{restaurant_id}/analytics/sales
Authorization: Bearer <MANAGER_TOKEN>
Query Parameters:
- period: string (today, week, month, quarter, year, custom)
- date_from: date (for custom period)
- date_to: date (for custom period)
- group_by: string (day, week, month, hour)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_revenue": 33480.25,
      "total_orders": 1205,
      "avg_order_value": 27.78,
      "growth_percent": 22.7,
      "previous_period_revenue": 27350.80
    },
    "breakdown": [
      {
        "period": "2025-09-13",
        "revenue": 1250.75,
        "orders": 45,
        "avg_order_value": 27.83
      }
    ],
    "order_types": {
      "dine_in": {"orders": 720, "revenue": 20088.15},
      "takeout": {"orders": 485, "revenue": 13392.10}
    },
    "payment_methods": {
      "card": {"orders": 890, "revenue": 24836.18},
      "cash": {"orders": 315, "revenue": 8644.07}
    }
  }
}
```

#### **Menu Performance Analytics**
```http
GET /api/v1/restaurants/{restaurant_id}/analytics/menu
Authorization: Bearer <MANAGER_TOKEN>
Query Parameters:
- period: string (week, month, quarter)
- category_id: UUID (optional filter)
- limit: integer (default: 20)
- sort_by: string (popularity, revenue, profit_margin)
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "top_items": [
      {
        "item_id": "item_001",
        "item_name": "Margherita Pizza",
        "category_name": "Main Courses",
        "times_ordered": 87,
        "total_quantity": 142,
        "total_revenue": 2413.58,
        "avg_selling_price": 16.99,
        "profit_margin": 11.74,
        "profit_margin_percent": 69.1,
        "popularity_rank": 1,
        "revenue_rank": 2
      }
    ],
    "categories": [
      {
        "category_id": "cat_002",
        "category_name": "Main Courses",
        "total_revenue": 18450.25,
        "order_count": 456,
        "avg_order_value": 40.46,
        "item_count": 12
      }
    ]
  }
}
```

#### **Table Performance Analytics**
```http
GET /api/v1/restaurants/{restaurant_id}/analytics/tables
Authorization: Bearer <MANAGER_TOKEN>
Query Parameters:
- period: string (week, month, quarter)
```

#### **Staff Performance Analytics**
```http
GET /api/v1/restaurants/{restaurant_id}/analytics/staff
Authorization: Bearer <OWNER_TOKEN>
Query Parameters:
- period: string (week, month, quarter)
- staff_type: string[] (waiter, kitchen, cashier)
```

#### **Customer Analytics**
```http
GET /api/v1/restaurants/{restaurant_id}/analytics/customers
Authorization: Bearer <MANAGER_TOKEN>
Query Parameters:
- period: string (week, month, quarter)
```

#### **Financial Reports**
```http
GET /api/v1/restaurants/{restaurant_id}/reports/financial
Authorization: Bearer <OWNER_TOKEN>
Query Parameters:
- report_type: string (daily, weekly, monthly, yearly)
- date_from: date
- date_to: date
- format: string (json, csv, pdf)
```

---

## 👨‍💼 Staff & User Management

### **13. Staff Management Endpoints**

#### **List Restaurant Staff**
```http
GET /api/v1/restaurants/{restaurant_id}/staff
Authorization: Bearer <MANAGER_TOKEN>
Query Parameters:
- role: string[] (owner, manager, staff)
- staff_type: string[] (waiter, kitchen, cashier)
- active_only: boolean (default: true)
- page: integer
- size: integer
```

#### **Get Staff Member Details**
```http
GET /api/v1/restaurants/{restaurant_id}/staff/{user_id}
Authorization: Bearer <MANAGER_TOKEN>
```

#### **Update Staff Member**
```http
PUT /api/v1/restaurants/{restaurant_id}/staff/{user_id}
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone_number": "+1-555-0125",
  "role": "manager",
  "staff_type": "manager",
  "is_active": true,
  "permissions": {
    "manage_menu": true,
    "process_refunds": true,
    "view_reports": true
  }
}
```

#### **Deactivate Staff Member**
```http
PATCH /api/v1/restaurants/{restaurant_id}/staff/{user_id}/deactivate
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "reason": "Employee terminated",
  "effective_date": "2025-09-15"
}
```

---

## 🔍 Search & Filtering

### **14. Search Endpoints**

#### **Global Search**
```http
GET /api/v1/restaurants/{restaurant_id}/search
Authorization: Bearer <STAFF_TOKEN>
Query Parameters:
- q: string (search query)
- types: string[] (menu_items, orders, customers, tables)
- limit: integer (default: 20)
```

#### **Menu Search (Public)**
```http
GET /api/v1/restaurants/{restaurant_id}/menu/search
Query Parameters:
- q: string (search in item names and descriptions)
- category: string (filter by category)
- dietary: string[] (vegetarian, vegan, gluten_free)
- price_range: string (0-15, 15-25, 25-35, 35+)
- limit: integer (default: 20)
```

---

## 📱 QR Code & Mobile Features

### **15. QR Code & Mobile Endpoints**

#### **Generate QR Codes**
```http
POST /api/v1/restaurants/{restaurant_id}/qr-codes/generate
Authorization: Bearer <MANAGER_TOKEN>
Content-Type: application/json

{
  "table_ids": ["table_001", "table_002"],
  "format": "png",
  "size": "medium",
  "include_logo": true
}
```

#### **Mobile Menu (Optimized)**
```http
GET /api/v1/restaurants/{restaurant_id}/mobile/menu
X-Session-Token: sess_token_xyz789
Query Parameters:
- optimize: boolean (default: true)
- include_images: boolean (default: true)
- image_size: string (small, medium, large)
```

#### **Mobile Order Status**
```http
GET /api/v1/mobile/orders/{order_id}/status
X-Session-Token: sess_token_xyz789
```

---

## 🔔 Notifications & Webhooks

### **16. Notification Endpoints**

#### **Get Notifications**
```http
GET /api/v1/notifications
Authorization: Bearer <STAFF_TOKEN>
Query Parameters:
- type: string[] (order_update, payment_received, staff_message)
- read: boolean (filter by read status)
- limit: integer (default: 50)
```

#### **Mark Notification as Read**
```http
PATCH /api/v1/notifications/{notification_id}/read
Authorization: Bearer <STAFF_TOKEN>
```

#### **Configure Webhook**
```http
POST /api/v1/restaurants/{restaurant_id}/webhooks
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "url": "https://yourdomain.com/webhooks/restaurant",
  "events": ["order.created", "payment.completed", "order.status_changed"],
  "secret": "webhook_secret_key"
}
```

---

## 🛠️ System & Utility Endpoints

### **17. System Endpoints**

#### **Health Check**
```http
GET /api/v1/health
```

#### **System Status**
```http
GET /api/v1/status
Authorization: Bearer <ADMIN_TOKEN>
```

#### **Upload File**
```http
POST /api/v1/restaurants/{restaurant_id}/upload
Authorization: Bearer <STAFF_TOKEN>
Content-Type: multipart/form-data

file: [binary data]
type: string (menu_image, restaurant_logo, qr_code)
```

#### **Get Restaurant Settings**
```http
GET /api/v1/restaurants/{restaurant_id}/settings
Authorization: Bearer <MANAGER_TOKEN>
```

#### **Update Restaurant Settings**
```http
PUT /api/v1/restaurants/{restaurant_id}/settings
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "timezone": "America/New_York",
  "currency_code": "USD",
  "tax_rate": 0.0875,
  "service_charge_rate": 0.15,
  "auto_accept_orders": false,
  "order_timeout_minutes": 30,
  "notification_settings": {
    "email_new_orders": true,
    "sms_payment_confirmations": false
  }
}
```

---

## 📋 API Usage Examples

### **Complete Guest Ordering Flow**

```bash
# 1. Guest scans QR code and gets table info
curl -X GET "https://api.restaurant-system.com/api/v1/public/tables/qr/QR_MARIO001_T01"

# 2. Create guest session
curl -X POST "https://api.restaurant-system.com/api/v1/public/guest-sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "table_id": "table_001",
    "guest_name": "John Customer",
    "party_size": 4
  }'

# 3. Browse menu
curl -X GET "https://api.restaurant-system.com/api/v1/restaurants/550e8400-e29b-41d4-a716-446655440000/menu/items?available_only=true"

# 4. Create order
curl -X POST "https://api.restaurant-system.com/api/v1/public/orders" \
  -H "X-Session-Token: sess_token_xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "guest_session_id": "session_abc123",
    "items": [
      {
        "menu_item_id": "item_001",
        "quantity": 2,
        "selected_options": ["opt_001"]
      }
    ]
  }'

# 5. Process payment
curl -X POST "https://api.restaurant-system.com/api/v1/orders/order_12345/payment-intent" \
  -H "X-Session-Token: sess_token_xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_method": "card"
  }'

# 6. Check order status
curl -X GET "https://api.restaurant-system.com/api/v1/orders/order_12345" \
  -H "X-Session-Token: sess_token_xyz789"
```

### **Staff Order Management Flow**

```bash
# 1. Staff login
curl -X POST "https://api.restaurant-system.com/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=staff@mario.com&password=StaffPass123"

# 2. Get pending orders
curl -X GET "https://api.restaurant-system.com/api/v1/restaurants/550e8400-e29b-41d4-a716-446655440000/orders?status=pending,confirmed" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# 3. Update order status
curl -X PATCH "https://api.restaurant-system.com/api/v1/orders/order_12345/status" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "preparing",
    "estimated_ready_time": "2025-09-13T12:35:00Z"
  }'

# 4. Process cash payment
curl -X POST "https://api.restaurant-system.com/api/v1/orders/order_12345/payment/cash" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "amount_paid": 60.00,
    "change_given": 3.10
  }'
```

---

## 🚀 Implementation Notes

### **Key Design Principles**

1. **Resource-Based URLs**: Every endpoint represents a resource or collection
2. **HTTP Method Semantics**: GET (read), POST (create), PUT (update/replace), PATCH (partial update), DELETE (remove)
3. **Consistent Response Format**: All responses follow the same JSON structure
4. **Proper Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), etc.
5. **Authentication & Authorization**: JWT tokens with role-based access control
6. **Multi-Tenant Security**: All restaurant data is automatically filtered by restaurant_id
7. **Pagination**: Large datasets are paginated with consistent parameters
8. **Error Handling**: Detailed error messages with context

### **Security Considerations**

- All staff endpoints require JWT authentication
- Public endpoints (guest ordering) use session tokens
- Role-based access control (Owner > Manager > Staff)
- Multi-tenant data isolation prevents cross-restaurant access
- Rate limiting and request validation on all endpoints
- Sensitive operations (payments, refunds) require elevated permissions

### **Performance Optimizations**

- Database indexes on frequently queried fields
- Pagination to limit response sizes
- Caching for menu items and restaurant settings
- Async processing for non-critical operations
- Batch operations for bulk updates

This comprehensive REST API design covers all scenarios for a modern restaurant management system with QR-based ordering, providing a solid foundation for building scalable restaurant applications.