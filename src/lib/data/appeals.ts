// Static appeal guides data
import type { AppealGuide } from '../types';

export const appealGuides: AppealGuide[] = [
  {
    id: 1,
    grantId: 1,
    grantSlug: 'old-age-grant',
    grantName: 'Old Age Grant',
    appealSteps: [
      { stepNumber: 1, title: 'Request Decline Reasons', description: 'Visit your local SASSA office and request a written explanation for why your application was declined. You have the right to know the specific reasons.' },
      { stepNumber: 2, title: 'Gather Supporting Documents', description: 'Collect documents that address the decline reasons. This may include updated bank statements, proof of age, or medical certificates.' },
      { stepNumber: 3, title: 'Write Your Appeal Letter', description: 'Write a clear letter explaining why you believe the decision was wrong. Reference specific facts and attach supporting documents.' },
      { stepNumber: 4, title: 'Submit Your Appeal', description: 'Submit your appeal at any SASSA office within 90 days of receiving the decline. Keep a copy of everything you submit.' },
      { stepNumber: 5, title: 'Attend the Hearing', description: 'You may be called for an appeal hearing. Bring all your documents and be prepared to explain your situation.' }
    ],
    requiredDocuments: [
      'Original decline letter from SASSA',
      'South African ID document',
      'Proof of residence',
      'Bank statements (last 3 months)',
      'Appeal letter explaining your case',
      'Any additional supporting documents'
    ],
    timeline: '90 days from the date of decline',
    commonPitfalls: [
      'Missing the 90-day deadline - mark your calendar!',
      'Not getting the decline reasons in writing',
      'Submitting incomplete documentation',
      'Not keeping copies of submitted documents',
      'Not addressing the specific reasons for decline'
    ]
  },
  {
    id: 2,
    grantId: 2,
    grantSlug: 'child-support-grant',
    grantName: 'Child Support Grant',
    appealSteps: [
      { stepNumber: 1, title: 'Get Decline Reasons', description: 'Request written reasons for the decline from SASSA. Common reasons include income threshold issues or caregiver status questions.' },
      { stepNumber: 2, title: 'Gather Evidence', description: 'Collect proof of your caregiver status, income documents, and the child\'s birth certificate.' },
      { stepNumber: 3, title: 'Prepare Appeal', description: 'Write an appeal letter addressing each decline reason with supporting evidence.' },
      { stepNumber: 4, title: 'Submit Within Deadline', description: 'Submit your appeal to SASSA within 90 days. Request a receipt as proof of submission.' },
      { stepNumber: 5, title: 'Follow Up', description: 'Check on your appeal status after 30 days if you haven\'t heard back.' }
    ],
    requiredDocuments: [
      'Decline letter',
      'Your ID document',
      'Child\'s birth certificate',
      'Proof of residence',
      'Proof of caregiver status (school letters, clinic cards)',
      'Income proof or affidavit'
    ],
    timeline: '90 days from decline',
    commonPitfalls: [
      'Not proving primary caregiver status adequately',
      'Missing income documentation',
      'Submitting after the 90-day deadline',
      'Not including the child\'s documents'
    ]
  },
  {
    id: 3,
    grantId: 3,
    grantSlug: 'disability-grant',
    grantName: 'Disability Grant',
    appealSteps: [
      { stepNumber: 1, title: 'Understand the Decline', description: 'Get written reasons. Disability grant declines often relate to the medical assessment or income threshold.' },
      { stepNumber: 2, title: 'Get Additional Medical Evidence', description: 'If declined due to medical reasons, get additional reports from specialists or your treating doctor.' },
      { stepNumber: 3, title: 'Request Re-assessment', description: 'You can request a new medical assessment by a different SASSA doctor.' },
      { stepNumber: 4, title: 'Submit Comprehensive Appeal', description: 'Include all medical evidence, specialist reports, and a detailed appeal letter.' },
      { stepNumber: 5, title: 'Prepare for Panel Review', description: 'Your appeal may go to a medical panel. Ensure all documentation clearly shows your disability.' }
    ],
    requiredDocuments: [
      'Decline letter',
      'ID document',
      'Original medical assessment',
      'Additional medical reports from specialists',
      'Hospital records if applicable',
      'Letter from treating doctor',
      'Proof of income'
    ],
    timeline: '90 days from decline',
    commonPitfalls: [
      'Relying only on the original medical assessment',
      'Not getting specialist opinions',
      'Missing medical appointments',
      'Not explaining how disability affects ability to work',
      'Incomplete medical history'
    ]
  }
];

export function getAllAppealGuides(): AppealGuide[] {
  return appealGuides;
}

export function getAppealGuideByGrantSlug(slug: string): AppealGuide | undefined {
  return appealGuides.find(g => g.grantSlug === slug);
}

export function getAllAppealSlugs(): string[] {
  return appealGuides.map(g => g.grantSlug);
}
