import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { validateInput, containsSAIDNumber, sanitizeForLogging } from './pii-validator';

describe('PII Validator', () => {
  /**
   * **Feature: grantguide-sa, Property 5: PII Detection and Rejection**
   * **Validates: Requirements 4.1, 4.6**
   * 
   * For any user input containing South African ID number patterns (13 digits),
   * the validator SHALL detect it and return containsPII = true
   */
  it('Property 5: detects SA ID numbers (13 consecutive digits)', () => {
    // Generate 13-digit ID numbers
    const digitArb = fc.integer({ min: 0, max: 9 });
    const idNumberArb = fc.array(digitArb, { minLength: 13, maxLength: 13 })
      .map(digits => digits.join(''));
    
    fc.assert(
      fc.property(
        idNumberArb,
        fc.string({ minLength: 0, maxLength: 50 }), // prefix
        fc.string({ minLength: 0, maxLength: 50 }), // suffix
        (idNumber, prefix, suffix) => {
          // Create input with ID number embedded
          const input = `${prefix} ${idNumber} ${suffix}`;
          const result = validateInput(input);
          
          // Should detect PII
          return result.containsPII === true && result.piiTypes.includes('ID number');
        }
      ),
      { numRuns: 100 }
    );
  });

  /**
   * Property: Clean text without PII patterns should pass validation
   */
  it('allows text without PII patterns', () => {
    // Generate alphabetic strings only
    const letterArb = fc.constantFrom(
      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
      'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
      ' ', '.', ',', '?', '!'
    );
    const textArb = fc.array(letterArb, { minLength: 10, maxLength: 200 })
      .map(chars => chars.join(''));
    
    fc.assert(
      fc.property(textArb, (text) => {
        const result = validateInput(text);
        // Text without numbers should be valid
        return result.isValid === true && result.containsPII === false;
      }),
      { numRuns: 100 }
    );
  });

  /**
   * Property: containsSAIDNumber should match validateInput for ID detection
   */
  it('containsSAIDNumber is consistent with validateInput', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 0, maxLength: 100 }),
        (text) => {
          const hasId = containsSAIDNumber(text);
          const validation = validateInput(text);
          
          // If containsSAIDNumber returns true, validation should detect ID
          if (hasId) {
            return validation.piiTypes.includes('ID number');
          }
          return true;
        }
      ),
      { numRuns: 100 }
    );
  });

  // Unit tests for specific cases
  describe('Unit Tests', () => {
    it('detects a valid SA ID number', () => {
      const result = validateInput('My ID is 9001015009087');
      expect(result.containsPII).toBe(true);
      expect(result.piiTypes).toContain('ID number');
      expect(result.isValid).toBe(false);
    });

    it('allows questions without PII', () => {
      const result = validateInput('What does PENDING status mean for my grant?');
      expect(result.containsPII).toBe(false);
      expect(result.isValid).toBe(true);
    });

    it('detects phone numbers', () => {
      const result = validateInput('Call me on 0821234567');
      expect(result.containsPII).toBe(true);
      expect(result.piiTypes).toContain('phone number');
    });

    it('detects email addresses', () => {
      const result = validateInput('Email me at test@example.com');
      expect(result.containsPII).toBe(true);
      expect(result.piiTypes).toContain('email address');
    });

    it('provides helpful error message', () => {
      const result = validateInput('My ID is 9001015009087');
      expect(result.message).toContain("don't share");
    });
  });

  describe('sanitizeForLogging', () => {
    it('redacts ID numbers', () => {
      const sanitized = sanitizeForLogging('ID: 9001015009087');
      expect(sanitized).not.toContain('9001015009087');
      expect(sanitized).toContain('[ID_REDACTED]');
    });

    it('redacts phone numbers', () => {
      const sanitized = sanitizeForLogging('Phone: 0821234567');
      expect(sanitized).not.toContain('0821234567');
    });

    it('redacts emails', () => {
      const sanitized = sanitizeForLogging('Email: test@example.com');
      expect(sanitized).not.toContain('test@example.com');
      expect(sanitized).toContain('[EMAIL_REDACTED]');
    });
  });
});
