# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170606_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='balance_initial',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='balance initial'),
        ),
    ]
