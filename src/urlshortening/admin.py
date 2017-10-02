from django.contrib import admin

from urlshortening.models import Url


class UrlsAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'url', 'pub_date', 'redirect_count')
    ordering = ('-pub_date',)

admin.site.register(Url, UrlsAdmin)
