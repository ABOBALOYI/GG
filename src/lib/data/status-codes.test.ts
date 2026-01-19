import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { getAllStatusCodes, getStatusByCode, getAllStatusCodeValues } from './status-codes';

describe('Status Codes Data', () => {
  /**
   * **Feature: grantguide-sa, Property 4: Status Code Information Completeness**
   * **Validates: Requirements 3.1, 3.2, 3.3**
   * 
   * For any status code query, the response SHALL contain: official meaning, 
   * simplified explanation, and recommended next steps
   */
  it('Property 4: all status codes have complete required fields', () => {
    const statusCodes = getAllStatusCodes();
    
    statusCodes.forEach(status => {
      // Required fields
      expect(status.id).toBeDefined();
      expect(status.code).toBeTruthy();
      expect(status.officialMeaning).toBeTruthy();
      expect(status.simplifiedMeaning).toBeTruthy();
      
      // Recommended actions must exist and have items
      expect(Array.isArray(status.recommendedActions)).toBe(true);
      expect(status.recommendedActions.length).toBeGreaterThan(0);
      
      // Related status codes must be an array
      expect(Array.isArray(status.relatedStatusCodes)).toBe(true);
    });
  });

  /**
   * Property: getStatusByCode is case-insensitive
   */
  it('getStatusByCode works case-insensitively', () => {
    const codes = getAllStatusCodeValues();
    
    codes.forEach(code => {
      const lower = getStatusByCode(code.toLowerCase());
      const upper = getStatusByCode(code.toUpperCase());
      const mixed = getStatusByCode(code.charAt(0).toUpperCase() + code.slice(1).toLowerCase());
      
      expect(lower).toBeDefined();
      expect(upper).toBeDefined();
      expect(mixed).toBeDefined();
      
      // All should return the same status
      expect(lower?.code).toBe(upper?.code);
      expect(upper?.code).toBe(mixed?.code);
    });
  });

  /**
   * Property: Invalid codes return undefined
   */
  it('getStatusByCode returns undefined for invalid codes', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 1, maxLength: 20 }).filter(s => 
          !getAllStatusCodeValues().map(c => c.toLowerCase()).includes(s.toLowerCase())
        ),
        (invalidCode) => {
          const status = getStatusByCode(invalidCode);
          return status === undefined;
        }
      ),
      { numRuns: 50 }
    );
  });

  /**
   * Property: Simplified meaning is more accessible than official meaning
   * (simplified should generally be longer with more explanation)
   */
  it('simplified meanings provide more context than official meanings', () => {
    const statusCodes = getAllStatusCodes();
    
    statusCodes.forEach(status => {
      // Simplified meaning should be substantial
      expect(status.simplifiedMeaning.length).toBeGreaterThan(20);
      // Should not just repeat the official meaning
      expect(status.simplifiedMeaning).not.toBe(status.officialMeaning);
    });
  });

  /**
   * Property: Related status codes reference valid codes
   */
  it('related status codes reference existing codes', () => {
    const allCodes = getAllStatusCodeValues();
    const statusCodes = getAllStatusCodes();
    
    statusCodes.forEach(status => {
      status.relatedStatusCodes.forEach(relatedCode => {
        expect(allCodes).toContain(relatedCode);
      });
    });
  });
});
