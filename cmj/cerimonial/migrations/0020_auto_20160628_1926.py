# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 22:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cerimonial', '0019_operadorareatrabalho_grupos_associados'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operadorareatrabalho',
            options={'verbose_name': 'Operador', 'verbose_name_plural': 'Operadores'},
        ),
        migrations.RenameField(
            model_name='operadorareatrabalho',
            old_name='operador',
            new_name='user',
        ),
    ]
