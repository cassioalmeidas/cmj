# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-20 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180220_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacao',
            name='areatrabalho',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='notificacao_set', to='core.AreaTrabalho', verbose_name='Área de Trabalho'),
        ),
    ]