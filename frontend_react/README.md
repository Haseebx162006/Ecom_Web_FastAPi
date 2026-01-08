# E-Commerce React Frontend

A modern, responsive React e-commerce frontend application built with React 18, Tailwind CSS, and Context API for state management. This application connects to a Spring Boot backend to provide a complete e-commerce experience.

## Features

- 🛍️ **Product Browsing**: Browse products with search and filtering capabilities
- 🛒 **Shopping Cart**: Add, remove, and update cart items
- 👤 **User Authentication**: Login and signup functionality
- 💳 **Checkout Process**: Complete order placement with shipping information
- 📱 **Responsive Design**: Mobile-friendly interface
- 🎨 **Modern UI**: Clean, modern design with Tailwind CSS
- 🔄 **Real-time Updates**: Live cart updates and state management

## Tech Stack

- **React 18** - Latest React with functional components and hooks
- **React Router v6** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Context API** - Global state management
- **Local Storage** - Persistent authentication state

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── LoadingSpinner.js
│   ├── ProductCard.js
│   ├── Navbar.js
│   └── Footer.js
├── context/            # Global state management
│   ├── AuthContext.js
│   └── CartContext.js
├── pages/              # Page components
│   ├── HomePage.js
│   ├── ProductsPage.js
│   ├── ProductDetailPage.js
│   ├── CartPage.js
│   ├── CheckoutPage.js
│   ├── LoginPage.js
│   └── SignupPage.js
├── services/           # API services
│   └── api.js
├── App.js             # Main app component
├── index.js           # App entry point
└── index.css          # Global styles
```

## API Endpoints

The frontend expects the following Spring Boot backend endpoints:

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration

### Products
- `GET /api/products` - Get all products
- `GET /api/products/{id}` - Get product by ID
- `GET /api/products?featured=true` - Get featured products

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart/items` - Add item to cart
- `PUT /api/cart/items/{id}` - Update cart item quantity
- `DELETE /api/cart/items/{id}` - Remove item from cart
- `DELETE /api/cart` - Clear cart

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders` - Get user's orders
- `GET /api/orders/{id}` - Get order by ID

## Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   REACT_APP_API_BASE_URL=http://localhost:8080
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

   The application will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

## Configuration

### Backend API URL

Update the API base URL in the `.env` file:

```env
REACT_APP_API_BASE_URL=http://localhost:8080
```

### Tailwind CSS Configuration

The project uses Tailwind CSS with a custom color scheme. You can modify the colors in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        50: '#eff6ff',
        100: '#dbeafe',
        // ... other shades
        900: '#1e3a8a',
      },
    },
  },
},
```

## Usage

### Authentication

1. **Sign Up**: Create a new account at `/signup`
2. **Login**: Sign in with your credentials at `/login`
3. **Logout**: Click the logout button in the navbar

### Shopping

1. **Browse Products**: Visit `/products` to see all available products
2. **Product Details**: Click on any product to view details
3. **Add to Cart**: Use the "Add to Cart" button on product pages
4. **Manage Cart**: Visit `/cart` to update quantities or remove items
5. **Checkout**: Complete your order at `/checkout`

## Key Features

### State Management

- **AuthContext**: Manages user authentication state
- **CartContext**: Handles shopping cart operations
- **Local Storage**: Persists authentication tokens and user data

### Error Handling

- API error responses are displayed to users
- Loading states for all async operations
- Graceful fallbacks for missing data

### Responsive Design

- Mobile-first approach
- Responsive grid layouts
- Touch-friendly interface elements

## Customization

### Adding New Pages

1. Create a new component in `src/pages/`
2. Add the route in `src/App.js`
3. Update navigation in `src/components/Navbar.js`

### Styling

- Use Tailwind CSS classes for styling
- Custom colors are defined in `tailwind.config.js`
- Component-specific styles can be added inline

### API Integration

- All API calls are centralized in `src/services/api.js`
- Add new endpoints as needed
- Update error handling for new endpoints

## Troubleshooting

### Common Issues

1. **API Connection Error**
   - Ensure your Spring Boot backend is running
   - Check the API base URL in `.env`
   - Verify CORS configuration on the backend

2. **Authentication Issues**
   - Clear browser localStorage
   - Check token format in API responses
   - Verify authentication endpoints

3. **Build Errors**
   - Clear `node_modules` and reinstall
   - Check for missing dependencies
   - Verify React version compatibility

### Development Tips

- Use React Developer Tools for debugging
- Check browser console for API errors
- Monitor network tab for request/response details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support or questions, please open an issue in the repository or contact the development team. 