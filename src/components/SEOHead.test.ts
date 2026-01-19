import { describe, it, expect } from 'vitest';
import {
  generateSEOMetadata,
  generateFAQSchema,
  generateBreadcrumbSchema,
} from './SEOHead';

describe('SEOHead', () => {
  /**
   * **Feature: grantguide-sa, Property 2: SEO Element Compliance**
   * **Validates: Requirements 1.4, 8.1, 8.2, 8.3**
   *
   * WHEN any content page is rendered THEN the System SHALL include proper
   * H1 title, H2/H3 section hierarchy, and meta descriptions
   */
  it('Property 2: generateSEOMetadata includes required fields', () => {
    const metadata = generateSEOMetadata({
      title: 'Test Page',
      description: 'Test description',
      path: '/test',
    });

    expect(metadata.title).toContain('Test Page');
    expect(metadata.title).toContain('GrantGuide SA');
    expect(metadata.description).toBe('Test description');
    expect(metadata.openGraph?.title).toBeDefined();
    expect(metadata.openGraph?.description).toBeDefined();
    expect(metadata.openGraph?.url).toContain('/test');
  });

  it('Property 2: generateSEOMetadata sets canonical URL', () => {
    const metadata = generateSEOMetadata({
      title: 'Test',
      description: 'Test',
      path: '/grants/old-age-grant',
    });

    expect(metadata.alternates?.canonical).toContain('/grants/old-age-grant');
  });

  /**
   * **Property 2: FAQ structured data for rich results**
   * **Validates: Requirements 8.3**
   */
  it('Property 2: generateFAQSchema creates valid FAQ structured data', () => {
    const faqs = [
      { question: 'What is SASSA?', answer: 'South African Social Security Agency' },
      { question: 'How to apply?', answer: 'Visit your nearest SASSA office' },
    ];

    const schema = generateFAQSchema(faqs);

    expect(schema['@context']).toBe('https://schema.org');
    expect(schema['@type']).toBe('FAQPage');
    expect(schema.mainEntity).toHaveLength(2);
    expect(schema.mainEntity[0]['@type']).toBe('Question');
    expect(schema.mainEntity[0].name).toBe('What is SASSA?');
    expect(schema.mainEntity[0].acceptedAnswer['@type']).toBe('Answer');
  });

  it('Property 2: generateBreadcrumbSchema creates valid breadcrumb data', () => {
    const breadcrumbs = [
      { name: 'Home', url: '/' },
      { name: 'Grants', url: '/grants' },
      { name: 'Old Age Grant', url: '/grants/old-age-grant' },
    ];

    const schema = generateBreadcrumbSchema(breadcrumbs);

    expect(schema['@context']).toBe('https://schema.org');
    expect(schema['@type']).toBe('BreadcrumbList');
    expect(schema.itemListElement).toHaveLength(3);
    expect(schema.itemListElement[0].position).toBe(1);
    expect(schema.itemListElement[2].name).toBe('Old Age Grant');
  });
});
