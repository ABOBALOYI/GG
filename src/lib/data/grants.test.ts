import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { getAllGrants, getGrantBySlug, getAllGrantSlugs } from './grants';

describe('Grants Data', () => {
  /**
   * **Feature: grantguide-sa, Property 1: Grant Page Completeness**
   * **Validates: Requirements 1.1**
   * 
   * For any valid grant in the database, the grant SHALL contain all required sections
   */
  it('Property 1: all grants have complete required fields', () => {
    const grants = getAllGrants();
    
    grants.forEach(grant => {
      // Required fields must exist and be non-empty
      expect(grant.id).toBeDefined();
      expect(grant.slug).toBeTruthy();
      expect(grant.name).toBeTruthy();
      expect(grant.description).toBeTruthy();
      
      // Eligibility criteria must have required fields
      expect(grant.eligibilityCriteria).toBeDefined();
      expect(grant.eligibilityCriteria.citizenshipRequirement).toBeTruthy();
      expect(grant.eligibilityCriteria.residencyRequirement).toBeTruthy();
      expect(Array.isArray(grant.eligibilityCriteria.additionalCriteria)).toBe(true);
      
      // Other required arrays
      expect(Array.isArray(grant.disqualifiers)).toBe(true);
      expect(grant.disqualifiers.length).toBeGreaterThan(0);
      
      expect(Array.isArray(grant.incomeThresholds)).toBe(true);
      expect(grant.incomeThresholds.length).toBeGreaterThan(0);
      
      expect(Array.isArray(grant.applicationSteps)).toBe(true);
      expect(grant.applicationSteps.length).toBeGreaterThan(0);
      
      expect(grant.processingTimeline).toBeTruthy();
      
      expect(Array.isArray(grant.commonMistakes)).toBe(true);
    });
  });

  /**
   * Property: getGrantBySlug returns correct grant or undefined
   */
  it('getGrantBySlug returns matching grant for valid slugs', () => {
    const slugs = getAllGrantSlugs();
    
    slugs.forEach(slug => {
      const grant = getGrantBySlug(slug);
      expect(grant).toBeDefined();
      expect(grant?.slug).toBe(slug);
    });
  });

  it('getGrantBySlug returns undefined for invalid slugs', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 50 }).filter(s => !getAllGrantSlugs().includes(s)),
        (invalidSlug) => {
          const grant = getGrantBySlug(invalidSlug);
          return grant === undefined;
        }
      ),
      { numRuns: 50 }
    );
  });

  /**
   * Property: All application steps are numbered sequentially
   */
  it('application steps are numbered sequentially starting from 1', () => {
    const grants = getAllGrants();
    
    grants.forEach(grant => {
      grant.applicationSteps.forEach((step, index) => {
        expect(step.stepNumber).toBe(index + 1);
        expect(step.title).toBeTruthy();
        expect(step.description).toBeTruthy();
      });
    });
  });

  /**
   * Property: Income thresholds have valid structure
   */
  it('income thresholds have valid applicant types and positive amounts', () => {
    const grants = getAllGrants();
    
    grants.forEach(grant => {
      grant.incomeThresholds.forEach(threshold => {
        expect(threshold.applicantType).toBeTruthy();
        expect(threshold.maxIncome).toBeGreaterThan(0);
      });
    });
  });
});
