# Generated by Django 5.1.3 on 2024-11-28 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Item', '0006_alter_item_item_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='id',
        ),
        migrations.AlterField(
            model_name='item',
            name='item_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
