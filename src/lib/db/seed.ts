// Seed data for GrantGuide SA
// Run with: npx tsx src/lib/db/seed.ts

import { createClient } from '@libsql/client';
import { readFileSync } from 'fs';
import { join } from 'path';

const db = createClient({
  url: process.env.TURSO_DATABASE_URL || 'file:local.db',
  authToken: process.env.TURSO_AUTH_TOKEN,
});

async function seed() {
  console.log('🌱 Seeding database...');

  // Run schema
  const schema = readFileSync(join(__dirname, 'schema.sql'), 'utf-8');
  const statements = schema.split(';').filter(s => s.trim());
  for (const statement of statements) {
    if (statement.trim()) {
      await db.execute(statement);
    }
  }
  console.log('✅ Schema created');

  // Seed grants
  const grants = [
    {
      slug: 'old-age-grant',
      name: 'Old Age Grant',
      description: 'Monthly grant for South African citizens aged 60 and older.',
      eligibility_criteria: JSON.stringify({
        ageRequirement: '60 years or older',
        citizenshipRequirement: 'South African citizen, permanent resident, or refugee',
        residencyRequirement: 'Must be residing in South Africa',
        incomeRequirement: 'Must pass the means test',
        additionalCriteria: [
          'Not receiving any other social grant',
          'Not cared for in a state institution'
        ]
      }),
      disqualifiers: JSON.stringify([
        'Receiving another social grant (except foster child grant)',
        'Income exceeds the means test threshold',
        'Assets exceed the means test threshold',
        'Maintained in a state institution'
      ]),
      income_thresholds: JSON.stringify([
        { applicantType: 'Single', maxIncome: 86280 },
        { applicantType: 'Married', maxIncome: 172560 }
      ]),
      application_steps: JSON.stringify([
        { stepNumber: 1, title: 'Gather Documents', description: 'Collect your ID, proof of residence, and bank statements' },
        { stepNumber: 2, title: 'Visit SASSA Office', description: 'Go to your nearest SASSA office with all documents' },
        { stepNumber: 3, title: 'Complete Application', description: 'Fill in the application form with assistance from SASSA staff' },
        { stepNumber: 4, title: 'Biometric Verification', description: 'Have your fingerprints and photo taken' },
        { stepNumber: 5, title: 'Wait for Outcome', description: 'SASSA will process your application within 90 days' }
      ]),
      processing_timeline: '90 days',
      common_mistakes: JSON.stringify([
        'Incomplete documentation',
        'Incorrect bank details',
        'Not declaring all income sources',
        'Missing the means test requirements'
      ])
    },
    {
      slug: 'child-support-grant',
      name: 'Child Support Grant',
      description: 'Monthly grant for primary caregivers of children under 18.',
      eligibility_criteria: JSON.stringify({
        ageRequirement: 'Child must be under 18 years',
        citizenshipRequirement: 'Child must be South African citizen or permanent resident',
        residencyRequirement: 'Both caregiver and child must reside in South Africa',
        incomeRequirement: 'Caregiver must pass the means test',
        additionalCriteria: [
          'Must be the primary caregiver of the child',
          'Child must not be cared for in a state institution'
        ]
      }),
      disqualifiers: JSON.stringify([
        'Child already receiving another grant',
        'Caregiver income exceeds threshold',
        'Child is in state care'
      ]),
      income_thresholds: JSON.stringify([
        { applicantType: 'Single caregiver', maxIncome: 52800 },
        { applicantType: 'Married caregiver', maxIncome: 105600 }
      ]),
      application_steps: JSON.stringify([
        { stepNumber: 1, title: 'Gather Documents', description: 'Collect your ID, child birth certificate, and proof of residence' },
        { stepNumber: 2, title: 'Visit SASSA Office', description: 'Go to your nearest SASSA office' },
        { stepNumber: 3, title: 'Complete Application', description: 'Fill in the CSG application form' },
        { stepNumber: 4, title: 'Verification', description: 'SASSA will verify your information' },
        { stepNumber: 5, title: 'Await Outcome', description: 'Processing takes up to 90 days' }
      ]),
      processing_timeline: '90 days',
      common_mistakes: JSON.stringify([
        'Missing child birth certificate',
        'Not proving primary caregiver status',
        'Incorrect income declaration'
      ])
    },
    {
      slug: 'disability-grant',
      name: 'Disability Grant',
      description: 'Monthly grant for people with disabilities that prevent them from working.',
      eligibility_criteria: JSON.stringify({
        ageRequirement: '18 to 59 years old',
        citizenshipRequirement: 'South African citizen, permanent resident, or refugee',
        residencyRequirement: 'Must be residing in South Africa',
        incomeRequirement: 'Must pass the means test',
        additionalCriteria: [
          'Must have a disability that renders you unable to work',
          'Disability must be confirmed by medical assessment'
        ]
      }),
      disqualifiers: JSON.stringify([
        'Receiving another social grant',
        'Income exceeds threshold',
        'Maintained in a state institution',
        'Disability does not meet criteria'
      ]),
      income_thresholds: JSON.stringify([
        { applicantType: 'Single', maxIncome: 86280 },
        { applicantType: 'Married', maxIncome: 172560 }
      ]),
      application_steps: JSON.stringify([
        { stepNumber: 1, title: 'Medical Assessment', description: 'Get assessed by a SASSA-appointed doctor' },
        { stepNumber: 2, title: 'Gather Documents', description: 'Collect ID, medical reports, and proof of residence' },
        { stepNumber: 3, title: 'Submit Application', description: 'Apply at your nearest SASSA office' },
        { stepNumber: 4, title: 'Assessment Panel', description: 'Your case will be reviewed by a panel' },
        { stepNumber: 5, title: 'Await Decision', description: 'Processing takes up to 90 days' }
      ]),
      processing_timeline: '90 days',
      common_mistakes: JSON.stringify([
        'Incomplete medical documentation',
        'Missing medical assessment appointment',
        'Not providing sufficient proof of disability'
      ])
    }
  ];

  for (const grant of grants) {
    await db.execute({
      sql: `INSERT OR REPLACE INTO grants (slug, name, description, eligibility_criteria, disqualifiers, income_thresholds, application_steps, processing_timeline, common_mistakes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      args: [
        grant.slug, grant.name, grant.description, grant.eligibility_criteria,
        grant.disqualifiers, grant.income_thresholds, grant.application_steps,
        grant.processing_timeline, grant.common_mistakes
      ]
    });
  }
  console.log('✅ Grants seeded');

  // Seed status codes
  const statusCodes = [
    {
      code: 'PENDING',
      official_meaning: 'Application is being processed',
      simplified_meaning: 'SASSA is still reviewing your application. This is normal and can take up to 90 days.',
      real_world_patterns: 'Most applications stay in PENDING for 30-60 days. If longer than 90 days, follow up.',
      recommended_actions: JSON.stringify(['Wait for SMS notification', 'Check status online after 30 days', 'Visit SASSA if no update after 90 days']),
      related_status_codes: JSON.stringify(['APPROVED', 'DECLINED'])
    },
    {
      code: 'APPROVED',
      official_meaning: 'Application has been approved',
      simplified_meaning: 'Congratulations! Your grant has been approved. You will start receiving payments.',
      real_world_patterns: 'First payment usually arrives within 30 days of approval.',
      recommended_actions: JSON.stringify(['Ensure bank details are correct', 'Wait for payment date SMS', 'Collect grant on payment date']),
      related_status_codes: JSON.stringify(['PENDING', 'ACTIVE'])
    },
    {
      code: 'DECLINED',
      official_meaning: 'Application has been declined',
      simplified_meaning: 'Your application was not successful. You have the right to appeal within 90 days.',
      real_world_patterns: 'Common reasons: income too high, missing documents, or not meeting criteria.',
      recommended_actions: JSON.stringify(['Request reasons for decline', 'Gather additional documents', 'Submit appeal within 90 days']),
      related_status_codes: JSON.stringify(['PENDING', 'APPEAL'])
    }
  ];

  for (const status of statusCodes) {
    await db.execute({
      sql: `INSERT OR REPLACE INTO status_codes (code, official_meaning, simplified_meaning, real_world_patterns, recommended_actions, related_status_codes)
            VALUES (?, ?, ?, ?, ?, ?)`,
      args: [status.code, status.official_meaning, status.simplified_meaning, status.real_world_patterns, status.recommended_actions, status.related_status_codes]
    });
  }
  console.log('✅ Status codes seeded');

  // Seed payment cycles for current month
  const now = new Date();
  const currentMonth = now.getMonth() + 1;
  const currentYear = now.getFullYear();

  const paymentCycles = [
    {
      month: currentMonth,
      year: currentYear,
      grant_id: 1, // Old Age Grant
      payment_dates: JSON.stringify([
        { method: 'bank', startDate: `${currentYear}-${String(currentMonth).padStart(2, '0')}-01`, endDate: `${currentYear}-${String(currentMonth).padStart(2, '0')}-01` },
        { method: 'cash', startDate: `${currentYear}-${String(currentMonth).padStart(2, '0')}-03`, endDate: `${currentYear}-${String(currentMonth).padStart(2, '0')}-05` },
        { method: 'post_office', startDate: `${currentYear}-${String(currentMonth).padStart(2, '0')}-03`, endDate: `${currentYear}-${String(currentMonth).padStart(2, '0')}-05` }
      ]),
      notes: 'Payments start on the 1st for bank accounts'
    }
  ];

  for (const cycle of paymentCycles) {
    await db.execute({
      sql: `INSERT OR REPLACE INTO payment_cycles (month, year, grant_id, payment_dates, notes)
            VALUES (?, ?, ?, ?, ?)`,
      args: [cycle.month, cycle.year, cycle.grant_id, cycle.payment_dates, cycle.notes]
    });
  }
  console.log('✅ Payment cycles seeded');

  // Seed appeal guides
  const appealGuides = [
    {
      grant_id: 1,
      appeal_steps: JSON.stringify([
        { stepNumber: 1, title: 'Request Decline Reasons', description: 'Ask SASSA for written reasons for the decline' },
        { stepNumber: 2, title: 'Gather Evidence', description: 'Collect documents that address the decline reasons' },
        { stepNumber: 3, title: 'Write Appeal Letter', description: 'Explain why you believe the decision was wrong' },
        { stepNumber: 4, title: 'Submit Appeal', description: 'Submit to SASSA within 90 days of decline' },
        { stepNumber: 5, title: 'Attend Hearing', description: 'You may be called for an appeal hearing' }
      ]),
      required_documents: JSON.stringify(['Original decline letter', 'ID document', 'Supporting evidence', 'Appeal letter']),
      timeline: '90 days from decline date',
      common_pitfalls: JSON.stringify([
        'Missing the 90-day deadline',
        'Not addressing specific decline reasons',
        'Submitting incomplete appeal'
      ])
    }
  ];

  for (const guide of appealGuides) {
    await db.execute({
      sql: `INSERT OR REPLACE INTO appeal_guides (grant_id, appeal_steps, required_documents, timeline, common_pitfalls)
            VALUES (?, ?, ?, ?, ?)`,
      args: [guide.grant_id, guide.appeal_steps, guide.required_documents, guide.timeline, guide.common_pitfalls]
    });
  }
  console.log('✅ Appeal guides seeded');

  // Seed FAQs
  const faqs = [
    { grant_id: 1, question: 'How long does the Old Age Grant application take?', answer: 'SASSA processes applications within 90 days. You will receive an SMS with the outcome.', display_order: 1 },
    { grant_id: 1, question: 'Can I apply online for the Old Age Grant?', answer: 'Yes, you can apply online at srd.sassa.gov.za or visit your nearest SASSA office.', display_order: 2 },
    { grant_id: 2, question: 'How many children can I claim Child Support Grant for?', answer: 'You can claim for up to 6 children as a primary caregiver.', display_order: 1 },
    { grant_id: null, question: 'What is the SASSA means test?', answer: 'The means test checks your income and assets to determine if you qualify for a grant. Different grants have different thresholds.', display_order: 1 }
  ];

  for (const faq of faqs) {
    await db.execute({
      sql: `INSERT INTO faqs (grant_id, question, answer, display_order) VALUES (?, ?, ?, ?)`,
      args: [faq.grant_id, faq.question, faq.answer, faq.display_order]
    });
  }
  console.log('✅ FAQs seeded');

  console.log('🎉 Database seeded successfully!');
}

seed().catch(console.error);
