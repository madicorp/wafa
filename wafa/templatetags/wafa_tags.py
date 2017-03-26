from django import template
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import activate, get_language, ugettext as _
register = template.Library()


@register.inclusion_tag("tags/menu.html", takes_context=True)
def menu(context, slug):
    self = context.get('self')
    return {
        'slug': slug,
        'request': context['request']
    }


@register.inclusion_tag("tags/header.html", takes_context=True)
def header(context, slug):
    self = context.get('self')
    return {
        'slug': slug,
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
    return {
        'request': context['request']
    }


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    path = context['request'].path
    url_parts = resolve(path)

    url = path
    cur_language = get_language()
    try:
        activate(lang)
        url = reverse(url_parts.view_name, args=url_parts.args, kwargs=url_parts.kwargs)
    finally:
        activate(cur_language)

    return "%s" % url


@register.simple_tag(name='dynamic_trans', takes_context=True)
def dynamic_trans(context, obj, field_name, get_lang_fn=get_language):
    field_name_language = field_name + '_' + get_lang_fn()
    try:
        # For django models
        return getattr(obj, field_name_language)
    except AttributeError:
        # For wagtail StructValue
        return obj[field_name_language]
