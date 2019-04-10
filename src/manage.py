#!/usr/bin/env python

import sys

import os

from infra.configure.constants import SecretKeyName
from lib.secret.secret import Secret

if __name__ == "__main__":
    # copy system arguments
    arguments = sys.argv[:]
    setting_path = f'sites.settings.{Secret.get(SecretKeyName.ENVIRONMENT)}'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_path)
    from django.core.management import execute_from_command_line

    execute_from_command_line(arguments)
