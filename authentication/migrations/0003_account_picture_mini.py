# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 18:52
from __future__ import unicode_literals

import authentication.utilmodels
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20170523_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='picture_mini',
            field=authentication.utilmodels.MyImageField(blank=True, upload_to=b''),
        ),
    ]
