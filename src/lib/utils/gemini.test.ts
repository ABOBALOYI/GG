import { describe, it, expect } from 'vitest';
import fc from 'fast-check';
import { buildPrompt, parseGeminiResponse, SYSTEM_PROMPT, RESPONSE_DISCLAIMER } from './gemini';

describe('Gemini Integration', () => {
  /**
   * **Feature: grantguide-sa, Property 6: Gemini System Prompt Injection**
   * **Validates: Requirements 4.3**
   * 
   * For any Gemini API call, the request SHALL include the mandatory system prompt
   * that identifies the assistant as unofficial and prohibits SASSA impersonation
   */
  it('Property 6: system prompt is always included in built prompts', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 10, maxLength: 500 }), // question
        fc.option(fc.string({ minLength: 0, maxLength: 200 })), // optional context
        (question, context) => {
          const prompt = buildPrompt(question, context ?? undefined);
          
          // System prompt must be included
          const hasSystemPrompt = prompt.includes(SYSTEM_PROMPT);
          
          // Must contain key safety phrases
          const hasUnofficialWarning = prompt.toLowerCase().includes('unofficial');
          const hasNotSASSA = prompt.toLowerCase().includes('not sassa');
          const hasNoPersonalInfo = prompt.toLowerCase().includes('never ask for');
          
          return hasSystemPrompt && hasUnofficialWarning && hasNotSASSA && hasNoPersonalInfo;
        }
      ),
      { numRuns: 100 }
    );
  });

  /**
   * **Feature: grantguide-sa, Property 7: AI Response Structure Conformance**
   * **Validates: Requirements 4.4**
   * 
   * For any successful AI response, the output SHALL contain the answer with disclaimer
   */
  it('Property 7: parsed responses always include disclaimer', () => {
    fc.assert(
      fc.property(
        fc.string({ minLength: 10, maxLength: 1000 }), // raw response text
        (rawResponse) => {
          const parsed = parseGeminiResponse(rawResponse);
          
          // Must have answer field with disclaimer
          const hasAnswer = typeof parsed.answer === 'string' && parsed.answer.length > 0;
          const hasDisclaimer = parsed.answer.includes(RESPONSE_DISCLAIMER);
          
          return hasAnswer && hasDisclaimer;
        }
      ),
      { numRuns: 100 }
    );
  });

  describe('buildPrompt', () => {
    it('includes the question in the prompt', () => {
      const question = 'What is the Old Age Grant?';
      const prompt = buildPrompt(question);
      
      expect(prompt).toContain(question);
      expect(prompt).toContain(SYSTEM_PROMPT);
    });

    it('includes context when provided', () => {
      const question = 'How do I apply?';
      const context = 'User is asking about Child Support Grant';
      const prompt = buildPrompt(question, context);
      
      expect(prompt).toContain(context);
      expect(prompt).toContain('RELEVANT CONTEXT');
    });

    it('system prompt contains safety rules', () => {
      expect(SYSTEM_PROMPT).toContain('NOT SASSA');
      expect(SYSTEM_PROMPT).toContain('UNOFFICIAL');
      expect(SYSTEM_PROMPT).toContain('NEVER ask for');
      expect(SYSTEM_PROMPT).toContain('ID numbers');
      expect(SYSTEM_PROMPT).toContain('bank details');
    });
  });

  describe('parseGeminiResponse', () => {
    it('wraps response with disclaimer', () => {
      const rawResponse = 'Your application is being processed.';
      const parsed = parseGeminiResponse(rawResponse);
      
      expect(parsed.answer).toContain(rawResponse);
      expect(parsed.answer).toContain(RESPONSE_DISCLAIMER);
    });

    it('always includes disclaimer', () => {
      const parsed = parseGeminiResponse('Any response');
      expect(parsed.answer).toContain(RESPONSE_DISCLAIMER);
    });
  });
});
