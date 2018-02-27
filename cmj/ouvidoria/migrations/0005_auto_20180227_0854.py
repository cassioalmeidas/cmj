# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-27 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ouvidoria', '0004_auto_20180223_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacao',
            name='tipo',
            field=models.IntegerField(choices=[(10, 'Acesso a Informação'), (20, 'Elogio'), (30, 'Sugestão'), (40, 'Reclamação'), (900, 'Denúncia')], default=10, verbose_name='Tipo de Solicitação'),
        ),
    ]
