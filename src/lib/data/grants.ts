// Static grant data - can be moved to database later
import type { Grant } from '../types';

export const grants: Grant[] = [
  {
    id: 1,
    slug: 'old-age-grant',
    name: 'Old Age Grant',
    description: 'Monthly grant for South African citizens aged 60 and older.',
    eligibilityCriteria: {
      ageRequirement: '60 years or older',
      citizenshipRequirement: 'South African citizen, permanent resident, or refugee',
      residencyRequirement: 'Must be residing in South Africa',
      incomeRequirement: 'Must pass the means test',
      additionalCriteria: [
        'Not receiving any other social grant',
        'Not cared for in a state institution'
      ]
    },
    disqualifiers: [
      'Receiving another social grant (except foster child grant)',
      'Income exceeds the means test threshold',
      'Assets exceed the means test threshold',
      'Maintained in a state institution'
    ],
    incomeThresholds: [
      { applicantType: 'Single', maxIncome: 86280 },
      { applicantType: 'Married', maxIncome: 172560 }
    ],
    applicationSteps: [
      { stepNumber: 1, title: 'Gather Documents', description: 'Collect your ID, proof of residence, and bank statements' },
      { stepNumber: 2, title: 'Visit SASSA Office', description: 'Go to your nearest SASSA office with all documents' },
      { stepNumber: 3, title: 'Complete Application', description: 'Fill in the application form with assistance from SASSA staff' },
      { stepNumber: 4, title: 'Biometric Verification', description: 'Have your fingerprints and photo taken' },
      { stepNumber: 5, title: 'Wait for Outcome', description: 'SASSA will process your application within 90 days' }
    ],
    processingTimeline: '90 days',
    commonMistakes: [
      'Incomplete documentation',
      'Incorrect bank details',
      'Not declaring all income sources',
      'Missing the means test requirements'
    ],
    updatedAt: '2026-01-01'
  },
  {
    id: 2,
    slug: 'child-support-grant',
    name: 'Child Support Grant',
    description: 'Monthly grant for primary caregivers of children under 18.',
    eligibilityCriteria: {
      ageRequirement: 'Child must be under 18 years',
      citizenshipRequirement: 'Child must be South African citizen or permanent resident',
      residencyRequirement: 'Both caregiver and child must reside in South Africa',
      incomeRequirement: 'Caregiver must pass the means test',
      additionalCriteria: [
        'Must be the primary caregiver of the child',
        'Child must not be cared for in a state institution'
      ]
    },
    disqualifiers: [
      'Child already receiving another grant',
      'Caregiver income exceeds threshold',
      'Child is in state care'
    ],
    incomeThresholds: [
      { applicantType: 'Single caregiver', maxIncome: 52800 },
      { applicantType: 'Married caregiver', maxIncome: 105600 }
    ],
    applicationSteps: [
      { stepNumber: 1, title: 'Gather Documents', description: 'Collect your ID, child birth certificate, and proof of residence' },
      { stepNumber: 2, title: 'Visit SASSA Office', description: 'Go to your nearest SASSA office' },
      { stepNumber: 3, title: 'Complete Application', description: 'Fill in the CSG application form' },
      { stepNumber: 4, title: 'Verification', description: 'SASSA will verify your information' },
      { stepNumber: 5, title: 'Await Outcome', description: 'Processing takes up to 90 days' }
    ],
    processingTimeline: '90 days',
    commonMistakes: [
      'Missing child birth certificate',
      'Not proving primary caregiver status',
      'Incorrect income declaration'
    ],
    updatedAt: '2026-01-01'
  },
  {
    id: 3,
    slug: 'disability-grant',
    name: 'Disability Grant',
    description: 'Monthly grant for people with disabilities that prevent them from working.',
    eligibilityCriteria: {
      ageRequirement: '18 to 59 years old',
      citizenshipRequirement: 'South African citizen, permanent resident, or refugee',
      residencyRequirement: 'Must be residing in South Africa',
      incomeRequirement: 'Must pass the means test',
      additionalCriteria: [
        'Must have a disability that renders you unable to work',
        'Disability must be confirmed by medical assessment'
      ]
    },
    disqualifiers: [
      'Receiving another social grant',
      'Income exceeds threshold',
      'Maintained in a state institution',
      'Disability does not meet criteria'
    ],
    incomeThresholds: [
      { applicantType: 'Single', maxIncome: 86280 },
      { applicantType: 'Married', maxIncome: 172560 }
    ],
    applicationSteps: [
      { stepNumber: 1, title: 'Medical Assessment', description: 'Get assessed by a SASSA-appointed doctor' },
      { stepNumber: 2, title: 'Gather Documents', description: 'Collect ID, medical reports, and proof of residence' },
      { stepNumber: 3, title: 'Submit Application', description: 'Apply at your nearest SASSA office' },
      { stepNumber: 4, title: 'Assessment Panel', description: 'Your case will be reviewed by a panel' },
      { stepNumber: 5, title: 'Await Decision', description: 'Processing takes up to 90 days' }
    ],
    processingTimeline: '90 days',
    commonMistakes: [
      'Incomplete medical documentation',
      'Missing medical assessment appointment',
      'Not providing sufficient proof of disability'
    ],
    updatedAt: '2026-01-01'
  },
  {
    id: 4,
    slug: 'srd-grant',
    name: 'Social Relief of Distress (SRD) Grant',
    description: 'A temporary grant for South African citizens and residents aged 18-59 with no income.',
    eligibilityCriteria: {
      ageRequirement: '18 to 59 years old',
      citizenshipRequirement: 'South African citizens, refugees, asylum seekers and special permit holders',
      residencyRequirement: 'Must reside within South Africa',
      incomeRequirement: 'Monthly income less than R624',
      additionalCriteria: [
        'Must not be receiving any other social grant',
        'Must not be receiving UIF or NSFAS'
      ]
    },
    disqualifiers: [
      'Receiving other social grants',
      'Receiving UIF or NSFAS benefits',
      'Income exceeds R624 per month',
      'Already in state institutions'
    ],
    incomeThresholds: [
      { applicantType: 'Individual', maxIncome: 7488 } // 624 * 12
    ],
    applicationSteps: [
      { stepNumber: 1, title: 'Online Application', description: 'Apply via the SRD portal (srd.sassa.gov.za)' },
      { stepNumber: 2, title: 'Submit ID', description: 'Enter your ID number and mobile number' },
      { stepNumber: 3, title: 'Choose Payment', description: 'Select bank account or cash send' },
      { stepNumber: 4, title: 'Monthly Check', description: 'SASSA verifies your status every month' }
    ],
    processingTimeline: '30-90 days',
    commonMistakes: [
      'Incorrect bank details',
      'Mismatch between name and ID',
      'Already receiving NSFAS/UIF'
    ],
    updatedAt: '2026-01-01'
  }
];

export function getAllGrants(): Grant[] {
  return grants;
}

export function getGrantBySlug(slug: string): Grant | undefined {
  return grants.find(g => g.slug === slug);
}

export function getAllGrantSlugs(): string[] {
  return grants.map(g => g.slug);
}
