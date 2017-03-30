from wagtail.wagtailcore.blocks import StreamBlock, DateBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import TextBlock
from wagtail.wagtailcore.blocks import StructBlock


class MemberBlock(StructBlock):
    member_name = TextBlock(label='Nom')
    deputy_name = TextBlock(label='Representant')
    country = TextBlock(label='Pays')
    activity_fr = TextBlock(label='Activite FR')
    activity_en = TextBlock(label='Activite EN')
    contact = TextBlock(label='Contact', required=False)


class AboutMembersBlock(StreamBlock):
    member = MemberBlock(label='Membre', icon='user', required=False)


class OfficerBlock(MemberBlock):
    image = ImageChooserBlock()
    position_fr = TextBlock(label='Poste FR', required=False)
    position_en = TextBlock(label='Poste EN', required=False)


class AboutOfficerBlock(StreamBlock):
    office = OfficerBlock(label='Membre', icon='user', required=False)


class CountryBlock(StructBlock):
    flag = ImageChooserBlock(label='Drapeau')
    name = TextBlock(label='Nom')


class AboutCountryBlock(StreamBlock):
    countries = CountryBlock(label='Pays Membre', required=False)
