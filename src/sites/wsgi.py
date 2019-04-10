import os
from django.core.wsgi import get_wsgi_application
from raven.contrib.django.middleware.wsgi import Sentry

from infra.configure.constants import SecretKeyName
from lib.secret.secret import Secret

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sites.settings.' + Secret.get(SecretKeyName.ENVIRONMENT))

application = get_wsgi_application()
application = Sentry(application)
