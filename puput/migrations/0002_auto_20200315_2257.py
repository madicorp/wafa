# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2020-03-15 22:57
from __future__ import unicode_literals

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('puput', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrypage',
            name='body_en',
            field=wagtail.fields.RichTextField(default='', verbose_name='body_en'),
        ),
        migrations.AlterField(
            model_name='entrypage',
            name='body_fr',
            field=wagtail.fields.RichTextField(default='', verbose_name='body_fr'),
        ),
        migrations.AlterField(
            model_name='entrypage',
            name='excerpt_en',
            field=wagtail.fields.RichTextField(blank=True, default='', help_text='Entry excerpt to be displayed on entries list. If this field is not filled, a truncate version of body text will be used.', verbose_name='excerpt_en'),
        ),
        migrations.AlterField(
            model_name='entrypage',
            name='excerpt_fr',
            field=wagtail.fields.RichTextField(blank=True, default='', help_text='Entry excerpt to be displayed on entries list. If this field is not filled, a truncate version of body text will be used.', verbose_name='excerpt_fr'),
        ),
    ]
