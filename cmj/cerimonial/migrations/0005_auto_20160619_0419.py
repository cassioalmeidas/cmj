# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-19 07:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cerimonial', '0004_auto_20160619_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telefone',
            name='operadora',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='telefones_set', to='cerimonial.OperadoraTelefonia', verbose_name='Operadora de Telefonia'),
        ),
    ]
