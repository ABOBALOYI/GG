import { Metadata } from 'next';
import Link from 'next/link';
import { getCurrentMonthPayments, formatMonthYear, getAvailableMonths } from '@/lib/data/payment-dates';
import PaymentTable from '@/components/PaymentTable';

export const metadata: Metadata = {
  title: 'SASSA Payment Dates - Monthly Grant Payment Schedule',
  description: 'Check SASSA grant payment dates for each month. Find out when Old Age, Child Support, and Disability grants are paid. Updated monthly with bank and cash payment schedules.',
  keywords: ['SASSA payment dates', 'grant payment schedule', 'when is SASSA paid', 'SASSA payment calendar'],
  openGraph: {
    title: 'SASSA Payment Dates - Monthly Schedule',
    description: 'Check when SASSA grants are paid each month. Bank and cash payment schedules.',
    url: 'https://grantsguide.co.za/payment-dates',
  },
  alternates: {
    canonical: 'https://grantsguide.co.za/payment-dates',
  },
};

export default function PaymentDatesPage() {
  const now = new Date();
  const currentMonth = now.getMonth() + 1;
  const currentYear = now.getFullYear();
  const payments = getCurrentMonthPayments();
  const availableMonths = getAvailableMonths();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        SASSA Payment Dates
      </h1>
      <p className="text-gray-600 mb-8">
        Find out when SASSA grants are paid each month. Payment dates vary by grant type and collection method.
      </p>

      {/* Month Navigation */}
      <div className="flex flex-wrap gap-2 mb-8">
        {availableMonths.map(({ month, year, slug }) => (
          <Link
            key={slug}
            href={`/payment-dates/${slug}`}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              month === currentMonth && year === currentYear
                ? 'bg-green-700 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {formatMonthYear(month, year)}
          </Link>
        ))}
      </div>

      {/* Current Month Payments */}
      <section>
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          {formatMonthYear(currentMonth, currentYear)} Payment Schedule
        </h2>
        
        {payments.map((payment) => (
          <PaymentTable
            key={payment.id}
            grantName={payment.grantName}
            paymentDates={payment.paymentDates}
            notes={payment.notes}
          />
        ))}
      </section>

      {/* Important Notes */}
      <section className="mt-8 bg-amber-50 border border-amber-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">Important Notes</h2>
        <ul className="space-y-2 text-gray-700">
          <li className="flex items-start">
            <span className="text-amber-600 mr-2">•</span>
            Bank payments are deposited on the 1st of each month (or the last working day before if the 1st falls on a weekend)
          </li>
          <li className="flex items-start">
            <span className="text-amber-600 mr-2">•</span>
            Cash payments at pay points follow a schedule based on grant type
          </li>
          <li className="flex items-start">
            <span className="text-amber-600 mr-2">•</span>
            Bring your SASSA card and ID when collecting at pay points
          </li>
          <li className="flex items-start">
            <span className="text-amber-600 mr-2">•</span>
            Uncollected grants may be suspended after 3 consecutive months
          </li>
        </ul>
      </section>

      {/* FAQ */}
      <section className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Frequently Asked Questions</h2>
        <div className="space-y-4">
          <details className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <summary className="px-4 py-3 cursor-pointer font-medium text-gray-900 hover:bg-gray-50">
              What if I miss my payment date?
            </summary>
            <p className="px-4 py-3 text-gray-600 border-t border-gray-100">
              If you miss your payment date at a cash pay point, you can collect at any SASSA pay point 
              or Post Office during the payment period. Bank payments remain in your account.
            </p>
          </details>
          <details className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <summary className="px-4 py-3 cursor-pointer font-medium text-gray-900 hover:bg-gray-50">
              Why hasn&apos;t my payment arrived?
            </summary>
            <p className="px-4 py-3 text-gray-600 border-t border-gray-100">
              If your bank payment hasn&apos;t arrived by the 2nd of the month, check your bank details 
              with SASSA. For cash payments, ensure you&apos;re going to the correct pay point on the right date.
            </p>
          </details>
        </div>
      </section>
    </div>
  );
}
