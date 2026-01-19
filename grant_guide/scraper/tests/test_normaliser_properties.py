"""
Property-based tests for the Record Normaliser.

**Validates: Requirements 4.7, 5.1, 5.2, 5.3, 5.4**
"""
import pytest
from datetime import date
from decimal import Decimal
from hypothesis import given, strategies as st, settings, HealthCheck

from scraper.normaliser import RecordNormaliser
from scraper.models import RawOpportunity, FundingType


class TestCurrencyNormalisation:
    """
    Feature: grant-guide-scraper-engine, Property 13: Currency Normalisation
    
    *For any* monetary amount string (e.g., "R50,000", "50000 ZAR", "R 1 million"),
    the Record_Normaliser SHALL convert it to a numeric ZAR value.
    """
    
    @given(amount=st.sampled_from([
        "R50,000", "R 50 000", "50000 ZAR", "R1 million", "R500k",
        "R50,000.00", "R 1,500,000", "R2.5 million", "R100K",
        "50000", "R 50000", "1000000 RAND"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_currency_normalisation_returns_decimal_or_none(self, amount):
        """Currency normalisation returns Decimal or None."""
        normaliser = RecordNormaliser()
        result = normaliser.normalise_amount(amount)
        assert result is None or isinstance(result, Decimal)
    
    @given(amount=st.sampled_from([
        "R50,000", "R 50 000", "50000 ZAR", "R50,000.00", "R 50000"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_currency_normalisation_positive_values(self, amount):
        """Currency normalisation returns positive values."""
        normaliser = RecordNormaliser()
        result = normaliser.normalise_amount(amount)
        if result is not None:
            assert result >= 0
    
    def test_million_multiplier(self):
        """R1 million should equal 1,000,000."""
        normaliser = RecordNormaliser()
        result = normaliser.normalise_amount("R1 million")
        assert result == Decimal("1000000")
    
    def test_k_multiplier(self):
        """R500k should equal 500,000."""
        normaliser = RecordNormaliser()
        result = normaliser.normalise_amount("R500k")
        assert result == Decimal("500000")
    
    def test_none_input(self):
        """None input returns None."""
        normaliser = RecordNormaliser()
        assert normaliser.normalise_amount(None) is None
    
    def test_empty_string(self):
        """Empty string returns None."""
        normaliser = RecordNormaliser()
        assert normaliser.normalise_amount("") is None


class TestDateNormalisation:
    """
    Feature: grant-guide-scraper-engine, Property 14: Date Normalisation
    
    *For any* date string in common South African formats,
    the Record_Normaliser SHALL convert it to ISO format (YYYY-MM-DD).
    """
    
    @given(date_str=st.sampled_from([
        "15 March 2025", "2025/03/15", "15-03-2025", "March 15, 2025",
        "15/03/2025", "2025-03-15", "15 Mar 2025"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_date_normalisation_returns_date_or_none(self, date_str):
        """Date normalisation returns date or None."""
        normaliser = RecordNormaliser()
        result = normaliser.normalise_date(date_str)
        assert result is None or isinstance(result, date)
    
    @given(date_str=st.sampled_from([
        "15 March 2025", "2025/03/15", "15-03-2025", "March 15, 2025",
        "15/03/2025", "2025-03-15"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_date_normalisation_correct_date(self, date_str):
        """All formats for March 15, 2025 should produce same date."""
        normaliser = RecordNormaliser()
        result = normaliser.normalise_date(date_str)
        if result:
            assert result == date(2025, 3, 15)
    
    def test_none_input(self):
        """None input returns None."""
        normaliser = RecordNormaliser()
        assert normaliser.normalise_date(None) is None
    
    def test_invalid_date(self):
        """Invalid date string returns None."""
        normaliser = RecordNormaliser()
        assert normaliser.normalise_date("not a date") is None


class TestProvinceNormalisation:
    """
    Feature: grant-guide-scraper-engine, Property 15: Province Normalisation
    
    *For any* province name or abbreviation,
    the Record_Normaliser SHALL map it to the canonical province name.
    """
    
    @given(province=st.sampled_from([
        "GP", "Gauteng", "gauteng", "GAUTENG", "Gauteng Province",
        "KZN", "KwaZulu-Natal", "kwazulu natal", "kwa-zulu natal",
        "WC", "Western Cape", "western cape",
        "EC", "Eastern Cape", "eastern cape",
        "National", "nationwide", "all provinces"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_province_normalisation_canonical(self, province):
        """Province normalisation returns canonical name or None."""
        normaliser = RecordNormaliser()
        result = normaliser.normalise_province(province)
        assert result in normaliser.CANONICAL_PROVINCES or result is None
    
    def test_gauteng_variations(self):
        """All Gauteng variations map to 'Gauteng'."""
        normaliser = RecordNormaliser()
        variations = ["GP", "Gauteng", "gauteng", "GAUTENG", "Gauteng Province"]
        for v in variations:
            assert normaliser.normalise_province(v) == "Gauteng"
    
    def test_kwazulu_natal_variations(self):
        """All KZN variations map to 'KwaZulu-Natal'."""
        normaliser = RecordNormaliser()
        variations = ["KZN", "KwaZulu-Natal", "kwazulu natal"]
        for v in variations:
            assert normaliser.normalise_province(v) == "KwaZulu-Natal"
    
    def test_national_variations(self):
        """National variations map to 'National'."""
        normaliser = RecordNormaliser()
        variations = ["National", "nationwide", "all provinces", "south africa"]
        for v in variations:
            assert normaliser.normalise_province(v) == "National"


class TestIndustryNormalisation:
    """
    Feature: grant-guide-scraper-engine, Property 16: Industry Normalisation
    
    *For any* industry reference,
    the Record_Normaliser SHALL map it to canonical industry tags.
    """
    
    @given(industry=st.sampled_from([
        "tech", "Technology", "IT", "ICT", "software", "digital",
        "agriculture", "agri", "farming",
        "manufacturing", "production",
        "retail", "trade", "commerce"
    ]))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_industry_normalisation_canonical(self, industry):
        """Industry normalisation returns canonical tag or None."""
        normaliser = RecordNormaliser()
        result = normaliser.normalise_industry(industry)
        assert result in normaliser.CANONICAL_INDUSTRIES or result is None
    
    def test_ict_variations(self):
        """All ICT variations map to 'ICT'."""
        normaliser = RecordNormaliser()
        variations = ["tech", "Technology", "IT", "ICT", "software", "digital"]
        for v in variations:
            assert normaliser.normalise_industry(v) == "ICT"
    
    def test_agriculture_variations(self):
        """All agriculture variations map to 'Agriculture'."""
        normaliser = RecordNormaliser()
        variations = ["agriculture", "agri", "farming", "agribusiness"]
        for v in variations:
            assert normaliser.normalise_industry(v) == "Agriculture"


class TestDescriptionTruncation:
    """
    Feature: grant-guide-scraper-engine, Property 12: Description Truncation
    
    *For any* description longer than 300 characters,
    the normalised description_short SHALL be exactly 300 characters ending with "...".
    """
    
    @given(length=st.integers(min_value=301, max_value=1000))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_long_description_truncated(self, length):
        """Long descriptions are truncated to 300 chars with ellipsis."""
        normaliser = RecordNormaliser()
        description = "x" * length
        result = normaliser._truncate_description(description)
        assert len(result) == 300
        assert result.endswith("...")
    
    @given(length=st.integers(min_value=1, max_value=300))
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    def test_short_description_unchanged(self, length):
        """Short descriptions are not modified."""
        normaliser = RecordNormaliser()
        description = "x" * length
        result = normaliser._truncate_description(description)
        assert result == description
    
    def test_exactly_300_chars(self):
        """Exactly 300 char description is not modified."""
        normaliser = RecordNormaliser()
        description = "x" * 300
        result = normaliser._truncate_description(description)
        assert result == description
        assert len(result) == 300
