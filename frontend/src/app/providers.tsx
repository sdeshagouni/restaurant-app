'use client';

import React from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { Toaster } from 'react-hot-toast';

import { CONFIG } from '@/config';
import { AuthProvider } from '@/store/auth';
import { UIProvider } from '@/store/ui';
import { DeviceProvider } from '@/hooks/useDevice';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 1,
    },
  },
});

interface ProvidersProps {
  children: React.ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <DeviceProvider>
        <AuthProvider>
          <UIProvider>
            {children}
            
            {/* Toast Notifications */}
            <Toaster
              position="top-center"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#363636',
                  color: '#fff',
                  borderRadius: '8px',
                  fontSize: '14px',
                  maxWidth: '500px',
                },
                success: {
                  style: {
                    background: CONFIG.THEME.COLORS.SUCCESS,
                  },
                  iconTheme: {
                    primary: '#fff',
                    secondary: CONFIG.THEME.COLORS.SUCCESS,
                  },
                },
                error: {
                  style: {
                    background: CONFIG.THEME.COLORS.ERROR,
                  },
                  iconTheme: {
                    primary: '#fff',
                    secondary: CONFIG.THEME.COLORS.ERROR,
                  },
                },
                loading: {
                  style: {
                    background: CONFIG.THEME.COLORS.PRIMARY,
                  },
                },
              }}
            />
            
            {/* Development Tools */}
            {CONFIG.DEV.ENABLE_DEVTOOLS && CONFIG.DEV.DEBUG_MODE && (
              <ReactQueryDevtools 
                initialIsOpen={false}
                position="bottom-right"
              />
            )}
          </UIProvider>
        </AuthProvider>
      </DeviceProvider>
    </QueryClientProvider>
  );
}