from django.test import TestCase

from urlshortening.models import Url, generate_short_id, get_short_url, invalidate_url, get_full_url


class UrlTestCase(TestCase):
    def setUp(self):
        self.short_id_len = 2
        self.retry_count = 5
        self.site = "http://example.com"

    def test_generate_short_id_unique(self):
        short_id_1 = "12"
        Url.objects.create(short_id=short_id_1)
        short_id_2 = generate_short_id(self.short_id_len, self.retry_count)

        self.assertNotEqual(short_id_1, short_id_2)
        self.assertEqual(len(short_id_2), self.short_id_len, self.retry_count)

    def test_generate_short_id_inc_len(self):
        short_id_len = 2
        for _ in range(256):
            short_id = generate_short_id(self.short_id_len, self.retry_count)
            Url.objects.create(short_id=short_id)
        short_id = generate_short_id(self.short_id_len, self.retry_count)

        self.assertGreaterEqual(len(short_id), short_id_len + 1)

    def test_get_short_url(self):
        url = get_short_url(self.site)
        self.assertEqual(url.url, self.site)

    def test_get_short_url_cache(self):
        url1 = get_short_url(self.site)
        url2 = get_short_url(self.site)

        self.assertEqual(url1.short_id, url2.short_id)

    def test_invalidate_url(self):
        url = get_short_url(self.site)
        self.assertEqual(url.is_expired, False)
        invalidate_url(url.short_id)
        self.assertEqual(Url.objects.get(short_id=url.short_id).is_expired, True)

    def test_get_full_url(self):
        url = get_short_url(self.site)
        site = get_full_url(url.short_id)

        self.assertEqual(url.url, site.url)
