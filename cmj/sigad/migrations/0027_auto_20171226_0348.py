# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-26 05:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sigad', '0026_auto_20171222_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classe',
            name='titulo',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='titulo',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='referenciaentredocumentos',
            name='titulo',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Título'),
        ),
    ]
