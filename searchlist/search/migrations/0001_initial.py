# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_category', models.CharField(choices=[('shelter', 'shelter'), ('food', 'food'), ('clinic', 'clinic')], max_length=25)),
                ('ratings', models.CharField(blank=True, choices=[('one badge', 'one badge'), ('two badge', 'two badge'), ('three badge', 'three badge')], default='one badge', max_length=25, null=True)),
                ('age_range', models.CharField(blank=True, choices=[('<=17', '<=17'), ('18-25', '18-25'), ('>26', '>26')], max_length=25, null=True)),
                ('org_name', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=400)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
