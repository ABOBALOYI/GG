"""
Property-based tests for required fields validation (P3).

**Validates: Requirements 2.1, 4.1**
"""
import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from opportunities.models import FundingOpportunity, Industry, Province


@pytest.fixture
def setup_data(db):
    """Create test data for property tests."""
    industry = Industry.objects.create(name="Test Industry", slug="test-industry")
    province = Province.objects.create(name="Test Province", slug="test-province")
    return industry, province


class TestRequiredFieldsValidation:
    """
    P3: Required Fields Validation
    
    Property: Active opportunities must have all required fields populated.
    
    **Validates: Requirements 2.1, 4.1**
    """

    @pytest.mark.django_db
    def test_active_requires_funding_name(self, setup_data):
        """Active opportunities must have funding_name."""
        industry, province = setup_data
        
        opp = FundingOpportunity(
            funding_name="",  # Missing
            funder="Test Funder",
            funding_type="grant",
            description="Test description",
            business_stage="startup",
            eligibility_requirements=["Req 1"],
            required_documents=["Doc 1"],
            application_steps=["Step 1"],
            apply_link="https://example.com/apply",
            source_link="https://example.com/source",
            last_verified=date.today(),
            status="active"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            opp.full_clean()
        
        assert 'funding_name' in str(exc_info.value)

    @pytest.mark.django_db
    def test_active_requires_funder(self, setup_data):
        """Active opportunities must have funder."""
        opp = FundingOpportunity(
            funding_name="Test Grant",
            funder="",  # Missing
            funding_type="grant",
            description="Test description",
            business_stage="startup",
            eligibility_requirements=["Req 1"],
            required_documents=["Doc 1"],
            application_steps=["Step 1"],
            apply_link="https://example.com/apply",
            source_link="https://example.com/source",
            last_verified=date.today(),
            status="active"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            opp.full_clean()
        
        assert 'funder' in str(exc_info.value)

    @pytest.mark.django_db
    def test_active_requires_apply_link(self, setup_data):
        """Active opportunities must have apply_link."""
        opp = FundingOpportunity(
            funding_name="Test Grant",
            funder="Test Funder",
            funding_type="grant",
            description="Test description",
            business_stage="startup",
            eligibility_requirements=["Req 1"],
            required_documents=["Doc 1"],
            application_steps=["Step 1"],
            apply_link="",  # Missing
            source_link="https://example.com/source",
            last_verified=date.today(),
            status="active"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            opp.full_clean()
        
        assert 'apply_link' in str(exc_info.value)

    @pytest.mark.django_db
    def test_active_requires_source_link(self, setup_data):
        """Active opportunities must have source_link."""
        opp = FundingOpportunity(
            funding_name="Test Grant",
            funder="Test Funder",
            funding_type="grant",
            description="Test description",
            business_stage="startup",
            eligibility_requirements=["Req 1"],
            required_documents=["Doc 1"],
            application_steps=["Step 1"],
            apply_link="https://example.com/apply",
            source_link="",  # Missing
            last_verified=date.today(),
            status="active"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            opp.full_clean()
        
        assert 'source_link' in str(exc_info.value)

    @pytest.mark.django_db
    def test_active_requires_eligibility_requirements(self, setup_data):
        """Active opportunities must have eligibility_requirements."""
        opp = FundingOpportunity(
            funding_name="Test Grant",
            funder="Test Funder",
            funding_type="grant",
            description="Test description",
            business_stage="startup",
            eligibility_requirements=[],  # Empty
            required_documents=["Doc 1"],
            application_steps=["Step 1"],
            apply_link="https://example.com/apply",
            source_link="https://example.com/source",
            last_verified=date.today(),
            status="active"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            opp.full_clean()
        
        assert 'eligibility_requirements' in str(exc_info.value)

    @pytest.mark.django_db
    def test_active_requires_required_documents(self, setup_data):
        """Active opportunities must have required_documents."""
        opp = FundingOpportunity(
            funding_name="Test Grant",
            funder="Test Funder",
            funding_type="grant",
            description="Test description",
            business_stage="startup",
            eligibility_requirements=["Req 1"],
            required_documents=[],  # Empty
            application_steps=["Step 1"],
            apply_link="https://example.com/apply",
            source_link="https://example.com/source",
            last_verified=date.today(),
            status="active"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            opp.full_clean()
        
        assert 'required_documents' in str(exc_info.value)

    @pytest.mark.django_db
    def test_active_requires_application_steps(self, setup_data):
        """Active opportunities must have application_steps."""
        opp = FundingOpportunity(
            funding_name="Test Grant",
            funder="Test Funder",
            funding_type="grant",
            description="Test description",
            business_stage="startup",
            eligibility_requirements=["Req 1"],
            required_documents=["Doc 1"],
            application_steps=[],  # Empty
            apply_link="https://example.com/apply",
            source_link="https://example.com/source",
            last_verified=date.today(),
            status="active"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            opp.full_clean()
        
        assert 'application_steps' in str(exc_info.value)

    @pytest.mark.django_db
    def test_draft_allows_missing_optional_validation(self, setup_data):
        """Draft opportunities skip our custom active-status validation."""
        opp = FundingOpportunity(
            funding_name="Test Grant",
            funder="Test Funder",  # Required by Django model
            funding_type="grant",
            description="Test description",
            business_stage="startup",
            eligibility_requirements=["Req 1"],  # Required by Django model
            required_documents=["Doc 1"],  # Required by Django model
            application_steps=["Step 1"],  # Required by Django model
            apply_link="https://example.com/apply",
            source_link="https://example.com/source",
            last_verified=date.today(),
            status="draft"  # Draft status - our custom validation is skipped
        )
        
        # Should not raise ValidationError - draft skips our custom active-status checks
        opp.full_clean()

    @pytest.mark.django_db
    def test_valid_active_opportunity_passes(self, setup_data):
        """A fully populated active opportunity should pass validation."""
        industry, province = setup_data
        
        opp = FundingOpportunity(
            funding_name="Complete Grant",
            funder="Complete Funder",
            funding_type="grant",
            description="A complete test description",
            business_stage="startup",
            eligibility_requirements=["Requirement 1", "Requirement 2"],
            required_documents=["Document 1", "Document 2"],
            application_steps=["Step 1", "Step 2"],
            apply_link="https://example.com/apply",
            source_link="https://example.com/source",
            last_verified=date.today(),
            status="active"
        )
        
        # Should not raise ValidationError
        opp.full_clean()
