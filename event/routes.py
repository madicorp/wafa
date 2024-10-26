# -*- coding: utf-8 -*-

from datetime import date

from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page
from wagtail.contrib.search_promotions.models import Query

USERNAME_REGEX = getattr(settings, 'PUPUT_USERNAME_REGEX', r'\w+')


class EventsRoutes(RoutablePageMixin):
    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def events_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.events = self.get_events().filter(date__year=year)
        self.search_type = _('date')
        self.search_term = year
        if month:
            self.events = self.events.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
        if day:
            self.events = self.events.filter(date__day=day)
            self.search_term = date_format(date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def events_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = _('tag')
        self.search_term = tag
        self.events = self.get_events().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def events_by_category(self, request, category, *args, **kwargs):
        self.search_type = _('category')
        self.search_term = category
        self.events = self.get_events().filter(event_categories__category__slug=category)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^author/(?P<author>%s)/$' % USERNAME_REGEX)
    def events_by_author(self, request, author, *args, **kwargs):
        self.search_type = _('author')
        self.search_term = author
        field_name = 'owner__%s' % getattr(settings, 'PUPUT_USERNAME_FIELD', 'username')
        self.events = self.get_events().filter(**{field_name: author})
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def events_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.events = self.get_events()
        if search_query:
            self.events = self.events.search(search_query)
            self.search_term = search_query
            self.search_type = _('search')
            Query.get(search_query).add_hit()
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def events_list(self, request, *args, **kwargs):
        self.events = self.get_events()
        return Page.serve(self, request, *args, **kwargs)
