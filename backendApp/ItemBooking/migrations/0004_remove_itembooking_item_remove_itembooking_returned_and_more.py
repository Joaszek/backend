# Generated by Django 5.1.3 on 2024-11-27 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItemBooking', '0003_itembooking_returned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itembooking',
            name='item',
        ),
        migrations.RemoveField(
            model_name='itembooking',
            name='returned',
        ),
        migrations.RemoveField(
            model_name='itembooking',
            name='user',
        ),
        migrations.AddField(
            model_name='itembooking',
            name='item_id',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='itembooking',
            name='student_id',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='itembooking',
            name='end_date',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='itembooking',
            name='start_date',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
