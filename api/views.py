import json
import redis
import time
import tldextract
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)


class VisitedLinks(APIView):
    def post(self, request):
        try:
            items = json.loads(self.request.body)
            for link in items['links']:
                redis_instance.set(time.time(), link)

        except redis.exceptions.RedisError as e:
            return Response({'status': 'redis error'})

        else:
            return Response({'status': 'ok'})


class VisitedDomains(APIView):
    def get(self, request):
        try:
            from_time = self.request.query_params.get('from') or 0
            to_time = self.request.query_params.get('to') or 'inf'
            domains = set()
            for key in redis_instance.keys():
                if float(from_time) <= float(key) <= float(to_time):
                    parsed_url = tldextract.extract(redis_instance[key])
                    domains.add(f'{parsed_url.domain}.{parsed_url.suffix}')

        except redis.exceptions.RedisError as e:
            return Response({'status': 'redis error'})

        except ValueError as e:
            return Response({'status': 'invalid request'})

        else:
            return Response({'domains': domains,
                             'status': 'ok'})


