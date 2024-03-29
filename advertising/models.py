import os

from django.db import models
from six import python_2_unicode_compatible
from wagtail.snippets.models import register_snippet

from .validators import valid_extension


@register_snippet
@python_2_unicode_compatible
class Advertising(models.Model):
    id_advertising = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=80)
    timeout = models.PositiveIntegerField(
        default=0, help_text="The input value is in seconds"
    )

    class Meta(object):
        ordering = ['id_advertising']
        verbose_name = "Advertising"
        verbose_name_plural = "Advertising"

    def __str__(self):
        return self.name


def generate_path(instance, filename):
    folder = "campaign_" + str(instance.advertising.id)
    return os.path.join("campaigns", folder, filename)


@register_snippet
@python_2_unicode_compatible
class ImageAdvertising(models.Model):
    advertising = models.ForeignKey(Advertising, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    url = models.URLField(max_length=450)
    photo = models.FileField("Photo", blank=False, null=False,
                             upload_to=generate_path,
                             validators=[valid_extension])

    def __str__(self):
        return self.advertising.name
