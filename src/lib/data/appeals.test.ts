import { describe, it, expect } from 'vitest';
import { getAllAppealGuides, getAppealGuideByGrantSlug, getAllAppealSlugs } from './appeals';

describe('Appeals Data', () => {
  /**
   * **Feature: grantguide-sa, Property 8: Appeal Guide Completeness**
   * **Validates: Requirements 5.1, 5.2**
   * 
   * For any appeal guide page, the content SHALL include: step-by-step instructions,
   * required documents list, timeline information, and common pitfalls
   */
  it('Property 8: all appeal guides have complete required fields', () => {
    const guides = getAllAppealGuides();
    
    guides.forEach(guide => {
      // Required fields
      expect(guide.id).toBeDefined();
      expect(guide.grantId).toBeDefined();
      expect(guide.grantSlug).toBeTruthy();
      expect(guide.grantName).toBeTruthy();
      
      // Appeal steps must exist and have items
      expect(Array.isArray(guide.appealSteps)).toBe(true);
      expect(guide.appealSteps.length).toBeGreaterThan(0);
      
      // Each step must have required fields
      guide.appealSteps.forEach((step, index) => {
        expect(step.stepNumber).toBe(index + 1);
        expect(step.title).toBeTruthy();
        expect(step.description).toBeTruthy();
      });
      
      // Required documents must exist
      expect(Array.isArray(guide.requiredDocuments)).toBe(true);
      expect(guide.requiredDocuments.length).toBeGreaterThan(0);
      
      // Timeline must exist
      expect(guide.timeline).toBeTruthy();
      
      // Common pitfalls must exist
      expect(Array.isArray(guide.commonPitfalls)).toBe(true);
      expect(guide.commonPitfalls.length).toBeGreaterThan(0);
    });
  });

  /**
   * Property: getAppealGuideByGrantSlug returns correct guide
   */
  it('getAppealGuideByGrantSlug returns matching guide for valid slugs', () => {
    const slugs = getAllAppealSlugs();
    
    slugs.forEach(slug => {
      const guide = getAppealGuideByGrantSlug(slug);
      expect(guide).toBeDefined();
      expect(guide?.grantSlug).toBe(slug);
    });
  });

  /**
   * Property: Timeline mentions 90 days (standard appeal period)
   */
  it('all appeal guides mention the 90-day deadline', () => {
    const guides = getAllAppealGuides();
    
    guides.forEach(guide => {
      expect(guide.timeline.toLowerCase()).toContain('90');
    });
  });

  /**
   * Property: Required documents include decline letter
   */
  it('all appeal guides require the decline letter', () => {
    const guides = getAllAppealGuides();
    
    guides.forEach(guide => {
      const hasDeclineLetter = guide.requiredDocuments.some(doc => 
        doc.toLowerCase().includes('decline')
      );
      expect(hasDeclineLetter).toBe(true);
    });
  });
});
