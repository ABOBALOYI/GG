'use client';

import { useState, useEffect } from 'react';
import { X, Cookie } from 'lucide-react';

const COOKIE_CONSENT_KEY = 'grantguide-cookie-consent';

export default function CookieConsent() {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem(COOKIE_CONSENT_KEY);
    if (!consent) {
      // Small delay to avoid layout shift on initial load
      const timer = setTimeout(() => setShowBanner(true), 1000);
      return () => clearTimeout(timer);
    }
  }, []);

  const acceptAll = () => {
    localStorage.setItem(COOKIE_CONSENT_KEY, JSON.stringify({
      analytics: true,
      advertising: true,
      timestamp: new Date().toISOString()
    }));
    setShowBanner(false);
    // Enable analytics/ads here when ready
  };

  const acceptEssential = () => {
    localStorage.setItem(COOKIE_CONSENT_KEY, JSON.stringify({
      analytics: false,
      advertising: false,
      timestamp: new Date().toISOString()
    }));
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 p-4 animate-slide-up">
      <div className="max-w-4xl mx-auto bg-white rounded-2xl shadow-2xl border border-gray-200 p-4 sm:p-6">
        <div className="flex items-start gap-4">
          <div className="hidden sm:flex w-12 h-12 bg-green-100 rounded-xl items-center justify-center flex-shrink-0">
            <Cookie className="w-6 h-6 text-green-700" />
          </div>
          
          <div className="flex-1">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 className="font-bold text-gray-900 text-sm sm:text-base">We use cookies 🍪</h3>
                <p className="text-gray-600 text-xs sm:text-sm mt-1 leading-relaxed">
                  We use cookies to improve your experience and show relevant ads. 
                  By clicking &quot;Accept All&quot;, you consent to our use of cookies. 
                  You can also choose to accept only essential cookies.
                </p>
              </div>
              <button 
                onClick={acceptEssential}
                className="text-gray-400 hover:text-gray-600 p-1 -mt-1 -mr-1"
                aria-label="Close"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-2 sm:gap-3 mt-4">
              <button
                onClick={acceptAll}
                className="px-4 py-2 bg-green-700 text-white rounded-lg font-semibold text-sm hover:bg-green-800 transition-colors"
              >
                Accept All
              </button>
              <button
                onClick={acceptEssential}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg font-semibold text-sm hover:bg-gray-200 transition-colors"
              >
                Essential Only
              </button>
              <a
                href="/privacy"
                className="px-4 py-2 text-gray-600 text-sm hover:text-green-700 transition-colors text-center sm:text-left"
              >
                Privacy Policy
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
