# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-11 15:42
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('votita', '0002_kidsgathering_generated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kidsgathering',
            name='presidents_features',
        ),
        migrations.AddField(
            model_name='kidsgathering',
            name='presidents_features',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Caracter\xedsticas de un buen presidente'),
        ),
    ]
