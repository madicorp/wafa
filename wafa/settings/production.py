from __future__ import absolute_import, unicode_literals

import dj_database_url


from .base import *

env = os.environ.copy()
DEBUG = env['DEBUG'] == "True"

SECRET_KEY = env['SECRET_KEY']
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

AWS_STORAGE_BUCKET_NAME = env['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = env['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = env['AWS_SECRET_ACCESS_KEY']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')
CONTACT_EMAIL = env['CONTACT_EMAIL']
EMAIL_HOST = env['EMAIL_HOST']
EMAIL_PORT = env['EMAIL_PORT']
EMAIL_HOST_USER = env['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },

        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            },
        }
    }

from location_field import settings as location_field_settings
location_field_settings.LOCATION_FIELD["provider.google.api_key"] = env['GEOPOSITION_GOOGLE_MAPS_API_KEY']

try:
    from .local import *
except ImportError:
    pass
