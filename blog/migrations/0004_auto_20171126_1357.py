# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-26 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_photo_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo_upload',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
