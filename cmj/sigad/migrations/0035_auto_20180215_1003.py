# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-15 12:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sigad', '0034_auto_20180215_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documento',
            name='capa',
        ),
        migrations.AddField(
            model_name='classe',
            name='capa',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capa', to='sigad.Documento', verbose_name='Documento'),
        ),
    ]
