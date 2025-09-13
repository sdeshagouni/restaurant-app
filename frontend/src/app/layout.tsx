import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

import { CONFIG, validateConfig } from '@/config';
import { Providers } from './providers';

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: {
    default: CONFIG.APP.NAME,
    template: `%s | ${CONFIG.APP.NAME}`,
  },
  description: CONFIG.APP.DESCRIPTION,
  keywords: [
    'restaurant management',
    'mobile ordering',
    'QR code ordering', 
    'restaurant POS',
    'table ordering',
    'food service'
  ],
  authors: [{ name: 'Restaurant Management Team' }],
  creator: 'Restaurant Management Team',
  publisher: 'Restaurant Management System',
  
  // PWA Configuration
  manifest: '/manifest.json',
  
  // Mobile Optimization
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 5,
    userScalable: true,
    viewportFit: 'cover',
  },
  
  // Apple Touch Icon and Meta Tags
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: CONFIG.PWA.SHORT_NAME,
    startupImage: [
      {
        url: '/icons/apple-splash-2048-2732.jpg',
        media: '(device-width: 1024px) and (device-height: 1366px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)',
      },
      {
        url: '/icons/apple-splash-1668-2388.jpg', 
        media: '(device-width: 834px) and (device-height: 1194px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)',
      },
      {
        url: '/icons/apple-splash-1536-2048.jpg',
        media: '(device-width: 768px) and (device-height: 1024px) and (-webkit-device-pixel-ratio: 2) and (orientation: portrait)',
      },
      {
        url: '/icons/apple-splash-1125-2436.jpg',
        media: '(device-width: 375px) and (device-height: 812px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)',
      },
      {
        url: '/icons/apple-splash-1242-2688.jpg',
        media: '(device-width: 414px) and (device-height: 896px) and (-webkit-device-pixel-ratio: 3) and (orientation: portrait)',
      },
    ],
  },
  
  // Icons
  icons: {
    icon: [
      { url: '/favicon.ico' },
      { url: '/icons/icon-192x192.png', sizes: '192x192', type: 'image/png' },
      { url: '/icons/icon-512x512.png', sizes: '512x512', type: 'image/png' },
    ],
    apple: [
      { url: '/icons/apple-touch-icon.png', sizes: '180x180' },
    ],
    other: [
      {
        rel: 'mask-icon',
        url: '/icons/safari-pinned-tab.svg',
        color: CONFIG.THEME.COLORS.PRIMARY,
      },
    ],
  },
  
  // Theme Colors
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: CONFIG.PWA.THEME_COLOR },
    { media: '(prefers-color-scheme: dark)', color: '#1a1a1a' },
  ],
  
  // Open Graph
  openGraph: {
    type: 'website',
    locale: 'en_US',
    title: CONFIG.APP.NAME,
    description: CONFIG.APP.DESCRIPTION,
    siteName: CONFIG.APP.NAME,
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: CONFIG.APP.NAME,
      },
    ],
  },
  
  // Twitter Card
  twitter: {
    card: 'summary_large_image',
    title: CONFIG.APP.NAME,
    description: CONFIG.APP.DESCRIPTION,
    images: ['/og-image.png'],
  },
  
  // Additional Meta Tags
  other: {
    'mobile-web-app-capable': 'yes',
    'apple-mobile-web-app-capable': 'yes',
    'apple-mobile-web-app-status-bar-style': 'default',
    'msapplication-TileColor': CONFIG.PWA.THEME_COLOR,
    'msapplication-config': '/browserconfig.xml',
  },
  
  // Robots
  robots: {
    index: CONFIG.APP.ENVIRONMENT === 'production',
    follow: CONFIG.APP.ENVIRONMENT === 'production',
    googleBot: {
      index: CONFIG.APP.ENVIRONMENT === 'production',
      follow: CONFIG.APP.ENVIRONMENT === 'production',
    },
  },
  
  // Verification (add your verification codes here)
  // verification: {
  //   google: 'your-google-verification-code',
  //   yandex: 'your-yandex-verification-code',
  //   yahoo: 'your-yahoo-verification-code',
  //   other: {
  //     me: 'your-domain.com',
  //   },
  // },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Validate configuration on startup
  if (CONFIG.DEV.DEBUG_MODE) {
    validateConfig();
  }

  return (
    <html lang="en" className={inter.variable}>
      <head>
        {/* Preload critical resources */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        
        {/* DNS Prefetch for external resources */}
        <link rel="dns-prefetch" href={CONFIG.API.BASE_URL} />
        
        {/* Additional Performance Hints */}
        <meta name="format-detection" content="telephone=no" />
        <meta name="format-detection" content="address=no" />
        <meta name="format-detection" content="email=no" />
      </head>
      <body 
        className={`${inter.className} antialiased`}
        suppressHydrationWarning={CONFIG.DEV.DEBUG_MODE}
      >
        <Providers>
          {/* Skip to main content for accessibility */}
          <a
            href="#main-content"
            className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-50 px-4 py-2 bg-primary-500 text-white rounded-md"
          >
            Skip to main content
          </a>
          
          {/* Main application content */}
          <div id="app-root" className="min-h-screen bg-gray-50">
            <main id="main-content" className="min-h-screen">
              {children}
            </main>
          </div>
          
          {/* Portal for modals and overlays */}
          <div id="modal-root" />
          <div id="toast-root" />
        </Providers>
        
        {/* Development tools (only in development) */}
        {CONFIG.DEV.ENABLE_DEVTOOLS && CONFIG.DEV.DEBUG_MODE && (
          <div 
            id="dev-tools" 
            className="fixed bottom-4 right-4 z-50 opacity-50 hover:opacity-100 transition-opacity"
          >
            <div className="bg-gray-800 text-white text-xs p-2 rounded">
              Environment: {CONFIG.APP.ENVIRONMENT}
              <br />
              Version: {CONFIG.APP.VERSION}
            </div>
          </div>
        )}
      </body>
    </html>
  );
}