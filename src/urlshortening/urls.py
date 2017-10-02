from django.conf.urls import url
from django.conf import settings

from urlshortening.views import get_full_link, get_short_link, get_redirect, invalidate

urlpatterns = [
    url(r'^expand/(?P<short_id>.+)/$', get_full_link),
    url(r'^short/$', get_short_link),
    url(r'^invalidate/$', invalidate),
    url(r'^{}/expand/(?P<short_id>.+)/$'.format(settings.REDIRECT_PREFIX), get_redirect)
]
