import time
import tldextract
from redis.exceptions import RedisError
from rest_framework.views import APIView
from rest_framework.response import Response

from .redis_client import redis_client


class VisitedLinks(APIView):
    """
    endpoint to post visited links
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
        try:
            items = request.data
            for link in items['links']:
                redis_client.lpush(time.time(), link)

        except RedisError as error:
            return Response({'status': f'redis error: {error}'}, status=500)

        return Response({'status': 'ok'})


class VisitedDomains(APIView):
    """
    endpoint to get unique visited domains for given time interval

    from_time and to_time should be in unix-time format
    """
    def get(self, request):
        try:
            from_time = request.query_params.get('from', 0)
            to_time = request.query_params.get('to', 'inf')

            parsed_links = [tldextract.extract(link) for key in redis_client.keys()
                            if float(from_time) <= float(key) <= float(to_time)
                            for link in redis_client.lrange(key, 0, -1)]

            domains = {f'{parsed_link.domain}.{parsed_link.suffix}' for parsed_link in parsed_links}

        except RedisError as error:
            return Response({'status': f'redis error: {error}'}, status=500)

        except ValueError as error:
            return Response({'status': f'invalid request: {error}'}, status=400)

        except Exception as error:
            return Response({'status': f'unknown error: {error}'}, status=500)

        return Response({'domains': domains,
                         'status': 'ok'})
