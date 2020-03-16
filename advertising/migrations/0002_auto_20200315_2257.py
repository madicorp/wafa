# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2020-03-15 22:57
from __future__ import unicode_literals

import advertising.models
import advertising.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertising', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertising',
            name='timeout',
            field=models.PositiveIntegerField(default=0, help_text='The input value is in seconds'),
        ),
        migrations.AlterField(
            model_name='imageadvertising',
            name='photo',
            field=models.FileField(upload_to=advertising.models.generate_path, validators=[advertising.validators.valid_extension], verbose_name='Photo'),
        ),
    ]