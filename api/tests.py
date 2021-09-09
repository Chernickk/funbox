import time
from django.test import TestCase
from rest_framework.test import APIClient
from .redis_client import redis_client


class TestApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        redis_client.flushdb()
        self.data = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor",
                "https://www.google.com/search?q=hello+world&oq=hello+world",
                "github.com/Chernickk/funbox"
            ]
        }

    def test_can_post_links(self):
        response = self.client.post('http://127.0.0.1:8000/visited_links/',
                                    data=self.data,
                                    format='json',
                                    follow=True)

        links = [link for key in redis_client.keys() for link in redis_client.lrange(key, 0, 1)]

        self.assertEqual(set(self.data['links']), set(links))
        self.assertEqual(response.data['status'], "ok")

    def test_can_retrieve_domains(self):
        post_time = time.time()

        [redis_client.lpush(post_time, link) for link in self.data['links']]

        response = self.client.get(f'http://127.0.0.1:8000/visited_domains?from={post_time - 1}&to={post_time + 1}',
                                   follow=True)

        self.assertEqual(
            set(response.data['domains']),
            {'ya.ru', 'funbox.ru', 'stackoverflow.com', 'google.com', 'github.com'}
        )
        self.assertEqual(response.data['status'], 'ok')

    def tearDown(self) -> None:
        redis_client.flushdb()
