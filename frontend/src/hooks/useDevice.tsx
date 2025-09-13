'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { CONFIG } from '@/config';

// =================================================================
// DEVICE TYPES
// =================================================================

interface DeviceInfo {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  orientation: 'portrait' | 'landscape';
  screenWidth: number;
  screenHeight: number;
  userAgent: string;
  platform: string;
  isIOS: boolean;
  isAndroid: boolean;
  isTouchDevice: boolean;
  devicePixelRatio: number;
}

interface DeviceContextType {
  device: DeviceInfo;
  refreshDevice: () => void;
}

// =================================================================
// DEVICE CONTEXT
// =================================================================

const DeviceContext = createContext<DeviceContextType | undefined>(undefined);

// =================================================================
// DEVICE HELPERS
// =================================================================

const getDeviceInfo = (): DeviceInfo => {
  if (typeof window === 'undefined') {
    // Server-side fallback
    return {
      isMobile: false,
      isTablet: false,
      isDesktop: true,
      orientation: 'landscape',
      screenWidth: 1024,
      screenHeight: 768,
      userAgent: '',
      platform: '',
      isIOS: false,
      isAndroid: false,
      isTouchDevice: false,
      devicePixelRatio: 1,
    };
  }

  const { innerWidth: screenWidth, innerHeight: screenHeight } = window;
  const { userAgent, platform } = navigator;
  const devicePixelRatio = window.devicePixelRatio || 1;

  // Breakpoint detection
  const isMobile = screenWidth < CONFIG.BREAKPOINTS.MOBILE;
  const isTablet = screenWidth >= CONFIG.BREAKPOINTS.MOBILE && screenWidth < CONFIG.BREAKPOINTS.DESKTOP;
  const isDesktop = screenWidth >= CONFIG.BREAKPOINTS.DESKTOP;

  // Orientation detection
  const orientation: 'portrait' | 'landscape' = screenHeight > screenWidth ? 'portrait' : 'landscape';

  // Platform detection
  const isIOS = /iPad|iPhone|iPod/.test(userAgent) || (platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const isAndroid = /Android/.test(userAgent);

  // Touch device detection
  const isTouchDevice = 'ontouchstart' in window || 
    navigator.maxTouchPoints > 0 || 
    // @ts-ignore - Legacy support
    navigator.msMaxTouchPoints > 0;

  return {
    isMobile,
    isTablet,
    isDesktop,
    orientation,
    screenWidth,
    screenHeight,
    userAgent,
    platform,
    isIOS,
    isAndroid,
    isTouchDevice,
    devicePixelRatio,
  };
};

// =================================================================
// DEVICE PROVIDER COMPONENT
// =================================================================

interface DeviceProviderProps {
  children: React.ReactNode;
}

export function DeviceProvider({ children }: DeviceProviderProps) {
  const [device, setDevice] = useState<DeviceInfo>(getDeviceInfo);

  const refreshDevice = () => {
    setDevice(getDeviceInfo());
  };

  // Update device info on resize and orientation change
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleResize = () => {
      refreshDevice();
    };

    const handleOrientationChange = () => {
      // Small delay to ensure screen dimensions are updated
      setTimeout(refreshDevice, 100);
    };

    // Add event listeners
    window.addEventListener('resize', handleResize);
    window.addEventListener('orientationchange', handleOrientationChange);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('orientationchange', handleOrientationChange);
    };
  }, []);

  // Apply device-specific classes to document
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const root = document.documentElement;

    // Remove all device classes
    root.classList.remove(
      'is-mobile', 'is-tablet', 'is-desktop',
      'is-portrait', 'is-landscape',
      'is-ios', 'is-android', 'is-touch'
    );

    // Add current device classes
    if (device.isMobile) root.classList.add('is-mobile');
    if (device.isTablet) root.classList.add('is-tablet');
    if (device.isDesktop) root.classList.add('is-desktop');
    if (device.orientation === 'portrait') root.classList.add('is-portrait');
    if (device.orientation === 'landscape') root.classList.add('is-landscape');
    if (device.isIOS) root.classList.add('is-ios');
    if (device.isAndroid) root.classList.add('is-android');
    if (device.isTouchDevice) root.classList.add('is-touch');

    // Set CSS custom properties for dynamic values
    root.style.setProperty('--screen-width', `${device.screenWidth}px`);
    root.style.setProperty('--screen-height', `${device.screenHeight}px`);
    root.style.setProperty('--device-pixel-ratio', device.devicePixelRatio.toString());
  }, [device]);

  // Handle viewport height on mobile (address bar height changes)
  useEffect(() => {
    if (typeof window === 'undefined' || !device.isMobile) return;

    const setVH = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    };

    setVH();
    window.addEventListener('resize', setVH);
    window.addEventListener('orientationchange', () => {
      setTimeout(setVH, 100);
    });

    return () => {
      window.removeEventListener('resize', setVH);
      window.removeEventListener('orientationchange', setVH);
    };
  }, [device.isMobile]);

  const contextValue: DeviceContextType = {
    device,
    refreshDevice,
  };

  return (
    <DeviceContext.Provider value={contextValue}>
      {children}
    </DeviceContext.Provider>
  );
}

// =================================================================
// DEVICE HOOK
// =================================================================

export function useDevice(): DeviceContextType {
  const context = useContext(DeviceContext);
  
  if (context === undefined) {
    throw new Error('useDevice must be used within a DeviceProvider');
  }
  
  return context;
}

// =================================================================
// ADDITIONAL DEVICE HOOKS
// =================================================================

/**
 * Hook to check if the current device is mobile
 */
export function useIsMobile(): boolean {
  const { device } = useDevice();
  return device.isMobile;
}

/**
 * Hook to check if the current device is tablet
 */
export function useIsTablet(): boolean {
  const { device } = useDevice();
  return device.isTablet;
}

/**
 * Hook to check if the current device is desktop
 */
export function useIsDesktop(): boolean {
  const { device } = useDevice();
  return device.isDesktop;
}

/**
 * Hook to check if the current device supports touch
 */
export function useIsTouchDevice(): boolean {
  const { device } = useDevice();
  return device.isTouchDevice;
}

/**
 * Hook to get current screen orientation
 */
export function useOrientation(): 'portrait' | 'landscape' {
  const { device } = useDevice();
  return device.orientation;
}

/**
 * Hook to get current screen dimensions
 */
export function useScreenSize(): { width: number; height: number } {
  const { device } = useDevice();
  return {
    width: device.screenWidth,
    height: device.screenHeight,
  };
}

/**
 * Hook to check if device is iOS
 */
export function useIsIOS(): boolean {
  const { device } = useDevice();
  return device.isIOS;
}

/**
 * Hook to check if device is Android
 */
export function useIsAndroid(): boolean {
  const { device } = useDevice();
  return device.isAndroid;
}

/**
 * Hook for responsive breakpoint detection
 */
export function useBreakpoint(): {
  isSm: boolean;
  isMd: boolean;
  isLg: boolean;
  isXl: boolean;
  is2Xl: boolean;
} {
  const { device } = useDevice();
  const width = device.screenWidth;

  return {
    isSm: width >= 640,
    isMd: width >= 768,
    isLg: width >= 1024,
    isXl: width >= 1280,
    is2Xl: width >= 1536,
  };
}

// Export types for use in other components
export type { DeviceInfo, DeviceContextType };