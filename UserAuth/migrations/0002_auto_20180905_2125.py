# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-05 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituteprofile',
            name='address_pincode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
