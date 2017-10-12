# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-05 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('backend_citizen', '0008_auto_20160804_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='unsubscribe_token',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='profile',
            name='unsubscribed',
            field=models.BooleanField(default=False),
        ),
    ]