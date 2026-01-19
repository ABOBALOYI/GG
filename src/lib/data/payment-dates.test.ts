import { describe, it, expect } from 'vitest';
import {
  getPaymentDatesForMonth,
  getCurrentMonthPayments,
  getAvailableMonths,
  formatMonthYear,
} from './payment-dates';

describe('Payment Dates Data', () => {
  /**
   * **Feature: grantguide-sa, Property 3: Payment Data Display**
   * **Validates: Requirements 2.1, 2.4**
   * 
   * WHEN a user visits a payment dates page THEN the System SHALL display 
   * payment schedules in a table format organized by grant type and collection method
   */
  it('Property 3: payment data includes grant type and collection methods', () => {
    const payments = getCurrentMonthPayments();

    expect(payments.length).toBeGreaterThan(0);

    payments.forEach((payment) => {
      // Must have grant identification
      expect(payment.grantId).toBeDefined();
      expect(payment.grantName).toBeTruthy();

      // Must have payment dates array with methods
      expect(Array.isArray(payment.paymentDates)).toBe(true);
      expect(payment.paymentDates.length).toBeGreaterThan(0);

      // Each payment date must have method and dates
      payment.paymentDates.forEach((pd) => {
        expect(['bank', 'cash', 'post_office']).toContain(pd.method);
        expect(pd.startDate).toBeTruthy();
        expect(pd.endDate).toBeTruthy();
      });
    });
  });

  it('Property 3: payment dates are organized by month and year', () => {
    const now = new Date();
    const month = now.getMonth() + 1;
    const year = now.getFullYear();

    const payments = getPaymentDatesForMonth(month, year);

    payments.forEach((payment) => {
      expect(payment.month).toBe(month);
      expect(payment.year).toBe(year);
    });
  });

  it('Property 3: includes multiple collection methods per grant', () => {
    const payments = getCurrentMonthPayments();

    payments.forEach((payment) => {
      const methods = payment.paymentDates.map((pd) => pd.method);
      // Should have at least bank and one other method
      expect(methods).toContain('bank');
      expect(methods.length).toBeGreaterThanOrEqual(2);
    });
  });

  it('getAvailableMonths returns current and future months', () => {
    const months = getAvailableMonths();

    expect(months.length).toBeGreaterThanOrEqual(3);

    // First month should be current month
    const now = new Date();
    expect(months[0].month).toBe(now.getMonth() + 1);
    expect(months[0].year).toBe(now.getFullYear());

    // Each month should have a slug
    months.forEach((m) => {
      expect(m.slug).toMatch(/^\d{4}-\d{2}$/);
    });
  });

  it('formatMonthYear returns readable format', () => {
    const formatted = formatMonthYear(1, 2025);
    expect(formatted).toContain('January');
    expect(formatted).toContain('2025');
  });
});
