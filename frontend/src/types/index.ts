/**
 * TypeScript Type Definitions for Restaurant Web UI
 */

// =================================================================
// AUTHENTICATION TYPES
// =================================================================

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  phone_number?: string;
  role: UserRole;
  staff_type?: StaffType;
  restaurant_id?: string;
  is_active: boolean;
  is_verified: boolean;
  last_login_at?: string;
  permissions?: Record<string, boolean>;
  preferences?: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LoginCredentials {
  username: string; // email
  password: string;
}

export interface AuthResponse {
  success: boolean;
  data?: {
    user: User;
    tokens?: AuthTokens;
  };
  message?: string;
  error?: string;
}

// =================================================================
// RESTAURANT TYPES
// =================================================================

export interface Restaurant {
  id: string;
  restaurant_name: string;
  restaurant_code: string;
  business_email: string;
  phone_number?: string;
  website_url?: string;
  address?: Address;
  currency_code: string;
  tax_rate: number;
  service_charge_rate: number;
  timezone: string;
  operating_hours?: OperatingHours;
  allows_takeout: boolean;
  allows_delivery: boolean;
  allows_reservations: boolean;
  delivery_radius_km?: number;
  minimum_delivery_amount?: number;
  status: RestaurantStatus;
  subscription_tier: SubscriptionTier;
  subscription_expires_at?: string;
  logo_url?: string;
  banner_url?: string;
  theme_color?: string;
  settings?: Record<string, any>;
  created_at: string;
  updated_at?: string;
}

export interface Address {
  street?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  coordinates?: {
    latitude: number;
    longitude: number;
  };
}

export interface OperatingHours {
  [key: string]: {
    open: string;
    close: string;
    is_closed: boolean;
  };
}

// =================================================================
// MENU TYPES
// =================================================================

export interface MenuCategory {
  id: string;
  restaurant_id: string;
  category_name: string;
  description?: string;
  image_url?: string;
  display_order: number;
  is_active: boolean;
  available_all_day: boolean;
  available_from?: string;
  available_until?: string;
  created_at: string;
  updated_at?: string;
  items?: MenuItem[];
  item_count?: number;
}

export interface MenuItem {
  id: string;
  restaurant_id: string;
  category_id?: string;
  category?: {
    id: string;
    name: string;
  };
  item_name: string;
  description?: string;
  price: number;
  cost_price?: number;
  prep_time_minutes: number;
  is_vegetarian: boolean;
  is_vegan: boolean;
  is_gluten_free: boolean;
  is_spicy: boolean;
  spice_level: number;
  calories?: number;
  is_available: boolean;
  image_url?: string;
  is_featured: boolean;
  is_popular: boolean;
  display_order: number;
  profit_margin?: number;
  profit_margin_percent?: number;
  options?: MenuItemOption[];
  created_at: string;
  updated_at?: string;
}

export interface MenuItemOption {
  id: string;
  restaurant_id: string;
  item_id: string;
  option_group: string;
  option_name: string;
  price_change: number;
  is_default: boolean;
  is_active: boolean;
  display_order: number;
  created_at: string;
}

// =================================================================
// ORDER TYPES
// =================================================================

export interface Order {
  id: string;
  restaurant_id: string;
  table_id?: string;
  guest_session_id?: string;
  served_by_user_id?: string;
  order_number: string;
  order_type: OrderType;
  order_status: OrderStatus;
  payment_status: PaymentStatus;
  guest_name?: string;
  guest_phone?: string;
  guest_email?: string;
  party_size: number;
  special_instructions?: string;
  subtotal: number;
  tax_amount: number;
  service_charge: number;
  discount_amount: number;
  total_amount: number;
  ordered_at: string;
  estimated_ready_time?: string;
  ready_at?: string;
  completed_at?: string;
  items: OrderItem[];
  table?: RestaurantTable;
  created_at: string;
  updated_at?: string;
}

export interface OrderItem {
  id: string;
  restaurant_id: string;
  order_id: string;
  menu_item_id: string;
  item_name: string;
  item_description?: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  item_status: ItemStatus;
  special_instructions?: string;
  selected_options?: Record<string, any>;
  menu_item?: MenuItem;
  created_at: string;
}

// =================================================================
// TABLE TYPES
// =================================================================

export interface RestaurantTable {
  id: string;
  restaurant_id: string;
  table_number: string;
  table_name?: string;
  capacity: number;
  location?: string;
  qr_code: string;
  qr_code_url?: string;
  qr_code_image_url?: string;
  is_active: boolean;
  requires_reservation: boolean;
  is_vip: boolean;
  position_x?: number;
  position_y?: number;
  has_power_outlet: boolean;
  has_view: boolean;
  is_wheelchair_accessible: boolean;
  current_status: string;
  created_at: string;
  updated_at?: string;
}

