from __future__ import unicode_literals

import datetime

from wagtail.wagtailsnippets.models import register_snippet

from django.conf import settings

from django.core.exceptions import ValidationError

from puput.abstracts import EntryAbstract
from .routes import EventsRoutes
from puput.utils import import_model, get_image_model_path
from .managers import TagManager, CategoryManager, EventsManager
from django.utils.encoding import python_2_unicode_compatible
from django.template.defaultfilters import slugify
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase, Tag as TaggitTag
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from django.db import models
from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page, PageBase
from wagtail.wagtailadmin.edit_handlers import InlinePanel, PageChooserPanel
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel

EventAbstract = import_model(getattr(settings, 'PUPUT_ENTRY_MODEL', EntryAbstract))


class Event(EventAbstract):
    link = models.URLField(verbose_name=_("Link"), blank=True)
    location = models.CharField(default="", verbose_name=_("Location"), max_length=250)
    tags = ClusterTaggableManager(through='event.TagEventPage', blank=True)
    categories = models.ManyToManyField('event.Category', through='event.CategoryEventPage', blank=True)
    start_date = models.DateTimeField(verbose_name=_("Event Start date"), default=datetime.datetime.today)
    end_date = models.DateTimeField(verbose_name=_("Event End date"),
                                    default=(datetime.datetime.today() + datetime.timedelta(days=1)))
    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            ImageChooserPanel('header_image'),
            FieldPanel('body_en', classname="full"),
            FieldPanel('body_fr', classname="full"),
            FieldPanel('excerpt_en', classname="full"),
            FieldPanel('excerpt_fr', classname="full"),
            FieldPanel('link', classname="full"),
            FieldPanel('location', classname="full"),
        ], heading=_("Content")),
        MultiFieldPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
        ], heading=_("Duration")),
        MultiFieldPanel([
            FieldPanel('tags'),
            InlinePanel('event_categories', label=_("Categories")),
            InlinePanel('related_eventpage_from', label=_("Related Entries"),
                        panels=[PageChooserPanel('eventpage_to')]),
        ], heading=_("Metadata")),
    ]

    class Meta:
        abstract = True


class EventsPage(EventsRoutes, Page):
    description = models.CharField(verbose_name=_('Description'), max_length=255, blank=True,
                                   help_text=_("The Event description that will appear under the title."))
    header_image = models.ForeignKey(get_image_model_path(), verbose_name=_('Header image'), null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+')

    display_categories = models.BooleanField(default=True, verbose_name=_('Display categories'))
    display_tags = models.BooleanField(default=True, verbose_name=_('Display tags'))
    display_popular_events = models.BooleanField(default=True, verbose_name=_('Display popular events'))
    display_last_events = models.BooleanField(default=True, verbose_name=_('Display last events'))
    display_archive = models.BooleanField(default=True, verbose_name=_('Display archive'))

    disqus_api_secret = models.TextField(blank=True)
    disqus_shortname = models.CharField(max_length=128, blank=True)

    num_events_page = models.IntegerField(default=5, verbose_name=_('Events per page'))
    num_last_events = models.IntegerField(default=3, verbose_name=_('Last events limit'))
    num_popular_events = models.IntegerField(default=3, verbose_name=_('Popular events limit'))
    num_tags_event_header = models.IntegerField(default=5, verbose_name=_('Tags limit event header'))

    short_feed_description = models.BooleanField(default=True, verbose_name=_('Use short description in feeds'))

    extra = EventsManager()

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        ImageChooserPanel('header_image'),
    ]
    settings_panels = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('display_categories'),
            FieldPanel('display_tags'),
            FieldPanel('display_popular_events'),
            FieldPanel('display_last_events'),
            FieldPanel('display_archive'),
        ], heading=_("Widgets")),
        MultiFieldPanel([
            FieldPanel('num_events_page'),
            FieldPanel('num_last_events'),
            FieldPanel('num_popular_events'),
            FieldPanel('num_tags_event_header'),
        ], heading=_("Parameters")),
        MultiFieldPanel([
            FieldPanel('short_feed_description'),
        ], heading=_("Feeds")),
    ]
    subpage_types = ['event.EventPage']

    def get_events(self):
        return EventPage.objects.descendant_of(self).live().order_by('-date').select_related('owner')

    def get_context(self, request, *args, **kwargs):
        context = super(EventsPage, self).get_context(request, *args, **kwargs)
        context['events'] = self.events
        context['events_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        return context

    @property
    def last_url_part(self):
        """
        Get the EventPage url without the domain
        """
        return self.get_url_parts()[-1]

    class Meta:
        verbose_name = _('Events')


@register_snippet
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name=_('Category name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children",
                               verbose_name=_('Parent category'))
    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError(_('Parent category cannot be self.'))
            if parent.parent and parent.parent == self:
                raise ValidationError(_('Cannot have circular Parents.'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class CategoryEventPage(models.Model):
    category = models.ForeignKey(Category, related_name="+", verbose_name=_('Category'))
    page = ParentalKey('EventPage', related_name='event_categories')
    panels = [
        FieldPanel('category')
    ]


class TagEventPage(TaggedItemBase):
    content_object = ParentalKey('EventPage', related_name='event_tags')


@register_snippet
class Tag(TaggitTag):
    objects = TagManager()

    class Meta:
        proxy = True


class EventPageRelated(models.Model):
    eventpage_from = ParentalKey('EventPage', verbose_name=_("Event"), related_name='related_eventpage_from')
    eventpage_to = ParentalKey('EventPage', verbose_name=_("Event"), related_name='related_eventpage_to')


class EventPage(six.with_metaclass(PageBase, Event, Page)):
    # Search
    search_fields = Page.search_fields + [
        index.SearchField('body_en'),
        index.SearchField('body_fr'),
        index.SearchField('excerpt_en'),
        index.SearchField('excerpt_fr'),
        index.FilterField('page_ptr_id')
    ]

    # Panels
    content_panels = getattr(Event, 'content_panels', [])

    promote_panels = Page.promote_panels + getattr(Event, 'promote_panels', [])

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
        FieldPanel('owner'),
    ] + getattr(Event, 'settings_panels', [])

    # Parent and child settings
    parent_page_types = ['event.EventsPage']
    subpage_types = []

    @property
    def events_page(self):
        return self.get_parent().specific

    @property
    def related(self):
        return [related.eventpage_to for related in self.related_eventpage_from.all()]

    @property
    def has_related(self):
        return self.related_eventpage_from.count() > 0

    def get_context(self, request, *args, **kwargs):
        context = super(EventPage, self).get_context(request, *args, **kwargs)
        context['events_page'] = self.events_page
        return context

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


EventPage._meta.get_field('owner').editable = True
