#!/usr/bin/env python

import os
import sys

from infra.configure.constants import SecretKeyName
from lib.secret.secret import Secret

allow_site = ['www', 'test', ]


def make_path(site_name: str, environment: str) -> str:
    if site_name == 'test':
        return '.'.join(['sites', site_name])

    # site와 environment를 받아서 개발환경 혹은 프로적션환경의 settings를 선택함
    return '.'.join(['sites', site_name, 'settings', environment])


if __name__ == "__main__":
    # copy system arguments
    arguments = sys.argv[:]

    site = arguments.pop(1)
    if site not in allow_site:
        # allow check
        print('not allow this site')
        exit(0)

    setting_path = make_path(site, Secret().get(SecretKeyName.ENVIRONMENT))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_path)
    from django.core.management import execute_from_command_line
    execute_from_command_line(arguments)
