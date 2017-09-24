from django.conf.urls import url

from urlshortening.views import get_full_link, get_short_link

urlpatterns = [
    url(r'^expand/(?P<short_id>.+)/$', get_full_link),
    url(r'^short/$', get_short_link)
]