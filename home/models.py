from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils import text

from wagtail.wagtailcore.blocks import StreamBlock, DateBlock
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import TextBlock
from wagtail.wagtailcore.blocks import StructBlock


class HomePage(Page):
    def clean(self):
        super(HomePage, self).clean()
        self.title = "{}".format("Home Page")

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
        FieldPanel('who_are_we_fr', classname='full title'),
        FieldPanel('who_are_we_en', classname='full title'),
        FieldPanel('mission_vision_fr', classname='full title'),
        FieldPanel('mission_vision_en', classname='full title'),
    ]

    promote_panels = Page.promote_panels


class MemberBlock(StructBlock):
    image = ImageChooserBlock()
    Member_name = TextBlock(label='Nom')
    deputy_name = TextBlock(label='Representant')
    country = TextBlock(label='Pays')
    activity_fr = TextBlock(label='Activite FR')
    activity_en = TextBlock(label='Activite EN')
    position_fr = TextBlock(label='Poste FR', required=False)
    position_en = TextBlock(label='Poste EN', required=False)
    position_description_fr = TextBlock(label='Description du Membre FR', required=False)
    position_description_en = TextBlock(label='Description du Membre EN', required=False)


class AboutMembersBlock(StreamBlock):
    member = MemberBlock(label='Membre', icon='user', required=False)


class OfficerBlock(StructBlock):
    member = MemberBlock(label='Membre', icon='user')
    code = TextBlock(label='Code')
    code_parent = TextBlock(label='Code Parent')


class AboutOfficerBlock(StreamBlock):
    office = OfficerBlock(label='Membre', icon='user', required=False)


class AboutPage(Page):
    def clean(self):
        super(AboutPage, self).clean()
        self.title = "{}".format("About Page")

    company_desc_fr = RichTextField(blank=False, verbose_name='Description de l\'association FR', default='')
    company_desc_en = RichTextField(blank=False, verbose_name='Description de l\'association EN', default='')
    # members = StreamField(AboutMembersBlock(), verbose_name='Membres')
    officers = StreamField(AboutOfficerBlock(), verbose_name='Bureau')
    search_fields = Page.search_fields + [
        index.SearchField('company_desc_fr'),
        index.SearchField('company_desc_en'),
        # index.SearchField('members'),
        index.SearchField('officers'),
    ]

    class Meta:
        verbose_name = "About Us Page"

    content_panels = [
        FieldPanel('company_desc_fr', classname='full title'),
        FieldPanel('company_desc_en', classname='full title'),
        # StreamFieldPanel('members'),
        StreamFieldPanel('officers'),
    ]

    promote_panels = Page.promote_panels
