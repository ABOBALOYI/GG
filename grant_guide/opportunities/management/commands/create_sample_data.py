"""
Management command to create sample funding opportunities for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from opportunities.models import FundingOpportunity, Industry, Province


class Command(BaseCommand):
    help = 'Create sample funding opportunities and admin user'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@grantguide.co.za', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))
        else:
            self.stdout.write('Superuser already exists')

        # Get industries and provinces
        industries = {i.slug: i for i in Industry.objects.all()}
        provinces = {p.slug: p for p in Province.objects.all()}
        
        today = date.today()
        
        # Sample opportunities
        opportunities_data = [
            {
                'funding_name': 'SEDA Technology Programme',
                'funder': 'Small Enterprise Development Agency (SEDA)',
                'funding_type': 'grant',
                'description': 'Support for technology-based small businesses to develop innovative products and services.',
                'business_stage': 'startup',
                'eligibility_requirements': [
                    'South African registered business',
                    'Less than 5 years in operation',
                    'Technology or innovation focus',
                    'Annual turnover below R10 million'
                ],
                'funding_amount': 'R50,000 - R500,000',
                'deadline': today + timedelta(days=45),
                'is_rolling': False,
                'required_documents': [
                    'Company registration documents (CIPC)',
                    'Tax clearance certificate',
                    'Business plan',
                    'Financial statements',
                    'ID copies of directors'
                ],
                'application_steps': [
                    'Register on SEDA portal',
                    'Complete online application form',
                    'Upload required documents',
                    'Attend assessment interview',
                    'Receive funding decision within 60 days'
                ],
                'apply_link': 'https://www.seda.org.za/programmes',
                'source_link': 'https://www.seda.org.za',
                'target_groups': ['innovators'],
                'industries': ['technology-ict', 'manufacturing'],
                'provinces': ['national'],
                'bbbee_requirement': 'yes',
            },
            {
                'funding_name': 'NEF Women Empowerment Fund',
                'funder': 'National Empowerment Fund (NEF)',
                'funding_type': 'loan',
                'description': 'Financing for women-owned businesses across all sectors.',
                'business_stage': 'sme',
                'eligibility_requirements': [
                    'At least 51% women ownership',
                    'South African citizen',
                    'Viable business plan',
                    'Minimum 2 years trading history'
                ],
                'funding_amount': 'R250,000 - R10 million',
                'deadline': None,
                'is_rolling': True,
                'required_documents': [
                    'Company registration documents',
                    'Audited financial statements (2 years)',
                    'Business plan with projections',
                    'Proof of women ownership',
                    'Tax compliance status'
                ],
                'application_steps': [
                    'Submit online enquiry',
                    'Receive application pack',
                    'Complete detailed application',
                    'Due diligence process',
                    'Investment committee approval'
                ],
                'apply_link': 'https://www.nefcorp.co.za/products/women-empowerment-fund/',
                'source_link': 'https://www.nefcorp.co.za',
                'target_groups': ['women'],
                'industries': ['retail-trade', 'manufacturing', 'professional-services'],
                'provinces': ['national'],
                'bbbee_requirement': 'yes',
            },
        ]

        created_count = 0
        for data in opportunities_data:
            industry_slugs = data.pop('industries')
            province_slugs = data.pop('provinces')
            
            opp, created = FundingOpportunity.objects.get_or_create(
                funding_name=data['funding_name'],
                defaults={
                    **data,
                    'last_verified': today,
                    'status': 'active'
                }
            )
            
            if created:
                for slug in industry_slugs:
                    if slug in industries:
                        opp.industries.add(industries[slug])
                for slug in province_slugs:
                    if slug in provinces:
                        opp.provinces.add(provinces[slug])
                created_count += 1
                self.stdout.write(f'Created: {opp.funding_name}')
            else:
                self.stdout.write(f'Already exists: {opp.funding_name}')

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} sample opportunities'))
        self.stdout.write(self.style.SUCCESS('Admin login: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('Visit http://127.0.0.1:8000/admin/'))
