# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-26 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchlist', '0015_auto_20171007_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='description',
            field=models.TextField(),
        ),
    ]