from rest_framework import serializers

from apps.domains.oauth2.constants import GrantType
from lib.base.serializers import BaseSerializer


class GrantTypeSerializer(BaseSerializer):
    grant_type = serializers.ChoiceField(required=True, choices=GrantType.SUPPORTED_LIST, label='grant type')
#
#
# class AuthorizationTokenForm(forms.Form):
#     client_id = ClientIdField()
#     client_secret = ClientSecretField()
#     code = CodeField()
#     redirect_uri = RedirectUriField()
#
#
# class RefreshTokenForm(forms.Form):
#     client_id = ClientIdField()
#     client_secret = ClientSecretField()
#     refresh_token = RefreshTokenField()
#
#
# class PasswordTokenForm(forms.Form):
#     client_id = ClientIdField()
#     client_secret = ClientSecretField()
#     username = UsernameField()
#     password = PasswordField()
