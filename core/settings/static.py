# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#############################################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, "assets/templates")  # ROOT dir for templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]


STATIC_ROOT = os.path.join(BASE_DIR, 'assets/staticfiles')
STATIC_URL = '/assets/static/'

# Extra places for collectstatic to find static files.

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets/static'),
)


MEDIA_ROOT_NAME = "assets/media"
# MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"