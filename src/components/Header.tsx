'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X } from 'lucide-react';
import LanguageSwitcher from './LanguageSwitcher';
import { useLanguage } from '@/lib/i18n/LanguageContext';

export default function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const pathname = usePathname();
  const { t } = useLanguage();

  const navItems = [
    { href: '/grants', labelKey: 'grants' as const },
    { href: '/payment-dates', labelKey: 'paymentDates' as const },
    { href: '/status', labelKey: 'statusDecoder' as const },
    { href: '/blog', label: 'Blog' },
    { href: '/help', labelKey: 'aiHelp' as const, highlight: true },
  ];

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`sticky top-0 left-0 right-0 z-[100] transition-all duration-500 ${isScrolled ? 'py-2' : 'py-4'}`}>
      <nav className={`max-w-7xl mx-auto px-4 transition-all duration-500 ${isScrolled ? 'scale-[0.98]' : 'scale-100'}`}>
        <div className={`glass shadow-2xl shadow-black/5 px-6 py-4 rounded-[32px] border border-white/40 flex items-center justify-between gap-4 transition-all duration-500 ${isScrolled ? 'bg-white/80' : 'bg-white/40'}`}>
          <Link href="/" className="flex items-center gap-3 group flex-shrink-0">
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-[18px] bg-gradient-to-br from-green-600 to-green-800 flex items-center justify-center shadow-lg shadow-green-900/20 group-hover:scale-110 group-hover:rotate-3 transition-all duration-500">
              <span className="text-white font-black text-lg sm:text-xl">G</span>
            </div>
            <span className="text-xl sm:text-2xl font-black text-gray-900 hidden xs:inline tracking-tight">
              Grant<span className="text-green-700">Guide</span>
            </span>
          </Link>

          <div className="hidden lg:flex items-center gap-2 bg-white/40 p-1.5 rounded-2xl border border-white/60">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`relative px-5 py-2.5 rounded-xl text-sm font-bold tracking-tight transition-all duration-300 ${pathname === item.href || pathname.startsWith(item.href + '/')
                  ? 'text-green-800 bg-white shadow-sm'
                  : 'text-gray-600 hover:text-green-700 hover:bg-white/50'
                  } ${item.highlight && !(pathname === item.href) ? 'bg-green-700 text-white shadow-lg hover:scale-105' : ''}`}
              >
                {item.label || t(item.labelKey!)}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-4">
            <LanguageSwitcher />
            <div className="h-8 w-px bg-gray-200 hidden lg:block" />
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="lg:hidden w-12 h-12 flex items-center justify-center rounded-2xl bg-white/60 hover:bg-white transition-colors border border-white/60"
            >
              {isMobileMenuOpen ? <X className="w-6 h-6 text-gray-900" /> : <Menu className="w-6 h-6 text-gray-900" />}
            </button>
          </div>
        </div>

        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: -20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -20 }}
              className="lg:hidden mt-4"
            >
              <div className="glass p-6 rounded-[32px] border border-white/40 shadow-2xl">
                <div className="space-y-2">
                  {navItems.map((item, i) => (
                    <motion.div key={item.href} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}>
                      <Link
                        href={item.href}
                        onClick={() => setIsMobileMenuOpen(false)}
                        className={`block px-6 py-4 rounded-2xl text-lg font-bold transition-all ${pathname === item.href ? 'bg-green-700 text-white' : 'hover:bg-green-50 text-gray-700'
                          }`}
                      >
                        {item.label || t(item.labelKey!)}
                      </Link>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
    </header>
  );
}