export interface GuestSession {
  id: string;
  restaurant_id: string;
  table_id: string;
  session_token: string;
  guest_name?: string;
  guest_phone?: string;
  guest_email?: string;
  party_size: number;
  special_requests?: string;
  cart_data?: Record<string, any>;
  preferences?: Record<string, any>;
  expires_at: string;
  is_active: boolean;
  table?: RestaurantTable;
  created_at: string;
  updated_at?: string;
}

// =================================================================
// ENUMS
// =================================================================

export enum UserRole {
  ADMIN = 'ADMIN',
  OWNER = 'OWNER',
  MANAGER = 'MANAGER',
  STAFF = 'STAFF',
  CUSTOMER = 'CUSTOMER',
}

export enum StaffType {
  OWNER = 'OWNER',
  MANAGER = 'MANAGER',
  HEAD_CHEF = 'HEAD_CHEF',
  CHEF = 'CHEF',
  WAITER = 'WAITER',
  CASHIER = 'CASHIER',
  HOST = 'HOST',
  BARTENDER = 'BARTENDER',
  KITCHEN = 'KITCHEN',
  CLEANER = 'CLEANER',
  DELIVERY = 'DELIVERY',
}

export enum RestaurantStatus {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  SUSPENDED = 'SUSPENDED',
  PENDING = 'PENDING',
  CLOSED = 'CLOSED',
}

export enum SubscriptionTier {
  TRIAL = 'TRIAL',
  BASIC = 'BASIC',
  PREMIUM = 'PREMIUM',
  ENTERPRISE = 'ENTERPRISE',
}

export enum OrderStatus {
  PENDING = 'PENDING',
  CONFIRMED = 'CONFIRMED',
  PREPARING = 'PREPARING',
  READY = 'READY',
  SERVED = 'SERVED',
  COMPLETED = 'COMPLETED',
  CANCELLED = 'CANCELLED',
  REFUNDED = 'REFUNDED',
}

export enum PaymentStatus {
  PENDING = 'PENDING',
  PROCESSING = 'PROCESSING',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
  CANCELLED = 'CANCELLED',
  REFUNDED = 'REFUNDED',
}

export enum OrderType {
  DINE_IN = 'DINE_IN',
  TAKEOUT = 'TAKEOUT',
  DELIVERY = 'DELIVERY',
  CATERING = 'CATERING',
}

export enum ItemStatus {
  ORDERED = 'ORDERED',
  PREPARING = 'PREPARING',
  READY = 'READY',
  SERVED = 'SERVED',
  CANCELLED = 'CANCELLED',
}

export enum PaymentMethod {
  CASH = 'CASH',
  CARD = 'CARD',
  DIGITAL_WALLET = 'DIGITAL_WALLET',
  BANK_TRANSFER = 'BANK_TRANSFER',
  CRYPTO = 'CRYPTO',
}

// =================================================================
// API RESPONSE TYPES
// =================================================================

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginationMeta {
  total: number;
  page: number;
  size: number;
  pages: number;
}

// Fixed: Create a separate interface that doesn't extend ApiResponse
export interface PaginatedResponse<T> {
  success: boolean;
  data: {
    items: T[];
    pagination: PaginationMeta;
  };
  message?: string;
  error?: string;
}

// Alternative approach for paginated data structure
export interface PaginatedData<T> {
  items: T[];
  pagination: PaginationMeta;
}

// =================================================================
// FORM TYPES
// =================================================================

export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'tel' | 'number' | 'textarea' | 'select' | 'checkbox' | 'radio';
  required?: boolean;
  placeholder?: string;
  options?: { label: string; value: string | number }[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
    message?: string;
  };
}

export interface FormErrors {
  [key: string]: string | string[];
}

// =================================================================
// UTILITY TYPES
// =================================================================

export interface LoadingState {
  isLoading: boolean;
  error?: string | null;
}

export interface DeviceInfo {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  orientation: 'portrait' | 'landscape';
  screenWidth: number;
  screenHeight: number;
}

export interface NotificationOptions {
  id?: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
  position?: 'top' | 'bottom';
  action?: {
    label: string;
    callback: () => void;
  };
}

// =================================================================
// COMPONENT PROP TYPES
// =================================================================

export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
  id?: string;
}

export interface ButtonProps extends BaseComponentProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}

// =================================================================
// GLOBAL APP STATE TYPES
// =================================================================

export interface AppState {
  auth: {
    user: User | null;
    tokens: AuthTokens | null;
    isAuthenticated: boolean;
    isLoading: boolean;
  };
  restaurant: {
    current: Restaurant | null;
    isLoading: boolean;
  };
  ui: {
    theme: 'light' | 'dark';
    sidebarOpen: boolean;
    notifications: NotificationOptions[];
  };
  device: DeviceInfo;
}

export default {};