# Generated by Django 4.2.6 on 2024-11-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Faculty', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
