import redis
import json
from app.config import settings

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


def set_cache(key, value, ttl=300):
    r.set(key, json.dumps(value), ex=ttl)


def get_cache(key):
    data = r.get(key)
    return json.loads(data) if data else None