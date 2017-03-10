from django import template
from home.models import *

register = template.Library()


@register.inclusion_tag("tags/slider.html", takes_context=True)
def slider(context):
    self = context.get('self')
    return {
        'request': context['request']
    }
