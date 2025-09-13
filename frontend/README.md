# Restaurant Web UI - Next.js + Tailwind CSS Base Framework

## 🎯 Project Overview

A complete Next.js + Tailwind CSS base framework optimized for mobile and tablet devices, specifically designed for restaurant management web applications. This framework provides a solid foundation with externalized configuration, performance optimizations, and mobile-first design patterns.

## 🚀 Getting Started

### Prerequisites

- Node.js 18.0+ 
- npm 8.0+

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Copy environment configuration:**
   ```bash
   cp .env.local .env.local.backup
   ```

3. **Configure your backend server URL:**
   Edit `.env.local` and update:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://your-backend-server:8000
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
restaurant-web-ui/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx       # Root layout with PWA config
│   │   ├── page.tsx         # Homepage
│   │   ├── providers.tsx    # Global providers
│   │   └── globals.css      # Global styles
│   ├── components/          # Reusable UI components
│   ├── config/             # Configuration management
│   │   └── index.ts        # Centralized config
│   ├── types/              # TypeScript definitions
│   │   └── index.ts        # All type definitions
│   ├── hooks/              # Custom React hooks
│   ├── store/              # State management
│   ├── services/           # API services
│   ├── utils/              # Utility functions
│   └── styles/             # Additional styles
├── public/                 # Static assets
├── .env.local             # Development environment
├── .env.production        # Production environment
├── next.config.js         # Next.js configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
└── package.json           # Dependencies and scripts
```

## ⚙️ Configuration Management

### Environment Variables

All configuration is externalized through environment variables:

#### API Configuration
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
NEXT_PUBLIC_API_TIMEOUT=30000
```

#### Feature Flags
```env
NEXT_PUBLIC_ENABLE_QR_ORDERING=true
NEXT_PUBLIC_ENABLE_DARK_MODE=true
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

#### Theme Configuration
```env
NEXT_PUBLIC_PRIMARY_COLOR=#FF6B35
NEXT_PUBLIC_SECONDARY_COLOR=#2C3E50
```

### Configuration Usage

```typescript
import { CONFIG } from '@/config';

// API Configuration
const apiUrl = CONFIG.API.BASE_URL;

// Feature Flags
if (CONFIG.FEATURES.QR_ORDERING) {
  // Enable QR ordering features
}

// Theme Colors
const primaryColor = CONFIG.THEME.COLORS.PRIMARY;
```

## 🎨 Design System

### Color Palette

- **Primary**: Orange (#FF6B35) - Restaurant brand color
- **Secondary**: Slate - Professional, readable text
- **Success**: Green - Confirmations, success states
- **Warning**: Amber - Warnings, pending states  
- **Error**: Red - Errors, destructive actions

### Mobile-First Components

Pre-built components optimized for touch interfaces:

```typescript
// Touch-friendly buttons
<button className="btn-primary touch-target">
  Order Now
</button>

// Mobile-optimized cards
<div className="card">
  <div className="card-header">
    <h3>Menu Item</h3>
  </div>
  <!-- Content -->
</div>
```

### Responsive Breakpoints

```css
/* Mobile first approach */
.container {
  @apply w-full px-4;           /* Mobile: 0px+ */
  @apply sm:px-6;               /* Small: 640px+ */
  @apply md:px-8;               /* Medium: 768px+ */
  @apply lg:px-12;              /* Large: 1024px+ */
  @apply xl:px-16;              /* XL: 1280px+ */
}
```

## 📱 Mobile Optimization Features

### Touch-Friendly Interface
- Minimum 44px touch targets (Apple guidelines)
- Touch gesture support
- Thumb-friendly navigation
- Visual feedback on interactions

### Performance Optimizations
- Image optimization and lazy loading
- Code splitting and tree shaking
- Service worker for offline support
- Critical CSS inlining

### PWA Support
- App manifest configuration
- Offline functionality
- Install prompts
- Push notifications ready

### Safe Area Support
```css
.mobile-header {
  @apply safe-top; /* Accounts for notch/dynamic island */
}

.mobile-content {
  @apply safe-x safe-bottom; /* Safe area padding */
}
```

## 🛠️ Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
npm run type-check   # TypeScript type checking
npm run format       # Format with Prettier

# Analysis
npm run analyze      # Bundle size analysis
```

## 🏗️ Adding New Features

### 1. Create New Pages

Add pages to the `src/app` directory:

```typescript
// src/app/menu/page.tsx
export default function MenuPage() {
  return (
    <div className="mobile-content">
      <h1>Restaurant Menu</h1>
      {/* Your menu content */}
    </div>
  );
}
```

### 2. Add API Services

Create service files in `src/services`:

```typescript
// src/services/menu.ts
import { CONFIG } from '@/config';

export const menuService = {
  async getMenu(restaurantId: string) {
    const response = await fetch(
      `${CONFIG.API.BASE_URL}/api/v1/restaurants/${restaurantId}/menu`
    );
    return response.json();
  }
};
```

### 3. Create Reusable Components

Add components to `src/components`:

```typescript
// src/components/MenuCard.tsx
interface MenuCardProps {
  item: MenuItem;
  onSelect: (item: MenuItem) => void;
}

export function MenuCard({ item, onSelect }: MenuCardProps) {
  return (
    <div className="card touch-item" onClick={() => onSelect(item)}>
      <h3>{item.name}</h3>
      <p>${item.price}</p>
    </div>
  );
}
```

## 🚀 Production Deployment

### 1. Update Environment Variables

Edit `.env.production`:

```env
NEXT_PUBLIC_API_BASE_URL=https://your-production-api.com
NEXT_PUBLIC_ENV=production
NEXT_PUBLIC_DEBUG_MODE=false
```

### 2. Build and Deploy

```bash
npm run build
npm run start
```

### 3. Deployment Platforms

This framework is optimized for:
- **Vercel** (recommended for Next.js)
- **Netlify**
- **AWS Amplify**
- **Docker containers**

## 🔧 Customization

### Theme Customization

Modify `tailwind.config.js` to customize colors, fonts, and spacing:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#YOUR_BRAND_COLOR',
        },
      },
    },
  },
};
```

### API Integration

Update configuration in `src/config/index.ts` to match your backend API structure.

## 📚 Key Libraries Included

- **Next.js 14** - React framework with App Router
- **Tailwind CSS** - Utility-first CSS framework
- **TypeScript** - Type safety and developer experience
- **React Query** - Server state management
- **Zustand** - Client state management
- **React Hook Form** - Form handling
- **Framer Motion** - Animations
- **React Hot Toast** - Notifications
- **Headless UI** - Accessible components

## 🎯 Next Steps

1. **Connect to Backend**: Update API base URL in environment variables
2. **Add Authentication**: Implement login/register pages
3. **Build Features**: Add restaurant-specific functionality
4. **Customize Design**: Modify theme to match brand
5. **Add Pages**: Create menu, orders, staff management pages

## 📄 License

This project is proprietary software for restaurant management use.

---

**Framework Ready!** 🎉 Your Next.js + Tailwind CSS base is configured and optimized for mobile restaurant management development.