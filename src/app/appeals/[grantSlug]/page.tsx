import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getAllAppealSlugs, getAppealGuideByGrantSlug } from '@/lib/data/appeals';
import { generateBreadcrumbSchema } from '@/components/SEOHead';

interface Props {
  params: Promise<{ grantSlug: string }>;
}

export async function generateStaticParams() {
  return getAllAppealSlugs().map((grantSlug) => ({ grantSlug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { grantSlug } = await params;
  const guide = getAppealGuideByGrantSlug(grantSlug);
  if (!guide) return { title: 'Appeal Guide Not Found' };

  return {
    title: `How to Appeal ${guide.grantName} Rejection`,
    description: `Step-by-step guide to appealing a ${guide.grantName} rejection. Learn what documents you need and how to submit your appeal.`,
  };
}

export default async function AppealGuidePage({ params }: Props) {
  const { grantSlug } = await params;
  const guide = getAppealGuideByGrantSlug(grantSlug);

  if (!guide) {
    notFound();
  }

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Appeals', url: '/appeals' },
    { name: guide.grantName, url: `/appeals/${grantSlug}` }
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
        <Link href="/appeals" className="hover:text-green-700">Appeals</Link>
        <span className="mx-2">/</span>
        <span className="text-gray-900">{guide.grantName}</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        How to Appeal {guide.grantName} Rejection
      </h1>
      <p className="text-lg text-gray-600 mb-8">
        Step-by-step guide to appealing your {guide.grantName} application
      </p>

      {/* Deadline Warning */}
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
        <p className="text-red-800 font-medium">
          ⏰ Deadline: You must appeal within <strong>{guide.timeline}</strong>
        </p>
      </div>

      {/* Appeal Steps */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Appeal Steps</h2>
        <div className="space-y-6">
          {guide.appealSteps.map((step) => (
            <div key={step.stepNumber} className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-green-700 text-white rounded-full flex items-center justify-center font-bold text-lg">
                {step.stepNumber}
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-1">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Required Documents */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Required Documents</h2>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
          <ul className="space-y-2">
            {guide.requiredDocuments.map((doc, i) => (
              <li key={i} className="flex items-start">
                <span className="text-green-600 mr-2">☐</span>
                <span className="text-gray-700">{doc}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Common Pitfalls */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Common Mistakes to Avoid</h2>
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
          <ul className="space-y-2">
            {guide.commonPitfalls.map((pitfall, i) => (
              <li key={i} className="flex items-start">
                <span className="text-amber-600 mr-2">⚠</span>
                <span className="text-gray-700">{pitfall}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Related Links */}
      <section className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-3">Related Information</h2>
        <div className="flex flex-wrap gap-3">
          <Link
            href={`/grants/${grantSlug}`}
            className="bg-white text-gray-700 border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors"
          >
            {guide.grantName} Requirements
          </Link>
          <Link
            href={`/checklist?grant=${grantSlug}`}
            className="bg-white text-gray-700 border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Document Checklist
          </Link>
          <Link
            href="/help"
            className="bg-green-700 text-white px-4 py-2 rounded-lg hover:bg-green-800 transition-colors"
          >
            Get AI Help
          </Link>
        </div>
      </section>
    </div>
  );
}
