"""
URL configuration for grant_guide project.
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from opportunities.sitemaps import StaticViewSitemap, OpportunitySitemap
from opportunities.seo import robots_txt

sitemaps = {
    'static': StaticViewSitemap,
    'opportunities': OpportunitySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('opportunities.urls')),
]
