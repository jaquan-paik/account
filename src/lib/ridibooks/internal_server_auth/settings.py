from django.conf import settings

RIDI_INTERNAL_AUTH_DATA = getattr(settings, 'RIDI_INTERNAL_AUTH_DATA', {})
RIDI_INTERNAL_AUTH_REQUIRE_EXP = getattr(settings, 'RIDI_INTERNAL_AUTH_REQUIRE_EXP', False)
