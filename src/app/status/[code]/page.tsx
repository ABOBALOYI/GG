import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getAllStatusCodeValues, getStatusByCode } from '@/lib/data/status-codes';
import { generateBreadcrumbSchema } from '@/components/SEOHead';

interface Props {
  params: Promise<{ code: string }>;
}

export async function generateStaticParams() {
  return getAllStatusCodeValues().map((code) => ({ code: code.toLowerCase() }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { code } = await params;
  const status = getStatusByCode(code);
  if (!status) return { title: 'Status Not Found' };

  return {
    title: `What Does "${status.code}" Mean? - SASSA Status Explained`,
    description: `${status.simplifiedMeaning} Learn what to do next when your SASSA status shows ${status.code}.`,
  };
}

export default async function StatusCodePage({ params }: Props) {
  const { code } = await params;
  const status = getStatusByCode(code);

  if (!status) {
    notFound();
  }

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Status Decoder', url: '/status' },
    { name: status.code, url: `/status/${code}` }
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
        <Link href="/status" className="hover:text-green-700">Status Decoder</Link>
        <span className="mx-2">/</span>
        <span className="text-gray-900">{status.code}</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        What Does &quot;{status.code}&quot; Mean?
      </h1>
      <p className="text-sm text-gray-500 mb-8">SASSA Application Status Explained</p>

      {/* Official Meaning */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">Official Meaning</h2>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <p className="text-gray-700">{status.officialMeaning}</p>
        </div>
      </section>

      {/* Simplified Explanation */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">What This Means for You</h2>
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-gray-700">{status.simplifiedMeaning}</p>
        </div>
      </section>

      {/* Real World Patterns */}
      {status.realWorldPatterns && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-3">What We&apos;ve Seen</h2>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-gray-700">{status.realWorldPatterns}</p>
          </div>
        </section>
      )}

      {/* Recommended Actions */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">What You Should Do</h2>
        <div className="space-y-3">
          {status.recommendedActions.map((action, i) => (
            <div key={i} className="flex items-start gap-3">
              <div className="flex-shrink-0 w-6 h-6 bg-green-700 text-white rounded-full flex items-center justify-center text-sm font-medium">
                {i + 1}
              </div>
              <p className="text-gray-700">{action}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Related Status Codes */}
      {status.relatedStatusCodes.length > 0 && (
        <section className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-3">Related Status Codes</h2>
          <div className="flex flex-wrap gap-2">
            {status.relatedStatusCodes.map((relatedCode) => (
              <Link
                key={relatedCode}
                href={`/status/${relatedCode.toLowerCase()}`}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-full hover:bg-gray-200 transition-colors"
              >
                {relatedCode}
              </Link>
            ))}
          </div>
        </section>
      )}

      {/* Help Section */}
      <section className="bg-amber-50 border border-amber-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">Need More Help?</h2>
        <p className="text-gray-600 mb-4">
          If you&apos;re unsure what to do next or have questions about your specific situation, 
          our AI assistant can provide personalized guidance.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/help"
            className="bg-green-700 text-white px-6 py-2 rounded-lg hover:bg-green-800 transition-colors"
          >
            Ask AI Assistant
          </Link>
          <Link
            href="/appeals"
            className="bg-white text-gray-700 border border-gray-300 px-6 py-2 rounded-lg hover:bg-gray-50 transition-colors"
          >
            View Appeal Guides
          </Link>
        </div>
      </section>
    </div>
  );
}
