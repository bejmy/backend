# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-14 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20171214_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, unique=True, verbose_name='account number'),
        ),
    ]
