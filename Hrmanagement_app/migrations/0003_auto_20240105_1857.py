# Generated by Django 3.0.7 on 2024-01-05 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hrmanagement_app', '0002_auto_20240105_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'AdminHr'), (2, 'Manager'), (3, 'Staff')], default=1, max_length=10),
        ),
    ]
