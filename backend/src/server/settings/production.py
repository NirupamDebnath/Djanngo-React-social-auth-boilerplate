from .base import *

DEBUG = config("DEBUG",cast=bool)
ALLOWED_HOSTS = ['ip-address','www.myhost.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSword"),
        'HOST': config("DB_HOST"),
        'PORT': config("DB_PORT")
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY")
# STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")