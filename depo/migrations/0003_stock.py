# Generated by Django 4.2.6 on 2023-10-19 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_alter_device_imei'),
        ('depo', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('color', models.CharField(blank=True, max_length=150, null=True)),
                ('material_party', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material')),
            ],
            options={
                'unique_together': {('material', 'color', 'material_party')},
            },
        ),
    ]