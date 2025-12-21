'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { FileText, Calendar, Search, CheckSquare, MessageCircle, Scale, ArrowRight, Sparkles, UserRound, Baby, Accessibility } from 'lucide-react';
import { useLanguage } from '@/lib/i18n/LanguageContext';
import ChatWidget from '@/components/ChatWidget';

// FAQ Schema for SEO
const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'Is GrantsGuide AI affiliated with SASSA?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'No. GrantsGuide AI is an independent, unofficial platform. We provide information to help you understand SASSA grants, but we are not connected to SASSA in any way. For official services, please visit sassa.gov.za.'
      }
    },
    {
      '@type': 'Question',
      name: 'Is this service free?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, GrantsGuide AI is completely free to use. We are supported by advertisements.'
      }
    },
    {
      '@type': 'Question',
      name: 'Can I apply for grants through this website?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'No. We only provide information and guidance. To apply for grants, you must visit a SASSA office or use the official SASSA website.'
      }
    },
    {
      '@type': 'Question',
      name: 'How accurate is the information?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'We strive to keep our information up-to-date, but SASSA policies can change. Always verify important information with SASSA directly.'
      }
    }
  ]
};

export default function HomePage() {
  const { t } = useLanguage();

  return (
    <div className="overflow-hidden mesh-gradient">
      {/* FAQ Schema for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />

      {/* Hero */}
      <section className="relative min-h-screen flex items-center justify-center px-4 pt-32 pb-20">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[10%] left-[5%] w-[40%] h-[40%] bg-green-200/20 rounded-full blur-[120px] animate-float" />
          <div className="absolute bottom-[10%] right-[5%] w-[35%] h-[35%] bg-amber-200/20 rounded-full blur-[100px] animate-float" style={{ animationDelay: '-2s' }} />
        </div>

        <div className="relative max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="inline-flex items-center gap-2 px-6 py-2 rounded-full glass border border-green-200/50 text-green-700 text-sm font-semibold mb-12 shadow-sm"
          >
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span className="tracking-wide uppercase font-bold">{t('freeToUse')} • {t('available')} 2026</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 50, damping: 20 }}
            className="text-5xl sm:text-6xl md:text-8xl font-black text-gray-900 mb-8 leading-[1.1] tracking-tight"
          >
            {t('heroTitle')} 2026 <br />
            <span className="gradient-text italic px-2">{t('sassaGrants')}</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.8 }}
            className="text-xl sm:text-2xl text-gray-600 max-w-3xl mx-auto mb-14 leading-relaxed font-medium"
          >
            {t('heroSubtitle')}
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="flex flex-wrap justify-center gap-6 mb-24"
          >
            <Link href="/grants" className="btn-glow flex items-center gap-3 text-lg group">
              {t('exploreGrants')}
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link href="/help" className="btn-outline glass flex items-center gap-3 text-lg group">
              <MessageCircle className="w-5 h-5 text-green-600" />
              {t('getAiHelp')}
            </Link>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="grid grid-cols-3 gap-12 max-w-2xl mx-auto bg-white/40 backdrop-blur-md rounded-3xl p-8 border border-white/50 shadow-xl shadow-black/5"
          >
            {[{ value: '100%', label: t('freeToUse') }, { value: '24/7', label: t('available') }, { value: '6+', label: t('grantTypes') }].map((stat, i) => (
              <div key={i} className="text-center relative">
                {i > 0 && <div className="absolute left-[-24px] top-1/2 -translate-y-1/2 h-10 w-px bg-gray-200" />}
                <div className="text-3xl sm:text-4xl font-black text-green-700 mb-2">{stat.value}</div>
                <div className="text-gray-500 text-xs sm:text-sm font-bold uppercase tracking-widest">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* AI Chat - Primary CTA */}
      <section className="py-20 px-4 relative overflow-hidden bg-gradient-to-b from-transparent to-white/50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <span className="inline-block px-4 py-1.5 rounded-full bg-green-100 text-green-700 font-bold text-xs uppercase tracking-widest mb-6">
              {t('needHelp')}
            </span>
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              {t('chatWithAi')}
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto font-medium">
              {t('aiAssistantHelp')}
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="max-w-2xl mx-auto"
          >
            <div className="shadow-2xl shadow-green-900/10 rounded-3xl">
              <ChatWidget />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section className="py-32 px-4 relative">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-24"
          >
            <span className="inline-block px-4 py-1.5 rounded-full bg-green-100 text-green-700 font-bold text-xs uppercase tracking-widest mb-6">
              {t('everythingYouNeed')}
            </span>
            <h2 className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 mb-8 leading-tight">
              {t('whatCanWeHelp')}
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto font-medium leading-relaxed">
              {t('navigateWithConfidence')}
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { icon: FileText, title: t('grantInformation'), desc: t('grantInfoDesc'), href: '/grants', color: 'from-green-500 to-emerald-600' },
              { icon: Calendar, title: t('paymentDatesTitle'), desc: t('paymentDatesDesc'), href: '/payment-dates', color: 'from-amber-400 to-orange-500' },
              { icon: Search, title: t('statusDecoderTitle'), desc: t('statusDecoderDesc'), href: '/status', color: 'from-blue-500 to-indigo-600' },
              { icon: CheckSquare, title: t('documentChecklist'), desc: t('documentChecklistDesc'), href: '/checklist', color: 'from-purple-500 to-violet-600' },
              { icon: MessageCircle, title: t('aiCaseworker'), desc: t('aiCaseworkerDesc'), href: '/help', color: 'from-pink-500 to-rose-600' },
              { icon: Scale, title: t('appealsGuide'), desc: t('appealsGuideDesc'), href: '/appeals', color: 'from-cyan-500 to-blue-600' },
            ].map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.5 }}
              >
                <Link href={feature.href} className="group block h-full">
                  <div className="card-premium h-full p-10 bg-white/70 backdrop-blur-sm relative overflow-hidden">
                    <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${feature.color} opacity-[0.03] group-hover:opacity-[0.08] transition-opacity rounded-bl-[100px]`} />
                    <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-8 shadow-lg shadow-black/5 group-hover:scale-110 group-hover:rotate-3 transition-all duration-500`}>
                      <feature.icon className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-4 group-hover:text-green-700 transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed font-medium mb-8">
                      {feature.desc}
                    </p>
                    <div className="flex items-center text-green-700 font-bold uppercase tracking-wider text-sm">
                      {t('learnMore')}
                      <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-2 transition-transform duration-300" />
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Popular Grants */}
      <section className="py-32 px-4 bg-white/50 backdrop-blur-sm border-y border-gray-100">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between mb-20">
            <div>
              <span className="text-green-700 font-bold text-xs uppercase tracking-[0.2em] mb-4 block">
                {t('mostSearched')}
              </span>
              <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mt-4 leading-tight">
                {t('popularGrants')}
              </h2>
            </div>
            <Link href="/grants" className="mt-8 md:mt-0 btn-outline glass inline-flex items-center text-green-700 font-bold hover:text-green-800 transition-all px-8 py-4">
              {t('viewAllGrants')} <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { slug: 'old-age-grant', name: 'Old Age Grant', desc: 'For South African citizens aged 60 and older.', amount: 'R2,180', icon: UserRound, color: 'from-green-500 to-emerald-600' },
              { slug: 'child-support-grant', name: 'Child Support Grant', desc: 'For primary caregivers of children under 18.', amount: 'R530', icon: Baby, color: 'from-amber-400 to-orange-500' },
              { slug: 'disability-grant', name: 'Disability Grant', desc: 'For people with disabilities preventing work.', amount: 'R2,180', icon: Accessibility, color: 'from-blue-500 to-indigo-600' }
            ].map((grant, i) => (
              <motion.div
                key={grant.slug}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <Link href={`/grants/${grant.slug}`} className="group block h-full">
                  <div className="card-premium h-full p-10 bg-white/80 border-b-4 border-b-transparent group-hover:border-b-green-500">
                    <div className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${grant.color} flex items-center justify-center mb-8 shadow-lg group-hover:scale-110 group-hover:rotate-3 transition-all duration-500`}>
                      <grant.icon className="w-10 h-10 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-3 group-hover:text-green-700 transition-colors">
                      {grant.name}
                    </h3>
                    <p className="text-gray-600 mb-10 leading-relaxed font-medium">
                      {grant.desc}
                    </p>
                    <div className="flex items-center justify-between pt-6 border-t border-gray-100">
                      <div>
                        <span className="text-3xl font-black text-green-700">{grant.amount}</span>
                        <span className="text-sm font-bold text-gray-500 block uppercase tracking-wider">{t('perMonth')}</span>
                      </div>
                      <div className="w-12 h-12 rounded-full border-2 border-gray-100 flex items-center justify-center group-hover:bg-green-700 group-hover:border-green-700 transition-all duration-300">
                        <ArrowRight className="w-6 h-6 text-gray-400 group-hover:text-white group-hover:translate-x-1 transition-all" />
                      </div>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-32 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-20 animate-pulse-glow rounded-3xl p-8">
            <h2 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-8">{t('faq')}</h2>
            <p className="text-xl text-gray-600 font-medium">{t('gotQuestions')}</p>
          </div>
          <div className="space-y-6">
            {[
              { q: t('isAffiliatedQuestion'), a: t('isAffiliatedAnswer') },
              { q: t('isFreeQuestion'), a: t('isFreeAnswer') },
              { q: t('canApplyQuestion'), a: t('canApplyAnswer') },
              { q: t('howAccurateQuestion'), a: t('howAccurateAnswer') }
            ].map((faq, i) => (
              <motion.details key={i} className="group glass-premium rounded-[32px] overflow-hidden">
                <summary className="flex items-center justify-between px-10 py-8 cursor-pointer list-none">
                  <span className="text-xl font-bold text-gray-900 pr-8">{faq.q}</span>
                  <div className="flex-shrink-0 w-12 h-12 rounded-2xl bg-white flex items-center justify-center shadow-sm group-open:bg-green-700 transition-all duration-300">
                    <svg className="w-6 h-6 text-gray-400 group-open:text-white group-open:rotate-180 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 9l-7 7-7-7" /></svg>
                  </div>
                </summary>
                <div className="px-10 pb-10 text-lg text-gray-600 font-medium leading-relaxed border-t border-gray-100 pt-6 mx-10">
                  {faq.a}
                </div>
              </motion.details>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

