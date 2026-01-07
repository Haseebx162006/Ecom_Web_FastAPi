"# E-commerce FastAPI Backend

A complete, production-ready e-commerce backend API built with FastAPI, SQLAlchemy, and PostgreSQL/MySQL/SQLite.

## Features

✅ **User Authentication & Authorization**
- User registration and login
- JWT token-based authentication
- Secure password hashing with bcrypt

✅ **Product Management**
- Create, read, update, delete products
- Product inventory management
- Complete CRUD endpoints

✅ **Order Management**
- Create orders with multiple items
- Order tracking and status updates
- Order history for users
- Automatic inventory updates

✅ **Database**
- SQLAlchemy ORM
- Support for SQLite, PostgreSQL, MySQL
- Automatic table creation
- Relational data models

✅ **API Features**
- Interactive API documentation (Swagger UI)
- CORS support for frontend integration
- Comprehensive error handling
- Input validation with Pydantic

---

## Project Structure

```
Backend/
├── main.py                  # Application entry point
├── database.py             # Database configuration
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── app/
│   ├── __init__.py
│   ├── dependencies.py     # JWT dependency for protected routes
│   ├── core/
│   │   ├── config.py       # Configuration constants
│   │   ├── security.py     # Password hashing & JWT operations
│   │   └── __init__.py
│   ├── Models/
│   │   ├── User.py         # User model
│   │   ├── Product.py      # Product model
│   │   ├── Order.py        # Order model
│   │   ├── Orderitem.py    # Order Item model
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── User.py         # User validation schemas
│   │   ├── Product.py      # Product validation schemas
│   │   ├── Order.py        # Order validation schemas
│   │   ├── OrderItem.py    # Order Item validation schemas
│   │   ├── Login.py        # Login validation schema
│   │   ├── Cart.py         # Cart validation schemas
│   │   └── __init__.py
│   ├── CRUD/
│   │   ├── Crud.py         # Database operations
│   │   └── __init__.py
│   └── Router/
│       ├── Auth.py         # Authentication endpoints
│       ├── Products.py     # Product endpoints
│       ├── Orders.py       # Order endpoints
│       ├── Login.py        # Login endpoint (deprecated - use Auth.py)
│       └── __init__.py
```

---

## Installation

### Prerequisites
- Python 3.8+
- pip or conda
- Virtual environment (recommended)

### Setup Steps

1. **Create and activate virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create .env file from template**
```bash
cp .env.example .env
```

4. **Configure database** (edit `.env`)
```
# For development with SQLite
DATABASE_URL=sqlite:///./ecommerce.db

# For PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_db

# For MySQL
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/ecommerce_db
```

5. **Run the application**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

---

## API Endpoints

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "created_at": "2024-01-07T10:30:00"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "john_doe"
}
```

---

### Product Endpoints

#### Create Product
```http
POST /api/products/
Content-Type: application/json

{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "quantity": 10
}
```

#### Get All Products
```http
GET /api/products/
```

#### Get Product by ID
```http
GET /api/products/{product_id}
```

#### Update Product
```http
PUT /api/products/{product_id}
Content-Type: application/json

{
  "name": "Updated Laptop",
  "price": 1099.99,
  "quantity": 8
}
```

#### Delete Product
```http
DELETE /api/products/{product_id}
```

---

### Order Endpoints

All order endpoints require authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

#### Create Order
```http
POST /api/orders/
Content-Type: application/json

{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "total_price": 2199.97,
  "status": "Pending",
  "created_at": "2024-01-07T10:35:00",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 999.99
    }
  ]
}
```

#### Get User Orders
```http
GET /api/orders/
```

#### Get Specific Order
```http
GET /api/orders/{order_id}
```

#### Update Order Status
```http
PUT /api/orders/{order_id}/status
Content-Type: application/json

