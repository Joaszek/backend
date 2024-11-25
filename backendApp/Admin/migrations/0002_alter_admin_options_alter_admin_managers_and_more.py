# Generated by Django 4.2.6 on 2024-11-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='admin',
            options={},
        ),
        migrations.AlterModelManagers(
            name='admin',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='admin',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='admin',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='admin',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='admin',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='first_name',
            field=models.CharField(blank=True, default='Adam', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='admin',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='admin',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='admin',
            name='last_name',
            field=models.CharField(blank=True, default='Kowalski', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='admin',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
