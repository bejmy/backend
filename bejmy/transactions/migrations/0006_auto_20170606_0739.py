# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 07:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_auto_20170606_0722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='balanced_at',
        ),
        migrations.AddField(
            model_name='transaction',
            name='balanced_changed',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='balanced', verbose_name='balanced changed'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='datetime',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='datetime'),
        ),
    ]
