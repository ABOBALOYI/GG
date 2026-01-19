// Static payment dates data
import type { PaymentCycle } from '../types';

// Generate payment dates for current and next month
function generatePaymentDates(month: number, year: number): PaymentCycle[] {
  const monthStr = String(month).padStart(2, '0');
  
  return [
    {
      id: 1,
      month,
      year,
      grantId: 1,
      grantName: 'Old Age Grant',
      paymentDates: [
        { method: 'bank', startDate: `${year}-${monthStr}-01`, endDate: `${year}-${monthStr}-01` },
        { method: 'cash', startDate: `${year}-${monthStr}-03`, endDate: `${year}-${monthStr}-05` },
        { method: 'post_office', startDate: `${year}-${monthStr}-03`, endDate: `${year}-${monthStr}-05` }
      ],
      notes: 'Older persons (75+) receive payments first at cash pay points'
    },
    {
      id: 2,
      month,
      year,
      grantId: 3,
      grantName: 'Disability Grant',
      paymentDates: [
        { method: 'bank', startDate: `${year}-${monthStr}-01`, endDate: `${year}-${monthStr}-01` },
        { method: 'cash', startDate: `${year}-${monthStr}-03`, endDate: `${year}-${monthStr}-05` },
        { method: 'post_office', startDate: `${year}-${monthStr}-03`, endDate: `${year}-${monthStr}-05` }
      ]
    },
    {
      id: 3,
      month,
      year,
      grantId: 2,
      grantName: 'Child Support Grant',
      paymentDates: [
        { method: 'bank', startDate: `${year}-${monthStr}-01`, endDate: `${year}-${monthStr}-01` },
        { method: 'cash', startDate: `${year}-${monthStr}-06`, endDate: `${year}-${monthStr}-07` },
        { method: 'post_office', startDate: `${year}-${monthStr}-06`, endDate: `${year}-${monthStr}-07` }
      ]
    }
  ];
}

export function getPaymentDatesForMonth(month: number, year: number): PaymentCycle[] {
  return generatePaymentDates(month, year);
}

export function getCurrentMonthPayments(): PaymentCycle[] {
  const now = new Date();
  return generatePaymentDates(now.getMonth() + 1, now.getFullYear());
}

export function getNextMonthPayments(): PaymentCycle[] {
  const now = new Date();
  const nextMonth = now.getMonth() + 2;
  const year = nextMonth > 12 ? now.getFullYear() + 1 : now.getFullYear();
  const month = nextMonth > 12 ? 1 : nextMonth;
  return generatePaymentDates(month, year);
}

export function formatMonthYear(month: number, year: number): string {
  const date = new Date(year, month - 1);
  return date.toLocaleDateString('en-ZA', { month: 'long', year: 'numeric' });
}

export function getAvailableMonths(): { month: number; year: number; slug: string }[] {
  const now = new Date();
  const months = [];
  
  // Current month and next 2 months
  for (let i = 0; i < 3; i++) {
    const date = new Date(now.getFullYear(), now.getMonth() + i);
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    months.push({
      month,
      year,
      slug: `${year}-${String(month).padStart(2, '0')}`
    });
  }
  
  return months;
}
