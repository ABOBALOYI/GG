"""
Models for the opportunities app.

This module contains the FundingOpportunity, Industry, Province, and AuditLog models.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta


# Choices
FUNDING_TYPE_CHOICES = [
    ('grant', 'Grant'),
    ('loan', 'Loan'),
    ('equity', 'Equity'),
    ('mixed', 'Mixed'),
    ('competition', 'Competition Prize'),
]

BUSINESS_STAGE_CHOICES = [
    ('startup', 'Startup'),
    ('sme', 'SME'),
    ('established', 'Established'),
    ('any', 'Any'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('expired', 'Expired'),
    ('draft', 'Draft'),
    ('needs_review', 'Needs Review'),
]

BBBEE_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
    ('unknown', 'Unknown'),
]

TARGET_GROUP_CHOICES = [
    ('women', 'Women'),
    ('youth', 'Youth'),
    ('township', 'Township'),
    ('rural', 'Rural'),
    ('exporters', 'Exporters'),
    ('innovators', 'Innovators'),
]


class Industry(models.Model):
    """
    Industry model representing business sectors that funding opportunities support.
    
    Examples: Agriculture, Manufacturing, Technology/ICT, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Industries"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Province(models.Model):
    """
    Province model representing South African provinces.
    
    Includes a special "National" option for opportunities available nationwide.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    is_national = models.BooleanField(default=False)  # For "National" option

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FundingOpportunity(models.Model):
    """
    Main model for funding opportunities.
    
    Stores all information about grants, loans, equity funding, competitions,
    and development finance opportunities for South African businesses.
    """
    # Required fields
    funding_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    funder = models.CharField(max_length=255)
    funding_type = models.CharField(max_length=20, choices=FUNDING_TYPE_CHOICES)
    description = models.TextField(max_length=500)  # 1-3 lines
    business_stage = models.CharField(max_length=20, choices=BUSINESS_STAGE_CHOICES)
    eligibility_requirements = models.JSONField(default=list)  # Array of strings
    funding_amount = models.CharField(max_length=100, blank=True)
    deadline = models.DateField(null=True, blank=True)  # null = Rolling
    is_rolling = models.BooleanField(default=False)
    required_documents = models.JSONField(default=list)  # Array of strings
    application_steps = models.JSONField(default=list)  # Array of numbered steps
    apply_link = models.URLField()
    source_link = models.URLField()
    last_verified = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    
    # Optional fields
    bbbee_requirement = models.CharField(max_length=10, choices=BBBEE_CHOICES, blank=True)
    target_groups = models.JSONField(default=list, blank=True)
    processing_time = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    
    # Relationships
    industries = models.ManyToManyField('Industry', related_name='opportunities')
    provinces = models.ManyToManyField('Province', related_name='opportunities')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)  # Admin notes, e.g., "Needs verification"
    
    # Audit
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_opportunities'
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='updated_opportunities'
    )

    class Meta:
        verbose_name_plural = "Funding Opportunities"
        ordering = ['deadline', '-created_at']

    def __str__(self):
        return self.funding_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.funding_name)
            slug = base_slug
            counter = 1
            while FundingOpportunity.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def clean(self):
        """Validate the model before saving."""
        errors = {}
        
        # Active status requires all required fields
        if self.status == 'active':
            if not self.funding_name:
                errors['funding_name'] = 'Funding name is required for active opportunities.'
            if not self.funder:
                errors['funder'] = 'Funder is required for active opportunities.'
            if not self.apply_link:
                errors['apply_link'] = 'Apply link is required for active opportunities.'
            if not self.source_link:
                errors['source_link'] = 'Source link is required for active opportunities.'
            if not self.eligibility_requirements:
                errors['eligibility_requirements'] = 'Eligibility requirements are required for active opportunities.'
            if not self.required_documents:
                errors['required_documents'] = 'Required documents are required for active opportunities.'
            if not self.application_steps:
                errors['application_steps'] = 'Application steps are required for active opportunities.'
        
        if errors:
            raise ValidationError(errors)

    @property
    def is_closing_soon(self):
        """Check if deadline is within 30 days."""
        if self.is_rolling or not self.deadline:
            return False
        today = date.today()
        return today <= self.deadline <= today + timedelta(days=30)

    @property
    def is_expired(self):
        """Check if deadline has passed."""
        if self.is_rolling or not self.deadline:
            return False
        return self.deadline < date.today()

    @property
    def deadline_display(self):
        """Return formatted deadline or 'Rolling/Always Open'."""
        if self.is_rolling:
            return "Rolling / Always Open"
        if self.deadline:
            return self.deadline.strftime("%d %B %Y")
        return "Not specified"


class AuditLog(models.Model):
    """
    Audit log for tracking changes to funding opportunities.
    """
    opportunity = models.ForeignKey(
        FundingOpportunity, on_delete=models.CASCADE, related_name='audit_logs'
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20)  # created, updated, status_changed
    changes = models.JSONField(default=dict)  # What changed
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} - {self.opportunity.funding_name} at {self.timestamp}"
