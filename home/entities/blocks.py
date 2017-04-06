from wagtail.wagtailcore.blocks import StreamBlock, DateBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailcore.blocks import TextBlock, RichTextBlock
from wagtail.wagtailcore.blocks import StructBlock
from django.db import models


class MemberBlock(StructBlock):
    member_name = TextBlock(label='Nom')
    country = TextBlock(label='Pays')
    activity_fr = TextBlock(label='Activite FR')
    activity_en = TextBlock(label='Activite EN')


class MemberMembersBlock(StreamBlock):
    member = MemberBlock(label='Membre', icon='user', required=False)


class OfficerBlock(MemberBlock):
    deputy_name = TextBlock(label='Representant')
    contact = TextBlock(label='Contact', required=False)
    image = ImageChooserBlock()
    position_fr = TextBlock(label='Poste FR', required=False)
    position_en = TextBlock(label='Poste EN', required=False)


class MemberOfficerBlock(StreamBlock):
    office = OfficerBlock(label='Membre', icon='user', required=False)


class ObjectifBlock(StructBlock):
    title_fr = TextBlock(label='Titre_fr')
    title_en = TextBlock(label='Titre_en')
    description_fr = TextBlock(label='description_fr')
    description_en = TextBlock(label='description_en')


class AboutObjectifBlock(StreamBlock):
    objectives = ObjectifBlock(label='Objectifs', required=False)
