# Generated by Django 5.1.3 on 2024-11-28 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomWithItems', '0003_alter_roomwithitems_building'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomwithitems',
            name='faculty',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
