# Generated by Django 4.2.17 on 2024-12-27 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rota', '0011_rota_sickness_or_absence_type_alter_rota_shift_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='email',
            field=models.EmailField(default='temp@example.com', max_length=255, unique=True),
        ),
    ]
