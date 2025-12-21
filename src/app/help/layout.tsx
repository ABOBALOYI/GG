import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'AI Caseworker - Get Help with SASSA Grants',
  description: 'Get instant answers to your SASSA questions with our AI-powered assistant. Ask about grant eligibility, application process, required documents, and more.',
  keywords: ['SASSA help', 'grant assistance', 'AI caseworker', 'SASSA questions', 'grant eligibility help'],
  openGraph: {
    title: 'AI Caseworker - SASSA Grant Help',
    description: 'Get instant answers to your SASSA questions with our AI-powered assistant.',
    url: 'https://grantsguide.co.za/help',
  },
  alternates: {
    canonical: 'https://grantsguide.co.za/help',
  },
};

export default function HelpLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
