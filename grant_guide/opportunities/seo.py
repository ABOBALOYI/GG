"""
SEO views for robots.txt and other SEO-related endpoints.
"""
from django.http import HttpResponse
from django.views.decorators.cache import cache_page


@cache_page(60 * 60 * 24)  # Cache for 24 hours
def robots_txt(request):
    """Generate robots.txt for search engines."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin and search",
        "Disallow: /admin/",
        "Disallow: /search/",
        "",
        "# Sitemap",
        f"Sitemap: https://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
