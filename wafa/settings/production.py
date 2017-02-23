from __future__ import absolute_import, unicode_literals
import yaml
from .base import *

DEBUG = False
configs = None
with open(BASE_DIR + '/config.yml') as file:
    configs = yaml.load(file)
DATABASES = {
    'default': {
        'ENGINE': configs['DB']['DATABASE_ENGINE'],
        'NAME': configs['DB']['DATABASE_NAME'],
        'USER': configs['DB']['DATABASE_USER'],
        'PASSWORD': configs['DB']['DATABASE_PASS'],
        'HOST': configs['DB']['DATABASE_HOST'],
        'PORT': configs['DB']['DATABASE_PORT'],
    }
}

SECRET_KEY = configs['SECRET_KEY']
try:
    from .local import *
except ImportError:
    pass
