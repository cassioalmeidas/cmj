# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-18 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='solicitante',
            field=models.CharField(blank=True, max_length=255, verbose_name='Solicitante'),
        ),
    ]