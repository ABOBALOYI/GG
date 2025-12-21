'use client';

import { useEffect, useRef } from 'react';

interface AdBannerProps {
  slot: string;
  format?: 'auto' | 'rectangle' | 'horizontal' | 'vertical';
  className?: string;
}

// AdSense publisher ID
const ADSENSE_CLIENT = 'ca-pub-4896697928226626';

export default function AdBanner({ slot, format = 'auto', className = '' }: AdBannerProps) {
  const adRef = useRef<HTMLDivElement>(null);
  const isLoaded = useRef(false);

  useEffect(() => {
    // Only load ads once and only in production
    if (isLoaded.current) return;
    
    try {
      // Check if AdSense script is loaded
      if (typeof window !== 'undefined' && (window as unknown as { adsbygoogle?: unknown[] }).adsbygoogle) {
        ((window as unknown as { adsbygoogle: unknown[] }).adsbygoogle = (window as unknown as { adsbygoogle: unknown[] }).adsbygoogle || []).push({});
        isLoaded.current = true;
      }
    } catch (error) {
      console.error('AdSense error:', error);
    }
  }, []);

  // Show placeholder in development
  if (process.env.NODE_ENV === 'development' || !ADSENSE_CLIENT.includes('ca-pub-')) {
    return (
      <div className={`bg-gray-100 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center text-gray-400 text-sm ${className}`}>
        <div className="text-center p-4">
          <p className="font-medium">Ad Space</p>
          <p className="text-xs">Slot: {slot}</p>
        </div>
      </div>
    );
  }

  return (
    <div ref={adRef} className={className}>
      <ins
        className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client={ADSENSE_CLIENT}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  );
}

// Predefined ad sizes for common placements
export function AdBannerTop() {
  return (
    <div className="w-full max-w-4xl mx-auto px-4 py-2">
      <AdBanner 
        slot="1234567890" 
        format="horizontal" 
        className="min-h-[90px] sm:min-h-[100px]"
      />
    </div>
  );
}

export function AdBannerSidebar() {
  return (
    <AdBanner 
      slot="2345678901" 
      format="rectangle" 
      className="min-h-[250px] w-full"
    />
  );
}

export function AdBannerInArticle() {
  return (
    <div className="my-6">
      <AdBanner 
        slot="3456789012" 
        format="auto" 
        className="min-h-[250px]"
      />
    </div>
  );
}

export function AdBannerFooter() {
  return (
    <div className="w-full bg-gray-50 py-4">
      <div className="max-w-4xl mx-auto px-4">
        <AdBanner 
          slot="4567890123" 
          format="horizontal" 
          className="min-h-[90px]"
        />
      </div>
    </div>
  );
}
