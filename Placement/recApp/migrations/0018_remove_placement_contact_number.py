# Generated by Django 5.1.3 on 2025-02-13 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recApp', '0017_remove_company_pincode_remove_company_street_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placement',
            name='contact_number',
        ),
    ]
