
# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
import os
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('tr', _('Turkish')),
    ('en', _('English')),
)

LANGUAGES_OBJ = (
    {
        "code": 'tr',
        "value": _('Turkish'),
    },
    {
        "code": 'en',
        "value": _('English'),
    },
)

LANGUAGE_CODE = 'tr'

USE_TZ = True

# TIME_ZONE = 'Europe/Istanbul'
TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True



