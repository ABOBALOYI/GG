"""
Django Filter classes for filtering funding opportunities.
"""
import django_filters
from django.db.models import Q
from datetime import date, timedelta
from .models import FundingOpportunity, Industry, Province, FUNDING_TYPE_CHOICES, BUSINESS_STAGE_CHOICES, TARGET_GROUP_CHOICES


class FundingOpportunityFilter(django_filters.FilterSet):
    """Filter for funding opportunities with search and multi-select filters."""
    
    # Text search
    search = django_filters.CharFilter(method='filter_search', label='Search')
    
    # Multi-select filters
    industries = django_filters.ModelMultipleChoiceFilter(
        queryset=Industry.objects.all(),
        field_name='industries',
        label='Industries'
    )
    provinces = django_filters.ModelMultipleChoiceFilter(
        queryset=Province.objects.all(),
        field_name='provinces',
        label='Provinces'
    )
    funding_type = django_filters.MultipleChoiceFilter(
        choices=FUNDING_TYPE_CHOICES,
        label='Funding Type'
    )
    business_stage = django_filters.MultipleChoiceFilter(
        choices=BUSINESS_STAGE_CHOICES,
        label='Business Stage'
    )
    target_groups = django_filters.MultipleChoiceFilter(
        choices=TARGET_GROUP_CHOICES,
        method='filter_target_groups',
        label='Target Group'
    )
    
    # Deadline urgency
    closing_soon = django_filters.BooleanFilter(
        method='filter_closing_soon',
        label='Closing Soon (within 30 days)'
    )
    
    # Rolling/Always Open filter
    rolling_only = django_filters.BooleanFilter(
        method='filter_rolling',
        label='Rolling / Always Open'
    )
    
    # Funder filter
    funder = django_filters.CharFilter(
        field_name='funder',
        lookup_expr='icontains',
        label='Funder'
    )

    class Meta:
        model = FundingOpportunity
        fields = ['industries', 'provinces', 'funding_type', 'business_stage']

    def filter_search(self, queryset, name, value):
        """Full-text search on funding_name, funder, description, eligibility."""
        if not value:
            return queryset
        # Search across multiple fields with relevance
        return queryset.filter(
            Q(funding_name__icontains=value) |
            Q(funder__icontains=value) |
            Q(description__icontains=value) |
            Q(funding_amount__icontains=value)
        ).distinct()

    def filter_target_groups(self, queryset, name, value):
        """Filter by target groups (stored as JSON array)."""
        if not value:
            return queryset
        # Filter opportunities that have any of the selected target groups
        q = Q()
        for group in value:
            q |= Q(target_groups__contains=group)
        return queryset.filter(q)

    def filter_closing_soon(self, queryset, name, value):
        """Filter opportunities closing within 30 days."""
        if not value:
            return queryset
        today = date.today()
        thirty_days = today + timedelta(days=30)
        return queryset.filter(
            deadline__gte=today,
            deadline__lte=thirty_days,
            is_rolling=False
        )
    
    def filter_rolling(self, queryset, name, value):
        """Filter for rolling/always open opportunities."""
        if not value:
            return queryset
        return queryset.filter(is_rolling=True)
