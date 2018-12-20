from django.db import models
from oauth2_provider.models import AbstractAccessToken, AbstractApplication, AbstractGrant, AbstractRefreshToken

from apps.domains.account.models import OAuth2User, User
from apps.domains.oauth2.constants import JwtAlg
from apps.domains.oauth2.managers import ApplicationManager, GrantManager, RefreshTokenManager
from lib.django.db.mysql import TinyBooleanField
from lib.utils.string import generate_random_str
from lib.utils.url import get_url_until_path

JWT_HS_256_SECRET_LEN = 32


def jwt_hs_256_secret():
    return generate_random_str(JWT_HS_256_SECRET_LEN)


class Application(AbstractApplication):
    GRANT_TYPES = (
        (AbstractApplication.GRANT_AUTHORIZATION_CODE, 'Authorization code'),
        (AbstractApplication.GRANT_PASSWORD, 'Resource owner password-based'),
    )
    CLIENT_TYPES = ((AbstractApplication.CLIENT_CONFIDENTIAL, 'Confidential'),)

    user = models.ForeignKey(
        OAuth2User, db_column='oauth2_user_id', related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE
    )

    client_type = models.CharField(
        max_length=32, choices=CLIENT_TYPES, default=AbstractApplication.CLIENT_CONFIDENTIAL, verbose_name='Client 종류',
        help_text='Confidential 만 지원한다.'
    )
    authorization_grant_type = models.CharField(
        max_length=32, choices=GRANT_TYPES, default=AbstractApplication.GRANT_AUTHORIZATION_CODE, verbose_name='Grant 종류',
        help_text='Authorization code와 Password 만 지원한다.'
    )

    is_in_house = TinyBooleanField(default=False, verbose_name='내부 서비스 여부')
    jwt_alg = models.CharField(max_length=6, choices=JwtAlg.get_choices(), default=JwtAlg.HS256, verbose_name='JWT 알고리즘')
    jwt_hs_256_secret = models.CharField(max_length=32, default=jwt_hs_256_secret, verbose_name='JWT HS256 Secret')

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    objects = ApplicationManager()

    class Meta(AbstractApplication.Meta):
        swappable = 'OAUTH2_PROVIDER_APPLICATION_MODEL'
        db_table = 'oauth2_application'


class Grant(AbstractGrant):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    objects = GrantManager()

    def redirect_uri_allowed(self, uri):
        return get_url_until_path(self.redirect_uri) == get_url_until_path(uri)

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
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    access_token = None

    scope = models.TextField(blank=True, editable=False, verbose_name='Scope')

    expires = models.DateTimeField(editable=False, verbose_name='만료일')

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    objects = RefreshTokenManager()

    class Meta(AbstractRefreshToken.Meta):
        swappable = 'OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL'
        db_table = 'oauth2_refreshtoken'

    def revoke(self):
        self.delete()
