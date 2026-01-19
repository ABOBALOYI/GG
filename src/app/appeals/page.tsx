import { Metadata } from 'next';
import Link from 'next/link';
import { AlertTriangle } from 'lucide-react';
import { getAllAppealGuides } from '@/lib/data/appeals';

export const metadata: Metadata = {
  title: 'SASSA Appeal Guides - How to Appeal a Declined Application',
  description: 'Learn how to appeal a SASSA grant rejection. Step-by-step guides for Old Age, Child Support, and Disability grant appeals. Know your rights and deadlines.',
  keywords: ['SASSA appeal', 'grant rejection appeal', 'how to appeal SASSA', 'appeal declined application', 'SASSA appeal process'],
  openGraph: {
    title: 'SASSA Appeal Guides - Appeal a Declined Application',
    description: 'Step-by-step guides on how to appeal a declined SASSA grant application.',
    url: 'https://grantsguide.co.za/appeals',
  },
  alternates: {
    canonical: 'https://grantsguide.co.za/appeals',
  },
};

export default function AppealsPage() {
  const guides = getAllAppealGuides();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">
        How to Appeal a SASSA Decision
      </h1>
      <p className="text-gray-600 mb-8">
        If your grant application was declined, you have the right to appeal within 90 days. 
        Choose your grant type below for a step-by-step appeal guide.
      </p>

      {/* Appeal Guides */}
      <div className="space-y-4 mb-8">
        {guides.map((guide) => (
          <Link
            key={guide.id}
            href={`/appeals/${guide.grantSlug}`}
            className="block bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md hover:border-green-300 transition-all"
          >
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  How to Appeal {guide.grantName} Rejection
                </h2>
                <p className="text-gray-600">
                  {guide.appealSteps.length} steps • Deadline: {guide.timeline}
                </p>
              </div>
              <span className="text-green-700">→</span>
            </div>
          </Link>
        ))}
      </div>

      {/* General Appeal Information */}
      <section className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">Your Appeal Rights</h2>
        <ul className="space-y-2 text-gray-700">
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">•</span>
            You have 90 days from the date of decline to submit an appeal
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">•</span>
            You have the right to know why your application was declined
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">•</span>
            You can submit additional documents with your appeal
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">•</span>
            You may be called for an appeal hearing
          </li>
          <li className="flex items-start">
            <span className="text-blue-600 mr-2">•</span>
            If your appeal is unsuccessful, you can approach the courts
          </li>
        </ul>
      </section>

      {/* Warning */}
      <section className="bg-red-50 border border-red-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-3 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-red-500" />
          Important Deadline
        </h2>
        <p className="text-gray-700">
          You must submit your appeal within <strong>90 days</strong> of receiving your decline letter. 
          After this deadline, you will need to submit a new application instead of an appeal.
        </p>
      </section>
    </div>
  );
}
