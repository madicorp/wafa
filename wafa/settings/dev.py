from __future__ import absolute_import, unicode_literals

from .base import *

env = os.environ.copy()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '38(^651wmne0(!4p7y$qf8&e6*#-u@wd%6enu#&ybto9dgv)ql'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

from location_field import settings as location_field_settings

location_field_settings.LOCATION_FIELD["provider.google.api_key"] = env['GEOPOSITION_GOOGLE_MAPS_API_KEY']
CONTACT_EMAIL = env['CONTACT_EMAIL']

try:
    from .local import *
except ImportError:
    pass
