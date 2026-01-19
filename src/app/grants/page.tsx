'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { getAllGrants } from '@/lib/data/grants';
import { ArrowRight, Users, Clock, FileText, UserRound, Baby, Accessibility } from 'lucide-react';
import { StaggerContainer, StaggerItem } from '@/components/ui/AnimatedCard';
import { generateBreadcrumbSchema } from '@/components/SEOHead';
import { LucideIcon } from 'lucide-react';

const grantIcons: Record<string, LucideIcon> = {
  'old-age-grant': UserRound,
  'child-support-grant': Baby,
  'disability-grant': Accessibility,
};

const grantAmounts: Record<string, string> = {
  'old-age-grant': 'R2,180',
  'child-support-grant': 'R530',
  'disability-grant': 'R2,180',
};

const breadcrumbs = [
  { name: 'Home', url: '/' },
  { name: 'Grants', url: '/grants' }
];

export default function GrantsPage() {
  const grants = getAllGrants();

  return (
    <div className="min-h-screen">
      {/* Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateBreadcrumbSchema(breadcrumbs)) }}
      />
      
      {/* Hero Section */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-green-50 via-white to-amber-50" />
        <div className="absolute top-0 right-0 w-96 h-96 bg-green-100/50 rounded-full blur-3xl -translate-y-1/2" />
        
        <div className="relative max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center max-w-3xl mx-auto"
          >
            <span className="inline-block px-4 py-2 rounded-full bg-green-100 text-green-700 text-sm font-medium mb-6">
              Complete Grant Directory
            </span>
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              SASSA Grants
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              Explore all available social grants, understand eligibility requirements, 
              and learn how to apply successfully.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Grants Grid */}
      <section className="py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {grants.map((grant, i) => (
              <StaggerItem key={grant.slug}>
                <Link href={`/grants/${grant.slug}`} className="block h-full">
                  <motion.article
                    whileHover={{ y: -8 }}
                    className="group relative bg-white rounded-3xl p-8 shadow-lg shadow-black/5 border border-gray-100 hover:shadow-2xl hover:shadow-green-700/10 transition-all duration-500 h-full flex flex-col"
                  >
                    {/* Gradient overlay */}
                    <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-green-50 to-amber-50 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                    
                    <div className="relative flex-1">
                      {/* Icon & Amount */}
                      <div className="flex items-start justify-between mb-6">
                        {(() => {
                          const IconComponent = grantIcons[grant.slug] || FileText;
                          return (
                            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-green-100 to-green-50 flex items-center justify-center group-hover:scale-110 transition-transform">
                              <IconComponent className="w-8 h-8 text-green-700" />
                            </div>
                          );
                        })()}
                        <div className="text-right">
                          <span className="text-2xl font-bold text-green-700">
                            {grantAmounts[grant.slug] || 'Varies'}
                          </span>
                          <span className="block text-xs text-gray-500">per month</span>
                        </div>
                      </div>

                      {/* Title & Description */}
                      <h2 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-green-700 transition-colors">
                        {grant.name}
                      </h2>
                      <p className="text-gray-600 mb-6 leading-relaxed">
                        {grant.description}
                      </p>

                      {/* Quick Info */}
                      <div className="space-y-3 mb-6">
                        <div className="flex items-center gap-2 text-sm text-gray-500">
                          <Users className="w-4 h-4" />
                          <span>{grant.eligibilityCriteria.ageRequirement}</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-gray-500">
                          <Clock className="w-4 h-4" />
                          <span>Processing: {grant.processingTimeline}</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-gray-500">
                          <FileText className="w-4 h-4" />
                          <span>{grant.applicationSteps.length} application steps</span>
                        </div>
                      </div>
                    </div>

                    {/* CTA */}
                    <div className="relative flex items-center justify-between pt-6 border-t border-gray-100 group-hover:border-green-100 transition-colors">
                      <span className="text-green-700 font-semibold">Learn more</span>
                      <span className="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center group-hover:bg-green-100 transition-colors">
                        <ArrowRight className="w-5 h-5 text-green-700 group-hover:translate-x-1 transition-transform" />
                      </span>
                    </div>
                  </motion.article>
                </Link>
              </StaggerItem>
            ))}
          </StaggerContainer>
        </div>
      </section>

      {/* Help CTA */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-gradient-to-br from-green-700 to-green-800 rounded-3xl p-10 md:p-14 text-center text-white relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
            <div className="relative">
              <h2 className="text-3xl font-bold mb-4">Not sure which grant you qualify for?</h2>
              <p className="text-green-100 mb-8 max-w-xl mx-auto">
                Our AI assistant can help you understand your eligibility and guide you through the process.
              </p>
              <Link
                href="/help"
                className="inline-flex items-center gap-2 bg-white text-green-700 px-8 py-4 rounded-2xl font-semibold hover:bg-green-50 transition-colors"
              >
                Chat with AI Assistant
                <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
