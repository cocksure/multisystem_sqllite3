# Generated by Django 4.2.10 on 2024-02-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={},
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['full_name'], name='hr_employee_full_na_bb6b90_idx'),
        ),
    ]
