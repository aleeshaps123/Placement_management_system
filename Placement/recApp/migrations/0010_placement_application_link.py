# Generated by Django 5.1.3 on 2025-01-10 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recApp', '0009_alter_placement_date_of_drive'),
    ]

    operations = [
        migrations.AddField(
            model_name='placement',
            name='application_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
