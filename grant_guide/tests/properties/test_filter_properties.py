"""
Property-based tests for filter correctness (P1, P4, P5).

**Validates: Requirements 1.2**
"""
import pytest
from hypothesis import given, strategies as st, settings
from datetime import date, timedelta
from django.test import RequestFactory
from opportunities.models import FundingOpportunity, Industry, Province
from opportunities.filters import FundingOpportunityFilter


@pytest.fixture
def setup_data(db):
    """Create test data for property tests."""
    industries = [
        Industry.objects.create(name=f"Industry {i}", slug=f"industry-{i}")
        for i in range(3)
    ]
    provinces = [
        Province.objects.create(name=f"Province {i}", slug=f"province-{i}")
        for i in range(3)
    ]
    return industries, provinces


@pytest.fixture
def create_opportunities(db, setup_data):
    """Factory to create opportunities with various attributes."""
    industries, provinces = setup_data
    
    def _create(count=5, **defaults):
        opps = []
        for i in range(count):
            opp = FundingOpportunity.objects.create(
                funding_name=defaults.get('funding_name', f"Opportunity {i}"),
                funder=defaults.get('funder', f"Funder {i}"),
                funding_type=defaults.get('funding_type', 'grant'),
                description=defaults.get('description', f"Description {i}"),
                business_stage=defaults.get('business_stage', 'startup'),
                eligibility_requirements=["Req 1"],
                deadline=defaults.get('deadline', date.today() + timedelta(days=30)),
                is_rolling=defaults.get('is_rolling', False),
                required_documents=["Doc 1"],
                application_steps=["Step 1"],
                apply_link="https://example.com/apply",
                source_link="https://example.com/source",
                last_verified=date.today(),
                status=defaults.get('status', 'active'),
                target_groups=defaults.get('target_groups', [])
            )
            opp.industries.add(industries[i % len(industries)])
            opp.provinces.add(provinces[i % len(provinces)])
            opps.append(opp)
        return opps
    return _create


class TestFilterCorrectness:
    """
    P1: Filter Correctness
    
    Property: When filtering by any criteria, all returned opportunities 
    must match ALL applied filters.
    
    **Validates: Requirements 1.2**
    """

    @pytest.mark.django_db
    def test_funding_type_filter_returns_only_matching(self, create_opportunities):
        """All results must match the selected funding type."""
        # Create opportunities with different funding types
        create_opportunities(2, funding_type='grant')
        create_opportunities(2, funding_type='loan')
        create_opportunities(1, funding_type='equity')
        
        # Filter by grant
        qs = FundingOpportunity.objects.filter(status='active')
        filterset = FundingOpportunityFilter({'funding_type': ['grant']}, queryset=qs)
        
        # Property: All results must be grants
        for opp in filterset.qs:
            assert opp.funding_type == 'grant', f"Expected grant, got {opp.funding_type}"

    @pytest.mark.django_db
    def test_business_stage_filter_returns_only_matching(self, create_opportunities):
        """All results must match the selected business stage."""
        create_opportunities(2, business_stage='startup')
        create_opportunities(2, business_stage='sme')
        create_opportunities(1, business_stage='established')
        
        qs = FundingOpportunity.objects.filter(status='active')
        filterset = FundingOpportunityFilter({'business_stage': ['sme']}, queryset=qs)
        
        for opp in filterset.qs:
            assert opp.business_stage == 'sme', f"Expected sme, got {opp.business_stage}"

    @pytest.mark.django_db
    def test_combined_filters_return_intersection(self, create_opportunities):
        """Combined filters must return intersection of all criteria."""
        create_opportunities(3, funding_type='grant', business_stage='startup')
        create_opportunities(2, funding_type='loan', business_stage='startup')
        create_opportunities(2, funding_type='grant', business_stage='sme')
        
        qs = FundingOpportunity.objects.filter(status='active')
        filterset = FundingOpportunityFilter({
            'funding_type': ['grant'],
            'business_stage': ['startup']
        }, queryset=qs)
        
        for opp in filterset.qs:
            assert opp.funding_type == 'grant', f"Expected grant, got {opp.funding_type}"
            assert opp.business_stage == 'startup', f"Expected startup, got {opp.business_stage}"


