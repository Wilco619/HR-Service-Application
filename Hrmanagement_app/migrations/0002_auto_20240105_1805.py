# Generated by Django 3.0.7 on 2024-01-05 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hrmanagement_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancereport',
            old_name='department_id',
            new_name='staff_id',
        ),
    ]
