"""
WSGI config for wafa project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

from __future__ import absolute_import, unicode_literals

import os
import os
import sys

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wafa.settings.production")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

execute_from_command_line(sys.argv)
