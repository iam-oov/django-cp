import redis

from django.conf import settings


def get_redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB):
    return redis.StrictRedis(
        host=host,
        port=port,
        db=db,
    )
