# Generated by Django 5.1.3 on 2024-11-29 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItemBooking', '0005_itembooking_returned'),
    ]

    operations = [
        migrations.AddField(
            model_name='itembooking',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
