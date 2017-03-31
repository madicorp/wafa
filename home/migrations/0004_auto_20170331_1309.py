# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 13:09
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20170331_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpage',
            name='num_events_page',
            field=models.IntegerField(default=5, verbose_name='Product per page'),
        ),
        migrations.AlterField(
            model_name='productpage',
            name='products',
            field=wagtail.wagtailcore.fields.StreamField([(b'products', wagtail.wagtailcore.blocks.StructBlock([(b'desc_fr', wagtail.wagtailcore.blocks.RichTextBlock(blank=False, default=b'', verbose_name=b"Description de l'edition FR")), (b'desc_en', wagtail.wagtailcore.blocks.RichTextBlock(blank=False, default=b'', verbose_name=b"Description de l'edition EN")), (b'file_fr', wagtail.wagtaildocs.blocks.DocumentChooserBlock(blank=True, verbose_name=b'Document Version FR')), (b'file_en', wagtail.wagtaildocs.blocks.DocumentChooserBlock(blank=True, verbose_name=b'Document Version FR')), (b'start_date', wagtail.wagtailcore.blocks.DateBlock(label=b"Date l'edition"))], blank=True, label=b'Produit'))], blank=True),
        ),
    ]
