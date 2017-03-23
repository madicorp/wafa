from django import template
from home.models import *

register = template.Library()


@register.inclusion_tag("tags/home/slider.html", takes_context=True)
def slider(context):
    self = context.get('self')
    return {
        'request': context['request']
    }


@register.inclusion_tag("tags/about/board-members.html", takes_context=True)
def board_members(context, members):
    self = context.get('self')
    return {
        'members': members,
        'request': context['request']
    }

