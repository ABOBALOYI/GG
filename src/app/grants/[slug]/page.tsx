import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getAllGrantSlugs, getGrantBySlug } from '@/lib/data/grants';
import FAQBlock from '@/components/FAQBlock';
import { generateFAQSchema, generateBreadcrumbSchema } from '@/components/SEOHead';

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return getAllGrantSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const grant = getGrantBySlug(slug);
  if (!grant) return { title: 'Grant Not Found' };

  return {
    title: `${grant.name} - Eligibility & How to Apply`,
    description: `Complete guide to the ${grant.name}. Learn about eligibility requirements, income thresholds, required documents, and how to apply.`,
  };
}

export default async function GrantPage({ params }: Props) {
  const { slug } = await params;
  const grant = getGrantBySlug(slug);

  if (!grant) {
    notFound();
  }

  const faqs = [
    {
      question: `How long does the ${grant.name} application take?`,
      answer: `SASSA typically processes ${grant.name} applications within ${grant.processingTimeline}. You will receive an SMS notification with the outcome.`
    },
    {
      question: `What documents do I need for the ${grant.name}?`,
      answer: 'You will need your South African ID, proof of residence, and bank statements. Additional documents may be required based on your situation.'
    },
    {
      question: `Can I appeal if my ${grant.name} application is declined?`,
      answer: 'Yes, you have 90 days from the date of decline to submit an appeal. Visit our appeals guide for more information.'
    }
  ];

  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Grants', url: '/grants' },
    { name: grant.name, url: `/grants/${slug}` }
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateFAQSchema(faqs)) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateBreadcrumbSchema(breadcrumbs)) }}
      />

      {/* Breadcrumbs */}
      <nav className="text-sm text-gray-500 mb-6">
        <Link href="/" className="hover:text-green-700">Home</Link>
        <span className="mx-2">/</span>
        <Link href="/grants" className="hover:text-green-700">Grants</Link>
        <span className="mx-2">/</span>
        <span className="text-gray-900">{grant.name}</span>
      </nav>

      <h1 className="text-3xl font-bold text-gray-900 mb-4">{grant.name}</h1>
      <p className="text-lg text-gray-600 mb-8">{grant.description}</p>

      {/* Quick Links */}
      <div className="flex flex-wrap gap-3 mb-8">
        <Link
          href={`/appeals/${slug}`}
          className="text-sm bg-gray-100 text-gray-700 px-4 py-2 rounded-full hover:bg-gray-200"
        >
          Appeal Guide →
        </Link>
        <Link
          href={`/checklist?grant=${slug}`}
          className="text-sm bg-gray-100 text-gray-700 px-4 py-2 rounded-full hover:bg-gray-200"
        >
          Document Checklist →
        </Link>
        <Link
          href="/payment-dates"
          className="text-sm bg-gray-100 text-gray-700 px-4 py-2 rounded-full hover:bg-gray-200"
        >
          Payment Dates →
        </Link>
      </div>

      {/* Eligibility Section */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Eligibility Requirements</h2>
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <ul className="space-y-3">
            {grant.eligibilityCriteria.ageRequirement && (
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                <span><strong>Age:</strong> {grant.eligibilityCriteria.ageRequirement}</span>
              </li>
            )}
            <li className="flex items-start">
              <span className="text-green-600 mr-2">✓</span>
              <span><strong>Citizenship:</strong> {grant.eligibilityCriteria.citizenshipRequirement}</span>
            </li>
            <li className="flex items-start">
              <span className="text-green-600 mr-2">✓</span>
              <span><strong>Residency:</strong> {grant.eligibilityCriteria.residencyRequirement}</span>
            </li>
            {grant.eligibilityCriteria.incomeRequirement && (
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                <span><strong>Income:</strong> {grant.eligibilityCriteria.incomeRequirement}</span>
              </li>
            )}
            {grant.eligibilityCriteria.additionalCriteria.map((criteria, i) => (
              <li key={i} className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                <span>{criteria}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Income Thresholds */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Income Thresholds (Means Test)</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-200 rounded-lg overflow-hidden">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Applicant Type</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900">Maximum Annual Income</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {grant.incomeThresholds.map((threshold, i) => (
                <tr key={i}>
                  <td className="px-4 py-3 text-gray-900">{threshold.applicantType}</td>
                  <td className="px-4 py-3 text-gray-700">R{threshold.maxIncome.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Disqualifiers */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">What Disqualifies You</h2>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <ul className="space-y-2">
            {grant.disqualifiers.map((item, i) => (
              <li key={i} className="flex items-start">
                <span className="text-red-600 mr-2">✗</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* Application Steps */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">How to Apply</h2>
        <div className="space-y-4">
          {grant.applicationSteps.map((step) => (
            <div key={step.stepNumber} className="flex gap-4">
              <div className="flex-shrink-0 w-8 h-8 bg-green-700 text-white rounded-full flex items-center justify-center font-semibold">
                {step.stepNumber}
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
        <p className="mt-4 text-sm text-gray-500">
          Processing time: <strong>{grant.processingTimeline}</strong>
        </p>
      </section>

      {/* Common Mistakes */}
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Common Mistakes to Avoid</h2>
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
          <ul className="space-y-2">
            {grant.commonMistakes.map((mistake, i) => (
              <li key={i} className="flex items-start">
                <span className="text-amber-600 mr-2">⚠</span>
                <span>{mistake}</span>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* FAQ */}
      <FAQBlock faqs={faqs} />

      {/* Last Updated */}
      <p className="text-sm text-gray-500 mt-8">
        Last updated: {new Date(grant.updatedAt).toLocaleDateString('en-ZA', { 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        })}
      </p>
    </div>
  );
}
