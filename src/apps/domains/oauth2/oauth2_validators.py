from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from oauth2_provider.exceptions import FatalClientError
from oauth2_provider.oauth2_validators import AccessToken, OAuth2Validator, RefreshToken
from oauth2_provider.settings import oauth2_settings

from lib.log.logger import logger


class RidiOAuth2Validator(OAuth2Validator):
    def validate_bearer_token(self, token, scopes, request):
        logger.info('-----------------------------------------------------------------------  ㅍ미ㅑㅇㅁㅅㄷ_ㅍㄷㅁㄱㄷㄱ ')
        raise NotImplementedError()

    @transaction.atomic
    def save_bearer_token(self, token, request, *args, **kwargs):
        if 'scope' not in token:
            raise FatalClientError('Failed to renew access token: missing scope')

        if request.grant_type == 'client_credentials':
            request.user = None

        refresh_token_code = token.get('refresh_token', None)
        if not refresh_token_code:
            return

        refresh_token_instance = getattr(request, "refresh_token_instance", None)
        if isinstance(refresh_token_instance, RefreshToken):
            logger.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        if not self.rotate_refresh_token(request) and isinstance(refresh_token_instance, RefreshToken):
            logger.info('-----------------------------------------------------------------------------')
            pass
        else:
            if isinstance(refresh_token_instance, RefreshToken):
                try:
                    refresh_token_instance.revoke()
                except (AccessToken.DoesNotExist, RefreshToken.DoesNotExist):
                    pass
                else:
                    setattr(request, "refresh_token_instance", None)

            refresh_token = RefreshToken(
                user=request.user,
                token=refresh_token_code,
                application=request.client,
            )
            refresh_token.save()

        # TODO: check out a more reliable way to communicate expire time to oauthlib
        token['expires_in'] = oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS

    def revoke_token(self, token, token_type_hint, request, *args, **kwargs):
        if token_type_hint not in ['refresh_token']:
            token_type_hint = None

        token_types = {
            'refresh_token': RefreshToken,
        }

        token_type = token_types.get(token_type_hint, AccessToken)
        try:
            token_type.objects.get(token=token).revoke()
        except ObjectDoesNotExist:
            for other_type in [_t for _t in token_types.values() if _t != token_type]:
                # slightly inefficient on Python2, but the queryset contains only one instance
                list(map(lambda t: t.revoke(), other_type.objects.filter(token=token)))
