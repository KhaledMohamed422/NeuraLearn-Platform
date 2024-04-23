from .base import *
from decouple import config

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_NAME'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),
    }
}

# Cashes
# REDIS_URL = 'redis://cache:6379'
# CACHES['default']['LOCATION'] = REDIS_URL

# Worker
CELERY_BROKER_URL= 'amqp://guest:guest@rabbitmq:5672/'