// Static status code data
import type { StatusCode } from '../types';

export const statusCodes: StatusCode[] = [
  {
    id: 1,
    code: 'PENDING',
    officialMeaning: 'Application is being processed',
    simplifiedMeaning: 'SASSA is still reviewing your application. This is normal and can take up to 90 days.',
    realWorldPatterns: 'Most applications stay in PENDING for 30-60 days. If longer than 90 days, follow up.',
    recommendedActions: [
      'Wait for SMS notification',
      'Check status online after 30 days',
      'Visit SASSA if no update after 90 days'
    ],
    relatedStatusCodes: ['APPROVED', 'DECLINED']
  },
  {
    id: 2,
    code: 'APPROVED',
    officialMeaning: 'Application has been approved',
    simplifiedMeaning: 'Congratulations! Your grant has been approved. You will start receiving payments.',
    realWorldPatterns: 'First payment usually arrives within 30 days of approval.',
    recommendedActions: [
      'Ensure bank details are correct',
      'Wait for payment date SMS',
      'Collect grant on payment date'
    ],
    relatedStatusCodes: ['PENDING', 'ACTIVE']
  },
  {
    id: 3,
    code: 'DECLINED',
    officialMeaning: 'Application has been declined',
    simplifiedMeaning: 'Your application was not successful. You have the right to appeal within 90 days.',
    realWorldPatterns: 'Common reasons: income too high, missing documents, or not meeting criteria.',
    recommendedActions: [
      'Request reasons for decline',
      'Gather additional documents',
      'Submit appeal within 90 days'
    ],
    relatedStatusCodes: ['PENDING', 'APPEAL']
  },
  {
    id: 4,
    code: 'ACTIVE',
    officialMeaning: 'Grant is active and payments are being made',
    simplifiedMeaning: 'Your grant is active. You should be receiving regular payments.',
    realWorldPatterns: 'Payments are made monthly. Check payment dates for your collection method.',
    recommendedActions: [
      'Collect payments on scheduled dates',
      'Update SASSA if your details change',
      'Report any missed payments'
    ],
    relatedStatusCodes: ['APPROVED', 'SUSPENDED']
  },
  {
    id: 5,
    code: 'SUSPENDED',
    officialMeaning: 'Grant has been temporarily suspended',
    simplifiedMeaning: 'Your grant payments have been paused. This could be due to various reasons.',
    realWorldPatterns: 'Common reasons: failed life certificate, uncollected payments, or review required.',
    recommendedActions: [
      'Visit SASSA to find out the reason',
      'Provide any required documents',
      'Complete life certificate if needed'
    ],
    relatedStatusCodes: ['ACTIVE', 'CANCELLED']
  },
  {
    id: 6,
    code: 'APPEAL',
    officialMeaning: 'Appeal is being processed',
    simplifiedMeaning: 'Your appeal has been received and is being reviewed.',
    realWorldPatterns: 'Appeals can take 30-90 days to process.',
    recommendedActions: [
      'Wait for appeal outcome',
      'Prepare for possible hearing',
      'Keep copies of all documents'
    ],
    relatedStatusCodes: ['DECLINED', 'APPROVED']
  },
  {
    id: 7,
    code: 'CANCELLED',
    officialMeaning: 'Grant has been cancelled',
    simplifiedMeaning: 'Your grant has been permanently stopped. This is different from suspension.',
    realWorldPatterns: 'Common reasons: beneficiary passed away, no longer eligible, or requested cancellation.',
    recommendedActions: [
      'Visit SASSA to understand the reason',
      'Reapply if circumstances have changed',
      'Appeal if you believe this was an error'
    ],
    relatedStatusCodes: ['SUSPENDED', 'DECLINED']
  }
];

export function getAllStatusCodes(): StatusCode[] {
  return statusCodes;
}

export function getStatusByCode(code: string): StatusCode | undefined {
  return statusCodes.find(s => s.code.toLowerCase() === code.toLowerCase());
}

export function getAllStatusCodeValues(): string[] {
  return statusCodes.map(s => s.code);
}
