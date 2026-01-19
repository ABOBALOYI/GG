"""
Compliance checker for validating scraped records against trust and safety rules.
"""
import re
from typing import Optional
from urllib.parse import urlparse

from .models import NormalisedOpportunity, ComplianceResult


class ComplianceChecker:
    """Validates records against trust and safety rules."""
    
    # Payment-related keywords that indicate pay-to-apply schemes
    PAYMENT_KEYWORDS = [
        'application fee', 'pay to apply', 'registration fee',
        'payment required', 'processing fee', 'admin fee',
        'fee payable', 'non-refundable fee', 'deposit required',
        'pay before', 'payment of r', 'fee of r'
    ]
    
    # Social media domains that are not acceptable as sole contact
    SOCIAL_MEDIA_DOMAINS = [
        'whatsapp.com', 'wa.me', 'chat.whatsapp.com',
        'telegram.org', 't.me', 'telegram.me',
        'facebook.com', 'fb.com', 'fb.me',
        'twitter.com', 'x.com',
        'instagram.com',
        'tiktok.com',
    ]
    
    # Patterns indicating access control
    ACCESS_CONTROL_PATTERNS = [
        r'<form[^>]*login',
        r'<form[^>]*signin',
        r'<input[^>]*type=["\']password["\']',
        r'please\s+log\s*in',
        r'sign\s+in\s+to\s+continue',
        r'authentication\s+required',
        r'captcha',
        r'recaptcha',
        r'hcaptcha',
        r'verify\s+you\s+are\s+human',
        r'paywall',
        r'subscribe\s+to\s+(read|view|access)',
        r'premium\s+content',
        r'members\s+only',
    ]
    
    def check(self, record: NormalisedOpportunity) -> ComplianceResult:
        """
        Run all compliance checks on a record.
        
        Args:
            record: Normalised opportunity record to validate.
            
        Returns:
            ComplianceResult with compliance status and any issues found.
        """
        issues = []
        rejection_reason = None
        
        # Check required fields
        field_issues = self.check_required_fields(record)
        issues.extend(field_issues)
        
        # Check for payment-to-apply
        payment_issues = self.check_no_payment_required(record)
        if payment_issues:
            issues.extend(payment_issues)
            rejection_reason = "Payment required to apply"
        
        # Check for social-media-only
        social_issues = self.check_no_social_media_only(record)
        if social_issues:
            issues.extend(social_issues)
            if not rejection_reason:
                rejection_reason = "Social media only contact"
        
        # Check URL validity
        url_issues = self.check_url_validity(record)
        issues.extend(url_issues)
        
        is_compliant = len(issues) == 0 or (
            len(issues) > 0 and rejection_reason is None
        )
        
        return ComplianceResult(
            is_compliant=is_compliant,
            issues=issues,
            rejection_reason=rejection_reason
        )
    
    def check_required_fields(self, record: NormalisedOpportunity) -> list[str]:
        """
        Check all required fields are present.
        
        Returns list of missing field names.
        """
        issues = []
        
        if not record.title:
            issues.append("Missing required field: title")
        if not record.funder_name:
            issues.append("Missing required field: funder_name")
        if not record.funding_type:
            issues.append("Missing required field: funding_type")
        if not record.official_apply_url:
            issues.append("Missing required field: official_apply_url")
        if not record.source_url:
            issues.append("Missing required field: source_url")
        
        return issues
    
    def check_no_payment_required(self, record: NormalisedOpportunity) -> list[str]:
        """
        Check for payment-to-apply indicators.
        
        Returns list of issues if payment indicators found.
        """
        issues = []
        
        # Check description
        if record.description_short:
            text = record.description_short.lower()
            for keyword in self.PAYMENT_KEYWORDS:
                if keyword in text:
                    issues.append(f"Payment indicator found in description: '{keyword}'")
                    break
        
        # Check eligibility bullets
        for bullet in record.eligibility_bullets:
            text = bullet.lower()
            for keyword in self.PAYMENT_KEYWORDS:
                if keyword in text:
                    issues.append(f"Payment indicator found in eligibility: '{keyword}'")
                    break
        
        # Check application steps
        for step in record.application_steps:
            text = step.lower()
            for keyword in self.PAYMENT_KEYWORDS:
                if keyword in text:
                    issues.append(f"Payment indicator found in application steps: '{keyword}'")
                    break
        
        return issues
    
    def check_no_social_media_only(self, record: NormalisedOpportunity) -> list[str]:
        """
        Check for social-media-only sources.
        
        Returns list of issues if only social media contact found.
        """
        issues = []
        
        # Check apply URL
        if record.official_apply_url:
            parsed = urlparse(record.official_apply_url)
            domain = parsed.netloc.lower()
            
            for social_domain in self.SOCIAL_MEDIA_DOMAINS:
                if social_domain in domain:
                    issues.append(f"Apply URL is social media only: {domain}")
                    break
        
        # Check source URL
        if record.source_url:
            parsed = urlparse(record.source_url)
            domain = parsed.netloc.lower()
            
            for social_domain in self.SOCIAL_MEDIA_DOMAINS:
                if social_domain in domain:
                    issues.append(f"Source URL is social media only: {domain}")
                    break
        
        return issues
    
    def check_url_validity(self, record: NormalisedOpportunity) -> list[str]:
        """
        Validate URLs are well-formed.
        
        Returns list of URL validation issues.
        """
        issues = []
        
        if record.official_apply_url:
            if not self._is_valid_url(record.official_apply_url):
                issues.append(f"Invalid apply URL format: {record.official_apply_url}")
        
        if record.source_url:
            if not self._is_valid_url(record.source_url):
                issues.append(f"Invalid source URL format: {record.source_url}")
        
        return issues
    
    def detect_access_control(self, html_content: str) -> bool:
        """
        Detect if HTML content contains access control indicators.
        
        Args:
            html_content: Raw HTML content to check.
            
        Returns:
            True if access control detected, False otherwise.
        """
        if not html_content:
            return False
        
        content_lower = html_content.lower()
        
        for pattern in self.ACCESS_CONTROL_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is well-formed."""
        try:
            result = urlparse(url)
            return all([result.scheme in ('http', 'https'), result.netloc])
        except Exception:
            return False
