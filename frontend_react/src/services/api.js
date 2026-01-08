import axios from 'axios';

// Create axios instance with base configuration
// Default to backend on port 8000; can be overridden by REACT_APP_API_BASE_URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  // backend register endpoint is /api/auth/register
  signup: (userData) => api.post('/api/auth/register', userData),
  logout: () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  },
};

// Products API calls
export const productsAPI = {
  getAllProducts: () => api.get('/api/products'),
  getProductById: (id) => api.get(`/api/products/${id}`),
  getFeaturedProducts: () => api.get('/api/products?featured=true'),
  // Create product with optional image upload (multipart/form-data)
  createProduct: (product) => {
    const formData = new FormData();
    if (product?.name) formData.append('name', product.name);
    if (product?.description) formData.append('description', product.description);
    if (product?.price !== undefined && product?.price !== null) formData.append('price', String(product.price));
    // Backend uses 'quantity' not 'stock'
    if (product?.quantity !== undefined && product?.quantity !== null) {
      formData.append('quantity', String(product.quantity));
    } else if (product?.stock !== undefined && product?.stock !== null) {
      formData.append('quantity', String(product.stock));
    }
    if (product?.category) formData.append('category', product.category);
    if (product?.featured !== undefined && product?.featured !== null) formData.append('featured', String(!!product.featured));
    if (product?.imageFile) formData.append('image', product.imageFile);
    if (product?.imageUrl) formData.append('imageUrl', product.imageUrl);

    return api.post('/api/products', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

// Cart API calls
export const cartAPI = {
  getCart: () => api.get('/api/cart'),
  addToCart: (productId, quantity = 1) => 
    api.post('/api/cart/items', { product_id: productId, quantity }),
  updateCartItem: (itemId, quantity) => 
    api.put(`/api/cart/items/${itemId}`, { quantity }),
  removeFromCart: (itemId) => api.delete(`/api/cart/items/${itemId}`),
  clearCart: () => api.delete('/api/cart'),
};

// Orders API calls
export const ordersAPI = {
  createOrder: (orderData) => {
    // Convert frontend format (productId) to backend format
    const backendOrderData = {
      items: orderData.items.map(item => ({
        productId: item.productId || item.product_id,
        quantity: item.quantity
      }))
    };
    return api.post('/api/orders', backendOrderData);
  },
  getOrders: () => api.get('/api/orders'),
  getOrderById: (id) => api.get(`/api/orders/${id}`),
};

export default api; 