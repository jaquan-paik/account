from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from oauth2_provider.models import AbstractAccessToken, AbstractApplication, AbstractGrant, AbstractRefreshToken
from oauthlib.uri_validate import is_absolute_uri

from apps.domains.account.models import OAuth2User, User
from apps.domains.oauth2.constants import JwtAlg, ACCESS_TOKEN_EXPIRE_SECONDS, GRANT_CODE_LENGTH, GrantType, REFRESH_TOKEN_EXPIRE_DAYS, \
    REFRESH_TOKEN_LENGTH
from apps.domains.oauth2.managers import ApplicationManager, GrantManager, RefreshTokenManager
from infra.configure.config import GeneralConfig
from lib.django.db.mysql import TinyBooleanField
from lib.utils.string import generate_random_str
from lib.utils.url import is_same_url, is_same_url_until_path
from datetime import timedelta

JWT_HS_256_SECRET_LEN = 32


def jwt_hs_256_secret():
    return generate_random_str(JWT_HS_256_SECRET_LEN)


def _get_grant_expires():
    return timezone.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)


def _create_random_code():
    return generate_random_str(GRANT_CODE_LENGTH)


def _get_refresh_token_expires():
    return timezone.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)


def _create_random_refresh_token():
    return generate_random_str(REFRESH_TOKEN_LENGTH)


class Application(AbstractApplication):
    GRANT_TYPES = (
        (AbstractApplication.GRANT_AUTHORIZATION_CODE, 'Authorization code'),
        (AbstractApplication.GRANT_PASSWORD, 'Resource owner password-based'),
        (GrantType.CLIENT_CREDENTIALS, 'Client Credentials'),
    )
    CLIENT_TYPES = ((AbstractApplication.CLIENT_CONFIDENTIAL, 'Confidential'),)

    user = models.ForeignKey(
        OAuth2User, db_column='oauth2_user_id', related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE
    )

    client_type = models.CharField(
        max_length=32, choices=CLIENT_TYPES, default=AbstractApplication.CLIENT_CONFIDENTIAL, verbose_name='Client 종류',
        help_text='Confidential 만 지원한다.'
    )
    authorization_grant_type = MultiSelectField(
        max_length=128, choices=GRANT_TYPES, default=AbstractApplication.GRANT_AUTHORIZATION_CODE, verbose_name='Grant 종류',
        help_text='Authorization code와 Password 만 지원한다.'
    )

    is_in_house = TinyBooleanField(default=False, verbose_name='내부 서비스 여부')
    jwt_alg = models.CharField(max_length=6, choices=JwtAlg.get_choices(), default=JwtAlg.HS256, verbose_name='JWT 알고리즘')
    jwt_hs_256_secret = models.CharField(max_length=32, default=jwt_hs_256_secret, verbose_name='JWT HS256 Secret')

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')
    _redirect_uris = models.TextField(db_column='redirect_uris')

    @property
    def redirect_uris(self):
        if not self.is_in_house:
            return self._redirect_uris

        redirect_uris = []
        # pylint: disable=no-member
        for redirect_uri in self._redirect_uris.split():
            if not is_absolute_uri(redirect_uri):
                redirect_uris.append(f"https://{GeneralConfig.get_site_domain()}{redirect_uri}")
            else:
                redirect_uris.append(redirect_uri)
        return ' '.join(redirect_uris)

    objects = ApplicationManager()

    def allows_grant_type(self, *grant_types):
        return any(allowed_grant_type in grant_types for allowed_grant_type in self.authorization_grant_type)

    def redirect_uri_allowed(self, uri):
        for allowed_uri in self.redirect_uris.split():
            if is_same_url_until_path(allowed_uri, uri):
                return True
        return False

    class Meta(AbstractApplication.Meta):
        swappable = 'OAUTH2_PROVIDER_APPLICATION_MODEL'
        db_table = 'oauth2_application'


class Grant(AbstractGrant):
    code = models.CharField(max_length=255, default=_create_random_code, unique=True, )
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE, to_field='idx')
    redirect_uri = models.CharField(max_length=16384)
    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')
    expires = models.DateTimeField(default=_get_grant_expires)

    objects = GrantManager()

    def redirect_uri_allowed(self, uri):
        return is_same_url(self.redirect_uri, uri)

    class Meta(AbstractGrant.Meta):
        swappable = 'OAUTH2_PROVIDER_GRANT_MODEL'
        db_table = 'oauth2_grant'


class AccessToken(AbstractAccessToken):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    token = models.TextField(verbose_name='JWT 토큰', )

    updated = None
    created = None
    last_modified = None

    class Meta(AbstractAccessToken.Meta):
        swappable = 'OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL'
        db_table = 'oauth2_accesstoken'

    @classmethod
    def from_payload(cls, token: str, payload: dict, client: Application = None) -> 'AccessToken':
        _client = client
        if _client is None:
            _client = Application.objects.get(client_id=payload['client_id'])

        user = User.objects.get(idx=payload['u_idx'])

        return cls(
            user=user,
            token=token,
            application=_client,
            expires=payload['exp'],
            scope=payload['scope'],
        )

    def revoke(self):
        raise NotImplementedError()


class RefreshToken(AbstractRefreshToken):
    token = models.CharField(max_length=30, unique=True, default=_create_random_refresh_token)

    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    access_token = None

    scope = models.TextField(blank=True, editable=False, verbose_name='Scope')

    expires = models.DateTimeField(editable=False, verbose_name='만료일', default=_get_refresh_token_expires)

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    objects = RefreshTokenManager()

    class Meta(AbstractRefreshToken.Meta):
        swappable = 'OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL'
        db_table = 'oauth2_refreshtoken'

    def revoke(self):
        self.delete()
