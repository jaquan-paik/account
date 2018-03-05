from django.db import models
from oauth2_provider.models import AbstractAccessToken, AbstractApplication, AbstractGrant, AbstractRefreshToken

from apps.domains.account.models import OAuth2User
from apps.domains.account.models import User
from apps.domains.oauth2.constants import JwtAlg
from lib.utils.string import generate_random_str

JWT_HS_256_SECRET_LEN = 32


def jwt_hs_256_secret():
    return generate_random_str(JWT_HS_256_SECRET_LEN)


class Application(AbstractApplication):
    GRANT_TYPES = ((AbstractApplication.GRANT_AUTHORIZATION_CODE, 'Authorization code'), )
    CLIENT_TYPES = ((AbstractApplication.CLIENT_CONFIDENTIAL, 'Confidential'),)

    user = models.ForeignKey(OAuth2User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    client_type = models.CharField(
        max_length=32, choices=CLIENT_TYPES, default=AbstractApplication.CLIENT_CONFIDENTIAL, verbose_name='Client 종류',
        help_text='Confidential 만 지원한다.'
    )
    authorization_grant_type = models.CharField(
        max_length=32, choices=GRANT_TYPES, default=AbstractApplication.GRANT_AUTHORIZATION_CODE, verbose_name='Grant 종류',
        help_text='Authorization code 만 지원한다.'
    )

    is_in_house = models.BooleanField(default=False, verbose_name='내부 서비스 여부')
    jwt_alg = models.CharField(max_length=6, choices=JwtAlg.get_choices(), default=JwtAlg.RS256, verbose_name='JWT 알고리즘')
    jwt_hs_256_secret = models.CharField(max_length=32, default=jwt_hs_256_secret, verbose_name='JWT HS256 Secret')

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    class Meta(AbstractApplication.Meta):
        swappable = 'OAUTH2_PROVIDER_APPLICATION_MODEL'
        db_table = 'oauth2_application'


class Grant(AbstractGrant):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    class Meta(AbstractGrant.Meta):
        swappable = 'OAUTH2_PROVIDER_GRANT_MODEL'
        db_table = 'oauth2_grant'


class AccessToken(AbstractAccessToken):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    token = models.TextField(verbose_name='JWT 토큰', )

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    class Meta(AbstractAccessToken.Meta):
        swappable = 'OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL'
        db_table = 'oauth2_accesstoken'


class RefreshToken(AbstractRefreshToken):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    class Meta(AbstractRefreshToken.Meta):
        swappable = 'OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL'
        db_table = 'oauth2_refreshtoken'
