# API Testing Guide

This guide shows how to test all endpoints of the E-commerce FastAPI backend.

## Quick Start

### 1. Start the Server
```bash
cd Backend
uvicorn main:app --reload
```

Server will run at: `http://localhost:8000`

### 2. Access API Documentation
- **Swagger UI (Interactive)**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Test Scenarios

### Scenario 1: User Registration & Login

#### Step 1: Register a New User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123456"
  }'
```

**Expected Response (201)**:
```json
{
  "id": 1,
  "username": "testuser",
  "created_at": "2024-01-07T10:30:00.123456"
}
```

#### Step 2: Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123456"
  }'
```

**Expected Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "testuser"
}
```

**Save the token for next requests**:
```bash
TOKEN="your_access_token_here"
```

---

### Scenario 2: Product Management

#### Create a Product
```bash
curl -X POST "http://localhost:8000/api/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop for developers",
    "price": 999.99,
    "quantity": 10
  }'
```

**Expected Response (201)**:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance laptop for developers",
  "price": 999.99,
  "quantity": 10
}
```

#### Create Another Product
```bash
curl -X POST "http://localhost:8000/api/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse",
    "description": "Wireless mouse",
    "price": 29.99,
    "quantity": 50
  }'
```

#### Get All Products
```bash
curl -X GET "http://localhost:8000/api/products/"
```

**Expected Response (200)**:
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "High-performance laptop for developers",
    "price": 999.99,
    "quantity": 10
  },
  {
    "id": 2,
    "name": "Mouse",
    "description": "Wireless mouse",
    "price": 29.99,
    "quantity": 50
  }
]
```

#### Get Specific Product
```bash
curl -X GET "http://localhost:8000/api/products/1"
```

#### Update Product
```bash
curl -X PUT "http://localhost:8000/api/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 899.99,
    "quantity": 8
  }'
```

**Expected Response (200)**:
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance laptop for developers",
  "price": 899.99,
  "quantity": 8
}
```

#### Delete Product
```bash
curl -X DELETE "http://localhost:8000/api/products/3"
```

**Expected Response (200)**:
```json
{
  "message": "Product deleted successfully"
}
```

---

### Scenario 3: Order Management (Authenticated)

#### Create an Order
```bash
curl -X POST "http://localhost:8000/api/orders/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      },
      {
        "product_id": 2,
        "quantity": 3
      }
    ]
  }'
```

**Expected Response (201)**:
```json
{
  "id": 1,
  "user_id": 1,
  "total_price": 2089.97,
  "status": "Pending",
  "created_at": "2024-01-07T10:35:00.123456",
  "updated_at": "2024-01-07T10:35:00.123456",
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 1,
      "quantity": 2,
      "price": 899.99
    },
    {
      "id": 2,
      "order_id": 1,
      "product_id": 2,
      "quantity": 3,
      "price": 29.99
    }
  ]
}
```

#### Get User Orders
```bash
curl -X GET "http://localhost:8000/api/orders/" \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response (200)**:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "total_price": 2089.97,
    "status": "Pending",
    "created_at": "2024-01-07T10:35:00.123456",
    "updated_at": "2024-01-07T10:35:00.123456",
    "items": [...]
  }
]
```

#### Get Specific Order
```bash
curl -X GET "http://localhost:8000/api/orders/1" \
  -H "Authorization: Bearer $TOKEN"
```

#### Update Order Status
```bash
curl -X PUT "http://localhost:8000/api/orders/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "Processing"
  }'
```

**Valid Statuses**: `Pending`, `Processing`, `Shipped`, `Delivered`, `Cancelled`

---

## Error Test Cases

### 1. Invalid Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nonexistent",
    "password": "wrongpassword"
  }'
```

**Expected Response (401)**:
```json
{
  "detail": "Invalid credentials"
}
```

### 2. Duplicate Username
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test123456"
  }'
```

**Expected Response (400)**:
```json
{
  "detail": "Username already registered"
}
```

### 3. Missing Authentication
```bash
curl -X GET "http://localhost:8000/api/orders/"
```

**Expected Response (403)**:
```json
{
  "detail": "Not authenticated"
}
```

### 4. Non-existent Product
```bash
curl -X GET "http://localhost:8000/api/products/999"
```

**Expected Response (404)**:
```json
{
  "detail": "Product with id 999 not found"
}
```

### 5. Insufficient Stock
```bash
curl -X POST "http://localhost:8000/api/orders/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 1000
      }
    ]
  }'
```

**Expected Response (400)**:
```json
{
  "detail": "Insufficient stock for product Laptop"
}
```

### 6. Invalid Order Status
```bash
curl -X PUT "http://localhost:8000/api/orders/1/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "InvalidStatus"
  }'
```

**Expected Response (400)**:
```json
{
  "detail": "Invalid status. Must be one of: ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']"
}
```

---

## Testing with Postman

### Import Collection
1. Open Postman
2. Click "Import"
3. Use the following base URL: `http://localhost:8000`

### Create Environments
1. Create environment variable `token` from login response
2. Use `{{token}}` in Authorization headers

### Authentication Setup
1. In each request requiring auth, go to "Authorization" tab
2. Select "Bearer Token"
3. Paste your token or use `{{token}}`

---

## Testing with JavaScript/Fetch

```javascript
// Base URL
const API_URL = 'http://localhost:8000';

// Register
async function register(username, password) {
  const response = await fetch(`${API_URL}/api/auth/register`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  });
  return await response.json();
}

// Login
async function login(username, password) {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  });
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
}

// Get Products
async function getProducts() {
  const response = await fetch(`${API_URL}/api/products/`);
  return await response.json();
}

// Create Order (authenticated)
async function createOrder(items) {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_URL}/api/orders/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({items})
  });
  return await response.json();
}

// Usage
(async () => {
  // Register
  await register('user123', 'pass123');
  
  // Login
  const loginData = await login('user123', 'pass123');
  console.log('Token:', loginData.access_token);
  
  // Get products
  const products = await getProducts();
  console.log('Products:', products);
  
  // Create order
  const order = await createOrder([
    {product_id: 1, quantity: 2}
  ]);
  console.log('Order:', order);
})();
```

---

## Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

**Expected Response (200)**:
```json
{
  "status": "healthy"
}
```

---

## Performance Testing

### Load Testing with Apache Bench
```bash
# Test product listing (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:8000/api/products/
```

### Load Testing with wrk
```bash
# Install wrk first
wrk -t12 -c400 -d30s http://localhost:8000/api/products/
```

---

## Notes

- All timestamps are in UTC
- Product quantities are decremented on order creation
- Orders cannot be created without items
- Users can only view their own orders
- Tokens expire after 30 minutes (configurable in .env)

---

## Troubleshooting

### 401 Unauthorized
- Token has expired - login again
- Token is invalid or malformed
- Token not included in header

### 403 Forbidden  
- User trying to access other user's order
- Insufficient permissions

### 500 Internal Server Error
- Check server logs
- Verify database connection
- Verify all imports are correct

### Database Locked (SQLite)
- Close other connections to the database
- Consider using PostgreSQL for production
