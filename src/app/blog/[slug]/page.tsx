import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { Calendar, Clock, ArrowLeft, Tag } from 'lucide-react';
import { getBlogPostBySlug, getAllBlogSlugs, getRecentBlogPosts } from '@/lib/data/blog-posts';
import { generateBreadcrumbSchema } from '@/components/SEOHead';
import { AdBannerSidebar, AdBannerInArticle } from '@/components/AdBanner';

interface Props {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  return getAllBlogSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = getBlogPostBySlug(slug);
  
  if (!post) {
    return { title: 'Post Not Found' };
  }

  return {
    title: post.title,
    description: post.excerpt,
    keywords: post.tags,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      url: `https://grantguide.co.za/blog/${slug}`,
      type: 'article',
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      tags: post.tags,
    },
    alternates: {
      canonical: `https://grantguide.co.za/blog/${slug}`,
    },
  };
}

const categoryColors: Record<string, string> = {
  guides: 'bg-green-100 text-green-700',
  news: 'bg-blue-100 text-blue-700',
  tips: 'bg-amber-100 text-amber-700',
  updates: 'bg-purple-100 text-purple-700',
};

export default async function BlogPostPage({ params }: Props) {
  const { slug } = await params;
  const post = getBlogPostBySlug(slug);

  if (!post) {
    notFound();
  }

  const recentPosts = getRecentBlogPosts(3).filter(p => p.slug !== slug);
  
  const breadcrumbs = [
    { name: 'Home', url: '/' },
    { name: 'Blog', url: '/blog' },
    { name: post.title, url: `/blog/${slug}` }
  ];

  // Article schema for SEO
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Organization',
      name: 'GrantGuide SA'
    },
    publisher: {
      '@type': 'Organization',
      name: 'GrantGuide SA',
      url: 'https://grantguide.co.za'
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `https://grantguide.co.za/blog/${slug}`
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateBreadcrumbSchema(breadcrumbs)) }}
      />

      {/* Header */}
      <header className="bg-white border-b border-gray-100">
        <div className="max-w-4xl mx-auto px-4 py-4 sm:py-6">
          <Link 
            href="/blog"
            className="inline-flex items-center gap-2 text-gray-600 hover:text-green-700 transition-colors mb-4 sm:mb-6 text-sm sm:text-base"
          >
            <ArrowLeft className="w-4 h-4" /> Back to Blog
          </Link>
          
          <div className="flex flex-wrap items-center gap-2 sm:gap-3 mb-3 sm:mb-4">
            <span className={`px-2 sm:px-3 py-1 rounded-full text-xs font-semibold uppercase ${categoryColors[post.category]}`}>
              {post.category}
            </span>
            <div className="flex items-center gap-1 text-gray-500 text-xs sm:text-sm">
              <Calendar className="w-3 h-3 sm:w-4 sm:h-4" />
              <span className="hidden sm:inline">
                {new Date(post.publishedAt).toLocaleDateString('en-ZA', { 
                  day: 'numeric', 
                  month: 'long', 
                  year: 'numeric' 
                })}
              </span>
              <span className="sm:hidden">
                {new Date(post.publishedAt).toLocaleDateString('en-ZA', { 
                  day: 'numeric', 
                  month: 'short', 
                  year: 'numeric' 
                })}
              </span>
            </div>
            <div className="flex items-center gap-1 text-gray-500 text-xs sm:text-sm">
              <Clock className="w-3 h-3 sm:w-4 sm:h-4" />
              {post.readTime} min
            </div>
          </div>
          
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 leading-tight">
            {post.title}
          </h1>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-8 sm:py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
          {/* Article Content */}
          <article className="lg:col-span-2">
            <div className="bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 p-5 sm:p-8 md:p-12">
              <div 
                className="prose prose-sm sm:prose-base lg:prose-lg prose-green max-w-none
                  prose-headings:font-bold prose-headings:text-gray-900
                  prose-h2:text-xl prose-h2:sm:text-2xl prose-h2:mt-6 prose-h2:sm:mt-8 prose-h2:mb-3 prose-h2:sm:mb-4
                  prose-h3:text-lg prose-h3:sm:text-xl prose-h3:mt-5 prose-h3:sm:mt-6 prose-h3:mb-2 prose-h3:sm:mb-3
                  prose-p:text-gray-600 prose-p:leading-relaxed prose-p:text-sm prose-p:sm:text-base
                  prose-li:text-gray-600 prose-li:text-sm prose-li:sm:text-base
                  prose-strong:text-gray-900
                  prose-a:text-green-700 prose-a:no-underline hover:prose-a:underline"
                dangerouslySetInnerHTML={{ __html: formatContent(post.content) }}
              />
              
              {/* Responsive table wrapper */}
              <style dangerouslySetInnerHTML={{ __html: `
                .prose table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
                .prose th, .prose td { padding: 8px 12px; border: 1px solid #e5e7eb; white-space: nowrap; }
                .prose th { background: #f9fafb; text-align: left; font-size: 0.875rem; }
                .prose td { font-size: 0.875rem; }
                @media (min-width: 640px) {
                  .prose th, .prose td { padding: 12px 16px; white-space: normal; }
                  .prose th { font-size: 1rem; }
                  .prose td { font-size: 1rem; }
                }
              `}} />
            </div>

            {/* Tags */}
            <div className="mt-6 sm:mt-8 flex items-center gap-2 sm:gap-3 flex-wrap">
              <Tag className="w-4 h-4 text-gray-400" />
              {post.tags.map((tag) => (
                <Link
                  key={tag}
                  href={`/blog?tag=${encodeURIComponent(tag)}`}
                  className="text-xs sm:text-sm text-gray-600 bg-white border border-gray-200 hover:border-green-300 hover:text-green-700 px-2 sm:px-3 py-1 rounded-full transition-colors"
                >
                  #{tag}
                </Link>
              ))}
            </div>

            {/* Disclaimer */}
            <div className="mt-6 sm:mt-8 bg-amber-50 border border-amber-200 rounded-lg sm:rounded-xl p-4 sm:p-6">
              <p className="text-amber-800 text-xs sm:text-sm">
                <strong>Disclaimer:</strong> This article is for informational purposes only. 
                GrantGuide SA is not affiliated with SASSA. For official information, 
                please visit <a href="https://www.sassa.gov.za" target="_blank" rel="noopener noreferrer" className="underline">sassa.gov.za</a>.
              </p>
            </div>

            {/* In-article Ad */}
            <AdBannerInArticle />
          </article>

          {/* Sidebar */}
          <aside className="space-y-6 sm:space-y-8">
            {/* Related Posts */}
            {recentPosts.length > 0 && (
              <div className="bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 p-4 sm:p-6">
                <h3 className="font-bold text-gray-900 mb-3 sm:mb-4 text-sm sm:text-base">Related Articles</h3>
                <div className="space-y-3 sm:space-y-4">
                  {recentPosts.map((relatedPost) => (
                    <Link 
                      key={relatedPost.id}
                      href={`/blog/${relatedPost.slug}`}
                      className="block group"
                    >
                      <h4 className="font-medium text-gray-900 group-hover:text-green-700 transition-colors line-clamp-2 text-sm sm:text-base">
                        {relatedPost.title}
                      </h4>
                      <p className="text-xs sm:text-sm text-gray-500 mt-1">
                        {relatedPost.readTime} min read
                      </p>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* CTA */}
            <div className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl sm:rounded-2xl p-4 sm:p-6 text-white lg:sticky lg:top-24">
              <h3 className="font-bold text-base sm:text-lg mb-2">Have Questions?</h3>
              <p className="text-green-100 text-xs sm:text-sm mb-3 sm:mb-4">
                Our AI assistant can help you understand SASSA grants.
              </p>
              <Link 
                href="/help"
                className="inline-block bg-white text-green-700 px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm hover:bg-green-50 transition-colors"
              >
                Ask AI Assistant
              </Link>
            </div>

            {/* Sidebar Ad */}
            <AdBannerSidebar />
          </aside>
        </div>
      </div>
    </div>
  );
}

// Simple markdown-like formatting
function formatContent(content: string): string {
  return content
    // Headers
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    // Bold
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Tables (basic)
    .replace(/\|(.+)\|/g, (match) => {
      const cells = match.split('|').filter(c => c.trim());
      if (cells.some(c => c.includes('---'))) {
        return ''; // Skip separator row
      }
      const isHeader = match.includes('---') || cells[0].includes('Type') || cells[0].includes('Action') || cells[0].includes('Applicant') || cells[0].includes('Timeframe') || cells[0].includes('Decline') || cells[0].includes('Grant');
      const tag = isHeader ? 'th' : 'td';
      return `<tr>${cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join('')}</tr>`;
    })
    // Wrap tables
    .replace(/(<tr>.*<\/tr>\n?)+/g, '<table><tbody>$&</tbody></table>')
    // Lists
    .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
    // Paragraphs
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(?!<)(.+)$/gm, '<p>$1</p>')
    // Clean up
    .replace(/<p><\/p>/g, '')
    .replace(/<p>(<h|<ul|<table)/g, '$1')
    .replace(/(<\/h\d>|<\/ul>|<\/table>)<\/p>/g, '$1')
    // Horizontal rules
    .replace(/^---$/gm, '<hr class="my-8 border-gray-200" />');
}
