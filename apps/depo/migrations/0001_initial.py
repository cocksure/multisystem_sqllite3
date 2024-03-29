# Generated by Django 4.2.6 on 2024-01-26 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0002_initial'),
        ('purchase', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('data', models.DateField()),
                ('invoice', models.CharField(blank=True, max_length=150, null=True)),
                ('contract_number', models.CharField(blank=True, max_length=150, null=True)),
                ('note', models.CharField(blank=True, max_length=250, null=True)),
                ('incoming_type', models.CharField(blank=True, choices=[('Перемешения', 'Перемешения'), ('По накладной', 'По накладной')], null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('from_warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incoming_from_warehouse', to='info.warehouse')),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Outgoing',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(editable=False, max_length=10, unique=True)),
                ('data', models.DateField()),
                ('outgoing_type', models.CharField(choices=[('расход', 'Расход'), ('продажа', 'Продажа'), ('перемешения', 'Перемещение')], default='перемешения', max_length=20)),
                ('status', models.CharField(blank=True, choices=[('Принят', 'Принят'), ('Отклонен', 'Отклонен'), ('В ожидании', 'В ожидании')], default='В ожидании', max_length=20, null=True)),
                ('note', models.CharField(blank=True, max_length=250, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('to_warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_to_warehouse', to='info.warehouse')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_warehouse', to='info.warehouse')),
            ],
            options={
                'ordering': ['-created_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='OutgoingMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('color', models.CharField(blank=True, max_length=150, null=True)),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material')),
                ('material_party', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='info.materialparty')),
                ('outgoing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_materials', to='depo.outgoing')),
            ],
        ),
        migrations.CreateModel(
            name='IncomingMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('color', models.CharField(blank=True, max_length=150, null=True)),
                ('comment', models.TextField(blank=True, max_length=1000, null=True)),
                ('incoming', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depo.incoming')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material')),
                ('material_party', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info.materialparty')),
                ('purchase_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.purchaseproduct')),
            ],
        ),
        migrations.AddField(
            model_name='incoming',
            name='outgoing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='depo.outgoing'),
        ),
        migrations.AddField(
            model_name='incoming',
            name='purchase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchase.purchase'),
        ),
        migrations.AddField(
            model_name='incoming',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='incoming',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incoming_warehouse', to='info.warehouse'),
        ),
    ]
