# Generated by Django 4.2.10 on 2024-02-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incoming',
            options={},
        ),
        migrations.AlterModelOptions(
            name='outgoing',
            options={},
        ),
        migrations.AddIndex(
            model_name='incoming',
            index=models.Index(fields=['warehouse', 'from_warehouse'], name='depo_incomi_warehou_6fe2e3_idx'),
        ),
        migrations.AddIndex(
            model_name='outgoing',
            index=models.Index(fields=['code'], name='depo_outgoi_code_98c757_idx'),
        ),
        migrations.AddIndex(
            model_name='stock',
            index=models.Index(fields=['material'], name='depo_stock_materia_8a9e23_idx'),
        ),
    ]