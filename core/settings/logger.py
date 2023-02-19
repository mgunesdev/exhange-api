import datetime
import os
import logging
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOW = datetime.datetime.now()
DAY_NAME = NOW.strftime('%A').lower()

MAXIMUM_FILE_LOGS = 1024 * 1024 * 10  # 10 MB
BACKUP_COUNT = 100

log = logging.getLogger(__name__)

min_level = 'INFO'
log_min_level = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': min_level,
            'class': 'logging.FileHandler',
            'filename': 'logs/file.log'
        },
        'app': {
            'level': min_level,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/app.log',
            'when': 'D',
            'backupCount': BACKUP_COUNT,
            'formatter': 'verbose',
        },
        'request': {
            'level': min_level,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/request.log',
            'when': 'D',
            'backupCount': BACKUP_COUNT,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': min_level,
            'class': 'django.utils.log.AdminEmailHandler',
            'email_backend': 'django.core.mail.backends.smtp.EmailBackend'
        },
    },
    'root': {
        'handlers': ['app'],
        'level': log_min_level,
    },
    'loggers': {
        '': {
            'level': log_min_level,
            'handlers': ['console'],
        },
        'django': {
            'handlers': ['app'],
            'level': log_min_level,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['app'],
            'level': log_min_level,
            'propagate': False
        },
        'django.server': {
            'handlers': ['app'],
            'level': log_min_level,
            'propagate': False,
        },
        'django.template': {
            'handlers': ['app'],
            'level': log_min_level,
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['app'],
            'level': log_min_level,
            'propagate': False,
        },
        'django.security.*': {
            'handlers': ['app'],
            'level': log_min_level,
            'propagate': False,
        }
    }
}
