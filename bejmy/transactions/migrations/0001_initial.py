# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 21:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='amount')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_as_destination', to='accounts.Account', verbose_name='destination')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_as_source', to='accounts.Account', verbose_name='source')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]