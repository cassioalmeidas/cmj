# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-29 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cerimonial', '0002_auto_20170328_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupodecontatos',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome do Grupo'),
        ),
    ]
