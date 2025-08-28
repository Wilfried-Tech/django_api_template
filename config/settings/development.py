from .base import *

DEBUG = True

INTERNAL_IPS = [
    '127.0.0.1',
]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ALLOWED_HOSTS.append('*')

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
    'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
