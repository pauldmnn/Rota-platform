# Generated by Django 4.2.17 on 2024-12-15 13:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rota', '0002_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rota',
            name='day',
        ),
        migrations.AddField(
            model_name='rota',
            name='date',
            field=models.DateField(default=datetime.date(2024, 1, 1)),
        ),
        migrations.AlterField(
            model_name='request',
            name='requested_day',
            field=models.DateField(),
        ),
    ]
