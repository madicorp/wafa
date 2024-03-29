from __future__ import absolute_import, unicode_literals

from .base import *

try:
    import dj_database_url
    from dotenv import load_dotenv
    load_dotenv(dotenv_path='.env.development')
except ImportError:
    pass

env = os.environ.copy()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if os.environ.get('DATABASE_URL') is not None:
    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)

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
