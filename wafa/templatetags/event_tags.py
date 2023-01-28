# -*- coding: utf-8 -*-
from django.template import Library

import datetime
from el_pagination.templatetags.el_pagination_tags import show_pages, paginate

from event.urls import get_event_url, get_feeds_url
from event.models import Category, Tag

from photologue.models import Photo

register = Library()


@register.inclusion_tag('event/tags/events_list.html', takes_context=True)
def upcoming_events(context, limit=None):
    events_page = context['events_page']
    events = events_page.get_events().filter(start_date__gt=datetime.date.today()).order_by('-date')
    if limit:
        events = events[:limit]
    context['events_upcoming'] = events
    return context


@register.inclusion_tag('event/tags/tags_list.html', takes_context=True)
def tags_list(context, limit=None, tags_qs=None):
    events_page = context['events_page']
    if tags_qs:
        tags = tags_qs.all()
    else:
        tags = Tag.objects.most_common(events_page)
    if limit:
        tags = tags[:limit]
    context['tags'] = tags
    return context


@register.inclusion_tag('event/tags/categories_list.html', takes_context=True)
def categories_list(context, categories_qs=None):
    events_page = context['events_page']
    if categories_qs:
        categories = categories_qs.all()
    else:
        categories = Category.objects.with_uses(events_page).filter(parent=None)
    context['categories'] = categories
    return context


@register.inclusion_tag('event/tags/gallery_widget.html', takes_context=True)
def gallery_widget(context, limit=None):
    photos = Photo.objects.on_site().is_public()
    if limit and len(photos) > 0:
        photos = photos[:limit]
    context['gallery_photos'] = photos
    return context


@register.simple_tag(takes_context=True)
def event_url(context, event, events_page):
    return get_event_url(event, events_page.page_ptr, context['request'].site.root_page)


@register.simple_tag(takes_context=True)
def canonical_url(context, event=None):
    if event and resolve(context.request.path_info).url_name == 'wagtail_serve':
        return context.request.build_absolute_uri(event_url(context, event, event.events_page))
    return context.request.build_absolute_uri()


@register.simple_tag(takes_context=True)
def image_url(context, url):
    return context.request.build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def feeds_url(context, events_page):
    return get_feeds_url(events_page.page_ptr, context['request'].site.root_page)


# Avoid to import endless_pagination in installed_apps and in the templates
register.tag('show_paginator', show_pages)
register.tag('paginate', paginate)
