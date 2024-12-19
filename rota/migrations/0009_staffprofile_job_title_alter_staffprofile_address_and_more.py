# Generated by Django 4.2.17 on 2024-12-19 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rota', '0008_staffprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='job_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='staffprofile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
