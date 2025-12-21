'use client';

import Link from 'next/link';
import { ExternalLink, AlertTriangle } from 'lucide-react';
import { useLanguage } from '@/lib/i18n/LanguageContext';

export default function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="bg-gray-950 text-white mt-auto border-t border-white/5">
      <div className="max-w-7xl mx-auto px-6 py-20 md:py-32">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-16 md:gap-8">
          <div className="md:col-span-4 max-w-sm">
            <Link href="/" className="flex items-center gap-3 mb-8">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-green-500 to-green-700 flex items-center justify-center shadow-lg shadow-green-500/20">
                <span className="text-white font-black text-xl">G</span>
              </div>
              <span className="text-2xl font-black tracking-tight">Grant<span className="text-green-500">Guide</span></span>
            </Link>
            <p className="text-gray-400 text-lg leading-relaxed mb-8 font-medium">{t('footerDesc')}</p>
          </div>

          <div className="md:col-span-2">
            <h3 className="font-bold text-white text-sm uppercase tracking-widest mb-8">{t('resources')}</h3>
            <ul className="space-y-4">
              <li><Link href="/grants" className="text-gray-400 hover:text-green-400 transition-colors font-medium">{t('allGrants')}</Link></li>
              <li><Link href="/payment-dates" className="text-gray-400 hover:text-green-400 transition-colors font-medium">{t('paymentDates')}</Link></li>
              <li><Link href="/status" className="text-gray-400 hover:text-green-400 transition-colors font-medium">{t('statusCodes')}</Link></li>
              <li><Link href="/checklist" className="text-gray-400 hover:text-green-400 transition-colors font-medium">{t('checklist')}</Link></li>
            </ul>
          </div>

          <div className="md:col-span-2">
            <h3 className="font-bold text-white text-sm uppercase tracking-widest mb-8">{t('getHelp')}</h3>
            <ul className="space-y-4">
              <li><Link href="/help" className="text-gray-400 hover:text-green-400 transition-colors font-medium">{t('aiAssistant')}</Link></li>
              <li><Link href="/appeals" className="text-gray-400 hover:text-green-400 transition-colors font-medium">{t('appeals')}</Link></li>
              <li><Link href="/blog" className="text-gray-400 hover:text-green-400 transition-colors font-medium">Blog</Link></li>
            </ul>
          </div>

          <div className="md:col-span-4">
            <h3 className="font-bold text-white text-sm uppercase tracking-widest mb-8">{t('officialResources')}</h3>
            <ul className="space-y-4">
              <li><a href="https://www.sassa.gov.za" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-green-400 transition-all font-medium inline-flex items-center gap-2 group decoration-2 underline-offset-4 hover:underline">
                {t('sassaOfficial')} <ExternalLink className="w-4 h-4 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
              </a></li>
              <li><a href="https://srd.sassa.gov.za" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-green-400 transition-all font-medium inline-flex items-center gap-2 group decoration-2 underline-offset-4 hover:underline">
                {t('srdPortal')} <ExternalLink className="w-4 h-4 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
              </a></li>
            </ul>
          </div>
        </div>
      </div>

      <div className="border-t border-white/5 bg-black/20">
        <div className="max-w-7xl mx-auto px-6 py-10">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-8">
            <div className="flex flex-col gap-2">
              <p className="text-gray-500 font-bold">© {new Date().getFullYear()} GrantGuide SA</p>
              <p className="text-gray-600 text-sm max-w-2xl font-medium">{t('footerDisclaimer')}</p>
              <div className="flex gap-4 mt-2">
                <Link href="/privacy" className="text-gray-500 hover:text-green-400 text-sm transition-colors">Privacy Policy</Link>
              </div>
            </div>
            <div className="flex items-center gap-4 bg-white/5 px-6 py-3 rounded-2xl border border-white/10">
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              <span className="text-gray-400 text-sm font-semibold uppercase tracking-wider">Independent Platform</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

