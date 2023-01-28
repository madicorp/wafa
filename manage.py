#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals

import os
import sys

if __name__ == "__main__":
    if os.environ.get('DJANGO_SETTINGS_MODULE') is None:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wafa.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
