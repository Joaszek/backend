# Generated by Django 5.1.3 on 2024-11-29 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomToRent', '0004_remove_roomtorent_room_to_rent_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtorent',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
