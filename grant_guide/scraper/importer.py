"""
Django importer for importing normalised records into the database.
"""
import logging
from datetime import date
from typing import Optional

from django.db import transaction

from .models import NormalisedOpportunity, ImportResult, OpportunityStatus

logger = logging.getLogger('scraper.import')


class DjangoImporter:
    """Imports normalised records into Django database."""
    
    # Mapping from scraper status to Django model status
    STATUS_MAPPING = {
        OpportunityStatus.ACTIVE: 'active',
        OpportunityStatus.EXPIRED: 'expired',
        OpportunityStatus.DRAFT_NEEDS_REVIEW: 'draft',
    }
    
    # Mapping from scraper funding type to Django model funding type
    FUNDING_TYPE_MAPPING = {
        'Grant': 'grant',
        'Loan': 'loan',
        'Equity': 'equity',
        'Mixed': 'mixed',
        'CompetitionPrize': 'competition',
    }
    
    # Mapping from scraper business stage to Django model business stage
    BUSINESS_STAGE_MAPPING = {
        'Startup': 'startup',
        'SME': 'sme',
        'Established': 'established',
        'Any': 'any',
    }
    
    def import_record(
        self,
        record: NormalisedOpportunity,
        existing_id: Optional[int] = None
    ) -> ImportResult:
        """
        Import a single record into Django database.
        
        Args:
            record: Normalised opportunity to import.
            existing_id: ID of existing record to update (if duplicate).
            
        Returns:
            ImportResult with success status and details.
        """
        from opportunities.models import FundingOpportunity, AuditLog
        
        try:
            model_data = self.map_to_model(record)
            
            with transaction.atomic():
                if existing_id:
                    # Update existing record
                    opp = FundingOpportunity.objects.get(id=existing_id)
                    changed_fields = self._get_changed_fields(opp, model_data)
                    
                    for field, value in model_data.items():
                        if field not in ('industries', 'provinces'):
                            setattr(opp, field, value)
                    
                    opp.last_verified = date.today()
                    opp.save()
                    
                    # Update ManyToMany relationships
                    self._update_relationships(opp, record)
                    
                    # Create audit log
                    AuditLog.objects.create(
                        opportunity=opp,
                        action='updated_by_scraper',
                        changes={'fields': changed_fields}
                    )
                    
                    logger.info(f"Updated: {record.title} (ID: {existing_id})")
                    return ImportResult(
                        success=True,
                        action='updated',
                        record_id=existing_id
                    )
                else:
                    # Create new record
                    opp = FundingOpportunity.objects.create(**model_data)
                    
                    # Set ManyToMany relationships
                    self._update_relationships(opp, record)
                    
                    # Create audit log
                    AuditLog.objects.create(
                        opportunity=opp,
                        action='created_by_scraper',
                        changes={'source': record.source_name}
                    )
                    
                    logger.info(f"Created: {record.title} (ID: {opp.id})")
                    return ImportResult(
                        success=True,
                        action='created',
                        record_id=opp.id
                    )
                    
        except Exception as e:
            logger.error(f"Failed to import '{record.title}': {e}")
            return ImportResult(
                success=False,
                action='skipped',
                error=str(e)
            )
    
    def import_batch(self, records: list[NormalisedOpportunity]) -> list[ImportResult]:
        """
        Import multiple records.
        
        Args:
            records: List of normalised opportunities to import.
            
        Returns:
            List of ImportResult for each record.
        """
        results = []
        for record in records:
            result = self.import_record(record)
            results.append(result)
        return results
    
    def map_to_model(self, record: NormalisedOpportunity) -> dict:
        """
        Map normalised record to FundingOpportunity model fields.
        
        Args:
            record: Normalised opportunity record.
            
        Returns:
            Dictionary of model field values.
        """
        # Format funding amount as range string
        funding_amount = self._format_funding_amount(
            record.funding_amount_min,
            record.funding_amount_max
        )
        
        return {
            'funding_name': record.title,
            'funder': record.funder_name,
            'funding_type': self.FUNDING_TYPE_MAPPING.get(
                record.funding_type.value if record.funding_type else 'Grant',
                'grant'
            ),
            'description': record.description_short,
            'business_stage': self.BUSINESS_STAGE_MAPPING.get(
                record.business_stage.value if record.business_stage else 'Any',
                'any'
            ),
            'eligibility_requirements': record.eligibility_bullets,
            'funding_amount': funding_amount,
            'deadline': record.deadline_date,
            'is_rolling': record.is_rolling,
            'required_documents': record.required_documents_bullets,
            'application_steps': record.application_steps,
            'apply_link': record.official_apply_url,
            'source_link': record.source_url,
            'last_verified': record.last_verified_date,
            'status': self.STATUS_MAPPING.get(record.status, 'draft'),
            'notes': f"Imported from {record.source_name}. " + 
                     (f"Issues: {', '.join(record.validation_issues)}" if record.validation_issues else ""),
        }
    
    def _update_relationships(
        self,
        opp,
        record: NormalisedOpportunity
    ) -> None:
        """Update ManyToMany relationships for industries and provinces."""
        # Update industries
        industries = self.get_or_create_industries(record.industry_tags)
        opp.industries.set(industries)
        
        # Update provinces
        provinces = self.get_provinces(record.province_tags)
        opp.provinces.set(provinces)
    
    def get_or_create_industries(self, tags: list[str]) -> list:
        """
        Get or create Industry records for tags.
        
        Args:
            tags: List of industry tag names.
            
        Returns:
            List of Industry model instances.
        """
        from opportunities.models import Industry
        from django.utils.text import slugify
        
        industries = []
        for tag in tags:
            industry, _ = Industry.objects.get_or_create(
                name=tag,
                defaults={'slug': slugify(tag)}
            )
            industries.append(industry)
        return industries
    
    def get_provinces(self, tags: list[str]) -> list:
        """
        Get Province records for tags.
        
        Args:
            tags: List of province names.
            
        Returns:
            List of Province model instances.
        """
        from opportunities.models import Province
        
        provinces = []
        for tag in tags:
            try:
                # Try exact match first
                province = Province.objects.get(name=tag)
                provinces.append(province)
            except Province.DoesNotExist:
                # Try case-insensitive match
                try:
                    province = Province.objects.get(name__iexact=tag)
                    provinces.append(province)
                except Province.DoesNotExist:
                    logger.warning(f"Province not found: {tag}")
        
        return provinces
    
    def _format_funding_amount(self, min_amount, max_amount) -> str:
        """Format funding amount as range string."""
        if min_amount is None and max_amount is None:
            return ""
        
        def format_amount(amount):
            if amount is None:
                return ""
            amount = int(amount)
            if amount >= 1_000_000:
                return f"R{amount / 1_000_000:.1f} million"
            elif amount >= 1_000:
                return f"R{amount:,}"
            return f"R{amount}"
        
        if min_amount and max_amount:
            return f"{format_amount(min_amount)} - {format_amount(max_amount)}"
        elif min_amount:
            return f"From {format_amount(min_amount)}"
        else:
            return f"Up to {format_amount(max_amount)}"
    
    def _get_changed_fields(self, existing, new_data: dict) -> list[str]:
        """Get list of fields that changed."""
        changed = []
        for field, new_value in new_data.items():
            if field in ('industries', 'provinces'):
                continue
            old_value = getattr(existing, field, None)
            if old_value != new_value:
                changed.append(field)
        return changed
