# Generated by Django 4.2.6 on 2023-11-21 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('depo', '0008_rename_type_outgoing_outgoing_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incoming',
            name='data',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='incomingmaterial',
            name='amount',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='outgoingmaterial',
            name='amount',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
    ]
