# Generated by Django 4.2.6 on 2023-11-28 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('depo', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='material_party',
        ),
    ]
