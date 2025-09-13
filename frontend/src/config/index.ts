/**
 * Configuration Management for Restaurant Web UI
 * Centralizes all environment-based configuration
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  VERSION: process.env.NEXT_PUBLIC_API_VERSION || 'v1',
  TIMEOUT: parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '30000'),
  
  // Endpoint configurations
  ENDPOINTS: {
    AUTH: process.env.NEXT_PUBLIC_AUTH_ENDPOINT || '/api/v1/auth',
    RESTAURANTS: process.env.NEXT_PUBLIC_RESTAURANTS_ENDPOINT || '/api/v1/restaurants',
    MENU: process.env.NEXT_PUBLIC_MENU_ENDPOINT || '/api/v1/restaurants',
    ORDERS: process.env.NEXT_PUBLIC_ORDERS_ENDPOINT || '/api/v1/orders',
    STAFF: process.env.NEXT_PUBLIC_STAFF_ENDPOINT || '/api/v1/restaurants',
  },
} as const;

// Application Configuration
export const APP_CONFIG = {
  NAME: process.env.NEXT_PUBLIC_APP_NAME || 'Restaurant Management',
  VERSION: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
  DESCRIPTION: process.env.NEXT_PUBLIC_APP_DESCRIPTION || 'Mobile & Tablet Optimized Restaurant Management Interface',
  ENVIRONMENT: process.env.NEXT_PUBLIC_ENV || 'development',
} as const;

// Authentication Configuration
export const AUTH_CONFIG = {
  TOKEN_STORAGE_KEY: process.env.NEXT_PUBLIC_TOKEN_STORAGE_KEY || 'restaurant_auth_token',
  REFRESH_TOKEN_KEY: process.env.NEXT_PUBLIC_REFRESH_TOKEN_KEY || 'restaurant_refresh_token',
  SESSION_TIMEOUT: parseInt(process.env.NEXT_PUBLIC_SESSION_TIMEOUT || '1800000'), // 30 minutes
  AUTO_LOGOUT_WARNING: parseInt(process.env.NEXT_PUBLIC_AUTO_LOGOUT_WARNING || '300000'), // 5 minutes
} as const;

// UI Theme Configuration
export const THEME_CONFIG = {
  THEME: process.env.NEXT_PUBLIC_THEME || 'restaurant',
  COLORS: {
    PRIMARY: process.env.NEXT_PUBLIC_PRIMARY_COLOR || '#FF6B35',
    SECONDARY: process.env.NEXT_PUBLIC_SECONDARY_COLOR || '#2C3E50',
    SUCCESS: process.env.NEXT_PUBLIC_SUCCESS_COLOR || '#27AE60',
    WARNING: process.env.NEXT_PUBLIC_WARNING_COLOR || '#F39C12',
    ERROR: process.env.NEXT_PUBLIC_ERROR_COLOR || '#E74C3C',
  },
} as const;

// Device Breakpoints Configuration
export const BREAKPOINTS = {
  MOBILE: parseInt(process.env.NEXT_PUBLIC_MOBILE_BREAKPOINT || '768'),
  TABLET: parseInt(process.env.NEXT_PUBLIC_TABLET_BREAKPOINT || '1024'),
  DESKTOP: parseInt(process.env.NEXT_PUBLIC_DESKTOP_BREAKPOINT || '1280'),
} as const;

// Performance Configuration
export const PERFORMANCE_CONFIG = {
  IMAGE_OPTIMIZATION: process.env.NEXT_PUBLIC_IMAGE_OPTIMIZATION === 'true',
  LAZY_LOADING: process.env.NEXT_PUBLIC_LAZY_LOADING === 'true',
  SERVICE_WORKER: process.env.NEXT_PUBLIC_SERVICE_WORKER === 'true',
  OFFLINE_SUPPORT: process.env.NEXT_PUBLIC_OFFLINE_SUPPORT === 'true',
} as const;

// Feature Flags Configuration
export const FEATURE_FLAGS = {
  QR_ORDERING: process.env.NEXT_PUBLIC_ENABLE_QR_ORDERING === 'true',
  DARK_MODE: process.env.NEXT_PUBLIC_ENABLE_DARK_MODE === 'true',
  ANALYTICS: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
  PUSH_NOTIFICATIONS: process.env.NEXT_PUBLIC_ENABLE_PUSH_NOTIFICATIONS === 'true',
} as const;

// Development Configuration
export const DEV_CONFIG = {
  ENABLE_DEVTOOLS: process.env.NEXT_PUBLIC_ENABLE_DEVTOOLS === 'true',
  DEBUG_MODE: process.env.NEXT_PUBLIC_DEBUG_MODE === 'true',
  MOCK_API: process.env.NEXT_PUBLIC_MOCK_API === 'true',
} as const;

// PWA Configuration
export const PWA_CONFIG = {
  NAME: process.env.NEXT_PUBLIC_PWA_NAME || 'Restaurant Manager',
  SHORT_NAME: process.env.NEXT_PUBLIC_PWA_SHORT_NAME || 'RestaurantMgr',
  DESCRIPTION: process.env.NEXT_PUBLIC_PWA_DESCRIPTION || 'Mobile restaurant management interface',
  THEME_COLOR: process.env.NEXT_PUBLIC_PWA_THEME_COLOR || '#FF6B35',
  BACKGROUND_COLOR: process.env.NEXT_PUBLIC_PWA_BACKGROUND_COLOR || '#FFFFFF',
} as const;

// File Upload Configuration
export const UPLOAD_CONFIG = {
  MAX_FILE_SIZE: parseInt(process.env.NEXT_PUBLIC_MAX_FILE_SIZE || '5242880'), // 5MB
  ALLOWED_IMAGE_TYPES: (process.env.NEXT_PUBLIC_ALLOWED_IMAGE_TYPES || 'image/jpeg,image/png,image/webp').split(','),
  IMAGE_QUALITY: parseInt(process.env.NEXT_PUBLIC_IMAGE_QUALITY || '80'),
} as const;

// Validation helpers
export const isProduction = () => APP_CONFIG.ENVIRONMENT === 'production';
export const isDevelopment = () => APP_CONFIG.ENVIRONMENT === 'development';
export const isDebugMode = () => DEV_CONFIG.DEBUG_MODE && isDevelopment();

// API URL builders
export const buildApiUrl = (endpoint: string) => `${API_CONFIG.BASE_URL}${endpoint}`;
export const buildAuthUrl = (path: string) => `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.AUTH}${path}`;
export const buildRestaurantUrl = (restaurantId: string, path: string = '') => 
  `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.RESTAURANTS}/${restaurantId}${path}`;

// Configuration validation (runs at startup)
export const validateConfig = () => {
  const requiredConfigs = [
    { key: 'API_BASE_URL', value: API_CONFIG.BASE_URL },
    { key: 'APP_NAME', value: APP_CONFIG.NAME },
  ];
  
  const missing = requiredConfigs.filter(({ value }) => !value);
  
  if (missing.length > 0 && isDevelopment()) {
    console.warn('Missing required configuration:', missing.map(({ key }) => key));
  }
  
  return missing.length === 0;
};

// Export all configurations as a single object for convenience
export const CONFIG = {
  API: API_CONFIG,
  APP: APP_CONFIG,
  AUTH: AUTH_CONFIG,
  THEME: THEME_CONFIG,
  BREAKPOINTS,
  PERFORMANCE: PERFORMANCE_CONFIG,
  FEATURES: FEATURE_FLAGS,
  DEV: DEV_CONFIG,
  PWA: PWA_CONFIG,
  UPLOAD: UPLOAD_CONFIG,
} as const;

export default CONFIG;