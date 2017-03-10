from __future__ import absolute_import, unicode_literals

import dj_database_url
import yaml
from .base import *

env = os.environ.copy()
DEBUG = env['DEBUG']

SECRET_KEY = env['SECRET_KEY']
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'
ALLOWED_HOSTS = [env['ALLOWED_HOSTS']]
try:
    from .local import *
except ImportError:
    pass
