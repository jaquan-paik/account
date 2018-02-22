from django.db import models
from oauth2_provider.models import AbstractAccessToken, AbstractApplication, AbstractGrant, AbstractRefreshToken

from apps.domains.account.models import Oauth2User


class Application(AbstractApplication):
    GRANT_TYPES = ((AbstractApplication.GRANT_AUTHORIZATION_CODE, 'Authorization code'), )
    CLIENT_TYPES = ((AbstractApplication.CLIENT_CONFIDENTIAL, 'Confidential'),)

    user = models.ForeignKey(Oauth2User, related_name='%(app_label)s_%(class)s', null=True, blank=True, on_delete=models.CASCADE)

    client_type = models.CharField(max_length=32, choices=CLIENT_TYPES, default=AbstractApplication.CLIENT_CONFIDENTIAL)
    authorization_grant_type = models.CharField(max_length=32, choices=GRANT_TYPES, default=AbstractApplication.GRANT_AUTHORIZATION_CODE)

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    class Meta(AbstractApplication.Meta):
        swappable = 'OAUTH2_PROVIDER_APPLICATION_MODEL'
        db_table = 'tb_oauth2_application'


class Grant(AbstractGrant):
    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    class Meta(AbstractGrant.Meta):
        swappable = 'OAUTH2_PROVIDER_GRANT_MODEL'
        db_table = 'tb_oauth2_grant'


class AccessToken(AbstractAccessToken):
    token = models.TextField(verbose_name='JWT 토큰', )

    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    class Meta(AbstractAccessToken.Meta):
        swappable = 'OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL'
        db_table = 'tb_oauth2_accesstoken'


class RefreshToken(AbstractRefreshToken):
    updated = None
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='등록일')
    last_modified = models.DateTimeField(auto_now=True, editable=False, verbose_name='수정일')

    class Meta(AbstractRefreshToken.Meta):
        swappable = 'OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL'
        db_table = 'tb_oauth2_refreshtoken'
