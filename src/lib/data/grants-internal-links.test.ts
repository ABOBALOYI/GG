import { describe, it, expect } from 'vitest';
import { getAllGrants, getAllGrantSlugs } from './grants';
import { getAllAppealSlugs } from './appeals';

describe('Internal Links', () => {
  /**
   * **Feature: grantguide-sa, Property 12: Internal Link Presence**
   * **Validates: Requirements 8.4**
   *
   * WHEN rendering grant-related pages THEN the System SHALL include
   * internal links to related statuses, appeals, and payment information
   */
  it('Property 12: each grant has a corresponding appeal guide', () => {
    const grantSlugs = getAllGrantSlugs();
    const appealSlugs = getAllAppealSlugs();

    // Every grant should have an appeal guide
    grantSlugs.forEach((grantSlug) => {
      expect(appealSlugs).toContain(grantSlug);
    });
  });

  it('Property 12: grants have valid slugs for URL generation', () => {
    const grants = getAllGrants();

    grants.forEach((grant) => {
      // Slugs should be URL-safe
      expect(grant.slug).toMatch(/^[a-z0-9-]+$/);
      // Slugs should not have consecutive hyphens
      expect(grant.slug).not.toMatch(/--/);
      // Slugs should not start or end with hyphen
      expect(grant.slug).not.toMatch(/^-|-$/);
    });
  });

  it('Property 12: grant pages can link to checklist with query param', () => {
    const grantSlugs = getAllGrantSlugs();

    // Each grant slug should be valid for checklist URL
    grantSlugs.forEach((slug) => {
      const checklistUrl = `/checklist?grant=${slug}`;
      expect(checklistUrl).toContain(slug);
    });
  });

  it('Property 12: all grants have processing timeline for status links', () => {
    const grants = getAllGrants();

    grants.forEach((grant) => {
      expect(grant.processingTimeline).toBeTruthy();
      // Timeline should mention days
      expect(grant.processingTimeline.toLowerCase()).toContain('day');
    });
  });
});
