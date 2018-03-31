# -*- coding: utf-8 -*-

from project.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("POSTGRES_DB", ""),
        'USER': os.environ.get("POSTGRES_USER", ""),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", ""),
        'HOST': os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        'PORT': os.environ.get("POSTGRES_PORT", 5432)
    }
}

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS", "*")]

STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get("STATIC_ROOT", "static"))

MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")
MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get("MEDIA_ROOT", "media"))

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", True)

DEBUG = False
