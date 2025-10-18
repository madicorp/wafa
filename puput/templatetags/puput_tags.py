# -*- coding: utf-8 -*-
from django.template import Library, loader

from el_pagination.templatetags.el_pagination_tags import paginate
from django.urls import resolve
from wagtail.models import Site
from ..urls import get_entry_url, get_feeds_url
from ..models import Category, Tag

register = Library()


@register.inclusion_tag('puput/tags/recent_entries_list.html', takes_context=True)
def recent_entries(context, limit=None):
    blog_page = context['blog_page']
    entries = blog_page.get_entries().order_by('-date')
    if limit:
        entries = entries[:limit]
    context['entries'] = entries
    return context


@register.inclusion_tag('puput/tags/popular_entries_list.html', takes_context=True)
def popular_entries(context, limit=None):
    blog_page = context['blog_page']
    entries = blog_page.get_entries().order_by('-num_comments', '-date')
    if limit:
        entries = entries[:limit]
    context['entries'] = entries
    return context


@register.inclusion_tag('puput/tags/tags_list.html', takes_context=True)
def tags_list(context, limit=None, tags_qs=None):
    blog_page = context['blog_page']
    if tags_qs:
        tags = tags_qs.all()
    else:
        tags = Tag.objects.most_common(blog_page)
    if limit:
        tags = tags[:limit]
    context['tags'] = tags
    return context


@register.inclusion_tag('puput/tags/categories_list.html', takes_context=True)
def categories_list(context, categories_qs=None):
    blog_page = context['blog_page']
    if categories_qs:
        categories = categories_qs.all()
    else:
        categories = Category.objects.with_uses(blog_page).filter(parent=None)
    context['categories'] = categories
    return context


@register.inclusion_tag('puput/tags/archives_list.html', takes_context=True)
def archives_list(context):
    blog_page = context['blog_page']
    context['archives'] = blog_page.get_entries().datetimes('date', 'day', order='DESC')
    return context


@register.simple_tag(takes_context=True)
def entry_url(context, entry, blog_page):
    request = context['request']
    site = Site.find_for_request(request) or getattr(request, 'site', None)
    root_page = site.root_page if site else getattr(blog_page.get_site(), 'root_page', None)
    # Return absolute URL to ensure correct links under i18n/prefix setups
    return request.build_absolute_uri(get_entry_url(entry, blog_page.page_ptr, root_page))


@register.simple_tag(takes_context=True)
def canonical_url(context, entry=None):
    if entry and resolve(context.request.path_info).url_name == 'wagtail_serve':
        return context.request.build_absolute_uri(entry_url(context, entry, entry.blog_page))
    return context.request.build_absolute_uri()


@register.simple_tag(takes_context=True)
def image_url(context, url):
    return context.request.build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def feeds_url(context, blog_page):
    request = context['request']
    site = Site.find_for_request(request)
    root_page = site.root_page if site else getattr(request, 'site', None).root_page
    return get_feeds_url(blog_page.page_ptr, root_page)


@register.simple_tag(takes_context=True)
def show_comments(context):
    blog_page = context['blog_page']
    entry = context['self']
    if blog_page.display_comments:
        if blog_page.disqus_shortname:
            template = loader.get_template('puput/comments/disqus.html')
            context['disqus_shortname'] = blog_page.disqus_shortname
            context['disqus_identifier'] = entry.id
            return template.render(context)
    return ""

# Avoid to import endless_pagination in installed_apps and in the templates
@register.inclusion_tag('puput/tags/paginator.html', takes_context=True)
def show_paginator(context):
    # Build the PageList from the context populated by {% paginate %}
    try:
        from el_pagination.models import PageList
        data = context.get('endless') or {}
        if not data:
            # Nothing to paginate (likely no {% paginate %} call earlier)
            return {'pages': None}
        pages = PageList(
            context['request'],
            data['page'],
            data['querystring_key'],
            context=context,
            default_number=data.get('default_number', 1),
            override_path=data.get('override_path'),
        )
        return {'pages': pages}
    except Exception:
        # Fail-safe: do not break the page if something is missing
        return {'pages': None}

# Re-export paginate tag from django-el-pagination
register.tag('paginate', paginate)
