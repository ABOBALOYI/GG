// Document requirements data
import type { DocumentRequirement, DocumentItem } from '../types';

export const documentRequirements: DocumentRequirement[] = [
  {
    id: 1,
    grantId: 1,
    scenario: 'first_time',
    documents: [
      { id: 'id', name: 'South African ID', description: 'Original green ID book or smart card', isRequired: true },
      { id: 'residence', name: 'Proof of Residence', description: 'Utility bill, lease agreement, or affidavit', isRequired: true, alternatives: ['Affidavit from ward councillor'] },
      { id: 'bank', name: 'Bank Statement', description: 'Last 3 months bank statements', isRequired: true, alternatives: ['SASSA can pay to Post Office if no bank account'] },
      { id: 'income', name: 'Proof of Income', description: 'Payslips, pension statements, or affidavit of no income', isRequired: true },
      { id: 'marriage', name: 'Marriage Certificate', description: 'If married, bring marriage certificate', isRequired: false }
    ]
  },
  {
    id: 2,
    grantId: 2,
    scenario: 'first_time',
    documents: [
      { id: 'id', name: 'Your ID Document', description: 'Original green ID book or smart card', isRequired: true },
      { id: 'child_birth', name: 'Child Birth Certificate', description: 'Original birth certificate of the child', isRequired: true },
      { id: 'residence', name: 'Proof of Residence', description: 'Utility bill or affidavit', isRequired: true },
      { id: 'caregiver', name: 'Proof of Caregiver Status', description: 'School letter, clinic card, or affidavit', isRequired: true },
      { id: 'income', name: 'Proof of Income', description: 'Payslips or affidavit of no income', isRequired: true },
      { id: 'child_id', name: 'Child ID (if available)', description: 'Child\'s ID if they have one', isRequired: false }
    ]
  },
  {
    id: 3,
    grantId: 3,
    scenario: 'first_time',
    documents: [
      { id: 'id', name: 'South African ID', description: 'Original green ID book or smart card', isRequired: true },
      { id: 'medical', name: 'Medical Assessment', description: 'Will be done by SASSA-appointed doctor', isRequired: true },
      { id: 'medical_reports', name: 'Medical Reports', description: 'Reports from your treating doctor or specialist', isRequired: true },
      { id: 'residence', name: 'Proof of Residence', description: 'Utility bill or affidavit', isRequired: true },
      { id: 'income', name: 'Proof of Income', description: 'Payslips or affidavit of no income', isRequired: true },
      { id: 'hospital', name: 'Hospital Records', description: 'If you have been hospitalized', isRequired: false }
    ]
  }
];

export function getDocumentsForGrant(grantId: number, scenario: string = 'first_time'): DocumentItem[] {
  const req = documentRequirements.find(r => r.grantId === grantId && r.scenario === scenario);
  return req?.documents || [];
}

export function getDocumentsByGrantSlug(slug: string): DocumentItem[] {
  const grantIdMap: Record<string, number> = {
    'old-age-grant': 1,
    'child-support-grant': 2,
    'disability-grant': 3
  };
  const grantId = grantIdMap[slug];
  if (!grantId) return [];
  return getDocumentsForGrant(grantId);
}
