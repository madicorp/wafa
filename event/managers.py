# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Count
from wagtail.models import PageManager
from puput.utils import strip_prefix_and_ending_slash


class TagManager(models.Manager):
    def most_common(self, event_page):
        events = event_page.get_events()
        return self.filter(eventpage__in=events).annotate(num_times=Count('eventpage')).order_by('-num_times')


class CategoryManager(models.Manager):
    def with_uses(self, event_page):
        events = event_page.get_events()
        return self.filter(eventpage__in=events).distinct()


class EventsManager(PageManager):
    def get_by_path(self, event_path):
        # Look for the event checking all the path
        from .models import EventsPage
        events = EventsPage.objects.filter(slug=event_path.split("/")[-1])
        for event in events:
            if strip_prefix_and_ending_slash(event.specific.last_url_part) == event_path:
                return event.specific
        return

