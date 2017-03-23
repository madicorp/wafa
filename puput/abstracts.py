import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.wagtailcore.fields import RichTextField

from .utils import get_image_model_path


class EntryAbstract(models.Model):
    body_en = RichTextField(default="", verbose_name=_('body_en'))
    body_fr = RichTextField(default="", verbose_name=_('body_fr'))
    tags = ClusterTaggableManager(through='puput.TagEntryPage', blank=True)
    date = models.DateTimeField(verbose_name=_("Post date"), default=datetime.datetime.today)
    header_image = models.ForeignKey(get_image_model_path(), verbose_name=_('Header image'), null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+', )
    categories = models.ManyToManyField('puput.Category', through='puput.CategoryEntryPage', blank=True)
    excerpt_en = RichTextField(default="", verbose_name=_('excerpt_en'), blank=True,
                               help_text=_("Entry excerpt to be displayed on entries list. "
                                           "If this field is not filled, a truncate version of body text will be used."))
    excerpt_fr = RichTextField(default="", verbose_name=_('excerpt_fr'), blank=True,
                               help_text=_("Entry excerpt to be displayed on entries list. "
                                           "If this field is not filled, a truncate version of body text will be used."))
    num_comments = models.IntegerField(default=0, editable=False)

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            ImageChooserPanel('header_image'),
            FieldPanel('body_en', classname="full"),
            FieldPanel('body_fr', classname="full"),
            FieldPanel('excerpt_en', classname="full"),
            FieldPanel('excerpt_fr', classname="full"),
        ], heading=_("Content")),
        MultiFieldPanel([
            FieldPanel('tags'),
            InlinePanel('entry_categories', label=_("Categories")),
            InlinePanel('related_entrypage_from', label=_("Related Entries"),
                        panels=[PageChooserPanel('entrypage_to')]),
        ], heading=_("Metadata")),
    ]

    class Meta:
        abstract = True
