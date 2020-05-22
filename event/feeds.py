# -*- coding: utf-8 -*-
from mimetypes import guess_type

from six.moves import urllib_parse

from django import http
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.template.defaultfilters import truncatewords_html
from django.utils.translation import get_language

from wagtail.wagtailcore.models import Site
from .models import EventsPage


class EventsPageFeedGenerator(Rss201rev2Feed):

    def add_root_elements(self, handler):
        super(EventsPageFeedGenerator, self).add_root_elements(handler)
        if self.feed['image_link']:
            handler.addQuickElement(u"image", '',
                                    {
                                        'url': self.feed['image_link'],
                                        'title': self.feed['title'],
                                        'link': self.feed['link'],
                                    })


class EventsPageFeed(Feed):

    feed_type = EventsPageFeedGenerator

    def __call__(self, request, *args, **kwargs):
        if request.resolver_match.url_name == 'events_page_feed_slug':
            self.events_page = EventsPage.extra.get_by_path(kwargs['events_path'])
            if not self.events_page:
                raise http.Http404
        else:
            self.events_page = EventsPage.objects.first()
        self.request = request
        return super(EventsPageFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return self.events_page.title

    def description(self):
        return self.events_page.description

    def link(self):
        return self.events_page.last_url_part

    def items(self):
        return self.events_page.get_events()[:20]

    def item_title(self, item):
        return item.title

    def _item_short_description(self, item):
        excerpt = item.excerpt_en if get_language() is 'en' else item.excerpt_fr
        body = item.body_en if get_language() is 'en' else item.body_fr
        if excerpt and excerpt.strip() != '':
            return excerpt
        else:
            return truncatewords_html(body, 70)

    def item_description(self, item):
        body = item.body_en if get_language() is 'en' else item.body_fr
        if self.events_page.short_feed_description:
            return self._item_short_description(item)
        return body

    def item_pubdate(self, item):
        return item.date

    def item_link(self, item):
        from .urls import get_event_url
        event_url = get_event_url(item, self.events_page.page_ptr, self.request.site.root_page)
        return self.request.build_absolute_uri(event_url)

    def item_enclosure_url(self, item):
        if item.header_image:
            site = Site.find_for_request(self.request)
            return urllib_parse.urljoin(site.root_url, item.header_image.file.url)
        return None

    def item_enclosure_mime_type(self, item):
        if item.header_image:
            mime, enc = guess_type(self.item_enclosure_url(item))
            return mime
        return None

    def item_enclosure_length(self, item):
        if item.header_image:
            return item.header_image.file.size
        return 0

    def _channel_image_link(self):
        if self.events_page.header_image:
            site = Site.find_for_request(self.request)
            return urllib_parse.urljoin(site.root_url, self.events_page.header_image.file.url)

    def feed_extra_kwargs(self, obj):
        return {
            'image_link': self._channel_image_link()
        }
