"""
Context processors for Grant Guide.
"""
from django.conf import settings


def google_adsense(request):
    """
    Add Google AdSense client ID to template context.
    """
    return {
        'GOOGLE_ADSENSE_CLIENT_ID': settings.GOOGLE_ADSENSE_CLIENT_ID,
    }
