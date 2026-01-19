"""
Management command to update funding opportunity statuses.

- Marks opportunities with passed deadlines as Expired
- Marks rolling opportunities not updated for 60 days as Needs Review
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from opportunities.models import FundingOpportunity
import logging

logger = logging.getLogger('opportunities')


class Command(BaseCommand):
    help = 'Update funding opportunity statuses based on deadlines and verification dates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        today = timezone.now().date()
        sixty_days_ago = today - timedelta(days=60)
        
        expired_count = 0
        needs_review_count = 0
        
        # Mark opportunities with passed deadlines as Expired
        expired_opportunities = FundingOpportunity.objects.filter(
            deadline__lt=today,
            is_rolling=False,
            status__in=['active', 'draft']
        )
        
        for opp in expired_opportunities:
            if dry_run:
                self.stdout.write(f'Would mark as expired: {opp.funding_name} (deadline: {opp.deadline})')
            else:
                opp.status = 'expired'
                opp.save(update_fields=['status', 'updated_at'])
                logger.info(f'Marked as expired: {opp.funding_name}')
            expired_count += 1
        
        # Mark rolling opportunities not updated for 60 days as Needs Review
        stale_rolling = FundingOpportunity.objects.filter(
            is_rolling=True,
            last_verified__lt=sixty_days_ago,
            status='active'
        )
        
        for opp in stale_rolling:
            if dry_run:
                self.stdout.write(f'Would mark as needs review: {opp.funding_name} (last verified: {opp.last_verified})')
            else:
                opp.status = 'needs_review'
                opp.save(update_fields=['status', 'updated_at'])
                logger.info(f'Marked as needs review: {opp.funding_name}')
            needs_review_count += 1
        
        # Summary
        action = 'Would update' if dry_run else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            f'{action} {expired_count} expired opportunities and {needs_review_count} needing review'
        ))
