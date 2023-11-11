# Generated by Django 4.2.6 on 2023-11-08 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('info', '0001_initial'),
        ('depo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material'),
        ),
        migrations.AddField(
            model_name='stock',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.warehouse'),
        ),
        migrations.AddField(
            model_name='outgoingmaterial',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.material'),
        ),
        migrations.AddField(
            model_name='outgoingmaterial',
            name='material_party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.materialparty'),
        ),
        migrations.AddField(
            model_name='outgoingmaterial',
            name='outgoing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depo.outgoing'),
        ),
    ]
