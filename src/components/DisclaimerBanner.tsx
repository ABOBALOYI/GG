'use client';

import { useState } from 'react';
import { AlertTriangle, X, ExternalLink } from 'lucide-react';
import { useLanguage } from '@/lib/i18n/LanguageContext';

export default function DisclaimerBanner() {
  const [isVisible, setIsVisible] = useState(true);
  const { t } = useLanguage();

  if (!isVisible) return null;

  return (
    <div className="bg-gradient-to-r from-red-600 to-orange-600 text-white shadow-2xl relative z-[110]" role="alert">
      <div className="max-w-7xl mx-auto px-6 py-3">
        <div className="flex items-center justify-between gap-6">
          <div className="flex items-center gap-4 flex-1">
            <div className="hidden sm:flex flex-shrink-0 w-10 h-10 rounded-xl bg-white/20 items-center justify-center animate-pulse border border-white/30">
              <AlertTriangle className="w-5 h-5 text-white" />
            </div>
            <p className="text-sm md:text-base font-bold tracking-tight">
              <span className="uppercase text-xs bg-white/20 px-2 py-0.5 rounded-md mr-2 border border-white/20">{t('unofficialSite')}</span>
              {t('notAffiliated')}. {t('forOfficialServices')} →{' '}
              <a href="https://www.sassa.gov.za" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 underline decoration-2 underline-offset-4 hover:text-amber-200 transition-colors">
                sassa.gov.za <ExternalLink className="w-4 h-4" />
              </a>
            </p>
          </div>
          <button onClick={() => setIsVisible(false)} className="flex-shrink-0 w-10 h-10 flex items-center justify-center rounded-xl hover:bg-white/20 transition-all">
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}

