# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160705_1011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bairro',
            options={'ordering': ('nome',), 'verbose_name': 'Bairro', 'verbose_name_plural': 'Bairros'},
        ),
        migrations.AlterModelOptions(
            name='cep',
            options={'ordering': ('numero',), 'verbose_name': 'CEP', 'verbose_name_plural': "CEP's"},
        ),
        migrations.AddField(
            model_name='bairro',
            name='codigo',
            field=models.PositiveIntegerField(default=1000, help_text='Código do Bairro no Cadastro Oficial do Município', verbose_name='Código'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bairro',
            name='outros_nomes',
            field=models.TextField(blank=True, help_text='Ocorrências similares', verbose_name='Outros Nomes'),
        ),
    ]