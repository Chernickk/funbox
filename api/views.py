import time
import tldextract
from rest_framework.views import APIView
from rest_framework.response import Response

from funbox.redis_client import redis_client


class VisitedLinks(APIView):
    """
    Receive JSON with visited links.

    valid format:
      {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
      }
    """

    def post(self, request):
        links = request.data['links']
        for link in links:
            redis_client.hset('links', time.time(), link)

        return Response({'status': 'ok'})


class VisitedDomains(APIView):
    """
    Returns unique visited domains for given time interval.

    'from_time' and 'to_time' should be in unix-time format.
    """

    def get(self, request):
        from_time = request.query_params.get('from', 0)
        to_time = request.query_params.get('to', 'inf')

        domains = set()

        for key in redis_client.hgetall('links'):
            if float(from_time) <= float(key) <= float(to_time):
                parsed_link = tldextract.extract(redis_client.hget('links', key))
                domains.add(f'{parsed_link.domain}.{parsed_link.suffix}')

        return Response({'domains': domains,
                         'status': 'ok'})
