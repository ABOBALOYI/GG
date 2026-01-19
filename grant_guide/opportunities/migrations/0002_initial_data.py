# Data migration for initial provinces and industries
from django.db import migrations
from django.utils.text import slugify


def create_initial_data(apps, schema_editor):
    Province = apps.get_model('opportunities', 'Province')
    Industry = apps.get_model('opportunities', 'Industry')
    
    # South African Provinces
    provinces = [
        ('Eastern Cape', False),
        ('Free State', False),
        ('Gauteng', False),
        ('KwaZulu-Natal', False),
        ('Limpopo', False),
        ('Mpumalanga', False),
        ('Northern Cape', False),
        ('North West', False),
        ('Western Cape', False),
        ('National', True),  # is_national=True
    ]
    
    for name, is_national in provinces:
        Province.objects.get_or_create(
            name=name,
            defaults={'slug': slugify(name), 'is_national': is_national}
        )
    
    # Industries
    industries = [
        'Agriculture',
        'Manufacturing',
        'Technology/ICT',
        'Tourism & Hospitality',
        'Retail & Trade',
        'Construction',
        'Mining',
        'Healthcare',
        'Education',
        'Creative Industries',
        'Transport & Logistics',
        'Financial Services',
        'Energy & Renewables',
        'Food & Beverage',
        'Professional Services',
    ]
    
    for name in industries:
        Industry.objects.get_or_create(
            name=name,
            defaults={'slug': slugify(name)}
        )


def reverse_initial_data(apps, schema_editor):
    Province = apps.get_model('opportunities', 'Province')
    Industry = apps.get_model('opportunities', 'Industry')
    Province.objects.all().delete()
    Industry.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('opportunities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data, reverse_initial_data),
    ]
