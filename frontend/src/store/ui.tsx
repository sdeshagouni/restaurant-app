'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { CONFIG } from '@/config';

// =================================================================
// UI STATE TYPES
// =================================================================

interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  notifications: NotificationOptions[];
  loading: boolean;
  modal: {
    isOpen: boolean;
    type?: string;
    data?: any;
  };
}

interface NotificationOptions {
  id: string;
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

type UIAction =
  | { type: 'SET_THEME'; payload: 'light' | 'dark' }
  | { type: 'TOGGLE_SIDEBAR' }
  | { type: 'SET_SIDEBAR'; payload: boolean }
  | { type: 'ADD_NOTIFICATION'; payload: Omit<NotificationOptions, 'id'> }
  | { type: 'REMOVE_NOTIFICATION'; payload: string }
  | { type: 'CLEAR_NOTIFICATIONS' }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'OPEN_MODAL'; payload: { type: string; data?: any } }
  | { type: 'CLOSE_MODAL' };

// =================================================================
// UI CONTEXT
// =================================================================

interface UIContextType {
  state: UIState;
  dispatch: React.Dispatch<UIAction>;
  // Convenience methods
  setTheme: (theme: 'light' | 'dark') => void;
  toggleSidebar: () => void;
  setSidebar: (open: boolean) => void;
  addNotification: (notification: Omit<NotificationOptions, 'id'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
  setLoading: (loading: boolean) => void;
  openModal: (type: string, data?: any) => void;
  closeModal: () => void;
}

const UIContext = createContext<UIContextType | undefined>(undefined);

// =================================================================
// UI REDUCER
// =================================================================

const initialState: UIState = {
  theme: 'light',
  sidebarOpen: false,
  notifications: [],
  loading: false,
  modal: {
    isOpen: false,
  },
};

function uiReducer(state: UIState, action: UIAction): UIState {
  switch (action.type) {
    case 'SET_THEME':
      return {
        ...state,
        theme: action.payload,
      };

    case 'TOGGLE_SIDEBAR':
      return {
        ...state,
        sidebarOpen: !state.sidebarOpen,
      };

    case 'SET_SIDEBAR':
      return {
        ...state,
        sidebarOpen: action.payload,
      };

    case 'ADD_NOTIFICATION':
      const newNotification: NotificationOptions = {
        ...action.payload,
        id: Date.now().toString(),
      };
      return {
        ...state,
        notifications: [...state.notifications, newNotification],
      };

    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload),
      };

    case 'CLEAR_NOTIFICATIONS':
      return {
        ...state,
        notifications: [],
      };

    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };

    case 'OPEN_MODAL':
      return {
        ...state,
        modal: {
          isOpen: true,
          type: action.payload.type,
          data: action.payload.data,
        },
      };

    case 'CLOSE_MODAL':
      return {
        ...state,
        modal: {
          isOpen: false,
        },
      };

    default:
      return state;
  }
}

// =================================================================
// UI PROVIDER COMPONENT
// =================================================================

interface UIProviderProps {
  children: React.ReactNode;
}

export function UIProvider({ children }: UIProviderProps) {
  const [state, dispatch] = useReducer(uiReducer, initialState);

  // Initialize theme from system preference or localStorage
  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
    
    if (savedTheme && CONFIG.FEATURES.DARK_MODE) {
      dispatch({ type: 'SET_THEME', payload: savedTheme });
    } else if (CONFIG.FEATURES.DARK_MODE) {
      // Use system preference
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      dispatch({ type: 'SET_THEME', payload: systemTheme });
    }
  }, []);

  // Apply theme to document
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(state.theme);
    
    // Save theme preference
    localStorage.setItem('theme', state.theme);
  }, [state.theme]);

  // Auto-remove notifications after duration
  useEffect(() => {
    const timers: NodeJS.Timeout[] = [];

    state.notifications.forEach((notification) => {
      if (notification.duration && notification.duration > 0) {
        const timer = setTimeout(() => {
          dispatch({ type: 'REMOVE_NOTIFICATION', payload: notification.id });
        }, notification.duration);
        timers.push(timer);
      }
    });

    return () => {
      timers.forEach(timer => clearTimeout(timer));
    };
  }, [state.notifications]);

  // Convenience methods
  const setTheme = (theme: 'light' | 'dark') => {
    if (CONFIG.FEATURES.DARK_MODE) {
      dispatch({ type: 'SET_THEME', payload: theme });
    }
  };

  const toggleSidebar = () => {
    dispatch({ type: 'TOGGLE_SIDEBAR' });
  };

  const setSidebar = (open: boolean) => {
    dispatch({ type: 'SET_SIDEBAR', payload: open });
  };

  const addNotification = (notification: Omit<NotificationOptions, 'id'>) => {
    dispatch({ type: 'ADD_NOTIFICATION', payload: notification });
  };

  const removeNotification = (id: string) => {
    dispatch({ type: 'REMOVE_NOTIFICATION', payload: id });
  };

  const clearNotifications = () => {
    dispatch({ type: 'CLEAR_NOTIFICATIONS' });
  };

  const setLoading = (loading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: loading });
  };

  const openModal = (type: string, data?: any) => {
    dispatch({ type: 'OPEN_MODAL', payload: { type, data } });
  };

  const closeModal = () => {
    dispatch({ type: 'CLOSE_MODAL' });
  };

  const contextValue: UIContextType = {
    state,
    dispatch,
    setTheme,
    toggleSidebar,
    setSidebar,
    addNotification,
    removeNotification,
    clearNotifications,
    setLoading,
    openModal,
    closeModal,
  };

  return (
    <UIContext.Provider value={contextValue}>
      {children}
    </UIContext.Provider>
  );
}

// =================================================================
// UI HOOK
// =================================================================

export function useUI(): UIContextType {
  const context = useContext(UIContext);
  
  if (context === undefined) {
    throw new Error('useUI must be used within a UIProvider');
  }
  
  return context;
}

// Export types for use in other components
export type { UIState, NotificationOptions };