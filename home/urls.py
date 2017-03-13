from .api import api_router
from django.conf.urls import url
from home import views
urlpatterns = [

    url(r'^api/v2/', api_router.urls),
    url(r'^api/v2/officers/$', views.board_members),
    url(r'^api/v2/officers/(?P<pk>[0-9]+)$', views.board_members),
]
