from __future__ import absolute_import, unicode_literals

import os
import dj_database_url
from .base import *

env = os.environ.copy()

# Debug
DEBUG = env.get("DEBUG", "False").lower() in ("true", "1", "yes", "True")

# Secret key
SECRET_KEY = env.get("SECRET_KEY", "")

# Allowed Hosts
ALLOWED_HOSTS = env.get("ALLOWED_HOSTS", "").split(",")

# Email
CONTACT_EMAIL = env.get("CONTACT_EMAIL", "")
EMAIL_HOST = env.get("EMAIL_HOST", "")
EMAIL_PORT = int(env.get("EMAIL_PORT", 587))  # cast to int
EMAIL_HOST_USER = env.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.get("EMAIL_HOST_PASSWORD", "")

# Database
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# AWS S3 Storage
AWS_STORAGE_BUCKET_NAME = env.get("AWS_STORAGE_BUCKET_NAME", "")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'access_key': env.get('AWS_ACCESS_KEY_ID', ''),
            'secret_key': env.get('AWS_SECRET_ACCESS_KEY', ''),
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
            'default_acl': env.get('AWS_DEFAULT_ACL', 'public-read'),
            'custom_domain': AWS_S3_CUSTOM_DOMAIN,
        },
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        'OPTIONS': {
            'location': STATIC_ROOT,
        },
    },
}

# Logging (only in production)
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            }
        }
    }

# Google Maps API Key for location_field
from location_field import settings as location_field_settings
location_field_settings.LOCATION_FIELD["provider.google.api_key"] = env.get("GEOPOSITION_GOOGLE_MAPS_API_KEY", "")

# Optional local overrides
try:
    from .local import *
except ImportError:
    pass
