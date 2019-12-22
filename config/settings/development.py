from .base import *
from pathlib import Path
from .secrets import load_secrets

secrets = load_secrets()


BASE_DIR = Path(__file__).resolve().parent.parent.parent
MAIN_SRC = str(
    Path(__file__).resolve().parent.parent.parent
).split('/')[-1]
MEDIA_ROOT = BASE_DIR / f'{MAIN_SRC}/media'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / f'{MAIN_SRC}/static_root'

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

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
}]

DATABASES = secrets.get('databases', {})

SECRET_KEY = secrets.get('secret_key', '')

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

SHELL_PLUS = "ipython"
