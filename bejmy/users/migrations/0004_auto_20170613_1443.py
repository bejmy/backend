# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-13 12:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20170613_1211'),
        ('users', '0003_user_default_balanced'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_source_account_most_used', models.BooleanField(default=False, verbose_name='default source account most used')),
                ('default_balanced', models.BooleanField(default=False, verbose_name='default balanced')),
                ('default_source_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='accounts.Account', verbose_name='default source account')),
            ],
            options={
                'verbose_name': 'settings',
                'verbose_name_plural': 'settings',
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_balanced',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_source_account',
        ),
        migrations.AddField(
            model_name='settings',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
