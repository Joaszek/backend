# Generated by Django 5.1.3 on 2024-11-28 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0006_remove_booking_room_id_booking_room_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
