# Generated by Django 4.2.10 on 2024-02-19 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatmessage_receivers_alter_chatmessage_room_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessage',
            name='receivers',
        ),
    ]
