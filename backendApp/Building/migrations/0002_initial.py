# Generated by Django 4.2 on 2024-11-21 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Building', '0001_initial'),
        ('Faculty', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to='Faculty.faculty'),
        ),
    ]