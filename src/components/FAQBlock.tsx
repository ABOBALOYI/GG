'use client';

import { motion } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

interface FAQ {
  question: string;
  answer: string;
}

interface FAQBlockProps {
  faqs: FAQ[];
  title?: string;
}

export default function FAQBlock({ faqs, title = 'Frequently Asked Questions' }: FAQBlockProps) {
  return (
    <section className="py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">{title}</h2>
      
      <div className="space-y-3">
        {faqs.map((faq, index) => (
          <motion.details
            key={index}
            initial={{ opacity: 0, y: 10 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.05 }}
            className="group bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow overflow-hidden"
          >
            <summary className="flex items-center justify-between px-6 py-5 cursor-pointer list-none">
              <span className="font-semibold text-gray-900 pr-4">{faq.question}</span>
              <span className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center group-open:bg-green-100 transition-colors">
                <ChevronDown className="w-4 h-4 text-gray-500 group-open:text-green-700 group-open:rotate-180 transition-all" />
              </span>
            </summary>
            <div className="px-6 pb-5 text-gray-600 leading-relaxed border-t border-gray-50">
              <p className="pt-4">{faq.answer}</p>
            </div>
          </motion.details>
        ))}
      </div>

      {/* FAQ Schema for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            mainEntity: faqs.map((faq) => ({
              '@type': 'Question',
              name: faq.question,
              acceptedAnswer: {
                '@type': 'Answer',
                text: faq.answer,
              },
            })),
          }),
        }}
      />
    </section>
  );
}
