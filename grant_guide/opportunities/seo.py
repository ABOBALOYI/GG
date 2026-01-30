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


@cache_page(60 * 60 * 24)  # Cache for 24 hours
def ads_txt(request):
    """Serve ads.txt for Google AdSense verification."""
    content = "google.com, pub-4896697928226626, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")
