# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 13:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import modelcluster.contrib.taggit
import modelcluster.fields
import puput.routes
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('wagtailimages', '0018_remove_rendition_filter'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', models.CharField(blank=True, help_text='The blog description that will appear under the title.', max_length=255, verbose_name='Description')),
                ('display_comments', models.BooleanField(default=False, verbose_name='Display comments')),
                ('display_categories', models.BooleanField(default=True, verbose_name='Display categories')),
                ('display_tags', models.BooleanField(default=True, verbose_name='Display tags')),
                ('display_popular_entries', models.BooleanField(default=True, verbose_name='Display popular entries')),
                ('display_last_entries', models.BooleanField(default=True, verbose_name='Display last entries')),
                ('display_archive', models.BooleanField(default=True, verbose_name='Display archive')),
                ('disqus_api_secret', models.TextField(blank=True)),
                ('disqus_shortname', models.CharField(blank=True, max_length=128)),
                ('num_entries_page', models.IntegerField(default=5, verbose_name='Entries per page')),
                ('num_last_entries', models.IntegerField(default=3, verbose_name='Last entries limit')),
                ('num_popular_entries', models.IntegerField(default=3, verbose_name='Popular entries limit')),
                ('num_tags_entry_header', models.IntegerField(default=5, verbose_name='Tags limit entry header')),
                ('short_feed_description', models.BooleanField(default=True, verbose_name='Use short description in feeds')),
                ('header_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Header image')),
            ],
            options={
                'verbose_name': 'Blog',
            },
            bases=(puput.routes.BlogRoutes, 'wagtailcore.page'),
            managers=[
                ('extra', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Category name')),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='puput.Category', verbose_name='Parent category')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryEntryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='puput.Category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='EntryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body_en', wagtail.wagtailcore.fields.RichTextField(default=b'', verbose_name='body_en')),
                ('body_fr', wagtail.wagtailcore.fields.RichTextField(default=b'', verbose_name='body_fr')),
                ('date', models.DateTimeField(default=datetime.datetime.today, verbose_name='Post date')),
                ('excerpt_en', wagtail.wagtailcore.fields.RichTextField(blank=True, default=b'', help_text='Entry excerpt to be displayed on entries list. If this field is not filled, a truncate version of body text will be used.', verbose_name='excerpt_en')),
                ('excerpt_fr', wagtail.wagtailcore.fields.RichTextField(blank=True, default=b'', help_text='Entry excerpt to be displayed on entries list. If this field is not filled, a truncate version of body text will be used.', verbose_name='excerpt_fr')),
                ('num_comments', models.IntegerField(default=0, editable=False)),
                ('categories', models.ManyToManyField(blank=True, through='puput.CategoryEntryPage', to='puput.Category')),
                ('header_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Header image')),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='EntryPageRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrypage_from', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_entrypage_from', to='puput.EntryPage', verbose_name='Entry')),
                ('entrypage_to', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_entrypage_to', to='puput.EntryPage', verbose_name='Entry')),
            ],
        ),
        migrations.CreateModel(
            name='TagEntryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_tags', to='puput.EntryPage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.tag',),
        ),
        migrations.AddField(
            model_name='tagentrypage',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puput_tagentrypage_items', to='taggit.Tag'),
        ),
        migrations.AddField(
            model_name='entrypage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='puput.TagEntryPage', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='categoryentrypage',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_categories', to='puput.EntryPage'),
        ),
    ]
