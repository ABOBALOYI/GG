import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Document Checklist Generator - SASSA Grant Applications',
  description: 'Generate a personalized checklist of documents needed for your SASSA grant application. Track your progress and ensure you have everything ready.',
  keywords: ['SASSA documents', 'grant application checklist', 'required documents', 'SASSA application requirements'],
  openGraph: {
    title: 'Document Checklist Generator - SASSA Grants',
    description: 'Generate a personalized checklist of documents needed for your SASSA grant application.',
    url: 'https://grantguide.co.za/checklist',
  },
  alternates: {
    canonical: 'https://grantguide.co.za/checklist',
  },
};

export default function ChecklistLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
