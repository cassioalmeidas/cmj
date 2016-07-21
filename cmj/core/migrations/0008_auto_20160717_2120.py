# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 00:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160714_1557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='impressoenderecamento',
            old_name='fontesizebase',
            new_name='fontsize',
        ),
        migrations.AddField(
            model_name='impressoenderecamento',
            name='rotate',
            field=models.PositiveSmallIntegerField(default=0, help_text='Em Graus', verbose_name='Grau de Rotação'),
        ),
    ]