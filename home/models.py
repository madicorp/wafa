from __future__ import absolute_import, unicode_literals
from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from django.conf import settings
from home.entities.blocks import AboutOfficerBlock, AboutMembersBlock, AboutCountryBlock, ProductStreamBlock
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


class HomePage(Page):
    who_are_we_fr = RichTextField(blank=False, verbose_name='Qui sommes nous FR', default='')
    who_are_we_en = RichTextField(blank=False, verbose_name='Qui sommes nous EN', default='')

    mission_vision_fr = RichTextField(blank=False, verbose_name='Vision/Mission FR', default='')
    mission_vision_en = RichTextField(blank=False, verbose_name='Vision/Mission EN', default='')
    search_fields = Page.search_fields + [
        index.SearchField('who_are_we_fr'),
        index.SearchField('who_are_we_en'),
        index.SearchField('mission_vision_fr'),
        index.SearchField('mission_vision_en')

    ]

    class Meta:
        verbose_name = "Home Page"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('who_are_we_fr', classname='full title'),
        FieldPanel('who_are_we_en', classname='full title'),
        FieldPanel('mission_vision_fr', classname='full title'),
        FieldPanel('mission_vision_en', classname='full title'),
    ]

    promote_panels = Page.promote_panels


class AboutPage(Page):
    company_desc_fr = RichTextField(blank=False, verbose_name='Description de l\'association FR', default='')
    company_desc_en = RichTextField(blank=False, verbose_name='Description de l\'association EN', default='')
    officers = StreamField(AboutOfficerBlock(), verbose_name='Bureau')
    countries = StreamField(AboutCountryBlock(), verbose_name='Pays', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('company_desc_fr'),
        index.SearchField('company_desc_en'),
        index.SearchField('officers'),
        index.SearchField('countries'),
    ]

    class Meta:
        verbose_name = "About Us Page"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('company_desc_fr', classname='full title'),
        FieldPanel('company_desc_en', classname='full title'),
        StreamFieldPanel('officers'),
        StreamFieldPanel('countries'),
    ]

    promote_panels = Page.promote_panels


class MemberPage(Page):
    membership_fr = RichTextField(blank=False, verbose_name='Conditions d\'admission FR', default='')
    membership_en = RichTextField(blank=False, verbose_name='Conditions d\'admission EN', default='')
    file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    members = StreamField(AboutMembersBlock(), verbose_name='Membres')
    search_fields = Page.search_fields + [
        index.SearchField('membership_fr'),
        index.SearchField('membership_en'),
        index.SearchField('file'),
        index.SearchField('members'),

    ]

    class Meta:
        verbose_name = "Member Page"

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('membership_fr', classname='full title'),
        FieldPanel('membership_en', classname='full title'),
        DocumentChooserPanel('file'),
        StreamFieldPanel('members'),
    ]

    promote_panels = Page.promote_panels


class ProductPage(Page):
    header_image = models.ForeignKey(getattr(settings, 'WAGTAILIMAGES_IMAGE_MODEL', 'wagtailimages.Image'),
                                     verbose_name=_('Header image'), null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+', )
    excerpt_en = RichTextField(default="", verbose_name=_('excerpt_en'), blank=True,
                               help_text=_("Entry excerpt to be displayed on entries list. "
                                           "If this field is not filled, a truncate version of body text will be used."))
    excerpt_fr = RichTextField(default="", verbose_name=_('excerpt_fr'), blank=True,
                               help_text=_("Entry excerpt to be displayed on entries list. "
                                           "If this field is not filled, a truncate version of body text will be used."))
    products = StreamField(ProductStreamBlock(), blank=True)

    num_events_page = models.IntegerField(default=5, verbose_name=_('Product per page'))
    content_panels = [
        FieldPanel('title', classname="full title"),
        ImageChooserPanel('header_image'),
        FieldPanel('excerpt_fr', classname='full title'),
        FieldPanel('excerpt_en', classname='full title'),
        StreamFieldPanel('products'),
    ]
    settings_panels = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('num_events_page'),
        ], heading=_("Parameters")),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('header_image'),
        index.SearchField('excerpt_fr'),
        index.SearchField('excerpt_en'),
        index.SearchField('products'),
    ]

    class Meta:
        verbose_name = "Product Page"
