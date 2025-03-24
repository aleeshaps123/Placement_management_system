# Generated by Django 5.1.3 on 2025-02-03 07:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recApp', '0013_delete_notification_student_academic_year_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='is_placed',
        ),
        migrations.AlterField(
            model_name='student',
            name='academic_year',
            field=models.CharField(default='2023-25', max_length=7, validators=[django.core.validators.RegexValidator(message="Academic year must be in the format 'YYYY-YY'.", regex='^\\d{4}-\\d{2}$')]),
        ),
    ]
