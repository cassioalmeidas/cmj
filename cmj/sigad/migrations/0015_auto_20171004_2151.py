# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-05 00:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sigad', '0014_auto_20171004_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classe',
            name='short_url',
        ),
        migrations.RemoveField(
            model_name='documento',
            name='short_url',
        ),
    ]
