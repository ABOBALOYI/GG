/**
 * PII (Personally Identifiable Information) Validator
 * Detects and rejects inputs containing sensitive information
 * 
 * **Feature: grantguide-sa, Property 5: PII Detection and Rejection**
 * **Validates: Requirements 4.1, 4.6**
 */

export interface PIIValidationResult {
  isValid: boolean;
  containsPII: boolean;
  piiTypes: string[];
  message?: string;
}

// South African ID number pattern: 13 digits
// Format: YYMMDD SSSS C A Z
const SA_ID_PATTERN = /\b\d{13}\b/g;

// Bank account patterns (various SA banks use 9-12 digits)
const BANK_ACCOUNT_PATTERN = /\b\d{9,12}\b/g;

// Phone number patterns (SA mobile: 0XX XXX XXXX or +27 XX XXX XXXX)
const PHONE_PATTERN = /\b(?:0\d{9}|\+27\d{9}|27\d{9})\b/g;

// Email pattern
const EMAIL_PATTERN = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;

/**
 * Validates input text for PII
 * Returns validation result with details about detected PII
 */
export function validateInput(text: string): PIIValidationResult {
  const piiTypes: string[] = [];
  
  // Check for SA ID numbers
  if (SA_ID_PATTERN.test(text)) {
    piiTypes.push('ID number');
  }
  
  // Reset regex lastIndex
  SA_ID_PATTERN.lastIndex = 0;
  
  // Check for bank account numbers (only if not already flagged as ID)
  // We need to be careful here as ID numbers are also 13 digits
  const potentialBankNumbers = text.match(BANK_ACCOUNT_PATTERN) || [];
  const idNumbers = text.match(SA_ID_PATTERN) || [];
  
  // Filter out numbers that are part of ID numbers
  const bankNumbers = potentialBankNumbers.filter(num => 
    !idNumbers.some(id => id.includes(num) || num.includes(id))
  );
  
  if (bankNumbers.length > 0 && !piiTypes.includes('ID number')) {
    // Additional check: bank account numbers in context
    const bankKeywords = /bank|account|acc|fnb|absa|standard|nedbank|capitec/i;
    if (bankKeywords.test(text)) {
      piiTypes.push('bank account number');
    }
  }
  
  // Check for phone numbers
  if (PHONE_PATTERN.test(text)) {
    piiTypes.push('phone number');
  }
  PHONE_PATTERN.lastIndex = 0;
  
  // Check for email addresses
  if (EMAIL_PATTERN.test(text)) {
    piiTypes.push('email address');
  }
  EMAIL_PATTERN.lastIndex = 0;
  
  const containsPII = piiTypes.length > 0;
  
  return {
    isValid: !containsPII,
    containsPII,
    piiTypes,
    message: containsPII 
      ? `Please don't share your ${piiTypes.join(', ')}. We don't need this information to help you.`
      : undefined
  };
}

/**
 * Checks if a string contains a valid SA ID number pattern
 */
export function containsSAIDNumber(text: string): boolean {
  return SA_ID_PATTERN.test(text);
}

/**
 * Sanitizes text by removing potential PII (for logging purposes)
 * Replaces detected PII with placeholders
 */
export function sanitizeForLogging(text: string): string {
  let sanitized = text;
  
  // Replace ID numbers
  sanitized = sanitized.replace(SA_ID_PATTERN, '[ID_REDACTED]');
  
  // Replace phone numbers
  sanitized = sanitized.replace(PHONE_PATTERN, '[PHONE_REDACTED]');
  
  // Replace emails
  sanitized = sanitized.replace(EMAIL_PATTERN, '[EMAIL_REDACTED]');
  
  // Replace potential bank account numbers (9-12 consecutive digits)
  sanitized = sanitized.replace(BANK_ACCOUNT_PATTERN, '[NUMBER_REDACTED]');
  
  return sanitized;
}
