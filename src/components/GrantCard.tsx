'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { ArrowRight, UserRound, Baby, Accessibility, FileText, LucideIcon } from 'lucide-react';
import type { Grant } from '@/lib/types';

interface GrantCardProps {
  grant: Grant;
  index?: number;
}

const grantIcons: Record<string, LucideIcon> = {
  'old-age-grant': UserRound,
  'child-support-grant': Baby,
  'disability-grant': Accessibility,
};

const grantColors: Record<string, string> = {
  'old-age-grant': 'from-green-500 to-emerald-600',
  'child-support-grant': 'from-amber-400 to-orange-500',
  'disability-grant': 'from-blue-500 to-indigo-600',
};

export default function GrantCard({ grant, index = 0 }: GrantCardProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ y: -8 }}
      className="group"
    >
      <Link href={`/grants/${grant.slug}`} className="block h-full">
        <div className="relative bg-white rounded-3xl p-8 shadow-lg shadow-black/5 border border-gray-100 hover:shadow-2xl hover:shadow-green-700/10 transition-all duration-500 h-full">
          {/* Gradient overlay on hover */}
          <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-green-50 to-amber-50 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          
          <div className="relative">
            {/* Icon */}
            {(() => {
              const IconComponent = grantIcons[grant.slug] || FileText;
              const colorClass = grantColors[grant.slug] || 'from-gray-500 to-gray-600';
              return (
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${colorClass} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <IconComponent className="w-7 h-7 text-white" />
                </div>
              );
            })()}
            
            {/* Title */}
            <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-green-700 transition-colors">
              {grant.name}
            </h3>
            
            {/* Description */}
            <p className="text-gray-600 mb-4 leading-relaxed">
              {grant.description}
            </p>
            
            {/* CTA */}
            <div className="flex items-center text-green-700 font-medium">
              <span>Learn more</span>
              <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>
      </Link>
    </motion.article>
  );
}