{
  "status": "Processing"
}
```

Valid statuses: `Pending`, `Processing`, `Shipped`, `Delivered`, `Cancelled`

---

## Database Models

### User Model
```python
- id: Integer (Primary Key)
- username: String (Unique, Required)
- hashed_password: String (Required)
- is_active: Boolean (Default: True)
- created_at: DateTime
- orders: Relationship (One-to-Many)
```

### Product Model
```python
- id: Integer (Primary Key)
- name: String (Required)
- description: String
- price: Float (Required)
- quantity: Integer (Required)
- order_items: Relationship (One-to-Many)
```

### Order Model
```python
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key)
- total_price: Float (Required)
- status: String (Default: "Pending")
- created_at: DateTime
- updated_at: DateTime
- items: Relationship (One-to-Many)
- user: Relationship (Many-to-One)
```

### OrderItem Model
```python
- id: Integer (Primary Key)
- order_id: Integer (Foreign Key)
- product_id: Integer (Foreign Key)
- quantity: Integer (Required)
- price: Float (Required)
- order: Relationship (Many-to-One)
- product: Relationship (Many-to-One)
```

---

## Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### How to use:

1. **Get Token**: Call `/api/auth/login` with credentials
2. **Include Token**: Add to request header:
   ```
   Authorization: Bearer <your_token>
   ```
3. **Protected Routes**: Endpoints requiring auth will automatically verify the token

### Token Expiration:
- Default: 30 minutes
- Can be changed in `.env` file: `ACCESS_TOKEN_EXPIRE=60`

---

## Testing the API

### Using Swagger UI (Interactive)
1. Start the server: `uvicorn main:app --reload`
2. Open: `http://localhost:8000/docs`
3. Use the "Authorize" button to add your JWT token
4. Test all endpoints directly in the UI

### Using curl

```bash
# Register
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get Products (no auth required)
curl -X GET "http://localhost:8000/api/products/"

# Create Order (requires auth)
curl -X POST "http://localhost:8000/api/orders/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items":[{"product_id":1,"quantity":2}]}'
```

### Using Postman
1. Import the API endpoints
2. In the Authorization tab, select "Bearer Token"
3. Paste your JWT token
4. Make requests to protected endpoints

---

## Environment Variables

Create a `.env` file in the `Backend` directory:

```env
# Database
DATABASE_URL=sqlite:///./ecommerce.db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30
```

**Important**: Never commit `.env` file to version control. Use `.env.example` instead.

---

## Dependencies

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
passlib==1.7.4
python-jose==3.3.0
bcrypt==4.1.1
python-multipart==0.0.6
python-dotenv==1.0.0
```

---

## Error Handling

The API returns standard HTTP status codes and descriptive error messages:

```json
{
  "detail": "Error description here"
}
```

### Common Status Codes:
- `200`: OK
- `201`: Created
- `400`: Bad Request (Invalid input)
- `401`: Unauthorized (Invalid/missing token)
- `403`: Forbidden (Not authorized)
- `404`: Not Found (Resource doesn't exist)
- `409`: Conflict (Duplicate username, etc.)
- `500`: Internal Server Error

---

## Security Best Practices

1. **Change Secret Key in Production**
   - Generate a new secret key
   - Use a cryptographically secure random string
   - Store it in environment variables

2. **Use HTTPS**
   - Always use HTTPS in production
   - Never send tokens over HTTP

3. **Token Management**
   - Store tokens securely on the client
   - Use httpOnly cookies if possible
   - Implement token refresh mechanism for long sessions

4. **CORS Configuration**
   - Update allowed origins in `main.py`
   - Don't use `allow_origins=["*"]` in production

5. **Database Security**
   - Use strong database passwords
   - Never commit credentials to version control
   - Use environment variables for all secrets

6. **Input Validation**
   - All inputs are validated with Pydantic
   - Avoid SQL injection with ORM

---

## Frontend Integration

### Example: Login and Store Token (JavaScript)

```javascript
// Register
fetch('http://localhost:8000/api/auth/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'user', password: 'pass'})
})

// Login
fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({username: 'user', password: 'pass'})
})
.then(res => res.json())
.then(data => {
  localStorage.setItem('token', data.access_token)
})

// Protected Request
fetch('http://localhost:8000/api/orders/', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
})
```

---

## Troubleshooting

### Import Errors
- Ensure all packages are installed: `pip install -r requirements.txt`
- Check that virtual environment is activated

### Database Connection Error
- Verify DATABASE_URL in `.env`
- For SQLite: Ensure directory exists
- For PostgreSQL/MySQL: Check server is running and credentials are correct

### CORS Issues
- Update `allow_origins` in `main.py` with your frontend URL
- Example: `allow_origins=["http://localhost:3000"]`

### Token Expiration
- Request a new token by logging in again
- Or increase `ACCESS_TOKEN_EXPIRE` in `.env`

---

## Future Enhancements

- [ ] Email verification on registration
- [ ] Password reset functionality
- [ ] Admin dashboard
- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] Product reviews and ratings
- [ ] Wishlist feature
- [ ] Search and filtering
- [ ] Pagination for large datasets
- [ ] Rate limiting and throttling

---

## License

This project is open source and available under the MIT License.

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review FastAPI documentation: https://fastapi.tiangolo.com/
3. Check SQLAlchemy documentation: https://docs.sqlalchemy.org/

---

## Version History

### v1.0.0 (Current)
- Initial release
- User authentication with JWT
- Complete product management
- Order management system
- API documentation with Swagger UI" 
