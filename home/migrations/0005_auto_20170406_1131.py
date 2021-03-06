# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 11:31
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('home', '0004_auto_20170331_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productpage',
            name='header_image',
        ),
        migrations.RemoveField(
            model_name='productpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='aboutpage',
            name='countries',
        ),
        migrations.RemoveField(
            model_name='aboutpage',
            name='officers',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='mission_vision_en',
        ),
        migrations.RemoveField(
            model_name='homepage',
            name='mission_vision_fr',
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='mission_en',
            field=wagtail.wagtailcore.fields.RichTextField(default='', verbose_name='Mission EN'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='mission_fr',
            field=wagtail.wagtailcore.fields.RichTextField(default='', verbose_name='Mission FR'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='objectives',
            field=wagtail.wagtailcore.fields.StreamField([(b'objectives', wagtail.wagtailcore.blocks.StructBlock([(b'title_fr', wagtail.wagtailcore.blocks.TextBlock(label=b'Titre_fr')), (b'title_en', wagtail.wagtailcore.blocks.TextBlock(label=b'Titre_en')), (b'description_fr', wagtail.wagtailcore.blocks.TextBlock(label=b'description_fr')), (b'description_en', wagtail.wagtailcore.blocks.TextBlock(label=b'description_en'))], label=b'Objectifs', required=False))], blank=True, verbose_name='Objectifs'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='vision_en',
            field=wagtail.wagtailcore.fields.RichTextField(default='', verbose_name='Vision EN'),
        ),
        migrations.AddField(
            model_name='aboutpage',
            name='vision_fr',
            field=wagtail.wagtailcore.fields.RichTextField(default='', verbose_name='Vision FR'),
        ),
        migrations.AddField(
            model_name='memberpage',
            name='officers',
            field=wagtail.wagtailcore.fields.StreamField([(b'office', wagtail.wagtailcore.blocks.StructBlock([(b'member_name', wagtail.wagtailcore.blocks.TextBlock(label=b'Nom')), (b'country', wagtail.wagtailcore.blocks.TextBlock(label=b'Pays')), (b'activity_fr', wagtail.wagtailcore.blocks.TextBlock(label=b'Activite FR')), (b'activity_en', wagtail.wagtailcore.blocks.TextBlock(label=b'Activite EN')), (b'deputy_name', wagtail.wagtailcore.blocks.TextBlock(label=b'Representant')), (b'contact', wagtail.wagtailcore.blocks.TextBlock(label=b'Contact', required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'position_fr', wagtail.wagtailcore.blocks.TextBlock(label=b'Poste FR', required=False)), (b'position_en', wagtail.wagtailcore.blocks.TextBlock(label=b'Poste EN', required=False))], icon=b'user', label=b'Membre', required=False))], blank=True, verbose_name='Bureau'),
        ),
        migrations.AlterField(
            model_name='memberpage',
            name='members',
            field=wagtail.wagtailcore.fields.StreamField([(b'member', wagtail.wagtailcore.blocks.StructBlock([(b'member_name', wagtail.wagtailcore.blocks.TextBlock(label=b'Nom')), (b'country', wagtail.wagtailcore.blocks.TextBlock(label=b'Pays')), (b'activity_fr', wagtail.wagtailcore.blocks.TextBlock(label=b'Activite FR')), (b'activity_en', wagtail.wagtailcore.blocks.TextBlock(label=b'Activite EN'))], icon=b'user', label=b'Membre', required=False))], blank=True, verbose_name='Membres'),
        ),
        migrations.DeleteModel(
            name='ProductPage',
        ),
    ]
