import { CONFIG } from '@/config';
import Image from 'next/image';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation Header */}
      <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-secondary-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <span className="text-xl font-bold text-secondary-900">{CONFIG.APP.NAME}</span>
            </div>

            {/* Navigation Links */}
            <nav className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-secondary-600 hover:text-secondary-900 transition-colors">Features</a>
              <a href="#how-it-works" className="text-secondary-600 hover:text-secondary-900 transition-colors">How it Works</a>
              <a href="#pricing" className="text-secondary-600 hover:text-secondary-900 transition-colors">Pricing</a>
              <a href="#support" className="text-secondary-600 hover:text-secondary-900 transition-colors">Support</a>
            </nav>

            {/* CTA Buttons */}
            <div className="flex items-center space-x-4">
              <button className="hidden sm:block text-secondary-600 hover:text-secondary-900 transition-colors">
                Sign In
              </button>
              <button className="btn-primary">
                Start Free Trial
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-secondary-50 pt-16 pb-20 lg:pt-20 lg:pb-28">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-2 lg:gap-12 lg:items-center">
            {/* Hero Content */}
            <div className="mb-12 lg:mb-0">
              <div className="mb-6">
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800">
                  🚀 Now Available for Restaurants
                </span>
              </div>
              
              <h1 className="text-4xl lg:text-6xl font-bold text-secondary-900 leading-tight mb-6">
                Transform Your Restaurant with 
                <span className="text-primary-500"> Smart Digital Management</span>
              </h1>
              
              <p className="text-xl text-secondary-600 mb-8 leading-relaxed">
                Streamline operations, boost efficiency, and delight customers with our mobile-first restaurant management platform. QR ordering, staff management, and real-time analytics - all in one place.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                <button className="btn-primary text-lg px-8 py-4">
                  Start Free 14-Day Trial
                </button>
                <button className="btn-secondary text-lg px-8 py-4">
                  Watch Demo Video
                </button>
              </div>

              {/* Trust Indicators */}
              <div className="flex items-center space-x-6 text-sm text-secondary-500">
                <div className="flex items-center space-x-1">
                  <svg className="w-4 h-4 text-success-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span>No setup fees</span>
                </div>
                <div className="flex items-center space-x-1">
                  <svg className="w-4 h-4 text-success-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span>Cancel anytime</span>
                </div>
                <div className="flex items-center space-x-1">
                  <svg className="w-4 h-4 text-success-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span>24/7 support</span>
                </div>
              </div>
            </div>

            {/* Hero Image */}
            <div className="relative">
              <div className="relative mx-auto w-full max-w-md lg:max-w-none">
                {/* Mobile mockup showing the app */}
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-primary-400 rounded-3xl transform rotate-3"></div>
                  <div className="relative bg-white rounded-3xl shadow-2xl p-2">
                    <div className="bg-secondary-900 rounded-2xl aspect-[9/16] flex items-center justify-center">
                      <div className="text-center text-white p-8">
                        <div className="w-16 h-16 mx-auto mb-4 bg-primary-500 rounded-2xl flex items-center justify-center">
                          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                          </svg>
                        </div>
                        <h3 className="text-lg font-semibold mb-2">QR Code Menu</h3>
                        <p className="text-sm opacity-80">Customers scan & order instantly</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Floating elements */}
                <div className="absolute -top-4 -right-4 bg-success-500 text-white px-3 py-1 rounded-full text-sm font-medium animate-bounce-light">
                  ⚡ Fast Setup
                </div>
                <div className="absolute -bottom-4 -left-4 bg-primary-500 text-white px-3 py-1 rounded-full text-sm font-medium">
                  📱 Mobile First
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-secondary-900 mb-4">
              Everything Your Restaurant Needs
            </h2>
            <p className="text-xl text-secondary-600 max-w-3xl mx-auto">
              Powerful features designed specifically for restaurant owners who want to modernize their operations and increase profits.
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="card text-center group hover:shadow-lg transition-shadow duration-300">
              <div className="w-16 h-16 mx-auto mb-6 bg-primary-100 rounded-2xl flex items-center justify-center group-hover:bg-primary-200 transition-colors">
                <svg className="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M12 12h-4.01M12 12v4M6 12H4m6 8h.01M12 20h4.01M12 20H7.99" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">QR Code Ordering</h3>
              <p className="text-secondary-600 leading-relaxed">
                Customers scan QR codes at tables to view menus, place orders, and pay - all contactless and efficient.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="card text-center group hover:shadow-lg transition-shadow duration-300">
              <div className="w-16 h-16 mx-auto mb-6 bg-success-100 rounded-2xl flex items-center justify-center group-hover:bg-success-200 transition-colors">
                <svg className="w-8 h-8 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">Staff Management</h3>
              <p className="text-secondary-600 leading-relaxed">
                Manage your team, assign roles, track performance, and streamline communication all in one dashboard.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="card text-center group hover:shadow-lg transition-shadow duration-300">
              <div className="w-16 h-16 mx-auto mb-6 bg-warning-100 rounded-2xl flex items-center justify-center group-hover:bg-warning-200 transition-colors">
                <svg className="w-8 h-8 text-warning-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">Digital Menu Control</h3>
              <p className="text-secondary-600 leading-relaxed">
                Update menus instantly, manage pricing, track popular items, and optimize your offerings in real-time.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="card text-center group hover:shadow-lg transition-shadow duration-300">
              <div className="w-16 h-16 mx-auto mb-6 bg-purple-100 rounded-2xl flex items-center justify-center group-hover:bg-purple-200 transition-colors">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">Real-time Analytics</h3>
              <p className="text-secondary-600 leading-relaxed">
                Track sales, monitor performance, identify trends, and make data-driven decisions to grow your business.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="card text-center group hover:shadow-lg transition-shadow duration-300">
              <div className="w-16 h-16 mx-auto mb-6 bg-blue-100 rounded-2xl flex items-center justify-center group-hover:bg-blue-200 transition-colors">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-5 5v-5zM4.5 5L7 7.5v-5H4.5zM19.5 5L17 7.5v-5h2.5zM7 17.5L4.5 15H7v2.5zM17 17.5l2.5-2.5H17v2.5z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">Order Tracking</h3>
              <p className="text-secondary-600 leading-relaxed">
                Real-time order status updates, kitchen notifications, and seamless order fulfillment workflow.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="card text-center group hover:shadow-lg transition-shadow duration-300">
              <div className="w-16 h-16 mx-auto mb-6 bg-green-100 rounded-2xl flex items-center justify-center group-hover:bg-green-200 transition-colors">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">Mobile Optimized</h3>
              <p className="text-secondary-600 leading-relaxed">
                Perfect experience on phones and tablets. Manage your restaurant from anywhere, anytime.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 bg-secondary-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-secondary-900 mb-4">
              Get Started in Under 5 Minutes
            </h2>
            <p className="text-xl text-secondary-600 max-w-3xl mx-auto">
              Simple 3-step process to transform your restaurant operations and start accepting digital orders.
            </p>
          </div>

          {/* Steps */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
            {/* Step 1 */}
            <div className="text-center">
              <div className="relative mx-auto w-24 h-24 mb-6">
                <div className="w-24 h-24 bg-primary-500 rounded-full flex items-center justify-center">
                  <span className="text-2xl font-bold text-white">1</span>
                </div>
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-success-500 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">Sign Up Your Restaurant</h3>
              <p className="text-secondary-600 leading-relaxed mb-4">
                Quick registration with your restaurant details. No credit card required for the free trial.
              </p>
              <ul className="text-sm text-secondary-500 space-y-1">
                <li>• Restaurant name & contact info</li>
                <li>• Choose your subscription plan</li>
                <li>• Verify your email address</li>
              </ul>
            </div>

            {/* Arrow */}
            <div className="hidden lg:flex items-center justify-center">
              <svg className="w-8 h-8 text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="relative mx-auto w-24 h-24 mb-6">
                <div className="w-24 h-24 bg-primary-500 rounded-full flex items-center justify-center">
                  <span className="text-2xl font-bold text-white">2</span>
                </div>
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-success-500 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">Set Up Menu & Staff</h3>
              <p className="text-secondary-600 leading-relaxed mb-4">
                Add your menu items, configure pricing, and invite your team members with appropriate roles.
              </p>
              <ul className="text-sm text-secondary-500 space-y-1">
                <li>• Upload menu categories & items</li>
                <li>• Set prices & descriptions</li>
                <li>• Add staff with role permissions</li>
              </ul>
            </div>

            {/* Arrow */}
            <div className="hidden lg:flex items-center justify-center">
              <svg className="w-8 h-8 text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="relative mx-auto w-24 h-24 mb-6">
                <div className="w-24 h-24 bg-primary-500 rounded-full flex items-center justify-center">
                  <span className="text-2xl font-bold text-white">3</span>
                </div>
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-success-500 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-3">Start Taking Orders</h3>
              <p className="text-secondary-600 leading-relaxed mb-4">
                Generate QR codes for your tables and start receiving digital orders immediately.
              </p>
              <ul className="text-sm text-secondary-500 space-y-1">
                <li>• Generate table QR codes</li>
                <li>• Print & place on tables</li>
                <li>• Customers start ordering!</li>
              </ul>
            </div>
          </div>

          {/* CTA */}
          <div className="text-center mt-12">
            <button className="btn-primary text-lg px-8 py-4">
              Start Your Free Trial Now
            </button>
            <p className="text-sm text-secondary-500 mt-2">
              No credit card required • 14-day free trial • Cancel anytime
            </p>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-secondary-900 mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-xl text-secondary-600 max-w-3xl mx-auto">
              Choose the plan that fits your restaurant size. All plans include core features with no hidden fees.
            </p>
          </div>

          {/* Pricing Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Starter Plan */}
            <div className="card relative">
              <div className="text-center">
                <h3 className="text-xl font-semibold text-secondary-900 mb-2">Starter</h3>
                <p className="text-secondary-600 mb-6">Perfect for small restaurants</p>
                <div className="mb-6">
                  <span className="text-4xl font-bold text-secondary-900">$29</span>
                  <span className="text-secondary-500">/month</span>
                </div>
                <button className="btn-secondary w-full mb-6">Start Free Trial</button>
                
                <ul className="text-left space-y-3 text-sm">
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Up to 5 tables
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    QR code ordering
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Menu management
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Basic analytics
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Email support
                  </li>
                </ul>
              </div>
            </div>

            {/* Professional Plan */}
            <div className="card relative border-2 border-primary-500">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="bg-primary-500 text-white px-4 py-1 rounded-full text-sm font-medium">Most Popular</span>
              </div>
              <div className="text-center">
                <h3 className="text-xl font-semibold text-secondary-900 mb-2">Professional</h3>
                <p className="text-secondary-600 mb-6">Great for growing restaurants</p>
                <div className="mb-6">
                  <span className="text-4xl font-bold text-secondary-900">$79</span>
                  <span className="text-secondary-500">/month</span>
                </div>
                <button className="btn-primary w-full mb-6">Start Free Trial</button>
                
                <ul className="text-left space-y-3 text-sm">
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Up to 20 tables
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    All Starter features
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Staff management
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Advanced analytics
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Priority support
                  </li>
                </ul>
              </div>
            </div>

            {/* Enterprise Plan */}
            <div className="card relative">
              <div className="text-center">
                <h3 className="text-xl font-semibold text-secondary-900 mb-2">Enterprise</h3>
                <p className="text-secondary-600 mb-6">For large restaurant chains</p>
                <div className="mb-6">
                  <span className="text-4xl font-bold text-secondary-900">$199</span>
                  <span className="text-secondary-500">/month</span>
                </div>
                <button className="btn-secondary w-full mb-6">Contact Sales</button>
                
                <ul className="text-left space-y-3 text-sm">
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Unlimited tables
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    All Professional features
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Multi-location management
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    Custom integrations
                  </li>
                  <li className="flex items-center">
                    <svg className="w-4 h-4 text-success-500 mr-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    24/7 phone support
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-secondary-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-secondary-900 mb-4">
              Trusted by Restaurant Owners
            </h2>
            <p className="text-xl text-secondary-600">
              See what restaurant owners are saying about our platform
            </p>
          </div>

          {/* Testimonials Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Testimonial 1 */}
            <div className="card">
              <div className="flex items-center mb-4">
                {Array.from({ length: 5 }).map((_, i) => (
                  <svg key={i} className="w-5 h-5 text-warning-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-secondary-600 mb-4">
                "This platform transformed our restaurant operations. Orders are more accurate, customers love the contactless experience, and our staff can focus on food quality instead of taking orders."
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                  MR
                </div>
                <div>
                  <p className="font-semibold text-secondary-900">Maria Rodriguez</p>
                  <p className="text-sm text-secondary-500">Owner, Casa Maria Restaurant</p>
                </div>
              </div>
            </div>

            {/* Testimonial 2 */}
            <div className="card">
              <div className="flex items-center mb-4">
                {Array.from({ length: 5 }).map((_, i) => (
                  <svg key={i} className="w-5 h-5 text-warning-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-secondary-600 mb-4">
                "Setup was incredibly easy - we were taking QR code orders within an hour! The analytics help us understand our customers better and the mobile interface is perfect for our fast-paced environment."
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-success-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                  JS
                </div>
                <div>
                  <p className="font-semibold text-secondary-900">James Smith</p>
                  <p className="text-sm text-secondary-500">Manager, Urban Bite Café</p>
                </div>
              </div>
            </div>

            {/* Testimonial 3 */}
            <div className="card">
              <div className="flex items-center mb-4">
                {Array.from({ length: 5 }).map((_, i) => (
                  <svg key={i} className="w-5 h-5 text-warning-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-secondary-600 mb-4">
                "Our revenue increased by 25% in the first month! Customers spend more when they can browse the menu at their own pace, and the staff management features keep our team organized."
              </p>
              <div className="flex items-center">
                <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                  AP
                </div>
                <div>
                  <p className="font-semibold text-secondary-900">Arjun Patel</p>
                  <p className="text-sm text-secondary-500">Owner, Spice Garden</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
            Ready to Transform Your Restaurant?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-3xl mx-auto">
            Join thousands of restaurant owners who've modernized their operations with our platform. Start your free trial today!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button className="bg-white text-primary-500 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-50 transition-colors">
              Start Free 14-Day Trial
            </button>
            <button className="text-white border border-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-white hover:text-primary-500 transition-colors">
              Schedule a Demo
            </button>
          </div>
          <p className="text-primary-100 text-sm mt-4">
            No credit card required • Setup in under 5 minutes • Cancel anytime
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer id="support" className="bg-secondary-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            {/* Company Info */}
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <span className="text-xl font-bold">{CONFIG.APP.NAME}</span>
              </div>
              <p className="text-secondary-400 mb-4">
                Modern restaurant management platform designed for mobile and tablet devices.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="text-secondary-400 hover:text-white transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M20 10c0-5.523-4.477-10-10-10S0 4.477 0 10c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V10h2.54V7.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V10h2.773l-.443 2.89h-2.33v6.988C16.343 19.128 20 14.991 20 10z" clipRule="evenodd" />
                  </svg>
                </a>
                <a href="#" className="text-secondary-400 hover:text-white transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M6.29 18.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0020 3.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.073 4.073 0 01.8 7.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 010 16.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
                <a href="#" className="text-secondary-400 hover:text-white transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.338 16.338H13.67V12.16c0-.995-.017-2.277-1.387-2.277-1.39 0-1.601 1.086-1.601 2.207v4.248H8.014v-8.59h2.559v1.174h.037c.356-.675 1.227-1.387 2.526-1.387 2.703 0 3.203 1.778 3.203 4.092v4.711zM5.005 6.575a1.548 1.548 0 11-.003-3.096 1.548 1.548 0 01.003 3.096zm-1.337 9.763H6.34v-8.59H3.667v8.59zM17.668 1H2.328C1.595 1 1 1.581 1 2.298v15.403C1 18.418 1.595 19 2.328 19h15.34c.734 0 1.332-.582 1.332-1.299V2.298C19 1.581 18.402 1 17.668 1z" clipRule="evenodd" />
                  </svg>
                </a>
              </div>
            </div>

            {/* Product */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Product</h3>
              <ul className="space-y-2 text-secondary-400">
                <li><a href="#features" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#pricing" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Demo</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Documentation</a></li>
              </ul>
            </div>

            {/* Support */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Support</h3>
              <ul className="space-y-2 text-secondary-400">
                <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact Support</a></li>
                <li><a href="#" className="hover:text-white transition-colors">System Status</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Training Resources</a></li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-secondary-400">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
              </ul>
            </div>
          </div>

          {/* Bottom Footer */}
          <div className="border-t border-secondary-800 mt-12 pt-8 flex flex-col lg:flex-row justify-between items-center">
            <p className="text-secondary-400">
              © 2025 {CONFIG.APP.NAME}. All rights reserved.
            </p>
            <div className="flex items-center space-x-6 mt-4 lg:mt-0">
              <span className="text-secondary-400 text-sm">
                Environment: {CONFIG.APP.ENVIRONMENT} | Version: {CONFIG.APP.VERSION}
              </span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}