/**
 * Gemini AI Integration
 * Wraps Gemini API calls with system prompt injection
 * 
 * **Feature: grantguide-sa, Property 6: Gemini System Prompt Injection**
 * **Validates: Requirements 4.3**
 */

import { GoogleGenerativeAI } from '@google/generative-ai';
import type { AIResponse } from '../types';

// Get current month info for payment dates
const now = new Date();
const currentMonth = now.toLocaleDateString('en-ZA', { month: 'long', year: 'numeric' });
const monthNum = String(now.getMonth() + 1).padStart(2, '0');
const year = now.getFullYear();

// System prompt that MUST be included in all Gemini calls
export const SYSTEM_PROMPT = `You are an AI assistant for GrantGuide SA, an UNOFFICIAL and INDEPENDENT platform that helps South Africans understand SASSA grants.

CRITICAL RULES:
1. You are NOT SASSA. You do NOT represent SASSA. Always make this clear.
2. You CANNOT process applications, check real statuses, or access SASSA systems.
3. You provide GENERAL INFORMATION ONLY based on publicly available SASSA guidelines.
4. NEVER ask for or accept ID numbers, bank details, or other personal information.
5. Always recommend users visit official SASSA offices or sassa.gov.za for official services.
6. Be helpful, accurate, and compassionate - many users are in difficult situations.
7. Keep responses concise and easy to understand.

=== SASSA GRANT AMOUNTS (2026) ===
- Old Age Grant: R2,180/month (for citizens 60+ years)
- Disability Grant: R2,180/month (for people 18-59 with disabilities)
- Child Support Grant: R530/month per child (for children under 18)
- Foster Child Grant: R1,180/month per foster child
- Care Dependency Grant: R2,180/month (for children with severe disabilities)
- Grant-in-Aid: R530/month (additional support for those needing full-time care)
- War Veterans Grant: R2,200/month

=== PAYMENT DATES FOR ${currentMonth.toUpperCase()} ===
All grants:
- Bank payments: 1st of the month (${year}-${monthNum}-01)
- Old Age & Disability (cash/post office): 3rd-5th of the month
- Child Support Grant (cash/post office): 6th-7th of the month

Note: If the 1st falls on a weekend, bank payments go through on the last working day before.

=== ELIGIBILITY REQUIREMENTS ===

OLD AGE GRANT:
- Age: 60 years or older
- Citizenship: SA citizen, permanent resident, or refugee
- Means test: Single person max income R86,280/year, Married R172,560/year
- Cannot receive another social grant

CHILD SUPPORT GRANT:
- Child must be under 18 years
- Must be primary caregiver
- Means test: Single caregiver max R52,800/year, Married R105,600/year

DISABILITY GRANT:
- Age: 18-59 years
- Must have disability preventing work (medical assessment required)
- Means test: Same as Old Age Grant

=== STATUS CODES ===
- PENDING: Application being processed (normal, takes up to 90 days)
- APPROVED: Grant approved, payments will start
- DECLINED: Application unsuccessful (can appeal within 90 days)
- ACTIVE: Grant active, receiving payments
- SUSPENDED: Payments paused (visit SASSA to resolve)
- CANCELLED: Grant permanently stopped

=== HOW TO APPLY ===
1. Gather documents: ID, proof of residence, bank statements
2. Visit nearest SASSA office
3. Complete application form
4. Biometric verification (fingerprints, photo)
5. Wait for outcome (up to 90 days)

=== APPEALS ===
- You have 90 days from decline date to appeal
- Request written reasons for decline
- Submit appeal at SASSA office with additional documents
- Appeal processing takes 30-90 days

=== CONTACT INFO ===
- SASSA toll-free: 0800 60 10 11
- Website: www.sassa.gov.za
- SRD Portal: srd.sassa.gov.za

Keep responses helpful, accurate, and remind users you are unofficial.`;

// Disclaimer that MUST be included in all responses
export const RESPONSE_DISCLAIMER =
  'This information is provided by GrantGuide SA, an unofficial platform. ' +
  'For official information and services, please visit sassa.gov.za or your nearest SASSA office.';

export interface GeminiRequest {
  question: string;
  context?: string;
}

/**
 * Builds the full prompt with system instructions
 */
