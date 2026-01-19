"""
Pytest configuration and fixtures for Grant Guide SA tests.
"""
import pytest
from datetime import date, timedelta
from hypothesis import settings, Verbosity

# Hypothesis settings
settings.register_profile("ci", max_examples=100)
settings.register_profile("dev", max_examples=10)
settings.register_profile("debug", max_examples=5, verbosity=Verbosity.verbose)
settings.load_profile("dev")


@pytest.fixture
def sample_industry(db):
    from opportunities.models import Industry
    return Industry.objects.create(name="Technology/ICT", slug="technology-ict")


@pytest.fixture
def sample_province(db):
    from opportunities.models import Province
    return Province.objects.create(name="Gauteng", slug="gauteng")


@pytest.fixture
def sample_opportunity(db, sample_industry, sample_province):
    from opportunities.models import FundingOpportunity
    opp = FundingOpportunity.objects.create(
        funding_name="Test Grant",
        funder="Test Funder",
        funding_type="grant",
        description="A test funding opportunity",
        business_stage="startup",
        eligibility_requirements=["Requirement 1", "Requirement 2"],
        funding_amount="R100,000 - R500,000",
        deadline=date.today() + timedelta(days=30),
        required_documents=["ID Document", "Business Plan"],
        application_steps=["Step 1: Register", "Step 2: Submit"],
        apply_link="https://example.com/apply",
        source_link="https://example.com/source",
        last_verified=date.today(),
        status="active"
    )
    opp.industries.add(sample_industry)
    opp.provinces.add(sample_province)
    return opp
