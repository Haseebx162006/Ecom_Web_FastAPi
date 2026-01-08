# Quick Setup Guide

## 1. Install Dependencies

```bash
npm install
```

## 2. Create Environment File

Create a `.env` file in the root directory:

```env
REACT_APP_API_BASE_URL=http://localhost:8080
```

## 3. Start Development Server

```bash
npm start
```

The application will be available at `http://localhost:3000`

## 4. Connect to Backend

Ensure your Spring Boot backend is running on `http://localhost:8080` with the following endpoints:

### Required API Endpoints:

**Authentication:**
- `POST /api/auth/login`
- `POST /api/auth/signup`

**Products:**
- `GET /api/products`
- `GET /api/products/{id}`
- `GET /api/products?featured=true`

**Cart:**
- `GET /api/cart`
- `POST /api/cart/items`
- `PUT /api/cart/items/{id}`
- `DELETE /api/cart/items/{id}`
- `DELETE /api/cart`

**Orders:**
- `POST /api/orders`
- `GET /api/orders`
- `GET /api/orders/{id}`

## 5. Test the Application

1. Visit `http://localhost:3000`
2. Sign up for a new account
3. Browse products
4. Add items to cart
5. Complete checkout process

## Troubleshooting

- **CORS Issues**: Ensure your Spring Boot backend has CORS configured
- **API Errors**: Check browser console for detailed error messages
- **Build Issues**: Clear `node_modules` and run `npm install` again 