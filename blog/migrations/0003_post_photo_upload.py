# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20171124_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo_upload',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
