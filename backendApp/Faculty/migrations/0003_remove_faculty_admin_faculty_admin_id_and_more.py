# Generated by Django 5.1.3 on 2024-11-27 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Faculty', '0002_alter_faculty_id_alter_faculty_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faculty',
            name='admin',
        ),
        migrations.AddField(
            model_name='faculty',
            name='admin_id',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='faculty',
            name='faculty_id',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
