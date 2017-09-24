import json
from django.conf import settings
from django.test import TestCase, override_settings


@override_settings(
    ROOT_URLCONF='urlshortening.urls',
    SHORT_URL_PATH='http://example.com/short-prefix/'
)
class ViewTestCase(TestCase):
    fixtures = ['urlshortening-test-data']

    def test_get_full_link(self):
        short_id = "000001"
        should_response = {"error": "", "data": {"full_url": "http://example.com/to-000001"}}

        response = self.client.get('/expand/{}/'.format(short_id))
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["data"], should_response["data"])
        self.assertEqual(response_data["error"], should_response["error"])

    def test_get_full_link_expired(self):
        short_id = "000002"
        should_response = {"data": "", "error": "Link is expired"}

        response = self.client.get('/expand/{}/'.format(short_id))
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["data"], should_response["data"])
        self.assertEqual(response_data["error"], should_response["error"])

    def test_get_full_link_not_found(self):
        short_id = "000003"
        should_response = {"data": "", "error": "Url doesn\'t exist"}

        response = self.client.get('/expand/{}/'.format(short_id))
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["data"], should_response["data"])
        self.assertEqual(response_data["error"], should_response["error"])

    def test_get_short_link(self):
        link = "http://example.com/a/b/c/d/e"

        response = self.client.post('/short/', data={"full_url": link})
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["data"]["short_url_path"], settings.SHORT_URL_PATH)
        self.assertEqual(response_data["error"], "")

    def test_get_short_link_empty(self):
        link = ""

        response = self.client.post('/short/', data={"full_url": link})
        response_data = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["error"], "full_url is empty")

