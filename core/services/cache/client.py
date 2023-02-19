# -*- coding: utf-8 -*-
from cacheops import cache, CacheMiss
import logging

logger = logging.getLogger(__name__)


class CacheKey:
    API_RATE_LIST = 'api_rate_list'


class CacheTtl:
    HOUR = 60 * 60 * 1 * 1
    DAY = 60 * 60 * 24 * 1
    WEEK = 60 * 60 * 24 * 7
    MONTH = 60 * 60 * 24 * 30


class CacheClient:
    is_enable = None
    key = None
    result = None
    ttl = CacheTtl.HOUR

    def __init__(self):
        self.is_enable = True

    def get(self, key):
        self.key = key
        try:
            cached = cache.get(self.key)
            if cached:
                return cached
        except CacheMiss:
            return None

    def set(self, key, result, ttl=None):
        self.key = key
        self.result = result
        if ttl is not None:
            self.ttl = ttl

        try:
            cache.set(
                cache_key=self.key,
                data=self.result,
                timeout=self.ttl
            )
        except CacheMiss:
            return False

        return True

    def update(self, key, result):
        cache.delete(key)
        self.set(key, result)
