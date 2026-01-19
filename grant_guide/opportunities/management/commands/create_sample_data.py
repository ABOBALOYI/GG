        else:
                self.stdout.write(f'Already exists: {opp.funding_name}')

        self.stdout.write(self.style.SUCCESS(f'Created {created_count} sample opportunities'))
        self.stdout.write(self.style.SUCCESS('Admin login: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('Visit http://127.0.0.1:8000/admin/'))
 today,
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
    ],
                'provinces': ['national'],
                'bbbee_requirement': 'unknown',
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
                    'last_verified':lication window',
                    'Complete assessment questionnaire',
                    'Shortlisting and interviews',
                    'Selection bootcamp',
                    'Final selection and onboarding'
                ],
                'apply_link': 'https://www.sabfoundation.co.za/tholoana/',
                'source_link': 'https://www.sabfoundation.co.za',
                'target_groups': ['township', 'rural'],
                'industries': ['retail-trade', 'food-beverage', 'manufacturing'   ],
                'funding_amount': 'R50,000 - R1.5 million',
                'deadline': today + timedelta(days=15),
                'is_rolling': False,
                'required_documents': [
                    'ID copy',
                    'Business registration',
                    'Bank statements (6 months)',
                    'Proof of business address',
                    'Application form'
                ],
                'application_steps': [
                    'Apply online during appion': 'Comprehensive support programme for township and rural entrepreneurs including funding, mentorship, and business development.',
                'business_stage': 'startup',
                'eligibility_requirements': [
                    'Township or rural based business',
                    'South African citizen',
                    'Business operational for 1-3 years',
                    'Annual turnover R50,000 - R5 million',
                    'Commitment to programme requirements'
             ps://www.elsenburg.com/services-support/farmer-support/',
                'source_link': 'https://www.elsenburg.com',
                'target_groups': ['rural'],
                'industries': ['agriculture'],
                'provinces': ['western-cape'],
                'bbbee_requirement': 'no',
            },
            {
                'funding_name': 'SAB Foundation Tholoana Enterprise Programme',
                'funder': 'SAB Foundation',
                'funding_type': 'grant',
                'descriptf land ownership/lease',
                    'Water use license',
                    'Farm business plan',
                    'Quotations for equipment'
                ],
                'application_steps': [
                    'Contact local extension officer',
                    'Complete application with assistance',
                    'Submit to district office',
                    'Farm inspection',
                    'Approval and disbursement'
                ],
                'apply_link': 'htt 'Previously disadvantaged individual',
                    'Valid water rights',
                    'Land ownership or long-term lease'
                ],
                'funding_amount': 'R20,000 - R250,000',
                'deadline': today + timedelta(days=60),
                'is_rolling': False,
                'required_documents': [
                    'ID document',
                    'Proof o': 'yes',
            },
            {
                'funding_name': 'Western Cape Agriculture Support Grant',
                'funder': 'Western Cape Department of Agriculture',
                'funding_type': 'grant',
                'description': 'Support for emerging farmers in the Western Cape. Covers equipment, infrastructure, and training costs.',
                'business_stage': 'any',
                'eligibility_requirements': [
                    'Western Cape based farm',
                    screening (2 weeks)',
                    'Detailed due diligence',
                    'Site visit and technical assessment',
                    'Board approval process'
                ],
                'apply_link': 'https://www.idc.co.za/green-industries/',
                'source_link': 'https://www.idc.co.za',
                'target_groups': ['innovators'],
                'industries': ['energy-renewables', 'manufacturing'],
                'provinces': ['national'],
                'bbbee_requirementon - R100 million',
                'deadline': None,
                'is_rolling': True,
                'required_documents': [
                    'Detailed business plan',
                    'Environmental impact assessment',
                    'Financial model and projections',
                    '3 years audited financials',
                    'Technical feasibility study'
                ],
                'application_steps': [
                    'Submit online application',
                    'Initial waste management, and sustainable manufacturing. Offers loans and equity investments.',
                'business_stage': 'established',
                'eligibility_requirements': [
                    'Registered South African company',
                    'Green/sustainable business focus',
                    'Minimum R5 million project value',
                    'Proven management team',
                    'Environmental impact assessment'
                ],
                'funding_amount': 'R5 millittps://www.gep.co.za',
                'target_groups': ['youth'],
                'industries': ['retail-trade', 'food-beverage', 'creative-industries'],
                'provinces': ['gauteng'],
                'bbbee_requirement': 'unknown',
            },
            {
                'funding_name': 'IDC Green Industries Fund',
                'funder': 'Industrial Development Corporation (IDC)',
                'funding_type': 'mixed',
                'description': 'Funding for businesses in renewable energy,              'Business plan',
                    'Quotations for equipment/stock'
                ],
                'application_steps': [
                    'Attend GEP information session',
                    'Complete application form',
                    'Submit at nearest GEP office',
                    'Attend panel interview',
                    'Receive outcome within 30 days'
                ],
                'apply_link': 'https://www.gep.co.za/youth-fund/',
                'source_link': 'h resident',
                    'South African citizen',
                    'Business registered in Gauteng',
                    'Not employed full-time elsewhere'
                ],
                'funding_amount': 'R10,000 - R100,000',
                'deadline': today + timedelta(days=20),
                'is_rolling': False,
                'required_documents': [
                    'Certified ID copy',
                    'Proof of Gauteng residence',
                    'Business registration',
      up',
                'eligibility_requirements': [
                    'Age 18-35 years',
                    'Gautengl-services'],
                'provinces': ['national'],
                'bbbee_requirement': 'yes',
            },
            {
                'funding_name': 'Gauteng Enterprise Propeller Youth Fund',
                'funder': 'Gauteng Enterprise Propeller (GEP)',
                'funding_type': 'grant',
                'description': 'Grant funding for youth entrepreneurs in Gauteng province. Supports business development, equipment purchase, and working capital.',
                'business_stage': 'startco.za/products/women-empowerment-fund/',
                'source_link': 'https://www.nefcorp.co.za',
                'target_groups': ['women'],
                'industries': ['retail-trade', 'manufacturing', 'professiona                    'Business plan with projections',
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
                'apply_link': 'https://www.nefcorp.y_requirements': [
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
ufacturing'],
                'provinces': ['national'],
                'bbbee_requirement': 'yes',
            },
            {
                'funding_name': 'NEF Women Empowerment Fund',
                'funder': 'National Empowerment Fund (NEF)',
                'funding_type': 'loan',
                'description': 'Financing for women-owned businesses across all sectors. Offers competitive interest rates and flexible repayment terms.',
                'business_stage': 'sme',
                'eligibilit': [
                    'Register on SEDA portal',
                    'Complete online application form',
                    'Upload required documents',
                    'Attend assessment interview',
                    'Receive funding decision within 60 days'
                ],
                'apply_link': 'https://www.seda.org.za/programmes',
                'source_link': 'https://www.seda.org.za',
                'target_groups': ['innovators'],
                'industries': ['technology-ict', 'manow R10 million'
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
                'application_steps                  'South African registered business',
                    'Less than 5 years in operation',
                    'Technology or innovation focus',
                    'Annual turnover belample opportunities
        opportunities_data = [
            {
                'funding_name': 'SEDA Technology Programme',
                'funder': 'Small Enterprise Development Agency (SEDA)',
                'funding_type': 'grant',
                'description': 'Support for technology-based small businesses to develop innovative products and services. Provides funding for R&D, prototyping, and market testing.',
                'business_stage': 'startup',
                'eligibility_requirements': [
  ts.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@grantguide.co.za', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))
        else:
            self.stdout.write('Superuser already exists')

        # Get industries and provinces
        industries = {i.slug: i for i in Industry.objects.all()}
        provinces = {p.slug: p for p in Province.objects.all()}
        
        today = date.today()
        
        # S.auth.models import User
from datetime import date, timedelta
from opportunities.models import FundingOpportunity, Industry, Province


class Command(BaseCommand):
    help = 'Create sample funding opportunities and admin user'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objec"""
Management command to create sample funding opportunities for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib