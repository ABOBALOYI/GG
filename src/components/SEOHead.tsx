import { Metadata } from 'next';

interface SEOProps {
  title: string;
  description: string;
  path: string;
  type?: 'website' | 'article';
}

export function generateSEOMetadata({ title, description, path, type = 'website' }: SEOProps): Metadata {
  const fullTitle = `${title} | GrantsGuide SA`;
  const url = `https://grantsguide.co.za${path}`;

  return {
    title: fullTitle,
    description,
    openGraph: {
      title: fullTitle,
      description,
      url,
      siteName: 'GrantsGuide SA',
      type,
      locale: 'en_ZA',
    },
    twitter: {
      card: 'summary_large_image',
      title: fullTitle,
      description,
    },
    alternates: {
      canonical: url,
    },
  };
}

// FAQ Schema for structured data
export interface FAQItem {
  question: string;
  answer: string;
}

export function generateFAQSchema(faqs: FAQItem[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(faq => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      },
    })),
  };
}

// Breadcrumb Schema
export interface BreadcrumbItem {
  name: string;
  url: string;
}

export function generateBreadcrumbSchema(items: BreadcrumbItem[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: `https://grantsguide.co.za${item.url}`,
    })),
  };
}
