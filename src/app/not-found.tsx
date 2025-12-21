'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Home, Search, HelpCircle, ArrowRight } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-16">
      <div className="text-center max-w-2xl mx-auto">
        {/* Animated 404 */}
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="relative mb-8"
        >
          <span className="text-[150px] md:text-[200px] font-bold text-gray-100 select-none">
            404
          </span>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-green-500 to-green-600 flex items-center justify-center shadow-xl shadow-green-500/25">
              <Search className="w-12 h-12 text-white" />
            </div>
          </motion.div>
        </motion.div>

        {/* Message */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Page Not Found
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Sorry, we couldn&apos;t find the page you&apos;re looking for. 
            It might have been moved or doesn&apos;t exist.
          </p>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="flex flex-wrap justify-center gap-4 mb-12"
        >
          <Link
            href="/"
            className="inline-flex items-center gap-2 bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-3 rounded-xl font-semibold shadow-lg shadow-green-600/25 hover:shadow-green-600/40 transition-all"
          >
            <Home className="w-5 h-5" />
            Go Home
          </Link>
          <Link
            href="/help"
            className="inline-flex items-center gap-2 bg-white text-green-700 border-2 border-green-700 px-6 py-3 rounded-xl font-semibold hover:bg-green-50 transition-colors"
          >
            <HelpCircle className="w-5 h-5" />
            Get Help
          </Link>
        </motion.div>

        {/* Popular Pages */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-gray-50 rounded-2xl p-8"
        >
          <h2 className="font-semibold text-gray-900 mb-6">Popular Pages</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { href: '/grants', label: 'All Grants' },
              { href: '/payment-dates', label: 'Payment Dates' },
              { href: '/status', label: 'Status Decoder' },
              { href: '/checklist', label: 'Document Checklist' },
            ].map((link, i) => (
              <Link
                key={link.href}
                href={link.href}
                className="group flex items-center justify-center gap-1 text-green-700 hover:text-green-800 font-medium transition-colors"
              >
                {link.label}
                <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </Link>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
