from __future__ import unicode_literals
from wagtail.wagtailcore.models import Page

from django.db import models
from location_field.models.plain import PlainLocationField
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel


class ContactPage(Page):
    address = models.CharField(max_length=255, blank=True, verbose_name=_('Address'))
    phone = models.CharField(max_length=255, blank=True, verbose_name=_('Phone'))
    fax = models.CharField(max_length=255, blank=True, verbose_name=_('Fax'))
    email = models.CharField(max_length=255, blank=True, verbose_name=_('Email'))

    facebook = models.URLField(blank=True, verbose_name='Facebook Page')
    twitter = models.URLField(blank=True, verbose_name='Twitter Page')
    googleplus = models.URLField(blank=True, verbose_name='Google+ Page')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn Page')

    city = models.CharField(max_length=255, blank=True)
    location = PlainLocationField(based_fields=['city'], blank=True, zoom=13)

    content_panels = [
        FieldPanel('title', classname="title"),

        MultiFieldPanel([
            FieldPanel('address', classname="full"),
            FieldPanel('phone', classname="full"),
            FieldPanel('fax', classname="full"),
            FieldPanel('email', classname="full"),
        ], heading=_("Contacts")),
        MultiFieldPanel([
            FieldPanel('facebook', classname="full"),
            FieldPanel('twitter', classname="full"),
            FieldPanel('googleplus', classname="full"),
            FieldPanel('linkedin', classname="full"),
        ], heading=_("Social Media")),
        MultiFieldPanel([
            FieldPanel('city', classname="full"),
            FieldPanel('location', classname="full"),
        ], heading=_("Google Maps")),
    ]

    class Meta:
        verbose_name = _('Contact')
