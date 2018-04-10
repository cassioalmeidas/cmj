# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-27 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_user_be_notified_by_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='be_notified_by_email',
            field=models.BooleanField(default=True, verbose_name='Receber Notificações por email?'),
        ),
    ]
