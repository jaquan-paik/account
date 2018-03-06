from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from oauth2_provider.exceptions import FatalClientError
from oauth2_provider.oauth2_validators import OAuth2Validator, RefreshToken
from oauth2_provider.settings import oauth2_settings

from apps.domains.oauth2.exceptions import JwtTokenErrorException
from apps.domains.oauth2.token import JwtHandler
from lib.log.logger import logger


class RidiOAuth2Validator(OAuth2Validator):
    def get_id_token(self, token, token_handler, request):
        raise NotImplementedError()

    def validate_silent_authorization(self, request):
        raise NotImplementedError()

    def validate_silent_login(self, request):
        raise NotImplementedError()

    def validate_user_match(self, id_token_hint, scopes, claims, request):
        raise NotImplementedError()

    def validate_bearer_token(self, token, scopes, request):
        if not token:
            return False

        try:
            access_token = JwtHandler.get_access_token(token)
        except JwtTokenErrorException:
            logger.error('Jwt token error. token: %s', token)
            return False

        if not access_token.is_valid(scopes):
            return False

        request.client = access_token.application
        request.user = access_token.user
        request.scopes = scopes

        # this is needed by django rest framework
        request.access_token = access_token
        return True

    @transaction.atomic
    def save_bearer_token(self, token, request, *args, **kwargs):
        if 'scope' not in token:
            raise FatalClientError('Failed to renew access token: missing scope')

        if request.grant_type == 'client_credentials':
            request.user = None

        # TODO: check out a more reliable way to communicate expire time to oauthlib
        token['expires_in'] = oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS

        refresh_token_code = token.get('refresh_token', None)
        if not refresh_token_code:
            return

        if self.rotate_refresh_token(request):
            refresh_token = RefreshToken(
                user=request.user,
                token=refresh_token_code,
                application=request.client,
                expires=datetime.now() + timedelta(seconds=oauth2_settings.REFRESH_TOKEN_EXPIRE_SECONDS),
                scope=token['scope'],
            )
            refresh_token.save()

        token['refresh_token_expires_in'] = oauth2_settings.REFRESH_TOKEN_EXPIRE_SECONDS

    def revoke_token(self, token, token_type_hint, request, *args, **kwargs):
        # Refresh 토큰만 Revoke 가능하다.
        if token_type_hint not in ['refresh_token']:
            return

        try:
            RefreshToken.objects.get(token=token).revoke()
        except ObjectDoesNotExist:
            pass

    def get_original_scopes(self, refresh_token, request, *args, **kwargs):
        rt = request.refresh_token_instance
        return rt.scope
