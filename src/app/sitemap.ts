import { MetadataRoute } from 'next';
import { getAllGrantSlugs } from '@/lib/data/grants';
import { getAllStatusCodeValues } from '@/lib/data/status-codes';
import { getAllAppealSlugs } from '@/lib/data/appeals';
import { getAvailableMonths } from '@/lib/data/payment-dates';
import { getAllBlogSlugs } from '@/lib/data/blog-posts';

const BASE_URL = 'https://grantsguide.co.za';

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: BASE_URL,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${BASE_URL}/grants`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${BASE_URL}/payment-dates`,
      lastModified: now,
      changeFrequency: 'daily',
      priority: 0.9,
    },
    {
      url: `${BASE_URL}/status`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/appeals`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/checklist`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    {
      url: `${BASE_URL}/help`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    {
      url: `${BASE_URL}/privacy`,
      lastModified: now,
      changeFrequency: 'yearly',
      priority: 0.3,
    },
  ];

  // Grant pages
  const grantPages: MetadataRoute.Sitemap = getAllGrantSlugs().map((slug) => ({
    url: `${BASE_URL}/grants/${slug}`,
    lastModified: now,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  // Status code pages
  const statusPages: MetadataRoute.Sitemap = getAllStatusCodeValues().map((code) => ({
    url: `${BASE_URL}/status/${code.toLowerCase()}`,
    lastModified: now,
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }));

  // Appeal pages
  const appealPages: MetadataRoute.Sitemap = getAllAppealSlugs().map((slug) => ({
    url: `${BASE_URL}/appeals/${slug}`,
    lastModified: now,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }));

  // Payment date pages
  const paymentPages: MetadataRoute.Sitemap = getAvailableMonths().map(({ slug }) => ({
    url: `${BASE_URL}/payment-dates/${slug}`,
    lastModified: now,
    changeFrequency: 'daily' as const,
    priority: 0.8,
  }));

  // Blog pages
  const blogPages: MetadataRoute.Sitemap = [
    {
      url: `${BASE_URL}/blog`,
      lastModified: now,
      changeFrequency: 'daily' as const,
      priority: 0.8,
    },
    ...getAllBlogSlugs().map((slug) => ({
      url: `${BASE_URL}/blog/${slug}`,
      lastModified: now,
      changeFrequency: 'weekly' as const,
      priority: 0.7,
    })),
  ];

  return [
    ...staticPages,
    ...grantPages,
    ...statusPages,
    ...appealPages,
    ...paymentPages,
    ...blogPages,
  ];
}