class TestSearchRelevance:
    """
    P4: Search Result Relevance
    
    Property: Search results must contain the search term in at least 
    one searchable field (funding_name, funder, description).
    
    **Validates: Requirements 1.2**
    """

    @pytest.mark.django_db
    def test_search_returns_matching_funding_name(self, create_opportunities):
        """Search term in funding_name should return the opportunity."""
        create_opportunities(1, funding_name="Special Agriculture Grant")
        create_opportunities(2, funding_name="Tech Innovation Fund")
        
        qs = FundingOpportunity.objects.filter(status='active')
        filterset = FundingOpportunityFilter({'search': 'Agriculture'}, queryset=qs)
        
        assert filterset.qs.count() == 1
        for opp in filterset.qs:
            assert 'agriculture' in opp.funding_name.lower()

    @pytest.mark.django_db
    def test_search_returns_matching_funder(self, create_opportunities):
        """Search term in funder should return the opportunity."""
        create_opportunities(1, funder="Department of Trade")
        create_opportunities(2, funder="Private Foundation")
        
        qs = FundingOpportunity.objects.filter(status='active')
        filterset = FundingOpportunityFilter({'search': 'Trade'}, queryset=qs)
        
        assert filterset.qs.count() == 1
        for opp in filterset.qs:
            assert 'trade' in opp.funder.lower()

    @pytest.mark.django_db
    def test_search_returns_matching_description(self, create_opportunities):
        """Search term in description should return the opportunity."""
        create_opportunities(1, description="Funding for renewable energy projects")
        create_opportunities(2, description="Support for manufacturing businesses")
        
        qs = FundingOpportunity.objects.filter(status='active')
        filterset = FundingOpportunityFilter({'search': 'renewable'}, queryset=qs)
        
        assert filterset.qs.count() == 1
        for opp in filterset.qs:
            assert 'renewable' in opp.description.lower()


class TestDeadlineUrgency:
    """
    P5: Deadline Urgency Correctness
    
    Property: "Closing Soon" filter returns only opportunities with 
    deadlines within 30 days.
    
    **Validates: Requirements 1.2**
    """

    @pytest.mark.django_db
    def test_closing_soon_returns_only_within_30_days(self, create_opportunities):
        """Closing soon filter must only return deadlines within 30 days."""
        today = date.today()
        
        # Create opportunities with various deadlines
        create_opportunities(2, deadline=today + timedelta(days=10))  # Within 30 days
        create_opportunities(2, deadline=today + timedelta(days=25))  # Within 30 days
        create_opportunities(2, deadline=today + timedelta(days=60))  # Beyond 30 days
        create_opportunities(1, is_rolling=True, deadline=None)  # Rolling
        
        qs = FundingOpportunity.objects.filter(status='active')
        filterset = FundingOpportunityFilter({'closing_soon': True}, queryset=qs)
        
        thirty_days = today + timedelta(days=30)
        for opp in filterset.qs:
            assert opp.deadline is not None, "Rolling opportunities should not appear"
            assert opp.deadline >= today, f"Deadline {opp.deadline} is in the past"
            assert opp.deadline <= thirty_days, f"Deadline {opp.deadline} is beyond 30 days"

    @pytest.mark.django_db
    def test_closing_soon_excludes_rolling(self, create_opportunities):
        """Rolling opportunities should not appear in closing soon results."""
        today = date.today()
        
        create_opportunities(2, deadline=today + timedelta(days=10))
        create_opportunities(2, is_rolling=True, deadline=None)
        
        qs = FundingOpportunity.objects.filter(status='active')
        filterset = FundingOpportunityFilter({'closing_soon': True}, queryset=qs)
        
        for opp in filterset.qs:
            assert not opp.is_rolling, "Rolling opportunities should be excluded"
