from math import ceil
from uuid import uuid4

from django.db.models import SlugField, URLField, DateTimeField, IntegerField, Model, BooleanField
from django.db.models.functions import Length
from django.conf import settings


def generate_token(length):
    return "".join([uuid4().hex for _ in range(ceil(length/32))])[:length]


def generate_short_id(short_id_length, retry_count):
    longest_url = Url.objects.annotate(short_id_len=Length('short_id')).order_by('-short_id_len')
    current_length = short_id_length
    if longest_url.first() and len(longest_url.first().short_id) > current_length:
        current_length = longest_url.first().short_id_len

    try_number = 0
    while try_number <= retry_count:
        try_number += 1
        short_id = generate_token(current_length)
        try:
            Url.objects.get(pk=short_id)
        except Url.DoesNotExist:
            return short_id

    current_length += 1
    return generate_short_id(current_length, retry_count)


def get_short_url(url):
    try:
        return Url.objects.get(url=url)
    except Url.DoesNotExist:
        short_id = generate_short_id(settings.INITIAL_URL_LEN, settings.RETRY_COUNT)
        return Url.objects.create(short_id=short_id, url=url)


def get_full_url(short_id):
    try:
        return Url.objects.get(short_id=short_id)
    except Url.DoesNotExist:
        raise Url.DoesNotExist


def invalidate_url(short_id):
    try:
        url = Url.objects.get(short_id=short_id)
        url.is_expired = True
        return url.save()
    except Url.DoesNotExist:
        raise Url.DoesNotExist


class Url(Model):
    short_id = SlugField(primary_key=True)
    url = URLField(max_length=200)
    pub_date = DateTimeField(auto_now=True)
    is_expired = BooleanField(default=False)
    redirect_count = IntegerField(default=0)

    def __str__(self):
        return self.short_id
