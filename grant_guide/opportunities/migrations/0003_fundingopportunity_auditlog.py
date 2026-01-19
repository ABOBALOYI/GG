# Migration for FundingOpportunity and AuditLog models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opportunities', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundingOpportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funding_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=280, unique=True)),
                ('funder', models.CharField(max_length=255)),
                ('funding_type', models.CharField(choices=[('grant', 'Grant'), ('loan', 'Loan'), ('equity', 'Equity'), ('mixed', 'Mixed'), ('competition', 'Competition Prize')], max_length=20)),
                ('description', models.TextField(max_length=500)),
                ('business_stage', models.CharField(choices=[('startup', 'Startup'), ('sme', 'SME'), ('established', 'Established'), ('any', 'Any')], max_length=20)),
                ('eligibility_requirements', models.JSONField(default=list)),
                ('funding_amount', models.CharField(blank=True, max_length=100)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('is_rolling', models.BooleanField(default=False)),
                ('required_documents', models.JSONField(default=list)),
                ('application_steps', models.JSONField(default=list)),
                ('apply_link', models.URLField()),
                ('source_link', models.URLField()),
                ('last_verified', models.DateField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('expired', 'Expired'), ('draft', 'Draft'), ('needs_review', 'Needs Review')], default='draft', max_length=15)),
                ('bbbee_requirement', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('unknown', 'Unknown')], max_length=10)),
                ('target_groups', models.JSONField(blank=True, default=list)),
                ('processing_time', models.CharField(blank=True, max_length=100)),
                ('contact_email', models.EmailField(blank=True, max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_opportunities', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_opportunities', to=settings.AUTH_USER_MODEL)),
                ('industries', models.ManyToManyField(related_name='opportunities', to='opportunities.industry')),
                ('provinces', models.ManyToManyField(related_name='opportunities', to='opportunities.province')),
            ],
            options={
                'verbose_name_plural': 'Funding Opportunities',
                'ordering': ['deadline', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=20)),
                ('changes', models.JSONField(default=dict)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='opportunities.fundingopportunity')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
