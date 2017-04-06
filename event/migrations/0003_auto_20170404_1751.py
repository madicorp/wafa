# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 17:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20170331_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='end_date',
            field=models.DateField(default=datetime.datetime.today, verbose_name='Event End date'),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='start_date',
            field=models.DateField(default=datetime.datetime.today, verbose_name='Event Start date'),
        ),
    ]
