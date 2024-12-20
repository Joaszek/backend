# Generated by Django 5.1.3 on 2024-11-27 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0003_alter_item_room_with_items_alter_item_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='building',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='item',
            name='end_date',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='item',
            name='faculty',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='item',
            name='start_date',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
