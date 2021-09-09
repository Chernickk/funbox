from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from funbox.redis_client import redis_client


class TestApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        redis_client.flushdb()

        # for post test
        self.json_some_link = {
            "links": [
                "https://ya.ru",
            ]
        }

        # for retrieve test
        self.retrieve_time = 1
        redis_client.hset('links',
                          self.retrieve_time,
                          "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor")

        # for format test
        self.format_time = 5
        links = [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
            "https://www.google.com/search?q=hello+world&oq=hello+world",
            "github.com/Chernickk/funbox"
        ]
        for i, link in enumerate(links):
            redis_client.hset('links', self.format_time + 0.01 * i, link)

    def test_can_post_links(self):
        url = reverse('visited_links')
        response = self.client.post(url,
                                    data=self.json_some_link,
                                    format='json',
                                    follow=True)

        self.assertEqual(response.data['status'], "ok")
        self.assertIn(self.json_some_link['links'][0], str(redis_client.hgetall('links')))

    def test_can_retrieve_domains(self):
        url = f'{reverse("visited_domains")}?from={self.retrieve_time}&to={self.retrieve_time}'

        response = self.client.get(url, follow=True)

        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(
            set(response.data['domains']),
            {"stackoverflow.com"}
        )

    def test_valid_domain_format_retrieved(self):
        url = f'{reverse("visited_domains")}?from={self.format_time}&to={self.format_time + 1}'

        response = self.client.get(url, follow=True)

        self.assertEqual(
            set(response.data['domains']),
            {'stackoverflow.com', 'ya.ru', 'google.com', 'funbox.ru', 'github.com'}
        )

    def tearDown(self) -> None:
        redis_client.flushdb()
