'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { User, AuthTokens } from '@/types';
import { CONFIG } from '@/config';
import Cookies from 'js-cookie';

// =================================================================
// AUTH STATE TYPES
// =================================================================

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; tokens: AuthTokens } }
  | { type: 'LOGOUT' }
  | { type: 'UPDATE_USER'; payload: User }
  | { type: 'UPDATE_TOKENS'; payload: AuthTokens }
  | { type: 'CLEAR_ERROR' };

// =================================================================
// AUTH CONTEXT
// =================================================================

interface AuthContextType {
  state: AuthState;
  dispatch: React.Dispatch<AuthAction>;
  // Convenience methods
  login: (user: User, tokens: AuthTokens) => void;
  logout: () => void;
  updateUser: (user: User) => void;
  updateTokens: (tokens: AuthTokens) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
  isOwnerOrManager: () => boolean;
  hasPermission: (permission: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// =================================================================
// AUTH REDUCER
// =================================================================

const initialState: AuthState = {
  user: null,
  tokens: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: action.payload,
      };

    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        isLoading: false,
      };

    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        tokens: action.payload.tokens,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };

    case 'LOGOUT':
      return {
        ...state,
        user: null,
        tokens: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };

    case 'UPDATE_USER':
      return {
        ...state,
        user: action.payload,
      };

    case 'UPDATE_TOKENS':
      return {
        ...state,
        tokens: action.payload,
      };

    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };

    default:
      return state;
  }
}

// =================================================================
// STORAGE HELPERS
// =================================================================

const getStoredTokens = (): AuthTokens | null => {
  if (typeof window === 'undefined') return null;

  try {
    const accessToken = localStorage.getItem(CONFIG.AUTH.TOKEN_STORAGE_KEY);
    const refreshToken = localStorage.getItem(CONFIG.AUTH.REFRESH_TOKEN_KEY);

    if (accessToken && refreshToken) {
      return {
        access_token: accessToken,
        refresh_token: refreshToken,
        token_type: 'bearer',
        expires_in: 0, // Will be refreshed
      };
    }
  } catch (error) {
    console.error('Error reading tokens from storage:', error);
  }

  return null;
};

const storeTokens = (tokens: AuthTokens): void => {
  if (typeof window === 'undefined') return;

  try {
    localStorage.setItem(CONFIG.AUTH.TOKEN_STORAGE_KEY, tokens.access_token);
    localStorage.setItem(CONFIG.AUTH.REFRESH_TOKEN_KEY, tokens.refresh_token);
  } catch (error) {
    console.error('Error storing tokens:', error);
  }
};

const clearStoredTokens = (): void => {
  if (typeof window === 'undefined') return;

  try {
    localStorage.removeItem(CONFIG.AUTH.TOKEN_STORAGE_KEY);
    localStorage.removeItem(CONFIG.AUTH.REFRESH_TOKEN_KEY);
  } catch (error) {
    console.error('Error clearing tokens:', error);
  }
};

const getStoredUser = (): User | null => {
  if (typeof window === 'undefined') return null;

  try {
    const userData = localStorage.getItem('restaurant_user_data');
    return userData ? JSON.parse(userData) : null;
  } catch (error) {
    console.error('Error reading user data from storage:', error);
    return null;
  }
};

const storeUser = (user: User): void => {
  if (typeof window === 'undefined') return;

  try {
    localStorage.setItem('restaurant_user_data', JSON.stringify(user));
  } catch (error) {
    console.error('Error storing user data:', error);
  }
};

const clearStoredUser = (): void => {
  if (typeof window === 'undefined') return;

  try {
    localStorage.removeItem('restaurant_user_data');
  } catch (error) {
    console.error('Error clearing user data:', error);
  }
};

// =================================================================
// AUTH PROVIDER COMPONENT
// =================================================================

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Initialize auth state from storage
  useEffect(() => {
    const initializeAuth = async () => {
      dispatch({ type: 'SET_LOADING', payload: true });

      try {
        const storedTokens = getStoredTokens();
        const storedUser = getStoredUser();

        if (storedTokens && storedUser) {
          // TODO: Validate tokens with backend
          dispatch({
            type: 'LOGIN_SUCCESS',
            payload: {
              user: storedUser,
              tokens: storedTokens,
            },
          });
        } else {
          dispatch({ type: 'SET_LOADING', payload: false });
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    };

    initializeAuth();
  }, []);

  // Auto-logout on session timeout
  useEffect(() => {
    if (!state.isAuthenticated || !state.user) return;

    const sessionTimeout = CONFIG.AUTH.SESSION_TIMEOUT;
    const warningTimeout = CONFIG.AUTH.AUTO_LOGOUT_WARNING;

    // Set warning timer
    const warningTimer = setTimeout(() => {
      // TODO: Show session expiry warning modal
      console.warn('Session will expire soon');
    }, sessionTimeout - warningTimeout);

    // Set logout timer
    const logoutTimer = setTimeout(() => {
      dispatch({ type: 'LOGOUT' });
      clearStoredTokens();
      clearStoredUser();
    }, sessionTimeout);

    return () => {
      clearTimeout(warningTimer);
      clearTimeout(logoutTimer);
    };
  }, [state.isAuthenticated, state.user]);

  // Convenience methods
  const login = (user: User, tokens: AuthTokens) => {
    dispatch({ type: 'LOGIN_SUCCESS', payload: { user, tokens } });
    storeUser(user);
    storeTokens(tokens);
  };

  const logout = () => {
    dispatch({ type: 'LOGOUT' });
    clearStoredTokens();
    clearStoredUser();
  };

  const updateUser = (user: User) => {
    dispatch({ type: 'UPDATE_USER', payload: user });
    storeUser(user);
  };

  const updateTokens = (tokens: AuthTokens) => {
    dispatch({ type: 'UPDATE_TOKENS', payload: tokens });
    storeTokens(tokens);
  };

  const setLoading = (loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  };

  const setError = (error: string | null) => {
    dispatch({ type: 'SET_ERROR', payload: error });
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const isOwnerOrManager = (): boolean => {
    return state.user?.role === 'OWNER' || state.user?.role === 'MANAGER';
  };

  const hasPermission = (permission: string): boolean => {
    if (!state.user) return false;
    
    // Owners and admins have all permissions
    if (state.user.role === 'OWNER' || state.user.role === 'ADMIN') {
      return true;
    }

    // Check specific permissions
    return state.user.permissions?.[permission] === true;
  };

  const contextValue: AuthContextType = {
    state,
    dispatch,
    login,
    logout,
    updateUser,
    updateTokens,
    setLoading,
    setError,
    clearError,
    isOwnerOrManager,
    hasPermission,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

// =================================================================
// AUTH HOOK
// =================================================================

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
}

// Export types for use in other components
export type { AuthState };