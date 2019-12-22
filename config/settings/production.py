from .base import *
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
MAIN_SRC = str(
    Path(__file__).resolve().parent.parent.parent
).split('/')[-1]

# Make sure to bind `media` and `static_root` to a S3 bucket or a media server.
# project_root/media
# project_root/static_root
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / '/static_root'

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / f'{MAIN_SRC}/static']
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / f'{MAIN_SRC}/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEBUG = False
