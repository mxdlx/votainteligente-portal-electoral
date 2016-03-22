# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-22 21:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('popolo', '0002_auto_20160311_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalTemporaryData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', picklefield.fields.PickledObjectField(editable=False)),
                ('rejected', models.BooleanField(default=False)),
                ('rejected_reason', models.TextField()),
                ('comments', picklefield.fields.PickledObjectField(editable=False)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_proposals', to='popolo.Area')),
                ('organization', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temporary_proposals', to='popolo.Organization')),
                ('proposer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temporary_proposals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