export function buildPrompt(question: string, context?: string): string {
  let prompt = SYSTEM_PROMPT + '\n\n';

  if (context) {
    prompt += `RELEVANT CONTEXT:\n${context}\n\n`;
  }

  prompt += `USER QUESTION:\n${question}`;

  return prompt;
}

/**
 * Calls the Gemini API with the user's question
 */
export async function callGemini(request: GeminiRequest): Promise<AIResponse> {
  const apiKey = process.env.GEMINI_API_KEY;

  // If no API key, use fallback responses
  if (!apiKey) {
    console.warn('GEMINI_API_KEY not set, using fallback responses');
    return getFallbackResponse(request.question);
  }

  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: 'gemini-2.0-flash',
      generationConfig: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 1024,
      },
    });

    const prompt = buildPrompt(request.question, request.context);
    const result = await model.generateContent(prompt);
    const response = result.response;
    const text = response.text();

    return {
      answer: text + '\n\n---\n' + RESPONSE_DISCLAIMER,
    };
  } catch (error) {
    console.error('Gemini API error:', error);
    // Fall back to mock responses on error
    return getFallbackResponse(request.question);
  }
}

/**
 * Fallback responses when API is unavailable - includes real SASSA data
 */
function getFallbackResponse(question: string): AIResponse {
  const q = question.toLowerCase();

  // Payment dates questions
  if (q.includes('payment') || q.includes('pay date') || q.includes('when') && (q.includes('paid') || q.includes('get') || q.includes('receive'))) {
    return {
      answer: `**SASSA Payment Dates for ${currentMonth}:**

**Bank Payments (all grants):** 1st of the month
- If the 1st falls on a weekend, payment is made on the last working day before.

**Cash/Post Office Payments:**
- Old Age Grant & Disability Grant: 3rd - 5th of the month
- Child Support Grant: 6th - 7th of the month

**Tips:**
- Bring your SASSA card and ID when collecting
- Uncollected grants may be suspended after 3 consecutive months
- Check your specific pay point for exact times

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Grant amounts
  if (q.includes('how much') || q.includes('amount') || q.includes('value') || (q.includes('r') && q.includes('grant'))) {
    return {
      answer: `**SASSA Grant Amounts (2026):**

- **Old Age Grant:** R2,180/month
- **Disability Grant:** R2,180/month  
- **Child Support Grant:** R530/month per child
- **Foster Child Grant:** R1,180/month per child
- **Care Dependency Grant:** R2,180/month
- **Grant-in-Aid:** R530/month (additional)
- **War Veterans Grant:** R2,200/month

These amounts are reviewed annually and may increase in April each year.

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Status questions
  if (q.includes('pending') || q.includes('status')) {
    return {
      answer: `**Understanding SASSA Status Codes:**

**PENDING** - Your application is being processed. This is normal and can take up to 90 days.

**What to do:**
1. Wait for an SMS notification from SASSA
2. Check your status online at srd.sassa.gov.za after 30 days
3. Visit your local SASSA office if no update after 90 days

**Other status codes:**
- **APPROVED** - Grant approved, payments will start
- **DECLINED** - Not successful (can appeal within 90 days)
- **ACTIVE** - Receiving payments
- **SUSPENDED** - Payments paused (visit SASSA)

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Appeal questions
  if (q.includes('declined') || q.includes('rejected') || q.includes('appeal')) {
    return {
      answer: `**How to Appeal a SASSA Decision:**

If your application was declined, you have **90 days** to appeal.

**Steps to appeal:**
1. Request written reasons for the decline from SASSA
2. Gather additional supporting documents
3. Visit your local SASSA office to submit the appeal
4. Keep copies of everything you submit

**Important:**
- The 90-day deadline is strict!
- You may be called for an appeal hearing
- Appeal processing takes 30-90 days
- If unsuccessful, you can approach the courts

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Old age grant
  if (q.includes('old age') || q.includes('pension') || (q.includes('60') && q.includes('year'))) {
    return {
      answer: `**Old Age Grant Information:**

**Amount:** R2,180 per month

**Eligibility:**
- Must be 60 years or older
- South African citizen, permanent resident, or refugee
- Must pass the means test:
  - Single: Max income R86,280/year
  - Married: Max income R172,560/year
- Cannot receive another social grant

**How to apply:**
1. Visit your nearest SASSA office with your ID
2. Bring proof of residence and bank statements
3. Application is free
4. Processing takes up to 90 days

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Child support grant
  if (q.includes('child support') || q.includes('child grant') || q.includes('csg')) {
    return {
      answer: `**Child Support Grant Information:**

**Amount:** R530 per month per child

**Eligibility:**
- Child must be under 18 years
- You must be the primary caregiver
- Must pass the means test:
  - Single caregiver: Max income R52,800/year
  - Married: Max income R105,600/year

**Documents needed:**
- Your ID
- Child's birth certificate
- Proof of residence

**How to apply:**
Visit your nearest SASSA office. Application is free and takes up to 90 days to process.

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Disability grant
  if (q.includes('disability')) {
    return {
      answer: `**Disability Grant Information:**

**Amount:** R2,180 per month

**Eligibility:**
- Age: 18-59 years old
- Must have a disability that prevents you from working
- Medical assessment by SASSA-appointed doctor required
- Must pass the means test:
  - Single: Max income R86,280/year
  - Married: Max income R172,560/year

**How to apply:**
1. Visit SASSA for medical assessment booking
2. Attend the medical assessment
3. Submit application with ID and proof of residence
4. Processing takes up to 90 days

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // How to apply
  if (q.includes('apply') || q.includes('application') || q.includes('how do i')) {
    return {
      answer: `**How to Apply for a SASSA Grant:**

**Step 1: Gather Documents**
- South African ID
- Proof of residence (utility bill, affidavit)
- Bank statements (3 months)
- For child grants: child's birth certificate

**Step 2: Visit SASSA Office**
- Find your nearest SASSA office
- No appointment needed
- Application is FREE

**Step 3: Complete Application**
- Fill in forms with SASSA staff assistance
- Biometric verification (fingerprints, photo)

**Step 4: Wait for Outcome**
- Processing takes up to 90 days
- You'll receive SMS notification
- Check status at srd.sassa.gov.za

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Documents needed
  if (q.includes('document') || q.includes('what do i need') || q.includes('bring')) {
    return {
      answer: `**Documents Needed for SASSA Applications:**

**For all grants:**
- South African ID (green book or smart card)
- Proof of residence (utility bill, lease, or affidavit)
- Bank statement or proof of banking details

**Additional documents:**
- **Child Support Grant:** Child's birth certificate
- **Disability Grant:** Medical reports (SASSA will arrange assessment)
- **Foster Child Grant:** Court order for foster care

**Tips:**
- Bring original documents AND copies
- If married, bring spouse's ID and income proof
- No certified copies needed for application

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Contact/office
  if (q.includes('contact') || q.includes('phone') || q.includes('office') || q.includes('number')) {
    return {
      answer: `**SASSA Contact Information:**

**Toll-free number:** 0800 60 10 11
**Website:** www.sassa.gov.za
**SRD Portal:** srd.sassa.gov.za

**Office hours:** Monday to Friday, 8:00 AM - 4:00 PM

**To find your nearest office:**
- Visit sassa.gov.za and use the office locator
- Or call the toll-free number

**What you can do online:**
- Check application status
- Update banking details
- Apply for SRD grant

---
${RESPONSE_DISCLAIMER}`,
    };
  }

  // Default response
  return {
    answer: `Thank you for your question about SASSA grants!

**I can help you with:**
- Grant amounts and eligibility
- Payment dates and schedules
- Application process
- Status codes explained
- Appeal procedures
- Required documents

**Quick info:**
- Old Age Grant: R2,180/month (60+ years)
- Child Support Grant: R530/month per child
- Disability Grant: R2,180/month

**For official assistance:**
- Call SASSA: 0800 60 10 11
- Visit: www.sassa.gov.za
- Go to your nearest SASSA office

Please ask a specific question and I'll do my best to help!

---
${RESPONSE_DISCLAIMER}`,
  };
}

/**
 * Parses Gemini response into structured format (kept for compatibility)
 */
export function parseGeminiResponse(rawResponse: string): AIResponse {
  return {
    answer: rawResponse + '\n\n---\n' + RESPONSE_DISCLAIMER,
  };
}
