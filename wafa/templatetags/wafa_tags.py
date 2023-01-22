from django import template
from django.urls import reverse, resolve

from django.utils.translation import activate, get_language
from django.utils.translation import gettext_lazy as _
from contact.models import ContactPage
from wagtail.documents import get_document_model
from django.shortcuts import get_object_or_404

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

register = template.Library()


@register.inclusion_tag("tags/menu.html", takes_context=True)
def menu(context, slug):
    self = context.get('self')
    return {
        'slug': slug,
        'request': context['request']
    }


@register.inclusion_tag("tags/header.html", takes_context=True)
def header(context, slug, offset=''):
    self = context.get('self')
    return {
        'slug': slug,
        'offset': offset,
        'request': context['request']
    }


@register.inclusion_tag("tags/page_title.html", takes_context=True)
def page_title(context, title, description):
    self = context.get('self')
    return {
        'title': _(title),
        'description': _(description),
        'request': context['request']
    }


@register.inclusion_tag("tags/footer.html", takes_context=True)
def footer(context):
    self = context.get('self')
    contact = ContactPage.objects.get(slug='contact')
    return {
        'request': context['request'],
        'contact': contact
    }


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    path = context['request'].path
    url_parts = resolve(path)

    cur_language = get_language()
    try:
        activate(lang)
        path = reverse(url_parts.view_name, args=url_parts.args, kwargs=url_parts.kwargs)
    finally:
        activate(cur_language)

    return "%s" % path


@register.simple_tag(name='dynamic_trans', takes_context=True)
def dynamic_trans(context, obj, field_name, get_lang_fn=get_language):
    field_name_language = field_name + '_' + get_lang_fn()
    try:
        # For django models
        return getattr(obj, field_name_language)
    except AttributeError:
        # For wagtail StructValue
        return obj[field_name_language]


@register.simple_tag(takes_context=False)
def split(value, separator):
    return value.split(separator)


@register.simple_tag(takes_context=False)
def product_document(html):
    id = BeautifulSoup(html).find('a', attrs={'linktype': 'document'}).get("id")
    return get_object_or_404(get_document_model(), id=id)


@register.simple_tag(takes_context=False)
def is_product(categories):
    for category in categories.all():
        if category.slug == 'wafbim' or category.slug == 'ferwam':
            return True
    return False


@register.inclusion_tag("tags/gallery_page_menu.html", takes_context=False)
def page_menu(page_slug):
    return {
        'page_slug': page_slug,
    }
