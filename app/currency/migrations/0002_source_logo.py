# Generated by Django 4.2.7 on 2024-01-04 16:03

import currency.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='logo',
            field=models.FileField(blank=True, default=None, null=True, upload_to=currency.models.source_directory_path, verbose_name='Logo'),
        ),
    ]
