"""
Sitemap configuration for SEO.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import FundingOpportunity


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 1.0
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['opportunities:home', 'opportunities:list']

    def location(self, item):
        return reverse(item)


class OpportunitySitemap(Sitemap):
    """Sitemap for funding opportunities."""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return FundingOpportunity.objects.filter(status='open')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('opportunities:detail', kwargs={'slug': obj.slug})
