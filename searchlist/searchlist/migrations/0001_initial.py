# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 16:45
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.us.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_category', models.CharField(choices=[('Crisis', 'Crisis'), ('Addiction', 'Addiction'), ('Childcare', 'Childcare'), ('Youth Services', 'Youth Services'), ('Veteran', 'Veteran'), ('Rehabilitation', 'Rehabilitation'), ('Mental/Physical Disability', 'Mental/Physical Disability'), ('Education', 'Education'), ('Employment', 'Employment'), ('Finances', 'Finances'), ('Clothing/Housewares', 'Clothing/Housewares'), ('Food', 'Food'), ('Healthcare', 'Healthcare'), ('Shelter', 'Shelter'), ('Legal', 'Legal'), ('Identification', 'Identification'), ('Spiritual', 'Spiritual')], max_length=25)),
                ('ratings', models.CharField(blank=True, default='one badge', max_length=25, null=True)),
                ('org_name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=400)),
                ('street', models.CharField(default='', max_length=128)),
                ('city', models.CharField(default='', max_length=128)),
                ('state', localflavor.us.models.USStateField(default='', max_length=2)),
                ('zip_code', localflavor.us.models.USZipCodeField(default='', max_length=10)),
                ('website', models.URLField(blank=True, null=True)),
                ('phone_number', localflavor.us.models.PhoneNumberField(max_length=20)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
