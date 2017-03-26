from django.conf import settings
from django.conf.urls import url, include
from django.core.urlresolvers import reverse

from .feeds import EventsPageFeed
from .views import EventPageServe
from puput.utils import strip_prefix_and_ending_slash

urlpatterns = [
    url(
        regex=r'^(?P<events_path>[-\w\/]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        view=EventPageServe.as_view(),
        name='event_page_serve_slug'
    ),
    url(
        regex=r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        view=EventPageServe.as_view(),
        name='event_page_serve'
    ),
    url(
        regex=r'^(?P<events_path>[-\w\/]+)/feed/$',
        view=EventsPageFeed(),
        name='events_page_feed_slug'
    ),
    url(
        regex=r'^feed/$',
        view=EventsPageFeed(),
        name='events_page_feed'
    )
]

if not getattr(settings, 'EVENT_AS_PLUGIN', False):
    from wagtail.wagtailcore import urls as wagtail_urls
    from wagtail.wagtailadmin import urls as wagtailadmin_urls
    from wagtail.wagtaildocs import urls as wagtaildocs_urls
    from wagtail.wagtailsearch import urls as wagtailsearch_urls
    from wagtail.contrib.wagtailsitemaps.views import sitemap

    urlpatterns.extend([
        url(
            regex=r'^events_admin/',
            view=include(wagtailadmin_urls)
        ),
        url(
            regex=r'',
            view=include(wagtail_urls)
        ),
        url(
            regex=r'^search/',
            view=include(wagtailsearch_urls)
        ),
        url(
            regex=r'^documents/',
            view=include(wagtaildocs_urls)
        ),
        url(
            regex='^sitemap\.xml$',
            view=sitemap
        )
    ])


def get_event_url(event, events_page, root_page):
    """
    Get the event url given and event page a events page instances.
    It will use an url or another depending if events_page is the root page.
    """
    if root_page == events_page:
        return reverse('event_page_serve', kwargs={
            'year': event.date.strftime('%Y'),
            'month': event.date.strftime('%m'),
            'day': event.date.strftime('%d'),
            'slug': event.slug
        })
    else:
        # The method get_url_parts provides a tuple with a custom URL routing
        # scheme. In the last position it finds the subdomain of the events, which
        # it is used to construct the event url.
        # Using the stripped subdomain it allows Puput to generate the urls for
        # every sitemap level
        events_path = strip_prefix_and_ending_slash(events_page.specific.last_url_part)
        return reverse('event_page_serve_slug', kwargs={
            'events_path': events_path,
            'year': event.date.strftime('%Y'),
            'month': event.date.strftime('%m'),
            'day': event.date.strftime('%d'),
            'slug': event.slug
        })


def get_feeds_url(events_page, root_page):
    """
    Get the feeds urls a events page instance.
    It will use an url or another depending if events_page is the root page.
    """
    if root_page == events_page:
        return reverse('events_page_feed')
    else:
        events_path = strip_prefix_and_ending_slash(events_page.specific.last_url_part)
        return reverse('events_page_feed_slug', kwargs={'events_path': events_path})
