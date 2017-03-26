from django import template
from event.models import EventPage
import datetime
register = template.Library()


@register.inclusion_tag("home/tags/slider.html", takes_context=True)
def slider(context):
    self = context.get('self')
    return {
        'request': context['request']
    }


@register.inclusion_tag("home/tags/board-members.html", takes_context=True)
def board_members(context, members):
    self = context.get('self')
    return {
        'members': members,
        'request': context['request']
    }


@register.inclusion_tag('home/tags/events_list.html', takes_context=True)
def upcoming_events(context, limit=None):
    events = EventPage.objects.live().order_by('-date').select_related('owner').filter(start_date__gt=datetime.date.today()).order_by('-date')
    if limit:
        events = events[:limit]
    context['events_upcoming'] = events
    return context

