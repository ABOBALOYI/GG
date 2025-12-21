import { Metadata } from 'next';
import Link from 'next/link';
import { getAllStatusCodes } from '@/lib/data/status-codes';

export const metadata: Metadata = {
  title: 'SASSA Status Codes Explained - Decode Your Application Status',
  description: 'Understand what your SASSA application status means. Decode status codes like PENDING, APPROVED, DECLINED, and learn what steps to take next.',
  keywords: ['SASSA status codes', 'application status', 'SASSA pending', 'SASSA approved', 'SASSA declined', 'status decoder'],
  openGraph: {
    title: 'SASSA Status Codes Explained',
    description: 'Understand what your SASSA application status means and what to do next.',
    url: 'https://grantsguide.co.za/status',
  },
  alternates: {
    canonical: 'https://grantsguide.co.za/status',
  },
};

export default function StatusPage() {
  const statusCodes = getAllStatusCodes();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        SASSA Status Decoder
      </h1>
      <p className="text-gray-600 mb-8">
        Not sure what your SASSA application status means? Find your status code below 
        to understand what it means and what you should do next.
      </p>

      <div className="space-y-4">
        {statusCodes.map((status) => (
          <Link
            key={status.id}
            href={`/status/${status.code.toLowerCase()}`}
            className="block bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md hover:border-green-300 transition-all"
          >
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  {status.code}
                </h2>
                <p className="text-gray-600">{status.simplifiedMeaning}</p>
              </div>
              <span className="text-green-700">→</span>
            </div>
          </Link>
        ))}
      </div>

      <section className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">
          Can&apos;t Find Your Status?
        </h2>
        <p className="text-gray-600 mb-4">
          If your status code isn&apos;t listed here, or you need help understanding your specific situation, 
          our AI assistant can help.
        </p>
        <Link
          href="/help"
          className="inline-block bg-green-700 text-white px-6 py-2 rounded-lg hover:bg-green-800 transition-colors"
        >
          Ask AI Assistant
        </Link>
      </section>
    </div>
  );
}
