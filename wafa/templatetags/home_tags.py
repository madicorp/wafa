from django import template
from event.models import EventPage
from puput.models import BlogPage
import datetime
import re

register = template.Library()


@register.inclusion_tag("home/tags/slider.html", takes_context=True)
def slider(context):
    self = context.get('self')
    market_news = BlogPage.objects.live().get(slug='market-news')
    return {
        'request': context['request'],
        'market_news': market_news,
        'market_news_entries': market_news.get_entries().order_by('-date')[:3]
    }


@register.inclusion_tag("home/tags/board_members.html", takes_context=True)
def board_members(context, members):
    self = context.get('self')
    return {
        'members': members,
        'request': context['request']
    }


@register.inclusion_tag("home/tags/partners.html", takes_context=True)
def partners_list(context, partners):
    self = context.get('self')
    return {
        'partners': partners,
        'request': context['request']
    }


@register.inclusion_tag('home/tags/market_news_list.html', takes_context=True)
def last_market_news(context, limit=None):
    market_news = BlogPage.objects.live().get(slug='market-news').get_entries().order_by('-date')
    if limit:
        market_news = market_news[:limit]
    context['market_news'] = market_news
    return context


@register.inclusion_tag('home/tags/blog_posts_list.html', takes_context=True)
def last_blog_posts(context, limit=None):
    blog_posts = BlogPage.objects.live().get(slug='wafa-hub').get_entries().order_by('-date')
    if limit:
        blog_posts = blog_posts[:limit]
    context['blog_posts'] = blog_posts
    return context


@register.inclusion_tag('home/tags/events_list.html', takes_context=True)
def upcoming_events(context, limit=None):
    events = EventPage.objects.live().order_by('-date').select_related('owner').filter(
        start_date__gt=datetime.date.today()).order_by('-date')
    if limit:
        events = events[:limit]
    context['events_upcoming'] = events
    return context


@register.simple_tag(takes_context=False)
def get_objectif_at(qualities, position):
    return qualities[position]


@register.simple_tag(takes_context=False)
def format_quality_text(s):
    return re.sub('-', '<br> -', s)
