"""
Views for the opportunities app.
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import FundingOpportunity, Industry, Province
from .filters import FundingOpportunityFilter


class OpportunityListView(ListView):
    """List view for funding opportunities with filtering and search."""
    model = FundingOpportunity
    template_name = 'opportunities/list.html'
    context_object_name = 'opportunities'
    paginate_by = 12

    def get_queryset(self):
        queryset = FundingOpportunity.objects.filter(status='active').select_related().prefetch_related('industries', 'provinces')
        
        # Apply filters
        self.filterset = FundingOpportunityFilter(self.request.GET, queryset=queryset)
        
        # Default sort by deadline (closing soon first), then by created_at
        return self.filterset.qs.order_by('deadline', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['industries'] = Industry.objects.all()
        context['provinces'] = Province.objects.all()
        context['total_count'] = self.filterset.qs.count()
        # Add choices for template
        from .models import FUNDING_TYPE_CHOICES, BUSINESS_STAGE_CHOICES, TARGET_GROUP_CHOICES
        context['funding_types'] = FUNDING_TYPE_CHOICES
        context['business_stages'] = BUSINESS_STAGE_CHOICES
        context['target_groups'] = TARGET_GROUP_CHOICES
        return context


class OpportunityDetailView(DetailView):
    """Detail view for a single funding opportunity."""
    model = FundingOpportunity
    template_name = 'opportunities/detail.html'
    context_object_name = 'opportunity'

    def get_queryset(self):
        return FundingOpportunity.objects.filter(status='active').prefetch_related('industries', 'provinces')


def home(request):
    """Home page - shows featured/recent opportunities."""
    opportunities = FundingOpportunity.objects.filter(
        status='active'
    ).select_related().prefetch_related(
        'industries', 'provinces'
    ).order_by('deadline', '-created_at')[:6]
    
    return render(request, 'opportunities/home.html', {
        'opportunities': opportunities,
        'total_active': FundingOpportunity.objects.filter(status='active').count(),
    })


def search_partial(request):
    """HTMX partial for search results."""
    queryset = FundingOpportunity.objects.filter(status='active').prefetch_related('industries', 'provinces')
    filterset = FundingOpportunityFilter(request.GET, queryset=queryset)
    opportunities = filterset.qs.order_by('deadline', '-created_at')
    
    # Paginate
    paginator = Paginator(opportunities, 12)
    page = request.GET.get('page', 1)
    opportunities = paginator.get_page(page)
    
    # Build query string for pagination links (preserve filters)
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = query_params.urlencode()
    
    return render(request, 'opportunities/_opportunity_list.html', {
        'opportunities': opportunities,
        'total_count': filterset.qs.count(),
        'query_string': query_string,
    })
