#!/usr/bin/env python

import os
import sys

from infra.configure.constants import SecretKeyName
from lib.secret.secret import Secret

if __name__ == "__main__":
    # copy system arguments
    arguments = sys.argv[:]
    if Secret().get(SecretKeyName.ENVIRONMENT) == 'development':
        setting_path = f'sites.settings.{Secret().get(SecretKeyName.ENVIRONMENT)}'
    else:
        setting_path = 'sites.settings.base'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_path)
    from django.core.management import execute_from_command_line

    execute_from_command_line(arguments)
