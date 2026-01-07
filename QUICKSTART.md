# Quick Start Guide

Get the E-commerce API up and running in 5 minutes!

## 1. Prerequisites

```bash
# Check Python version (3.8+)
python --version

# Check pip
pip --version
```

## 2. Setup (Windows)

```bash
# Navigate to Backend directory
cd Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Setup (macOS/Linux)

```bash
# Navigate to Backend directory
cd Backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 4. Configure Database

```bash
# Copy example environment file
cp .env.example .env

# The default uses SQLite (perfect for development)
# No additional setup needed!

# To use PostgreSQL, edit .env:
# DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_db
```

## 5. Run the Server

```bash
# Activate virtual environment (if not already activated)
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Start the server
uvicorn main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

## 6. Access the API

### Interactive Documentation
Open your browser and go to: **http://localhost:8000/docs**

You'll see a beautiful Swagger UI where you can:
- Browse all endpoints
- Test each endpoint
- View response schemas
- Try authentication

## 7. First Test

### Register a User

In Swagger UI:
1. Click **"POST /api/auth/register"**
2. Click **"Try it out"**
3. Enter:
```json
{
  "username": "testuser",
  "password": "Test123456"
}
```
4. Click **"Execute"**

You should see: ✅ 201 Created

### Login

1. Click **"POST /api/auth/login"**
2. Click **"Try it out"**
3. Enter:
```json
{
  "username": "testuser",
  "password": "Test123456"
}
```
4. Click **"Execute"**

You'll get a response with `access_token`. Copy it!

### Authorize in Swagger

1. Click **"Authorize"** button (top right)
2. Paste your token in the format: `Bearer your_token_here`
3. Click **"Authorize"** then **"Close"**

Now all authenticated endpoints will work!

## 8. Quick API Tests

### Create a Product

```bash
curl -X POST "http://localhost:8000/api/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "quantity": 10
  }'
```

### Get All Products

```bash
curl -X GET "http://localhost:8000/api/products/"
```

### Create an Order (requires authentication)

```bash
curl -X POST "http://localhost:8000/api/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": 1, "quantity": 2}
    ]
  }'
```

## 9. Common Issues

### ModuleNotFoundError

```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Port 8000 Already in Use

```bash
# Use a different port
uvicorn main:app --reload --port 8001
```

### Database Error

```bash
# For SQLite (should work out of box)
# Just make sure .env has:
DATABASE_URL=sqlite:///./ecommerce.db
```

### Import Errors

```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

## 10. Project Structure

```
Backend/
├── main.py              # Start here!
├── database.py          # Database config
├── requirements.txt     # Dependencies
├── .env.example        # Configuration template
├── app/
│   ├── Models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   ├── CRUD/           # Database operations
│   └── Router/         # API endpoints
│       ├── Auth.py     # Login/Register
│       ├── Products.py # Product CRUD
│       └── Orders.py   # Order management
```

## 11. Next Steps

### For Development

1. **Read Full README**: `README.md`
2. **Testing Guide**: `TESTING.md`
3. **API Documentation**: Visit `/docs`

### For Production

1. **Deployment Guide**: `DEPLOYMENT.md`
2. **Change Secret Key** in `.env`
3. **Switch to PostgreSQL** for better performance
4. **Set up HTTPS**
5. **Configure CORS** for your frontend domain

## 12. Useful Commands

```bash
# Stop the server
CTRL+C

# Deactivate virtual environment
deactivate

# View API docs in alternative format
http://localhost:8000/redoc

# Check health status
curl http://localhost:8000/health

# View Swagger JSON
curl http://localhost:8000/openapi.json
```

## 13. Connect Frontend

Update your frontend's API base URL:

```javascript
// Example: React
const API_URL = 'http://localhost:8000';

// Register
fetch(`${API_URL}/api/auth/register`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'user', password: 'pass'})
})

// Login
fetch(`${API_URL}/api/auth/login`, {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'user', password: 'pass'})
})
.then(r => r.json())
.then(d => localStorage.setItem('token', d.access_token))

// Get Products
fetch(`${API_URL}/api/products/`)

// Create Order (with auth)
fetch(`${API_URL}/api/orders/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  },
  body: JSON.stringify({items: [{product_id: 1, quantity: 2}]})
})
```

## 14. File Structure Explained

```
Backend/
├── main.py                    # FastAPI app initialization
│                             # Include routers
├── database.py               # SQLAlchemy setup
│                             # Session management
├── requirements.txt          # Python packages list
├── .env.example             # Environment template (copy to .env)
├── .gitignore               # Git ignore rules
│
├── app/
│   ├── __init__.py          # Package marker
│   ├── dependencies.py      # JWT authentication dependency
│   │
│   ├── core/
│   │   ├── config.py        # Constants (SECRET_KEY, etc)
│   │   └── security.py      # Password & JWT functions
│   │
│   ├── Models/              # Database models
│   │   ├── User.py          # User table
│   │   ├── Product.py       # Product table
│   │   ├── Order.py         # Order table
│   │   └── Orderitem.py     # Order items table
│   │
│   ├── schemas/             # Pydantic validation
│   │   ├── User.py          # User schemas
│   │   ├── Product.py       # Product schemas
│   │   ├── Order.py         # Order schemas
│   │   ├── OrderItem.py     # OrderItem schemas
│   │   └── Login.py         # Login schema
│   │
│   ├── CRUD/                # Database operations
│   │   └── Crud.py          # All CRUD functions
│   │
│   └── Router/              # API endpoints
│       ├── Auth.py          # /api/auth routes
│       ├── Products.py      # /api/products routes
│       ├── Orders.py        # /api/orders routes
│       └── Login.py         # Legacy login route
```

---

## Support

- **API Docs**: http://localhost:8000/docs
- **Full Guide**: README.md
- **Deployment**: DEPLOYMENT.md
- **Testing**: TESTING.md

Happy coding! 🚀
