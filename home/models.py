from __future__ import absolute_import, unicode_literals
from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.search import index
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from home.entities.blocks import MemberOfficerBlock, MemberMembersBlock, AboutObjectifBlock, AboutPartnerBlock, \
    ExecutiveOfficerBlock
from django.utils.translation import gettext_lazy as _


class HomePage(Page):
    who_are_we_fr = RichTextField(blank=False, verbose_name="Qui sommes nous FR", default='')
    who_are_we_en = RichTextField(blank=False, verbose_name="Qui sommes nous EN", default='')

    search_fields = Page.search_fields + [
        index.SearchField('who_are_we_fr'),
        index.SearchField('who_are_we_en'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('who_are_we_fr', classname='full title'),
        FieldPanel('who_are_we_en', classname='full title'),
    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = _("Home Page")


class AboutPage(Page):
    company_desc_fr = RichTextField(blank=False, verbose_name="Description de l\'association FR", default='')
    company_desc_en = RichTextField(blank=False, verbose_name="Description de l\'association EN", default='')
    page_image = models.ForeignKey('wagtailimages.Image',
                                   verbose_name=_('Header image'),
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL,
                                   related_name='+')
    mission_fr = RichTextField(blank=False, verbose_name="Mission FR", default='')
    mission_en = RichTextField(blank=False, verbose_name="Mission EN", default='')
    vision_fr = RichTextField(blank=False, verbose_name="Vision FR", default='')
    vision_en = RichTextField(blank=False, verbose_name="Vision EN", default='')
    objectives = StreamField(AboutObjectifBlock(), blank=True, verbose_name='Objectifs')
    partners = StreamField(AboutPartnerBlock(), blank=True, verbose_name='Partners')

    search_fields = Page.search_fields + [
        index.SearchField('company_desc_fr'),
        index.SearchField('company_desc_en'),
        index.SearchField('mission_fr'),
        index.SearchField('mission_en'),
        index.SearchField('vision_fr'),
        index.SearchField('vision_en'),
        index.SearchField('objectives'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('page_image'),
        MultiFieldPanel([
            FieldPanel('company_desc_fr', classname='full title'),
            FieldPanel('company_desc_en', classname='full title'),
            FieldPanel('mission_fr', classname='full title'),
            FieldPanel('mission_en', classname='full title'),
            FieldPanel('vision_fr', classname='full title'),
            FieldPanel('vision_en', classname='full title'),
            FieldPanel('objectives'),
        ], heading=_("About Company")),
        MultiFieldPanel([
            FieldPanel('partners'),
        ], heading=_("Partners")),
    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = _("About Us Page")


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
    executive_officers = StreamField(ExecutiveOfficerBlock(), blank=True, verbose_name='Executive Officers')
    officers = StreamField(MemberOfficerBlock(), blank=True, verbose_name='Officers')
    members = StreamField(MemberMembersBlock(), blank=True, verbose_name='Membres')
    search_fields = Page.search_fields + [
        index.SearchField('membership_fr'),
        index.SearchField('membership_en'),
        index.SearchField('file'),
        index.SearchField('members'),
        index.SearchField('officers'),
        index.SearchField('executive_officers'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        MultiFieldPanel([
            FieldPanel('membership_fr', classname='full title'),
            FieldPanel('membership_en', classname='full title'),
            FieldPanel('file'),
        ], heading=_("Membership")),
        MultiFieldPanel([
            FieldPanel('executive_officers'),
            FieldPanel('officers'),
            FieldPanel('members'),
        ], heading=_("Members")),

    ]

    promote_panels = Page.promote_panels

    class Meta:
        verbose_name = _("Member Page")
