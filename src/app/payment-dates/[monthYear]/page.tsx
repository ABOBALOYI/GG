import { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { getPaymentDatesForMonth, formatMonthYear, getAvailableMonths } from '@/lib/data/payment-dates';
import PaymentTable from '@/components/PaymentTable';
import { generateBreadcrumbSchema } from '@/components/SEOHead';

interface Props {
  params: Promise<{ monthYear: string }>;
}

export async function generateStaticParams() {
  return getAvailableMonths().map(({ slug }) => ({ monthYear: slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { monthYear } = await params;
  const [yearStr, monthStr] = monthYear.split('-');
  const month = parseInt(monthStr);
  const year = parseInt(yearStr);
  
  if (isNaN(month) || isNaN(year)) {
    return { title: 'Payment Dates Not Found' };
  }

  const monthName = formatMonthYear(month, year);
  return {
    title: `SASSA Payment Dates ${monthName}`,
    description: `SASSA grant payment schedule for ${monthName}. Find out when Old Age, Child Support, and Disability grants are paid.`,
  };
}

export default async function PaymentDatesMonthPage({ params }: Props) {
  const { monthYear } = await params;
  const [yearStr, monthStr] = monthYear.split('-');
  const month = parseInt(monthStr);
  const year = parseInt(yearStr);

  if (isNaN(month) || isNaN(year) || month < 1 || month > 12) {
    notFound();
  }

  const payments = getPaymentDatesForMonth(month, year);
  const availableMonths = getAvailableMonths();
  const monthName = formatMonthYear(month, year);

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Payment Dates', url: '/payment-dates' },
    { name: monthName, url: `/payment-dates/${monthYear}` }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateBreadcrumbSchema(breadcrumbs)) }}
      />

      {/* Breadcrumbs */}
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-green-700">Home</Link>
        <span className="mx-2">/</span>
        <Link href="/payment-dates" className="hover:text-green-700">Payment Dates</Link>
        <span className="mx-2">/</span>
        <span className="text-gray-900">{monthName}</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        SASSA Payment Dates - {monthName}
      </h1>
      <p className="text-gray-600 mb-8">
        Payment schedule for all SASSA grants in {monthName}.
      </p>

      {/* Month Navigation */}
      <div className="flex flex-wrap gap-2 mb-8">
        {availableMonths.map(({ month: m, year: y, slug }) => (
          <Link
            key={slug}
            href={`/payment-dates/${slug}`}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              m === month && y === year
                ? 'bg-green-700 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {formatMonthYear(m, y)}
          </Link>
        ))}
      </div>

      {/* Payment Tables */}
      <section>
        {payments.map((payment) => (
          <PaymentTable
            key={payment.id}
            grantName={payment.grantName}
            paymentDates={payment.paymentDates}
            notes={payment.notes}
          />
        ))}
      </section>

      {/* Collection Tips */}
      <section className="mt-8 bg-green-50 border border-green-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">Collection Tips</h2>
        <ul className="space-y-2 text-gray-700">
          <li className="flex items-start">
            <span className="text-green-600 mr-2">✓</span>
            Arrive early at pay points to avoid long queues
          </li>
          <li className="flex items-start">
            <span className="text-green-600 mr-2">✓</span>
            Always bring your SASSA card and ID document
          </li>
          <li className="flex items-start">
            <span className="text-green-600 mr-2">✓</span>
            Check your balance before leaving the pay point
          </li>
          <li className="flex items-start">
            <span className="text-green-600 mr-2">✓</span>
            Report any issues to SASSA immediately
          </li>
        </ul>
      </section>

      {/* Related Links */}
      <section className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Related Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            href="/grants"
            className="block bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <h3 className="font-medium text-gray-900">Grant Information</h3>
            <p className="text-sm text-gray-600">Learn about eligibility and how to apply</p>
          </Link>
          <Link
            href="/status"
            className="block bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <h3 className="font-medium text-gray-900">Status Decoder</h3>
            <p className="text-sm text-gray-600">Understand your application status</p>
          </Link>
        </div>
      </section>
    </div>
  );
}
