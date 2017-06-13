# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['order'], 'verbose_name': 'account', 'verbose_name_plural': 'accounts'},
        ),
        migrations.AddField(
            model_name='account',
            name='uses',
            field=models.PositiveIntegerField(default=0, verbose_name='uses'),
        ),
    ]
