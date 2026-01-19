'use client';

import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  gradient?: boolean;
  glow?: boolean;
}

export default function GlassCard({ 
  children, 
  className = '',
  gradient = false,
  glow = false
}: GlassCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
      className={`
        relative rounded-3xl p-6 md:p-8
        ${gradient 
          ? 'bg-gradient-to-br from-white/80 to-white/40' 
          : 'bg-white/70'
        }
        backdrop-blur-xl border border-white/50
        shadow-xl shadow-black/5
        ${glow ? 'animate-pulse-glow' : ''}
        ${className}
      `}
    >
      {children}
    </motion.div>
  );
}

export function FeatureCard({ 
  icon, 
  title, 
  description,
  href,
  delay = 0
}: { 
  icon: ReactNode; 
  title: string; 
  description: string;
  href?: string;
  delay?: number;
}) {
  const content = (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ y: -8, transition: { duration: 0.3 } }}
      className="group relative bg-white rounded-3xl p-8 shadow-lg shadow-black/5 border border-gray-100 hover:shadow-2xl hover:shadow-green-700/10 transition-all duration-500"
    >
      {/* Gradient overlay on hover */}
      <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-green-50 to-amber-50 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      
      <div className="relative">
        {/* Icon container */}
        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-100 to-green-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
          <span className="text-green-700">{icon}</span>
        </div>
        
        <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-green-700 transition-colors">
          {title}
        </h3>
        <p className="text-gray-600 leading-relaxed">
          {description}
        </p>
        
        {href && (
          <div className="mt-4 flex items-center text-green-700 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
            Learn more
            <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        )}
      </div>
    </motion.div>
  );

  if (href) {
    return <a href={href} className="block">{content}</a>;
  }
  return content;
}
