# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-26 02:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('searchlist', '0005_auto_20180126_0233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='service_animals',
        ),
    ]
