# Generated by Django 5.1.3 on 2024-11-27 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0005_item_item_id_alter_item_room_with_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_id',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]