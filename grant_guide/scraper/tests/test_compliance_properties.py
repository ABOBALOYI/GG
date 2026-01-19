"""
Property-based tests for the Compliance Checker.

**Validates: Requirements 1.2, 1.6, 1.7, 4.5**
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

from scraper.compliance import ComplianceChecker
from scraper.models import (
    NormalisedOpportunity, RecordType, FundingType, FunderType,
    BusinessStage, OpportunityStatus
)
from datetime import date


def create_valid_record(**overrides) -> NormalisedOpportunity:
    """Create a valid normalised record with optional overrides."""
    defaults = {
        'record_type': RecordType.FUNDING_OPPORTUNITY,
        'title': 'Test Funding Opportunity',
        'funder_name': 'Test Funder',
        'funder_type': FunderType.GOV,
        'funding_type': FundingType.GRANT,
        'description_short': 'A test funding opportunity for businesses.',
        'industry_tags': ['ICT'],
        'province_tags': ['Gauteng'],
        'business_stage': BusinessStage.SME,
        'eligibility_bullets': ['Must be registered in SA'],
        'funding_amount_min': None,
        'funding_amount_max': None,
        'deadline_date': date(2025, 12, 31),
        'is_rolling': False,
        'required_documents_bullets': ['ID copy'],
        'application_steps': ['Apply online'],
        'official_apply_url': 'https://example.gov.za/apply',
        'source_url': 'https://example.gov.za/funding',
        'source_name': 'Test Source',
        'last_verified_date': date.today(),
        'status': OpportunityStatus.ACTIVE,
        'raw_content_hash': 'abc123',
        'validation_issues': []
    }
    defaults.update(overrides)
    return NormalisedOpportunity(**defaults)


class TestPaymentToApplyRejection:
    """
    Feature: grant-guide-scraper-engine, Property 4: Payment-to-Apply Rejection
    
    *For any* opportunity description or page content containing payment requirement
    indicators, the Compliance_Checker SHALL reject the record.
    """
    
    @given(keyword=st.sampled_from([
        "application fee", "pay to apply", "registration fee",
        "payment required", "processing fee", "admin fee",
        "fee payable", "non-refundable fee"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_payment_keywords_in_description_rejected(self, keyword):
        """Records with payment keywords in description are flagged."""
        checker = ComplianceChecker()
        record = create_valid_record(
            description_short=f"This opportunity requires {keyword} of R500."
        )
        result = checker.check(record)
        assert len(result.issues) > 0
        assert any('payment' in issue.lower() for issue in result.issues)
    
    @given(keyword=st.sampled_from([
        "application fee", "pay to apply", "registration fee"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_payment_keywords_in_eligibility_rejected(self, keyword):
        """Records with payment keywords in eligibility are flagged."""
        checker = ComplianceChecker()
        record = create_valid_record(
            eligibility_bullets=[f"Applicants must pay {keyword}"]
        )
        result = checker.check(record)
        assert len(result.issues) > 0
    
    @given(keyword=st.sampled_from([
        "application fee", "payment required"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_payment_keywords_in_steps_rejected(self, keyword):
        """Records with payment keywords in application steps are flagged."""
        checker = ComplianceChecker()
        record = create_valid_record(
            application_steps=[f"Step 1: Pay {keyword}"]
        )
        result = checker.check(record)
        assert len(result.issues) > 0


class TestSocialMediaOnlyRejection:
    """
    Feature: grant-guide-scraper-engine, Property 5: Social-Media-Only Rejection
    
    *For any* record where the only contact method or application URL is a
    social media page, the Compliance_Checker SHALL reject the record.
    """
    
    @given(domain=st.sampled_from([
        "whatsapp.com", "wa.me", "chat.whatsapp.com",
        "telegram.org", "t.me",
        "facebook.com", "fb.com"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_social_media_apply_url_rejected(self, domain):
        """Records with social media apply URLs are flagged."""
        checker = ComplianceChecker()
        record = create_valid_record(
            official_apply_url=f"https://{domain}/apply"
        )
        result = checker.check(record)
        assert len(result.issues) > 0
        assert any('social media' in issue.lower() for issue in result.issues)
    
    @given(domain=st.sampled_from([
        "whatsapp.com", "telegram.org", "facebook.com"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_social_media_source_url_rejected(self, domain):
        """Records with social media source URLs are flagged."""
        checker = ComplianceChecker()
        record = create_valid_record(
            source_url=f"https://{domain}/funding"
        )
        result = checker.check(record)
        assert len(result.issues) > 0


class TestAccessControlDetection:
    """
    Feature: grant-guide-scraper-engine, Property 2: Access Control Detection
    
    *For any* HTML page containing login forms, paywall indicators, CAPTCHA challenges,
    the Scraper_Engine SHALL detect these patterns and skip the resource.
    """
    
    @given(pattern=st.sampled_from([
        '<form action="/login"',
        '<input type="password"',
        'please log in to continue',
        'sign in to continue',
        'authentication required',
        'captcha',
        'recaptcha',
        'verify you are human',
        'subscribe to read',
        'premium content',
        'members only'
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_access_control_patterns_detected(self, pattern):
        """Access control patterns are detected in HTML."""
        checker = ComplianceChecker()
        html = f"<html><body>{pattern}</body></html>"
        assert checker.detect_access_control(html) is True
    
    def test_normal_content_not_flagged(self):
        """Normal content without access control is not flagged."""
        checker = ComplianceChecker()
        html = "<html><body><h1>Funding Opportunity</h1><p>Apply now!</p></body></html>"
        assert checker.detect_access_control(html) is False


class TestMissingDataHandling:
    """
    Feature: grant-guide-scraper-engine, Property 10: Missing Data Handling
    
    *For any* extracted record where a required field cannot be extracted,
    the status SHALL be set to "DraftNeedsReview".
    """
    
    @given(field=st.sampled_from([
        'title', 'funder_name', 'official_apply_url', 'source_url'
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_missing_required_field_flagged(self, field):
        """Missing required fields are flagged."""
        checker = ComplianceChecker()
        record = create_valid_record(**{field: ''})
        result = checker.check(record)
        assert len(result.issues) > 0
        assert any(field in issue.lower() for issue in result.issues)
    
    def test_complete_record_compliant(self):
        """Complete record with all required fields is compliant."""
        checker = ComplianceChecker()
        record = create_valid_record()
        result = checker.check(record)
        # Should have no rejection reason (may have minor issues)
        assert result.rejection_reason is None


class TestURLValidity:
    """Test URL validation."""
    
    @given(url=st.sampled_from([
        'https://example.gov.za/apply',
        'http://example.com/funding',
        'https://www.dsbd.gov.za/programmes'
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_valid_urls_accepted(self, url):
        """Valid URLs are accepted."""
        checker = ComplianceChecker()
        record = create_valid_record(official_apply_url=url)
        issues = checker.check_url_validity(record)
        assert not any('apply' in issue.lower() for issue in issues)
    
    @given(url=st.sampled_from([
        'not-a-url',
        'ftp://example.com',
        'javascript:void(0)'
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_invalid_urls_flagged(self, url):
        """Invalid URLs are flagged."""
        checker = ComplianceChecker()
        record = create_valid_record(official_apply_url=url)
        issues = checker.check_url_validity(record)
        assert len(issues) > 0
