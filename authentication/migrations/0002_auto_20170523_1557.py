# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 12:57
from __future__ import unicode_literals

import authentication.utilmodels
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='picture',
            field=authentication.utilmodels.MyImageField(blank=True, upload_to=b''),
        ),
    ]