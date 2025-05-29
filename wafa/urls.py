from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.urls import re_path as url
from django.contrib import admin
from puput.urls import urlpatterns as puput_urlpatterns
from event.urls import urlpatterns as event_urlpatterns
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from contact.views import post_message
from wagtail.contrib.sitemaps.views import sitemap
from search import views as search_views
from django.shortcuts import redirect
from django.utils.translation import get_language

def redirect_to_language(request):
    return redirect(f'/{get_language()}/')

urlpatterns = [
    url(r'^$', redirect_to_language),
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^sitemap\.xml$', sitemap),
]

urlpatterns += i18n_patterns(
    url('', include(event_urlpatterns)),
    url('', include(puput_urlpatterns)),
    url(r'^activities_gallery/', include('photologue.urls', namespace='photologue')),
    url(r'^search/$', search_views.search, name='search'),
    url('', include(wagtail_urls)),
    url(r'^contact/sendemail\.php', post_message),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
