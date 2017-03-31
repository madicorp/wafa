from __future__ import absolute_import, unicode_literals

import dj_database_url


from .base import *

env = os.environ.copy()
DEBUG = env['DEBUG']

SECRET_KEY = '38(^651wmne0(!4p7y$qf8&e6*#-u@wd%6enu#&ybto9dgv)ql'
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')
CONTACT_EMAIL = env['CONTACT_EMAIL']
EMAIL_HOST = env['EMAIL_HOST']
EMAIL_PORT = env['EMAIL_PORT']
EMAIL_HOST_USER = env['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']

from location_field import settings as location_field_settings
location_field_settings.LOCATION_FIELD["provider.google.api_key"] = env['GEOPOSITION_GOOGLE_MAPS_API_KEY']

try:
    from .local import *
except ImportError:
    pass
