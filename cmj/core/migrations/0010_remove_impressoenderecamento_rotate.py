# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 02:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160717_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='impressoenderecamento',
            name='rotate',
        ),
    ]