# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-20 12:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_notificacao_user_origin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notificacao',
            options={'permissions': (('popup_notificacao', 'Visualização das notificações em Popup no Avatar do Usuário'),), 'verbose_name': 'Notificação', 'verbose_name_plural': 'Notificações'},
        ),
    ]