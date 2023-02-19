from decouple import config

CACHEOPS_REDIS = {
    'host': config('CACHE_HOST'),
    'port': config('CACHE_PORT'),
    'db': config('CACHE_DEFAULT_DB'),
}

HOUR = 60 * 60 * 1 * 1
DAY = 60 * 60 * 24 * 1
WEEK = 60 * 60 * 24 * 7
MONTH = 60 * 60 * 24 * 30

CACHEOPS = {
    # 'core.example_model': {'ops': ('get', 'fetch'), 'timeout': MONTH},
}
