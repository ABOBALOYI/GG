import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import DisclaimerBanner from "@/components/DisclaimerBanner";
import CookieConsent from "@/components/CookieConsent";
import { LanguageProvider } from "@/lib/i18n/LanguageContext";

// AdSense client ID
const ADSENSE_CLIENT = 'ca-pub-4896697928226626';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL('https://grantsguide.co.za'),
  title: {
    default: "GrantsGuide AI - Free SASSA Grant Information & Help 2026",
    template: "%s | GrantsGuide AI 2026",
  },
  description: "Your 2026 guide to SASSA grants in South Africa. Check eligibility, payment dates, status codes, and get AI-powered help. Unofficial - free and always updated for 2026.",
  keywords: [
    "SASSA 2026",
    "SASSA grants 2026",
    "South Africa grants",
    "social grants 2026",
    "SASSA payment dates 2026",
    "SASSA status check",
    "old age grant 2026",
    "child support grant 2026",
    "disability grant 2026",
    "SASSA application 2026",
    "SASSA appeal",
    "grant eligibility",
    "SRD grant 2026",
  ],
  authors: [{ name: "GrantsGuide AI" }],
  creator: "GrantsGuide AI",
  publisher: "GrantsGuide AI",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "en_ZA",
    url: "https://grantsguide.co.za",
    siteName: "GrantsGuide AI",
    title: "GrantsGuide AI - Free SASSA Grant Information & Help 2026",
    description: "Your 2026 guide to SASSA grants. Check eligibility, payment dates, status codes, and get AI-powered help.",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "GrantsGuide AI - Your Guide to SASSA Grants",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "GrantsGuide AI - Free SASSA Grant Information 2026",
    description: "Your 2026 guide to SASSA grants. Check eligibility, payment dates, and get AI-powered help.",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    // Add your verification codes here
    // google: "your-google-verification-code",
  },
  alternates: {
    canonical: "https://grantsguide.co.za",
    languages: {
      "en-ZA": "https://grantsguide.co.za",
      "zu-ZA": "https://grantsguide.co.za?lang=zu",
      "xh-ZA": "https://grantsguide.co.za?lang=xh",
      "af-ZA": "https://grantsguide.co.za?lang=af",
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "GrantsGuide AI",
    url: "https://grantsguide.co.za",
    description: "Free guide to SASSA grants in South Africa",
    potentialAction: {
      "@type": "SearchAction",
      target: "https://grantsguide.co.za/status?q={search_term_string}",
      "query-input": "required name=search_term_string",
    },
  };

  const organizationJsonLd = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "GrantsGuide AI",
    url: "https://grantsguide.co.za",
    logo: "https://grantsguide.co.za/logo.png",
    description: "Free, unofficial SASSA grant information platform",
    areaServed: {
      "@type": "Country",
      name: "South Africa",
    },
  };

  return (
    <html lang="en-ZA">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#166534" />
        <meta name="google-adsense-account" content="ca-pub-4896697928226626" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationJsonLd) }}
        />
        {/* Google AdSense - only load if client ID is configured */}
        {ADSENSE_CLIENT && (
          <script
            async
            src={`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CLIENT}`}
            crossOrigin="anonymous"
          />
        )}
      </head>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen flex flex-col`}>
        <LanguageProvider>
          <DisclaimerBanner />
          <Header />
          <main className="flex-1">{children}</main>
          <Footer />
          <CookieConsent />
        </LanguageProvider>
      </body>
    </html>
  );
}
