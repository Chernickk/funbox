import time
from django.test import TestCase
from rest_framework.test import APIClient


class TestApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_can_post_links_and_retrieve_domains(self):
        data = {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
            ]
        }
        data2 = {
            "links": [
                "https://funbox.ru/q/python.pdf",
                "https://www.google.com/search?q=hello+world&oq=hello+world",
                "github.com/Chernickk/funbox"
            ]
        }

        post_time = time.time()
        response = self.client.post('http://127.0.0.1:8000/visited_links/', data=data, format='json', follow=True)
        self.assertEqual(response.data['status'], 'ok')
        time.sleep(0.1)

        post_time_2 = time.time()
        response = self.client.post('http://127.0.0.1:8000/visited_links/', data=data2, format='json', follow=True)
        self.assertEqual(response.data['status'], 'ok')

        response = self.client.get('http://127.0.0.1:8000/visited_domains', follow=True)
        self.assertEqual(response.data['domains'],
                         {'ya.ru', 'funbox.ru', 'stackoverflow.com', 'google.com', 'github.com'})
        self.assertEqual(response.data['status'], 'ok')

        response = self.client.get(f'http://127.0.0.1:8000/visited_domains?from={post_time}&to={post_time + 0.05}',
                                   follow=True)
        self.assertEqual(response.data['domains'],
                         {'ya.ru', 'funbox.ru', 'stackoverflow.com'})
        self.assertEqual(response.data['status'], 'ok')

        response = self.client.get(f'http://127.0.0.1:8000/visited_domains?from={post_time_2}&to={post_time_2 + 0.05}',
                                   follow=True)
        self.assertEqual(response.data['domains'],
                         {'funbox.ru', 'google.com', 'github.com'})
        self.assertEqual(response.data['status'], 'ok')
