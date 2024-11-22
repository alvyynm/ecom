from decouple import config
from .base import *

DEBUG = False

SECRET_KEY = config('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': config('POSTGRES_PORT')
    }
}
