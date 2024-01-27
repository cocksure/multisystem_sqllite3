# Generated by Django 4.2.6 on 2024-01-26 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hr', '0002_initial'),
        ('purchase', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseproduct',
            name='assigned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_purchaseproducts_per_material', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchaseproduct',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='executor_purchaseproducts', to='hr.employee'),
        ),
        migrations.AddField(
            model_name='purchaseproduct',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material'),
        ),
        migrations.AddField(
            model_name='purchaseproduct',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='purchase.purchase'),
        ),
        migrations.AddField(
            model_name='purchaseproduct',
            name='rejected_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rejected_purchaseproducts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchaseproduct',
            name='signed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='signed_purchaseproducts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchaseproduct',
            name='specification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='info.specification'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchase',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.department'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='requester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hr.employee'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchase',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.warehouse'),
        ),
    ]