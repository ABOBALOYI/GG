import { Metadata } from 'next';
import Link from 'next/link';
import { Calendar, Clock, ArrowRight, Tag } from 'lucide-react';
import { getAllBlogPosts, getAllTags } from '@/lib/data/blog-posts';
import { AdBannerSidebar } from '@/components/AdBanner';

export const metadata: Metadata = {
  title: 'SASSA Guides & News - GrantGuide SA Blog',
  description: 'Latest guides, tips, and news about SASSA grants. Learn about payment dates, application processes, eligibility requirements, and more.',
  keywords: ['SASSA blog', 'grant guides', 'SASSA news', 'social grant tips', 'SASSA updates'],
  openGraph: {
    title: 'SASSA Guides & News - GrantsGuide AI Blog',
    description: 'Latest guides, tips, and news about SASSA grants.',
    url: 'https://grantsguide.co.za/blog',
  },
  alternates: {
    canonical: 'https://grantsguide.co.za/blog',
  },
};

const categoryColors: Record<string, string> = {
  guides: 'bg-green-100 text-green-700',
  news: 'bg-blue-100 text-blue-700',
  tips: 'bg-amber-100 text-amber-700',
  updates: 'bg-purple-100 text-purple-700',
};

export default function BlogPage() {
  const posts = getAllBlogPosts();
  const tags = getAllTags();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero */}
      <section className="bg-gradient-to-br from-green-700 to-green-900 text-white py-10 sm:py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-3 sm:mb-4">
            SASSA Guides & News
          </h1>
          <p className="text-base sm:text-lg md:text-xl text-green-100 max-w-2xl mx-auto">
            Helpful articles about SASSA grants, payment dates, application tips, and the latest updates.
          </p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto px-4 py-8 sm:py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6 sm:space-y-8">
            {posts.map((post) => (
              <article key={post.id} className="bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-shadow">
                <div className="p-5 sm:p-8">
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
                  
                  <Link href={`/blog/${post.slug}`}>
                    <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2 sm:mb-3 hover:text-green-700 transition-colors leading-tight">
                      {post.title}
                    </h2>
                  </Link>
                  
                  <p className="text-sm sm:text-base text-gray-600 mb-4 sm:mb-6 leading-relaxed line-clamp-3">
                    {post.excerpt}
                  </p>
                  
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                    <div className="flex flex-wrap gap-2">
                      {post.tags.slice(0, 3).map((tag) => (
                        <span key={tag} className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                          #{tag}
                        </span>
                      ))}
                    </div>
                    <Link 
                      href={`/blog/${post.slug}`}
                      className="inline-flex items-center gap-2 text-green-700 font-semibold hover:text-green-800 transition-colors text-sm sm:text-base"
                    >
                      Read more <ArrowRight className="w-4 h-4" />
                    </Link>
                  </div>
                </div>
              </article>
            ))}
          </div>

          {/* Sidebar */}
          <aside className="space-y-6 sm:space-y-8">
            {/* Categories - horizontal scroll on mobile */}
            <div className="bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 p-4 sm:p-6">
              <h3 className="font-bold text-gray-900 mb-3 sm:mb-4 text-sm sm:text-base">Categories</h3>
              <div className="flex lg:flex-col gap-2 overflow-x-auto pb-2 lg:pb-0 -mx-1 px-1 lg:mx-0 lg:px-0">
                {['guides', 'news', 'tips', 'updates'].map((cat) => (
                  <Link 
                    key={cat}
                    href={`/blog?category=${cat}`}
                    className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-gray-50 transition-colors whitespace-nowrap lg:whitespace-normal flex-shrink-0 lg:flex-shrink"
                  >
                    <span className="capitalize text-gray-700 text-sm">{cat}</span>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ml-2 ${categoryColors[cat]}`}>
                      {posts.filter(p => p.category === cat).length}
                    </span>
                  </Link>
                ))}
              </div>
            </div>

            {/* Popular Tags */}
            <div className="bg-white rounded-xl sm:rounded-2xl shadow-sm border border-gray-100 p-4 sm:p-6">
              <h3 className="font-bold text-gray-900 mb-3 sm:mb-4 flex items-center gap-2 text-sm sm:text-base">
                <Tag className="w-4 h-4" /> Popular Tags
              </h3>
              <div className="flex flex-wrap gap-2">
                {tags.slice(0, 15).map((tag) => (
                  <Link
                    key={tag}
                    href={`/blog?tag=${encodeURIComponent(tag)}`}
                    className="text-xs sm:text-sm text-gray-600 bg-gray-100 hover:bg-green-100 hover:text-green-700 px-2 sm:px-3 py-1 rounded-full transition-colors"
                  >
                    {tag}
                  </Link>
                ))}
              </div>
            </div>

            {/* CTA */}
            <div className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl sm:rounded-2xl p-4 sm:p-6 text-white">
              <h3 className="font-bold text-base sm:text-lg mb-2">Need Help?</h3>
              <p className="text-green-100 text-xs sm:text-sm mb-3 sm:mb-4">
                Our AI assistant can answer your SASSA questions instantly.
              </p>
              <Link 
                href="/help"
                className="inline-block bg-white text-green-700 px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm hover:bg-green-50 transition-colors"
              >
                Chat with AI
              </Link>
            </div>

            {/* Ad Space */}
            <AdBannerSidebar />
          </aside>
        </div>
      </div>
    </div>
  );
}
