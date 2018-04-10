# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-18 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sigad', '0023_auto_20171217_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='classe',
            name='tipo_doc_padrao',
            field=models.IntegerField(choices=[(0, 'Documento'), (10, 'Banco de Imagem'), (20, 'Galeria Pública'), (700, 'Container Simples'), (701, 'Container Extendido'), (100, 'Texto'), (800, 'Vídeo'), (850, 'Áudio'), (900, 'Imagem'), (901, 'Galeria de Imagens')], default=0, verbose_name='Tipo Padrão para Documentos desta Classe'),
        ),
    ]
