# Generated by Django 4.2.6 on 2023-11-06 13:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('arrival_date', models.DateField()),
                ('status', models.CharField(choices=[('new', 'Новая'), ('confirmed', 'Подтверждена'), ('distributed', 'Распределена'), ('rejected', 'Отклонена'), ('accepted', 'Принята'), ('delivered', 'Доставлена'), ('in_stock', 'В складе')], default='new')),
                ('note', models.TextField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('signed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('rejected_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('distributed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('accepted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('new', 'Новая'), ('confirmed', 'Подтверждена'), ('distributed', 'Распределена'), ('rejected', 'Отклонена'), ('accepted', 'Принята'), ('delivered', 'Доставлена'), ('in_stock', 'В складе')], default='new')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.purchase')),
            ],
        ),
    ]
