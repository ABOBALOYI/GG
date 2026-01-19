import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description: 'Privacy Policy for GrantsGuide AI - Learn how we collect, use, and protect your information.',
};

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-10">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Privacy Policy</h1>
          <p className="text-gray-500 text-sm mb-8">Last updated: December 2024</p>
          
          <div className="prose prose-gray max-w-none">
            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">1. Introduction</h2>
            <p className="text-gray-600 mb-4">
              GrantsGuide AI (&quot;we&quot;, &quot;our&quot;, or &quot;us&quot;) is committed to protecting your privacy. 
              This Privacy Policy explains how we collect, use, and safeguard your information when you 
              visit our website grantsguide.co.za.
            </p>
            <p className="text-gray-600 mb-4">
              <strong>Important:</strong> GrantsGuide AI is an unofficial, independent information platform. 
              We are not affiliated with SASSA (South African Social Security Agency) or any government entity.
            </p>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">2. Information We Collect</h2>
            
            <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">2.1 Information You Provide</h3>
            <ul className="list-disc pl-6 text-gray-600 mb-4 space-y-2">
              <li>Questions you ask our AI assistant (we do not store personal identification numbers)</li>
              <li>Checklist progress (stored locally on your device only)</li>
              <li>Language preferences</li>
            </ul>

            <h3 className="text-lg font-semibold text-gray-800 mt-6 mb-3">2.2 Automatically Collected Information</h3>
            <ul className="list-disc pl-6 text-gray-600 mb-4 space-y-2">
              <li>Device type and browser information</li>
              <li>IP address (anonymized)</li>
              <li>Pages visited and time spent</li>
              <li>Referring website</li>
            </ul>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">3. How We Use Your Information</h2>
            <ul className="list-disc pl-6 text-gray-600 mb-4 space-y-2">
              <li>To provide and improve our services</li>
              <li>To respond to your questions via our AI assistant</li>
              <li>To analyze website usage and improve user experience</li>
              <li>To display relevant advertisements</li>
            </ul>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">4. Cookies and Tracking</h2>
            <p className="text-gray-600 mb-4">We use cookies for:</p>
            <ul className="list-disc pl-6 text-gray-600 mb-4 space-y-2">
              <li><strong>Essential cookies:</strong> Required for the website to function properly</li>
              <li><strong>Analytics cookies:</strong> Help us understand how visitors use our site (Google Analytics)</li>
              <li><strong>Advertising cookies:</strong> Used to show relevant ads (Google AdSense)</li>
            </ul>
            <p className="text-gray-600 mb-4">
              You can manage your cookie preferences through our cookie consent banner or your browser settings.
            </p>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">5. Third-Party Services</h2>
            <p className="text-gray-600 mb-4">We use the following third-party services:</p>
            <ul className="list-disc pl-6 text-gray-600 mb-4 space-y-2">
              <li><strong>Google Analytics:</strong> For website analytics</li>
              <li><strong>Google AdSense:</strong> For displaying advertisements</li>
              <li><strong>Google Gemini AI:</strong> For our AI assistant feature</li>
            </ul>
            <p className="text-gray-600 mb-4">
              These services have their own privacy policies. We encourage you to review them.
            </p>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">6. Data Security</h2>
            <p className="text-gray-600 mb-4">
              We implement appropriate security measures to protect your information. However, no method 
              of transmission over the Internet is 100% secure.
            </p>
            <p className="text-gray-600 mb-4">
              <strong>We do not store:</strong>
            </p>
            <ul className="list-disc pl-6 text-gray-600 mb-4 space-y-2">
              <li>South African ID numbers</li>
              <li>SASSA reference numbers</li>
              <li>Bank account details</li>
              <li>Personal addresses</li>
            </ul>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">7. Your Rights</h2>
            <p className="text-gray-600 mb-4">Under POPIA (Protection of Personal Information Act), you have the right to:</p>
            <ul className="list-disc pl-6 text-gray-600 mb-4 space-y-2">
              <li>Access your personal information</li>
              <li>Correct inaccurate information</li>
              <li>Request deletion of your information</li>
              <li>Object to processing of your information</li>
              <li>Withdraw consent at any time</li>
            </ul>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">8. Children&apos;s Privacy</h2>
            <p className="text-gray-600 mb-4">
              Our website is not intended for children under 13. We do not knowingly collect personal 
              information from children under 13.
            </p>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">9. Changes to This Policy</h2>
            <p className="text-gray-600 mb-4">
              We may update this Privacy Policy from time to time. We will notify you of any changes by 
              posting the new Privacy Policy on this page and updating the &quot;Last updated&quot; date.
            </p>

            <h2 className="text-xl font-bold text-gray-900 mt-8 mb-4">10. Contact Us</h2>
            <p className="text-gray-600 mb-4">
              If you have any questions about this Privacy Policy, please contact us at:
            </p>
            <p className="text-gray-600 mb-4">
              Email: privacy@grantsguide.co.za
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
